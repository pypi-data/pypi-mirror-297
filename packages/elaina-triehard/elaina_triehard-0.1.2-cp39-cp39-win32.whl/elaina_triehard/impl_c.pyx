# cython: language_level=3

from libc.stdlib cimport malloc, realloc, free
from libc.string cimport memcpy
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from cpython.unicode cimport PyUnicode_FromString
from libc.stdlib cimport qsort

cdef extern from *:
    """
    #if defined(__GNUC__) || defined(__clang__)
        #define HAS_BUILTIN_POPCOUNTLL 1
    #else
        #define HAS_BUILTIN_POPCOUNTLL 0
    #endif

    static int portable_popcount64(unsigned long long x) {
    #if HAS_BUILTIN_POPCOUNTLL
        return __builtin_popcountll(x);
    #else
        x = x - ((x >> 1) & 0x5555555555555555ULL);
        x = (x & 0x3333333333333333ULL) + ((x >> 2) & 0x3333333333333333ULL);
        x = (x + (x >> 4)) & 0x0F0F0F0F0F0F0F0FULL;
        return (int)((x * 0x0101010101010101ULL) >> 56);
    #endif
    }
    """
    int portable_popcount64(unsigned long long x)


cdef int popcount(unsigned long long x):
    """
    计算整数 x 中设置为 1 的位数。
    """
    return portable_popcount64(x)


cdef int compare_unsigned_char(const void *a, const void *b) noexcept nogil:
    """
    比较两个 unsigned char 值的比较函数，用于 qsort。
    """
    cdef unsigned char val_a = (<unsigned char *> a)[0]
    cdef unsigned char val_b = (<unsigned char *> b)[0]
    return val_a - val_b


cdef struct TrieHardNode:
    unsigned long long mask
    unsigned int* children_indices  # 子节点索引数组
    int num_children
    bint is_terminal
    char* word  # 新增字段，存储完整的单词


cdef class TrieHard:
    """
    TrieHard 的主类。
    """
    cdef unsigned long long[256] byte_to_mask
    cdef TrieHardNode* nodes  # 节点数组
    cdef int num_nodes
    cdef unsigned char** bytes_strings  # 字节字符串数组
    cdef int* bytes_lengths  # 字符串长度数组
    cdef int num_strings
    cdef int max_mask_bit

    def __init__(self, strings):
        """
        初始化 TrieHard，并根据给定的字符串列表构建 Trie。
        """
        cdef unsigned char b
        cdef int i, j, length
        cdef unsigned char* bs
        cdef bytes bs_py
        cdef unsigned char[256] unique_bytes_list
        cdef int num_unique_bytes
        cdef int[256] byte_present = [0] * 256

        # 初始化成员变量
        self.nodes = NULL
        self.num_nodes = 0
        self.bytes_strings = NULL
        self.bytes_lengths = NULL
        self.num_strings = 0
        self.max_mask_bit = 0

        num_unique_bytes = 0
        self.byte_to_mask = [0] * 256

        self.num_strings = len(strings)
        if self.num_strings == 0:
            return  # 无需构建 Trie

        self.bytes_strings = <unsigned char**>malloc(self.num_strings * sizeof(unsigned char*))
        if self.bytes_strings == NULL:
            raise MemoryError("Failed to allocate memory for bytes_strings.")

        self.bytes_lengths = <int*>malloc(self.num_strings * sizeof(int))
        if self.bytes_lengths == NULL:
            free(self.bytes_strings)
            self.bytes_strings = NULL
            raise MemoryError("Failed to allocate memory for bytes_lengths.")

        # 初始化为 NULL，便于在异常时正确释放
        for i in range(self.num_strings):
            self.bytes_strings[i] = NULL

        try:
            for i in range(self.num_strings):
                bs_py = strings[i].encode('utf-8')
                bs = <unsigned char*>bs_py
                length = len(bs_py)
                self.bytes_lengths[i] = length
                self.bytes_strings[i] = <unsigned char*>PyMem_Malloc(length * sizeof(unsigned char))
                if self.bytes_strings[i] == NULL:
                    raise MemoryError("Failed to allocate memory for bytes_strings[i].")
                memcpy(self.bytes_strings[i], bs, length * sizeof(unsigned char))
                for j in range(length):
                    b = bs[j]
                    if byte_present[b] == 0:
                        byte_present[b] = 1
                        unique_bytes_list[num_unique_bytes] = b
                        num_unique_bytes += 1

            # 使用 qsort 对 unique_bytes_list 进行排序
            qsort(unique_bytes_list, num_unique_bytes, sizeof(unsigned char), compare_unsigned_char)

            # 为每个唯一字节分配位掩码
            self.max_mask_bit = 0
            for i in range(num_unique_bytes):
                b = unique_bytes_list[i]
                self.byte_to_mask[b] = 1 << self.max_mask_bit
                self.max_mask_bit += 1

            # 构建 Trie
            self._build_trie()
        except Exception as e:
            self.__dealloc__()
            raise e

    cdef void _build_trie(self):
        """
        构建 Trie 的辅助函数，从根节点开始。
        """
        cdef int i
        self.num_nodes = 1
        self.nodes = <TrieHardNode*>malloc(self.num_nodes * sizeof(TrieHardNode))
        if self.nodes == NULL:
            raise MemoryError("Failed to allocate memory for nodes.")
        # 初始化根节点
        self.nodes[0].mask = 0
        self.nodes[0].children_indices = NULL
        self.nodes[0].num_children = 0
        self.nodes[0].is_terminal = False
        self.nodes[0].word = NULL
        self._build_node(0, self.bytes_strings, self.bytes_lengths, self.num_strings, 0)

    cdef void _build_node(self, int node_index, unsigned char** strings, int* lengths, int num_strings, int position):
        """
        递归地构建 Trie 节点。
        """
        cdef dict byte_to_strings
        cdef bint is_terminal
        cdef unsigned char* bs
        cdef int length
        cdef unsigned long long mask
        cdef int num_children
        cdef unsigned char[256] sorted_keys
        cdef int num_sorted_keys
        cdef unsigned char b
        cdef int i, j
        cdef unsigned int* children_indices
        cdef int child_node_index
        cdef list child_strings_list
        cdef list child_lengths_list
        cdef int child_num_strings
        cdef unsigned char** child_strings_array
        cdef int* child_lengths_array
        cdef TrieHardNode* temp_nodes

        byte_to_strings = {}
        is_terminal = False
        mask = 0
        num_sorted_keys = 0
        children_indices = NULL

        # 初始化 byte_to_strings
        for i in range(num_strings):
            bs = strings[i]
            length = lengths[i]
            if position == length:
                is_terminal = True  # 当前节点为终端节点
                # 存储完整的单词
                word_length = length
                self.nodes[node_index].word = <char*>malloc((word_length + 1) * sizeof(char))
                if self.nodes[node_index].word == NULL:
                    raise MemoryError("Failed to allocate memory for word.")
                memcpy(self.nodes[node_index].word, bs, word_length * sizeof(char))
                self.nodes[node_index].word[word_length] = b'\0'  # 添加字符串结束符
            if position < length:
                b = bs[position]
                if b not in byte_to_strings:
                    byte_to_strings[b] = {'strings': [], 'lengths': []}
                    sorted_keys[num_sorted_keys] = b
                    num_sorted_keys += 1
                byte_to_strings[b]['strings'].append(bs)
                byte_to_strings[b]['lengths'].append(length)

        # 构建掩码
        for i in range(num_sorted_keys):
            b = sorted_keys[i]
            mask |= self.byte_to_mask[b]

        num_children = num_sorted_keys

        # 使用 qsort 对 sorted_keys 进行排序
        qsort(sorted_keys, num_children, sizeof(unsigned char), compare_unsigned_char)

        # 创建子节点索引数组
        if num_children > 0:
            children_indices = <unsigned int*>malloc(num_children * sizeof(unsigned int))
            if children_indices == NULL:
                raise MemoryError("Failed to allocate memory for children_indices.")

        # 初始化当前节点
        self.nodes[node_index].mask = mask
        self.nodes[node_index].num_children = num_children
        self.nodes[node_index].is_terminal = is_terminal
        self.nodes[node_index].children_indices = children_indices
        # 如果不是终端节点，word 设置为 NULL
        if not is_terminal and self.nodes[node_index].word != NULL:
            free(self.nodes[node_index].word)
            self.nodes[node_index].word = NULL

        # 创建子节点
        for i in range(num_children):
            child_node_index = self.num_nodes
            children_indices[i] = child_node_index
            # 重新分配 nodes 数组
            temp_nodes = <TrieHardNode*>realloc(self.nodes, (self.num_nodes + 1) * sizeof(TrieHardNode))
            if temp_nodes == NULL:
                raise MemoryError("Failed to reallocate memory for nodes.")
            self.nodes = temp_nodes
            self.num_nodes += 1
            # 初始化子节点
            self.nodes[child_node_index].mask = 0
            self.nodes[child_node_index].num_children = 0
            self.nodes[child_node_index].is_terminal = False
            self.nodes[child_node_index].children_indices = NULL
            self.nodes[child_node_index].word = NULL

        # 递归地构建子节点
        for i in range(num_children):
            b = sorted_keys[i]
            child_node_index = children_indices[i]
            child_strings_list = byte_to_strings[b]['strings']
            child_lengths_list = byte_to_strings[b]['lengths']
            child_num_strings = len(child_strings_list)
            child_strings_array = <unsigned char**>malloc(child_num_strings * sizeof(unsigned char*))
            if child_strings_array == NULL:
                raise MemoryError("Failed to allocate memory for child_strings_array.")
            child_lengths_array = <int*>malloc(child_num_strings * sizeof(int))
            if child_lengths_array == NULL:
                free(child_strings_array)
                raise MemoryError("Failed to allocate memory for child_lengths_array.")
            for j in range(child_num_strings):
                child_strings_array[j] = child_strings_list[j]
                child_lengths_array[j] = child_lengths_list[j]
            try:
                self._build_node(child_node_index, child_strings_array, child_lengths_array, child_num_strings, position + 1)
            finally:
                free(child_strings_array)
                free(child_lengths_array)

    cpdef str get_closest_prefix(self, str key):
        """
        接收一个字符串，返回 Trie 中与之匹配的完整单词。
        如果没有匹配的单词，则返回空字符串。
        """
        cdef TrieHardNode* current_node
        cdef int position
        cdef bytes key_bytes
        cdef int key_length
        cdef unsigned char* key_ptr
        cdef unsigned char b
        cdef unsigned long long input_mask
        cdef unsigned long long less_significant_bits
        cdef int child_index
        cdef char* matched_word = NULL

        position = 0
        key_bytes = key.encode('utf-8')
        key_length = len(key_bytes)
        key_ptr = <unsigned char*>key_bytes

        if self.nodes == NULL:
            return ''

        current_node = &self.nodes[0]
        while position < key_length:
            if current_node.is_terminal and current_node.word != NULL:
                matched_word = current_node.word
            b = key_ptr[position]
            input_mask = self.byte_to_mask[b]
            if input_mask == 0 or (current_node.mask & input_mask) == 0:
                break  # 当前字节不被允许，停止搜索
            less_significant_bits = (input_mask - 1) & current_node.mask
            child_index = popcount(less_significant_bits)
            current_node = &self.nodes[current_node.children_indices[child_index]]
            position += 1

        # 检查最后一个节点是否为终端节点
        if current_node.is_terminal and current_node.word != NULL:
            matched_word = current_node.word

        if matched_word != NULL:
            # 返回匹配的完整单词
            return PyUnicode_FromString(matched_word)
        else:
            return ''

    def __dealloc__(self):
        """
        释放 TrieHard 分配的内存。
        """
        cdef int i
        if self.nodes != NULL and self.num_nodes > 0:
            # 释放每个节点的 children_indices 和 word
            for i in range(self.num_nodes):
                if self.nodes[i].children_indices != NULL:
                    free(self.nodes[i].children_indices)
                    self.nodes[i].children_indices = NULL
                if self.nodes[i].word != NULL:
                    free(self.nodes[i].word)
                    self.nodes[i].word = NULL
            free(self.nodes)
            self.nodes = NULL
            self.num_nodes = 0
        if self.bytes_strings != NULL and self.num_strings > 0:
            for i in range(self.num_strings):
                if self.bytes_strings[i] != NULL:
                    PyMem_Free(self.bytes_strings[i])
                    self.bytes_strings[i] = NULL
            free(self.bytes_strings)
            self.bytes_strings = NULL
            self.num_strings = 0
        if self.bytes_lengths != NULL:
            free(self.bytes_lengths)
            self.bytes_lengths = NULL

from __future__ import annotations


class TrieHardNode:
    """
    TrieHard 的节点类，包含掩码、子节点索引和是否为终端节点的标志。
    """
    def __init__(self, mask, children_indices, is_terminal=False):
        self.mask = mask  # 整数，表示允许的字节集合
        self.children_indices = children_indices  # 子节点在节点列表中的索引
        self.is_terminal = is_terminal  # 是否为终端节点（表示一个完整的单词）


class TrieHard:
    """
    TrieHard 的主类，负责构建 Trie 和执行查询操作。
    """
    def __init__(self, strings: list[str]):
        """
        初始化 TrieHard，并根据给定的字符串列表构建 Trie。

        参数：
        - strings: 字符串列表，用于构建 Trie。
        """
        # 收集所有字符串中的唯一字节
        unique_bytes = set()
        self.bytes_strings = [s.encode('utf-8') for s in strings]
        for bs in self.bytes_strings:
            for b in bs:
                unique_bytes.add(b)
        # 为每个唯一字节分配一个唯一的位掩码
        self.byte_to_mask = {}
        for i, b in enumerate(sorted(unique_bytes)):
            self.byte_to_mask[b] = 1 << i
        # 构建 Trie 节点
        self.nodes = []
        self._build_trie()

    def _build_trie(self):
        """
        构建 Trie 的辅助函数，从根节点开始。
        """
        self.nodes = []
        self.nodes.append(None)  # 占位符，用于稍后填充根节点
        self._build_node(0, self.bytes_strings, 0)

    def _build_node(self, node_index, strings, position):
        """
        递归地构建 Trie 节点。

        参数：
        - node_index: 当前节点的索引。
        - strings: 到达当前节点的字节字符串列表。
        - position: 当前处理的字符串中的位置。
        """
        byte_to_strings = {}
        is_terminal = False
        for bs in strings:
            if position < len(bs):
                b = bs[position]
                if b not in byte_to_strings:
                    byte_to_strings[b] = []
                byte_to_strings[b].append(bs)
            else:
                # 字符串在此结束，标记为终端节点
                is_terminal = True
        # 构建掩码
        mask = 0
        for b in sorted(byte_to_strings.keys()):
            mask |= self.byte_to_mask[b]
        node = TrieHardNode(mask, [], is_terminal)
        self.nodes[node_index] = node
        # 按字节的排序顺序构建子节点
        for b in sorted(byte_to_strings.keys()):
            child_node_index = len(self.nodes)
            node.children_indices.append(child_node_index)
            self.nodes.append(None)  # 占位符
            self._build_node(child_node_index, byte_to_strings[b], position + 1)


    def get_closest_prefix(self, key: str):
        """
        接收一个字符串，返回 Trie 中与之匹配的最长前缀。
        如果没有匹配的前缀，则返回空字符串。
        """
        current_node = self.nodes[0]
        position = 0
        key_bytes = key.encode('utf-8')
        last_terminal_position = -1
        while position < len(key_bytes):
            b = key_bytes[position]
            if b in self.byte_to_mask:
                input_mask = self.byte_to_mask[b]
                if current_node.mask & input_mask == 0:
                    break  # 当前字节不被允许，停止搜索
                # 计算子节点的索引
                less_significant_bits = (input_mask - 1) & current_node.mask
                child_index = bin(less_significant_bits).count('1')
                current_node = self.nodes[current_node.children_indices[child_index]]
                if current_node.is_terminal:
                    last_terminal_position = position
                position += 1
            else:
                break  # 字节未在 Trie 中出现
        if last_terminal_position != -1:
            # 返回匹配的最长前缀
            return key_bytes[:last_terminal_position + 1].decode('utf-8')
        else:
            return ''

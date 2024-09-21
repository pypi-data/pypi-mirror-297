try:
    from .impl_c import TrieHard as TrieHard
    from .impl_c import TrieHardNode as TrieHardNode
except ImportError:
    from .impl_py import TrieHard as TrieHard
    from .impl_py import TrieHardNode as TrieHardNode

import heapq


# 1. Why does Huffman coding produce shorter codes for frequently occurring characters?
#    Huffman coding builds a binary tree where characters with higher frequencies are placed
#    closer to the root. Since the code for each character is determined by the path from the
#    root to its leaf node, characters nearer to the root get shorter binary codes. This ensures
#    that the most common characters use the fewest bits, minimizing the total encoded length.
#
# 2. Why must Huffman codes be prefix-free?
#    Huffman codes must be prefix-free (no code is a prefix of another) so that the encoded
#    bit-string can be decoded unambiguously without needing delimiters. When reading the
#    bit-string left to right, at each step there is exactly one matching code, allowing the
#    decoder to identify character boundaries and reconstruct the original string correctly.


class Node:
    """A node in the Huffman tree."""

    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def calculate_frequency(input_string: str) -> dict:
    """Returns a dictionary containing the frequency of each character."""
    freq = {}
    for ch in input_string:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def build_huffman_tree(freq_dict: dict):
    """Builds the Huffman tree using the frequency dictionary and returns the root node."""
    heap = [Node(char=ch, freq=f) for ch, f in freq_dict.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        # Special case: only one unique character
        node = heapq.heappop(heap)
        root = Node(freq=node.freq, left=node)
        return root

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heapq.heappop(heap)


def generate_codes(root) -> dict:
    """Generates the binary Huffman codes for each character."""
    codes = {}

    def _traverse(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code if current_code else "0"
            return
        _traverse(node.left, current_code + "0")
        _traverse(node.right, current_code + "1")

    _traverse(root, "")
    return codes


def encode_string(input_string: str, codes: dict) -> str:
    """Encodes the input string using the generated Huffman codes."""
    return "".join(codes[ch] for ch in input_string)


def huffman_encode(input_string: str) -> str:
    """Calls all components and returns the final encoded string."""
    freq = calculate_frequency(input_string)
    root = build_huffman_tree(freq)
    codes = generate_codes(root)
    return encode_string(input_string, codes)


def huffman_decode(encoded_string: str, root) -> str:
    """Given an encoded bit-string and the Huffman tree root, returns the original string."""
    # Special case: single unique character (left child is the only leaf)
    if root.char is not None:
        return root.char * len(encoded_string)
    if root.left and root.left.char is not None and root.right is None:
        return root.left.char * len(encoded_string)

    decoded = []
    current = root
    for bit in encoded_string:
        if bit == "0":
            current = current.left
        else:
            current = current.right
        if current.char is not None:
            decoded.append(current.char)
            current = root
    return "".join(decoded)


if __name__ == "__main__":
    input_string = input("Enter a sentence: ")
    encoded_output = huffman_encode(input_string)
    print("Encoded Output:")
    print(encoded_output)

    # Rebuild components for decoding
    freq = calculate_frequency(input_string)
    root = build_huffman_tree(freq)
    decoded_output = huffman_decode(encoded_output, root)
    print("Decoded Output:")
    print(decoded_output)

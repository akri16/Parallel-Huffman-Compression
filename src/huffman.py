import heapq
import os
from multiprocessing import Pool, Manager, cpu_count
from src.sort import merge_sort_parallel
import time as t

last_mapping = None


class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, HeapNode):
            return False
        return self.freq == other.freq


def get_byte_array(padded_encoded_text, p):
    if len(padded_encoded_text) % 8 != 0:
        print("Encoded text not padded properly")
        exit(0)

    bytes_s = [padded_encoded_text[i:i + 8] for i in range(0, len(padded_encoded_text), 8)]
    pool = Pool(p)
    l = pool.map(calculate_bytes_array, bytes_s)
    pool.close()

    return bytearray(l)


def calculate_bytes_array(byte):
    return int(byte, 2)


def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * extra_padding]

    return encoded_text


def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text


def make_frequency_dict(text):
    frequency = {}
    for character in text:
        if character not in frequency:
            frequency[character] = 0
        frequency[character] += 1
    return frequency


class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

        if os.path.splitext(path)[1] == ".bin" and last_mapping is not None:
            self.reverse_mapping = last_mapping

    # functions for compression:
    def make_heap(self, frequency, p):
        pool = Pool(p)
        l = pool.starmap(self.make_heap_i, ((key, frequency) for key in frequency))
        self.heap = merge_sort_parallel(l, p)
        pool.close()

    def make_heap_i(self, key, freq):
        return HeapNode(key, freq[key])

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = list(text)
        for i, character in enumerate(encoded_text):
            encoded_text[i] = self.codes[character]
        return ''.join(encoded_text)

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        times = dict()

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            t1 = t.time()
            frequency = make_frequency_dict(text)
            t2 = t.time()
            print(t2 - t1)

            for x in range(1, 8):
                start_time = t.time()
                self.make_heap(frequency, x)
                end_time = t.time()
                times[x] = end_time - start_time

            t1 = t.time()
            self.merge_nodes()
            t2 = t.time()
            print(t2 - t1)

            t1 = t.time()
            self.make_codes()
            t2 = t.time()
            print(t2 - t1)

            t1 = t.time()
            encoded_text = self.get_encoded_text(text)
            t2 = t.time()
            print(t2 - t1)

            t1 = t.time()
            padded_encoded_text = pad_encoded_text(encoded_text)
            t2 = t.time()
            print(t2 - t1)

            # t1 = t.time()
            # b = get_byte_array(padded_encoded_text)
            # t2 = t.time()
            # print(t2 - t1)

            for x in range(1, 8):
                start_time = t.time()
                b = get_byte_array(padded_encoded_text, x)
                end_time = t.time()
                times[x] += end_time - start_time

            output.write(bytes(b))

        global last_mapping
        last_mapping = self.reverse_mapping
        print("Compressed")
        return Data(output_path, times)

    """ functions for decompression: """

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("Decompressed")
        return output_path


class Data:
    def __init__(self, path, times):
        self.path = path
        self.times = times

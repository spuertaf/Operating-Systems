from bitarray import bitarray

class Compressor:
    def __init__(
        self,
        maximum_table_size = 10_000
    ):
        """Initialize the Compressor object.

        Args:
            maximum_table_size (int, optional): Maximum table size for compression. Defaults to 10_000.
        """
        self.code_dict = {chr(i): i for i in range(256)}
        self.decode_dict = {i : chr(i) for i in range(256)}
        self.maximum_table_size = maximum_table_size
        
    def format_symbol(self, symbol, num_bits):
        """Format a symbol into a bitarray with a specified number of bits.

        Args:
            symbol (int): The symbol to format.
            num_bits (int): The number of bits to use for the representation.

        Returns:
            bitarray: A bitarray representing the symbol.
        """
        return bitarray(('{0:0%sb}' % num_bits).format(symbol),endian="little")
    
    
    def compress(self, file_content: str, out_file_path: str):
        """Compresses the given file content and writes the result to the specified file.

        Args:
            file_content (str): The content of the file to compress.
            out_file_path (str): The path to write the compressed data.
        """
        with open(out_file_path, "wb") as bin_file:
            self._compress(file_content, bin_file)
    
    
    def _compress(self, uncompressed_data: str, out_file) -> bitarray:
        """Performs LZW compression on the given data and writes the result to the output file.

        Args:
            uncompressed_data (str): The data to compress.
            out_file (TextIOWrapper): The output file object to write the compressed data to.

        Returns:
            bitarray: The compressed data as a bitarray.
        """
        fosy = self.format_symbol
        pattern = ""            # String is null.
        out_buffer = bitarray(endian="little")
        bits_per_symbol = 9
        dict_size = 256

        # iterating through the input symbols.
        # LZW Compression algorithm
        for symbol in uncompressed_data:            
            pattern_plus_symbol = pattern + symbol # get input symbol.
            if pattern_plus_symbol in self.code_dict:
                pattern = pattern_plus_symbol
            else:
                
                out_buffer += fosy(self.code_dict[pattern], bits_per_symbol)

                pattern = symbol
                
                if(len(self.code_dict) <= self.maximum_table_size):
                    self.code_dict[pattern_plus_symbol] = dict_size
                    dict_size += 1

                if(dict_size >= 2 ** bits_per_symbol):
                    bits_per_symbol += 1

        if pattern in self.code_dict:
            out_buffer += fosy(self.code_dict[pattern], bits_per_symbol)

        out_file.write(out_buffer.tobytes())
        
        return out_buffer
    
    def read_code(self, bits):
        """Reads a code from the given bitarray.

        Args:
            bits (bitarray): The bitarray to read the code from.

        Returns:
            int: The decoded code.
        """
        i = 0
        for bit in bits:
            i = (i << 1) | bit

        return i
    
    def decompress(self, in_file) -> str:
        """Decompresses the data from the given input file and returns the decompressed content.

        Args:
            in_file (TextIOWrapper): The input file object containing the compressed data.

        Returns:
            str: The decompressed data.
        """
        data_bits = bitarray(endian="little")
        data_bits.frombytes(in_file.read())
        bits_per_symbol = 9

        num_bits_unread = len(data_bits)
        dict_size = 256
        next_code = 256
        decompressed_data = ""
        pattern = ""

        i = 0
        start = 0
        while(True):
            #TO DO : check when bit per symbol changing
            end = start + bits_per_symbol
            code = self.read_code(data_bits[start:end])
            start = end
        
            if not (code in self.decode_dict):
                self.decode_dict[code] = pattern + (pattern[0]) #????

            decompressed_data += self.decode_dict[code]
            
            if not(len(pattern) == 0):
                self.decode_dict[next_code] = pattern + (self.decode_dict[code][0])
                next_code += 1
            pattern = self.decode_dict[code]

            dict_size += 1
            num_bits_unread -= bits_per_symbol

            if(num_bits_unread <= 0):
                break

            if(dict_size >= 2 ** bits_per_symbol):
                bits_per_symbol += 1
            
            i += 1
        
        return decompressed_data
    
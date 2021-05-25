icon_path = "../res/compress.ico"
accepted_ext = {'Text Files': '*.txt', 'Binary Files': '*.bin'}

COMPRESS = 0
DECOMP = 1

# strings
root_title = "Fast CompDe"
choose_file = "Choose File"
compress = "Compress"
decompress = "Decompress"
hello = "    Hello!     "
compressing = "Compressing . . . "
decompressing = "Decompressing . . ."
num_processes = "Number of Processes"
exec_time = "Execution Time (ms)"

def output_stat(output_path, org_size, new_size):
    size = lambda x: round(x / 1000, 2)
    return "Compressed file path: {} \n\nOriginal Size: {} KB \n Compressed " \
           "Size: {} KB \n Compression Ratio: {}" \
        .format(output_path, size(org_size), size(new_size), round(new_size / org_size, 3))

def filename_with_size(name, size): return "{} - {} MB".format(name, round(size / 10 ** 6, 2))
def decomp_msg(path): return "Decompressed file path: {}".format(path)


# colours
color_bg = "white"
color_primary = "#34b4eb"
color_white = "#FFFFFF"
color_on_primary = "#FFFFFF"
color_on_bg = "#000000"

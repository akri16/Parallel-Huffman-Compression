from tkinter import filedialog, ttk
from tkinter import *
from src.huffman import HuffmanCoding
import os
import threading as th

COMPRESS = 0
DECOMP = 1


def open_chooser():
    filename = filedialog.askopenfilename(title="Compress", filetypes=[("Text Files", "*.txt"),
                                                                       ("Binary Files", "*.bin")])
    root.filename = filename
    ext = os.path.splitext(filename)[1]
    if ext in (".txt", ".bin"):
        btn2["state"] = "normal"
        if ext == ".txt":
            btn2["text"] = "Compress"
            root.state = COMPRESS
        else:
            btn2["text"] = "Decompress"
            root.state = DECOMP


def get_output_text(output_path, input_path, times = dict()):
    t = ""
    org_size = os.stat(input_path).st_size
    new_size = os.stat(output_path).st_size

    for k, v in times.items():
        t += str(k) + ': ' + str(round(v * 1000, 3)) + ' ms'
        t += '\n'

    t = t[:-1]

    return "Compressed file path: " + output_path \
           + "\n\n Original Size: " + str(round(org_size / 1000, 2)) + " Kb" \
           + "\n Compressed Size: " + str(round(new_size / 1000, 2)) + " Kb"\
           + "\n Compression Ratio: " + str(round(new_size / org_size, 3)) \
           + "\n\n Heap build time with cores: \n" + t


def comp_dec():
    btn2["text"] = "Compress"
    btn2["state"] = "disable"
    if root.state == COMPRESS:
        label["text"] = "Compressing . . . "
        h = HuffmanCoding(root.filename)
        data = h.compress()
        label["text"] = get_output_text(data.path, root.filename, data.times)

    elif root.state == DECOMP:
        label["text"] = "Decompressing . . . ."
        h = HuffmanCoding(root.filename)
        decom_path = h.decompress(root.filename)
        label["text"] = "Decompressed file path: " + decom_path

    root.state = None


if __name__ == '__main__':
    icon_path = "res/compress.ico"
    root = Tk()
    root.iconbitmap(icon_path)
    root.title("Fast CompDe")
    root.configure(background='white')
    root.state = None

    label = Label(text="    Hello!     ", bg="white", fg="black", font="helvetica 12",
                  wraplength=300, justify="center")
    label.grid(row=1, column=0, columnspan=4, padx=20, pady=(20, 40))

    btn1 = Button(text="Choose File", command=open_chooser, width=20, relief='flat', fg="white", bg="#34b8fb")
    btn1.grid(row=0, column=0, padx=32, pady=40)

    btn2 = Button(text="Compress", state=DISABLED, command=lambda: th.Thread(target=comp_dec).start(), width=20,
                  relief='flat', fg="white", bg="#34b4eb")
    btn2.grid(row=0, column=1, columnspan=3, padx=32, pady=40)

    root.mainloop()

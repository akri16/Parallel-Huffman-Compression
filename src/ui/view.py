from tkinter import *
from tkinter import filedialog
from src.huffman import HuffmanCoding
from multiprocessing import Process
import matplotlib.pyplot as plt
import src.ui.constants as const
import src.utils as util
import threading as th
from src.ui.styles import *


def plot_output(title, times):
    min_time_p = min(times, key=times.get)
    plt.plot(times.keys(), times.values())
    plt.title(title)
    plt.xlabel(const.num_processes)
    plt.ylabel(const.exec_time)
    plt.plot(min_time_p, times[min_time_p], 'ro')
    plt.show()


def get_output(output_path, input_path, times):
    org_size = util.get_size(input_path)
    new_size = util.get_size(output_path)
    filename_with_size = const.filename_with_size(util.get_file_name(output_path), org_size)
    times = dict(map(lambda x: (x[0], round(x[1] * 1000, 3)), times.items()))

    Process(target=plot_output, args=(filename_with_size, times)).start()
    return const.output_stat(output_path, org_size, new_size)


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.state = None
        self.filename = None

        self.label = Label(text=const.hello)
        self.btn_choose = Button(text=const.choose_file, command=self.open_chooser)
        self.btn_compd = Button(text=const.compress, command=lambda: th.Thread(target=self.comp_dec).start(),
                                state=DISABLED)

        self.label.grid(row=1, column=0, columnspan=4, padx=20, pady=(20, 40))
        self.btn_choose.grid(row=0, column=0, padx=32, pady=40)
        self.btn_compd.grid(row=0, column=1, columnspan=3, padx=32, pady=40)

        root_style(self)
        label_style(self.label)
        button_style(self.btn_compd, self.btn_choose)

    def open_chooser(self):
        filename = filedialog.askopenfilename(title=const.compress, filetypes=const.accepted_ext.items())
        self.filename = filename
        ext = util.get_file_type(filename)

        if ext in [".txt", ".bin"]:
            self.btn_compd.configure(state=NORMAL)
            if ext == ".txt":
                self.btn_compd.configure(text=const.compress)
                self.state = const.COMPRESS
            else:
                self.btn_compd.configure(text=const.decompress)
                self.state = const.DECOMP

    def comp_dec(self):
        self.btn_compd.config(text=const.compress, state=DISABLED)

        if self.state == const.COMPRESS:
            self.label.config(text=const.compressing)
            h = HuffmanCoding(self.filename)
            data = h.compress()
            self.label.config(text=get_output(data.path, self.filename, data.times))

        elif self.state == const.DECOMP:
            self.label.configure(text=const.decompressing)
            h = HuffmanCoding(self.filename)
            decom_path = h.decompress(self.filename)
            self.label.config(text=const.decomp_msg(decom_path))

        self.state = None

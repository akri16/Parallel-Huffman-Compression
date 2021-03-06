from src.ui.constants import *

__all__ = ["button_style", "label_style", "root_style"]

from src.utils import get_actual_path


def button_style(*btns):
    for btn in btns:
        btn.configure(width=20, relief='flat', fg=color_on_primary, bg=color_primary)


def label_style(*labels):
    for label in labels:
        label.configure(bg=color_bg, fg=color_on_bg, font="helvetica 12",
                        wraplength=300, justify="center")


def root_style(*roots):
    import pathlib
    print(pathlib.Path().absolute())

    for root in roots:
        root.iconbitmap(get_actual_path(__file__, icon_path))
        root.title(root_title)
        root.configure(background=color_bg)

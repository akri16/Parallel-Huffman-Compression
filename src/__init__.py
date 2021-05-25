from src.ui.view import App
import multiprocessing as mp

if __name__ == '__main__':
    mp.freeze_support()
    print("Hi")
    app = App()
    app.mainloop()

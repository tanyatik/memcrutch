import tkinter
import tkinter as tk
from tkhtmlview import HTMLLabel
from typing import Optional

import local_search
from carousel_iterator import CarouselIterator


class NoteSearchWindow(tkinter.Frame):
    """
    Window that enables searching through notes on a local filesystem, and displaying search results.
    Initially the search results are empty, and the window is blank.
    Using a keyboard shortcut, the user can enter the search query in a pop-up window,
    after which point the main window will display search results, if found any.
    Notes are assumed to be in Markdown format.
    """
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master=master)
        self.master = master
        # Box where search results will be
        self.result_box = HTMLLabel(
            self,
            width='1',
            html=f'<h1>This window will display the result of your search query</h1>')

        self.pack(fill=tkinter.BOTH, expand=1)

    def search_query_callback(self, event):
        query_box = tkinter.Toplevel(self)
        query_box.geometry("400x50")
        query_box.bind('<KeyPress-Escape>', lambda event: query_box.destroy())

        def return_pressed_callback(event):
            del event  # unused
            self.search_notes(query_text=query_box_entry.get())
            query_box.destroy()
        query_box.bind('<KeyPress-Return>', return_pressed_callback)

        query_box_entry = tkinter.Entry(query_box, width=50)
        query_box_entry.focus_set()
        query_box_entry.pack()

    def search_notes(self, query_text):
        results = local_search.search_notes(query_text)
        results_carousel = CarouselIterator(results)

        def display_result():
            try:
                search_result = results_carousel.current()
                self.result_box.set_html(search_result.html)
            except StopIteration as e:
                self.result_box.set_html('No result found')
            self.result_box.pack(fill=tkinter.BOTH, expand=1)
            self.result_box.fit_height()

        def display_previous_result():
            results_carousel.previous()
            display_result()

        def display_next_result():
            results_carousel.next()
            display_result()

        display_result()
        previous_button = tk.Button(self.master, text="Previous", command=display_previous_result)
        previous_button.pack(side=tkinter.LEFT)
        next_button = tk.Button(self.master, text="Next", command=display_next_result)
        next_button.pack(side=tkinter.RIGHT)

        self.master.attributes('-topmost', True)


if __name__ == '__main__':
    # Set up root window
    root = tk.Tk()
    root.title('Memcrutch')
    root.geometry('400x400')
    root.attributes('-alpha', 0.8)

    app = NoteSearchWindow(root)
    # The app now will be called by a 'launcher' app when the search shortcut is pressed,
    # so we can assume that the search callback already needs to be called
    app.search_query_callback(None)
    tk.mainloop()

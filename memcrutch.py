import tkinter
import tkinter as tk
from tkhtmlview import HTMLLabel
import local_search


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

        # Display first result
        # TODO: cycle through search results
        got_result = False
        for first_result in results:
            self.result_box.set_html(first_result.html)
            got_result = True
            break

        if not got_result:
            self.result_box.set_html('No result found')

        self.result_box.pack(fill=tkinter.BOTH, expand=1)
        self.result_box.fit_height()


if __name__ == '__main__':
    # Set up root window
    root = tk.Tk()
    root.title('Memcrutch')
    root.geometry('400x400')
    root.attributes('-alpha', 0.8)
    root.attributes('-topmost', True)

    app = NoteSearchWindow(root)
    # The app now will be called by a 'launcher' app when the search shortcut is pressed,
    # so we can assume that the search callback already needs to be called
    app.search_query_callback(None)
    tk.mainloop()

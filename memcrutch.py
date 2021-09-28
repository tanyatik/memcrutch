import tkinter
import tkinter as tk
from tkhtmlview import HTMLLabel
import local_search

# Settings
SEARCH_QUERY_KEYBOARD_SHORTCUT = '<Command-Shift-KeyPress-F>'
SEARCH_QUERY_KEYBOARD_SHORTCUT_HELP_TEXT = 'Command+Shift+F>'


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
            html=f'<h1>Press {SEARCH_QUERY_KEYBOARD_SHORTCUT_HELP_TEXT} to enter your search query</h1>')

        self.pack(fill=tkinter.BOTH, expand=1)

    def search_query_callback(self, event):
        print(f'search query callback called! {event}')
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

        # Display results
        # TODO: cycle through search results
        if not results:
            self.result_box.set_html('No result found')
            self.result_box.pack(fill=tkinter.BOTH, expand=1)
            self.result_box.fit_height()

        for first_result in results:
            self.result_box.set_html(first_result.html)
            self.result_box.pack(fill=tkinter.BOTH, expand=1)
            self.result_box.fit_height()
            break


if __name__ == '__main__':
    # Set up root window
    root = tk.Tk()
    root.title('Memcrutch')
    root.geometry('400x400')
    root.attributes('-alpha', 0.6)
    root.attributes('-topmost', True)
    # root.withdraw()

    app = NoteSearchWindow(root)
    root.bind(SEARCH_QUERY_KEYBOARD_SHORTCUT, app.search_query_callback)
    tk.mainloop()

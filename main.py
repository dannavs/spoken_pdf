import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from types import NoneType

from pypdf import PdfReader
import subprocess


current_page = 1
file_page_count = 0
file_contents = PdfReader
file_loc = NoneType


def open_file_dialog():
    global file_loc
    speak("Open PDF")
    file_loc = filedialog.askopenfilename(title="Choose a PDF file to read", filetypes=[("PDF files", "*.pdf")])
    if file_loc:
        # user_pdf_file_label.config(text=f'Opened file: {file_loc}')
        pdf_to_text(file_loc)

def pdf_to_text(file_loc):
    print(f"Get the text to read from {file_loc}.")
    global current_page, file_page_count, file_contents
    try:
        with open(file_loc, 'r'):
            file_contents = PdfReader(file_loc)
            file_page_count = len(file_contents.pages)
            file_contents_page_temp = file_contents.pages[current_page - 1]
            file_text.delete('1.0', tk.END)
            file_text.insert(tk.END, file_contents_page_temp.extract_text())
            user_pdf_file_label.config(text=f'Page: {current_page} / {file_page_count}')
    except Exception as error_msg:
        user_pdf_file_label.config(text=f'Error: {error_msg}')


def page_change(direction):
    global current_page, file_page_count, file_contents, file_loc

    if file_page_count == 0: # if no file open / zero pages
        return
    if direction == 'forward': # move one page forward
        current_page += 1
        if current_page > file_page_count: # if at the end, go to the first page
            current_page = 1
    elif direction == 'backward': # move one page backward
        current_page -= 1
        if current_page < 1: # if at the beginning, go to the last page
            current_page = file_page_count
    else:
        print("Strange page number")

    # print(f'Trying to show page {current_page - 1}')
    file_contents_page_temp = file_contents.pages[current_page - 1]
    user_pdf_file_label.config(text=f'Page: {current_page} / {file_page_count}')
    file_text.delete('1.0', tk.END)
    file_text.insert(tk.END, file_contents_page_temp.extract_text())


def speak(words):
    if file_page_count == 0: # if no file open / zero pages
        return
    try:
        subprocess.call(['say', words])
    except TypeError:
        print("No PDF text loaded")

root = tk.Tk()
root.title("PDF Read to Me")

frame_main = ttk.Frame(root, padding="5 5 5 5")
frame_main.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

user_pdf_file_open = ttk.Button(frame_main, text="Open PDF", command=open_file_dialog, width=25)
user_pdf_file_open.grid(row=0, column=1)

user_pdf_read_aloud = ttk.Button(frame_main, text="Read Aloud", command=lambda: speak(file_contents.pages[current_page - 1].extract_text()))
user_pdf_read_aloud.grid(row=1, column=1)

user_pdf_file_label = ttk.Label(frame_main, text="")
user_pdf_file_label.grid(row=1, column=1)

user_pdf_page_back = ttk.Button(frame_main, text="Back", command=lambda: page_change('backward'))
user_pdf_page_back.grid(row=2, column=0)
user_pdf_page_number = ttk.Label(frame_main)
user_pdf_file_label.grid(row=2, column=1)
user_pdf_page_forward = ttk.Button(frame_main, text="Forward", command=lambda: page_change('forward'))
user_pdf_page_forward.grid(row=2, column=2)

file_text = tk.Text(frame_main, wrap=tk.WORD, height=50, width=100)
file_text.grid(row=3, column=0, columnspan=3)


root.mainloop()
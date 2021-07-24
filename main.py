from PyPDF2 import PdfFileReader
from tkinter import *
from tkinter import filedialog
import simpleaudio as sa
import requests
import os

# -------------------- Program Logic -------------------- #
TTS_URL_ENDPOINT = "http://api.voicerss.org/?key="
API_KEY = os.environ.get("API_KEY")


def choose_pdf():
    filename = filedialog.askopenfilename(
        initialdir="/",  # for Linux and Mac users
        # initialdir = "C:/",   for windows users
        title="Select a File",
        filetypes=(("PDF files", "*.pdf*"), ("all files", "*.*")))
    if filename:
        return filename


def read_pdf():
    filename = choose_pdf()
    reader = PdfFileReader(filename)
    pageObj = reader.getNumPages()
    for page_count in range(pageObj):
        page = reader.getPage(page_count)
        page_data = page.extractText()
        textbox.insert(END, page_data)


def read_aloud():
    text_to_read = textbox.get("1.0", END)
    target = f"{TTS_URL_ENDPOINT}{API_KEY}&hl=en-us&src={text_to_read}"
    response = requests.get(target)

    with open('tts.wav', 'bw') as f:
        f.write(response.content)

    w_object = sa.WaveObject.from_wave_file("tts.wav")
    p_object = w_object.play()


# -------------------- UI -------------------- #


ws = Tk()
ws.title('PythonGuides')
ws.geometry('400x300')
ws.config(bg='#D9653B')

textbox = Text(
    ws,
    height=13,
    width=40,
    wrap='word',
    bg='#D9BDAD'
)
textbox.pack(expand=True)

Button(
    ws,
    text='Choose Pdf File',
    padx=20,
    pady=10,
    bg='#262626',
    fg='white',
    command=read_pdf
).pack(expand=True, side=LEFT, pady=10)

Button(
    ws,
    text="Read Text",
    padx=20,
    pady=10,
    bg='#262626',
    fg='white',
    command=read_aloud
).pack(expand=True, side=LEFT, pady=10)

ws.mainloop()

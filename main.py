import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
from gtts import gTTS
import threading

# -------------------------------- CONSTANTS -------------------------- #
WHITE = "#FFFFFF"
BLUE = "#231955"
GREEN = "#7DCE13"
RED='#FF1E00'


# ------------------------------- FUNCTIONS --------------------------- #
def upload_file():
    global convert_text
    global filename
    # Upload the file
    f_types = [('PDF Files', '*.pdf')]
    filename = filedialog.askopenfilename(filetypes=f_types)

    # Get the filename
    get_filename_alone = filename.split('/')[-1:][0]

    # Display the filename
    upd_file_name_lbl.config(text=get_filename_alone)

    # Enable the convert button
    button_convert.config(state=tk.NORMAL)

    # Read the PDF document
    reader = PdfReader(filename)
    number_of_pages = len(reader.pages)

    # Extract the text in all pages
    convert_text = ""
    for i in range(0, number_of_pages):
        page = reader.pages[i]
        convert_text = convert_text + " " + page.extract_text()


def convert_file():
    # Disable the buttons
    button_upload.config(state=tk.DISABLED)
    button_convert.config(state=tk.DISABLED)

    # Get the audio file name
    audio_file = f"{filename.split('/')[-1:][0]}"
    audio_file = audio_file.replace('pdf', 'mp3')
    language = 'en'

    # Convert text to Audio
    convert_mp3 = gTTS(text=convert_text, lang=language, slow=True)

    # Save the audio file
    convert_mp3.save(audio_file)

    # Display the completion message
    mp3_file_name_lbl.config(text=f"{audio_file} Saved....")

    # Disable the buttons
    button_upload.config(state=tk.NORMAL)


# -------------------------------- UI SETUP --------------------------- #
window = tk.Tk()
window.title("Convert PDF into AudioBook")
window.minsize(width=300, height=400)
window.config(padx=10, pady=10, bg=WHITE)

# Get the image
folder_img = tk.PhotoImage(file='bg-img.png')

# Show app name
app_name = tk.Label(window, text="Convert PDF into AudioBook", bg=WHITE, fg=BLUE, font=('Arial', 16, 'italic'))
app_name.grid(column=0, row=0, sticky='we')

# Show image using label
image_label = tk.Label(window, image=folder_img)
image_label.grid(column=0, row=1, sticky='we')

# Show Upload Button
button_upload = tk.Button(window, text="Upload PDF", bg=BLUE, fg=WHITE, highlightthickness=0, command=lambda:upload_file())
button_upload.grid(column=0, row=2, sticky='we')

# Show Convert Button
button_convert = tk.Button(window, text="Convert", bg=BLUE, fg=WHITE, highlightthickness=0, state=tk.DISABLED, command=threading.Thread(target=convert_file).start)
button_convert.grid(column=0, row=3, sticky='we')

# Show upload file name using label
upd_file_name_lbl = tk.Label(window, text="", bg=WHITE, fg=RED, font=('Arial', 10, 'italic'))
upd_file_name_lbl.grid(column=0, row=4, columnspan=3, sticky='we')

# Show mp3 file name using label
mp3_file_name_lbl = tk.Label(window, text="", bg=WHITE, fg=RED, font=('Arial', 10, 'italic'))
mp3_file_name_lbl.grid(column=0, row=5, columnspan=3, sticky='we')

window.mainloop()
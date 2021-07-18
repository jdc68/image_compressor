from PIL import Image as Pimage
from tkinter.filedialog import *
import os
import tempfile
import tkinter as tk

file_paths = ""
saveDirectory = ""


def chose_files():
    global file_paths
    file_paths = askopenfilenames()


def choose_save_directory():
    global saveDirectory
    saveDirectory = askdirectory()
    print(saveDirectory)


def compress_images():
    try:
        min_file_size = int(ent_min_file_size.get()) * 1000
        lbl_status.config(text="Compressing " + str(len(file_paths)) + " files...")
    except ValueError:
        lbl_status.config(text="The minimal file size should be an integer")
    img_index = len([name for name in os.listdir(saveDirectory) if os.path.isfile(os.path.join(saveDirectory, name))]) + 1
    try:
        for file_path in file_paths:
            with tempfile.TemporaryDirectory() as tempDirectory:
                quality = 100
                save_path = saveDirectory + "/img{}_compressed.jpg" \
                    .format(img_index)
                img = Pimage.open(file_path)
                converted_img = img.convert('RGB')
                if os.stat(file_path).st_size > min_file_size:
                    while quality >= 1:
                        temp_path = tempDirectory + "/img{}_compressed.jpg" \
                            .format(quality)
                        converted_img.save(temp_path, optimize=True, quality=quality)
                        if os.stat(temp_path).st_size <= min_file_size:
                            converted_img.save(save_path, optimize=True, quality=quality)
                            msg = "Image {} compressed from {} KB to {} KB with quality {}%" \
                                .format(img_index, os.stat(file_path).st_size / 1000, os.stat(temp_path).st_size / 1000,
                                        quality)
                            print(msg)
                            break
                        else:
                            quality -= 1
                else:
                    msg = "Image {} is already  small enough, no need to compress" \
                        .format(img_index)
                    print(msg)
                    converted_img.save(save_path)
                img_index += 1
        lbl_status.config(text=str(len(file_paths)) + " files compressed successfully!")
    except FileNotFoundError:
        lbl_status.config(text="Please choose a directory for compressed files")
    except:
        lbl_status.config(text="Couldn't compress files")




window = tk.Tk()
window.title("Image Compressor")
frm = tk.Frame(master=window)
ent_frm = tk.Frame(master=frm)
btn_save = tk.Button(
    text="Choose save directory",
    width=20,
    height=2,
    command=choose_save_directory,
    master=frm
)
btn_files = tk.Button(
    text="Choose files to compress",
    width=20,
    height=2,
    command=chose_files,
    master=frm
)
btn_compress = tk.Button(
    text="Compress",
    width=20,
    height=2,
    command=compress_images,
    master=frm
)
lbl_size = tk.Label(master=ent_frm, text="Minimal size of output files (KB):")
ent_min_file_size = tk.Entry(master=ent_frm, width=20)

frm.grid(row=0, column=0, padx=20, pady=20)
btn_save.grid(row=0, column=1)
btn_files.grid(row=0, column=3)
ent_frm.grid(row=1, column=2, padx=40, pady=40)
lbl_size.grid(row=0, column=1)
ent_min_file_size.grid(row=1, column=1)
btn_compress.grid(row=2, column=2)
lbl_status = tk.Label(master=frm, text="")
lbl_status.grid(row=3, column=2)

window.mainloop()

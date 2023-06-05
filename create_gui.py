import pickle
from tkinter import *
from tkinter.font import Font
from tkinter import filedialog      ### exe erstellen und testen
import pickle                       ### Horizontale srollbar beim öffen von xml datei?
import sys
import os
import customtkinter,tkinter
import xml.etree.ElementTree as ET

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, gr

root = customtkinter.CTk()
root.title("pyMANGA.exe")
#root.iconbitmap("pyMANGA_image.ico")

#width= root.winfo_screenwidth()
#height= root.winfo_screenheight()
#root.geometry("%dx%d+0+0" % (width, height))
root.state("zoomed")
#root.attributes('-fullscreen',True)
#root.geometry("1400x900")

# Create layout

#progressbar = customtkinter.CTkProgressBar(master=root, mode='indeterminate')
#progressbar.pack(padx=10, pady=10)


bg_frame = customtkinter.CTkFrame(master=root, corner_radius=10)
bg_frame.pack(fill=X, side="bottom",padx=10,anchor =SW, pady=10)

bg_frame1 = customtkinter.CTkFrame(master=root, width=300, height=840, corner_radius=10)
bg_frame1.pack(fill=Y,side="left", padx=10,pady=10)

textbox_frame = customtkinter.CTkFrame(master=root,width=1000, height=830, corner_radius=10)
textbox_frame.pack(side="left",fill=BOTH,padx=10,pady=10,expand=True)

#textbox_frame2 = customtkinter.CTkFrame(master=root,width=1000, height=830, corner_radius=10)
#textbox_frame2.pack(side="left",fill=Y,padx=10,pady=10)


button_frame = customtkinter.CTkFrame(master=bg_frame1, width=280, height=90, corner_radius=10)
button_frame.pack(side="top",padx=10,pady=10,ipady=5)

label_frame = customtkinter.CTkFrame(master=bg_frame1,width=280, height=700, corner_radius=10)
label_frame.pack(fill=Y,padx=10,pady=10,expand=True)

Open_path = customtkinter.CTkLabel(textbox_frame,
                                    corner_radius=10,
                                    fg_color='#333333',
                                    text='Open path:        ',
                                    anchor=W)
Open_path.pack(fill=X, side="top",padx=10, pady=5)

description = customtkinter.CTkLabel(label_frame,
                                    corner_radius=10,
                                    width=280,
                                    height=700,
                                    text='Application description of pyMANGA:',
                                    anchor=NW)
description.pack(padx=10, pady=5)

# Create textbox
textbox = customtkinter.CTkTextbox(textbox_frame, width=980, height=810)#textbox = Text(textbox_frame, width=980, height=810,bg="#292929",bd=0,fg="white")
textbox.pack(fill=BOTH, side="left", padx=10, pady=10,expand =True)

manga_dir = os.getcwd()
#description = open(file_name, ("r"))

# Functions
def go():

    global file_name
    textbox.delete(1.0, END)
    status_bar.configure(text='Ready        ')

    file_name = filedialog.askopenfilename(
        #initialdir="/Benchmarks",
        title="Open file",
        filetypes=(
            ("Dat Files", "*.xml"),
            ("All Files", "*.*"))
    )
    name = file_name

    Open_path.configure(text="Open file: " + f'{name}     ')

    basename = os.path.basename(file_name)
    root.title("pyMANGA.exe - Open file: " + basename)

    input_file = open(file_name, ("r"))
    stuff = input_file.read()
    textbox.insert(END, stuff)
    input_file.close()

def start ():
    commandline = manga_dir.replace("\\","/") + '/pyMANGA/MANGA.py -i ' + file_name #commandline = manga_dir.replace("\\","/") + '/pyMANGA/MANGA.py -i ' + file_name
    print(commandline)
    print(file_name)
    file_save = open(file_name, ("w"))
    file_save.write(textbox.get(1.0, END))
    file_save.close()

    try:
        os.system(commandline)
        success = "pyMANGA was successfully executed, select an output file."
        status_bar.configure(text= f'{success}     ')

        tree = ET.parse(file_name)
        root_tree = tree.getroot()
        for tree_output in root_tree.findall("tree_output"):
            # print(tree_output.tag,tree_output.attrib)

            output = tree_output.find("output_dir")
            # print(output)
            global output_text
            output_text = output.text
            # print(output_text)

        file_output = filedialog.askopenfilename(
            initialdir=output_text,
            title="Open output file",
            filetypes=(
                ("Dat Files", "*.csv"),
                ("All Files", "*.*"))
        )
        output_path = open(file_output, ("r"))
        stuff_output = output_path.read()
        output_path.close()

        window = customtkinter.CTkToplevel()
        # window.geometry("400x200")
        window.title("pyMANGA.exe")
        #window.iconbitmap("pyMANGA_image.ico")
        window.geometry("1500x500")

        basename_w = os.path.basename(file_output)
        window.title("pyMANGA.exe - Output file: " + basename_w)

        bg_frame_w = customtkinter.CTkFrame(master=window, width=150, height=840, corner_radius=10)
        bg_frame_w.pack(fill=Y, side="left", padx=10, pady=10)
        button_frame_w = customtkinter.CTkFrame(master=bg_frame_w, width=280, height=90, corner_radius=10)
        button_frame_w.pack(side="top", padx=10, pady=10)
        textbox_frame3 = customtkinter.CTkFrame(master=window, width=1000, height=830, corner_radius=10)
        textbox_frame3.pack(side="top", fill=BOTH, padx=10, pady=10)

        output_path = customtkinter.CTkLabel(textbox_frame3,
                                             corner_radius=10,
                                             fg_color='#333333',
                                             text='Output path: '+file_output,
                                             anchor=W)

        output_path.pack(fill=X, side="top", padx=10, pady=5)

        textbox3 = customtkinter.CTkTextbox(textbox_frame3, width=1000, height=830, corner_radius=10)#textbox3 = Text(textbox_frame3, width=1000, height=830,bg="#292929",bd=0, fg="white")#
        textbox3.pack(side="top", fill=BOTH, padx=10, pady=10)

        textbox3.insert(END, stuff_output)

        def output():
            textbox3.delete(1.0, END)
            file_output1 = filedialog.askopenfilename(
                initialdir=output_text,
                title="Open output file",
                filetypes=(
                    ("Dat Files", "*.csv"),
                    ("All Files", "*.*"))
            )
            name1 = file_output1
            output_path1 = open(file_output1, ("r"))
            stuff_output = output_path1.read()

            basename_w1 = os.path.basename(file_output1)
            window.title("pyMANGA.exe - Output file: " + basename_w1)
            print(output_path1)
            output_path.configure(text="Open file: " + f'{name1}')

            textbox3.insert(END, stuff_output)
            output_path1.close()
            window.attributes("-topmost", True)

        open_output = customtkinter.CTkButton(button_frame_w,
                                              text="Open output file",
                                              width=11,
                                              height=32,
                                              border_width=1,
                                              command=output)
        # go_button.grid(row=1, column=0, padx=5,pady=5)
        open_output.pack(padx=60, pady=20)


    except:
        error = "An error occurred during the execution of pyMANGA."
        status_bar.configure(text= f'{error}     ')
    #progressbar.stop

#Add some buttons
go_button = customtkinter.CTkButton(button_frame,
                                    text="Load a work file",
                                    width= 11,
                                    height=32,
                                    border_width=1,
                                    command=go)
#go_button.grid(row=1, column=0, padx=5,pady=5)
go_button.pack(side="top",padx=60,pady=10)
#go_button.grid(row=1, column=0, padx=5,pady=5)

start_button = customtkinter.CTkButton(button_frame,
                                       text="Start pyMANGA",
                                       width  = 12,
                                       height=32,
                                       border_width=1,
                                       command=start#command=lambda: [progressbar.start(),start()]
                                       )

#start_button.grid(row=1, column=0, padx=5,pady=5)
start_button.pack(side="top",padx=60)
# Add status bar to bottom of App
status_bar = customtkinter.CTkLabel(bg_frame,
                                    corner_radius=10,
                                    fg_color='#1F1F1F',
                                    width=1180,
                                    height=25,
                                    text='Ready        ',
                                    anchor=E)
status_bar.pack(fill=X, side="bottom",padx=5,anchor =SW, pady=5)

root.mainloop()

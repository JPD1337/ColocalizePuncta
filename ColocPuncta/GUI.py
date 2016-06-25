import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
import os
import os.path

class ColocGUI:
    def  __init__(self):
        self.root = tk.Tk()

        self.folder_one = tk.StringVar()
        self.folder_two = tk.StringVar()
        self.distinct_channel_one = tk.StringVar()
        self.distinct_channel_two = tk.StringVar()

        self.files_one = tk.StringVar()
        self.files_two = tk.StringVar()

        self.folder_one.trace_variable("w", self.update_files)
        self.folder_two.trace_variable("w", self.update_files)
        self.distinct_channel_one.trace_variable("w", self.update_files)
        self.distinct_channel_two.trace_variable("w", self.update_files)

        self.root.title("Colocalization toolkit")
        self.root.iconbitmap("files/icon.ico")
        self.initialize_gui()

        self.root.minsize(800, 600)
        self.root.geometry("800x600+200+150")
        self.root.mainloop()

    def initialize_gui(self):
        self.create_main_settings()
        self.create_bottom_bar()

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def pick_folder(self, folder_number):
        selected_folder = tkinter.filedialog.askdirectory(title="Pick folder with pictures of channel {}".format(folder_number), mustexist=True)

        if os.path.isdir(selected_folder):
            if folder_number == 1:
                self.folder_one.set(selected_folder)
            elif folder_number == 2:
                self.folder_two.set(selected_folder)

    def update_files(self, *args):
        folder_one = self.folder_one.get()
        folder_two = self.folder_two.get()

        distinct_one = self.distinct_channel_one.get()
        distinct_two = self.distinct_channel_two.get()

        #TODO: export to seperate function

        if os.path.isdir(folder_one) and os.path.isdir(folder_two):
            files_one = os.listdir(folder_one)
            self.files_one = tk.StringVar(value=files_one)
            self.files_one_listbox.configure(listvariable=self.files_one)

            files_two = os.listdir(folder_two)
            self.files_two = tk.StringVar(value=files_two)
            self.files_two_listbox.configure(listvariable=self.files_two)

            for i in range(0,len(files_one)):
                f_new = os.path.join(folder_two, files_one[i].replace(distinct_one, distinct_two))

                if f_new == os.path.join(folder_one, files_one[i]):
                    self.files_one_listbox.itemconfigure(i, background='red')
                elif os.path.isfile(f_new):
                    self.files_one_listbox.itemconfigure(i, background='light green')
                else:
                    self.files_one_listbox.itemconfigure(i, background='orange')

            for i in range(0,len(files_two)):
                f_new = os.path.join(folder_one, files_two[i].replace(distinct_two, distinct_one))

                if f_new == os.path.join(folder_two, files_two[i]):
                    self.files_two_listbox.itemconfigure(i, background='red')
                elif os.path.isfile(f_new):
                    self.files_two_listbox.itemconfigure(i, background='light green')
                else:
                    self.files_two_listbox.itemconfigure(i, background='orange')

    def create_main_settings(self):
        settings_frame = ttk.Frame(self.root)
        
        ttk.Label(settings_frame, text = "Channel 1 folder:").grid(row = 0, column = 0)
        ttk.Entry(settings_frame, textvariable=self.folder_one).grid(row = 0, column = 1, sticky='WE')
        ttk.Button(settings_frame, text = "Browse...", command=lambda: self.pick_folder(1)).grid(row = 0, column = 2)

        ttk.Label(settings_frame, text = "Channel 2 folder:").grid(row = 1, column = 0)
        ttk.Entry(settings_frame, textvariable=self.folder_two).grid(row = 1, column = 1, sticky='WE')
        ttk.Button(settings_frame, text = "Browse...", command=lambda: self.pick_folder(2)).grid(row = 1, column = 2)

        channel_settings_frame = ttk.Frame(settings_frame)

        ttk.Label(channel_settings_frame, text = "Distinct name of channel 1 images:").grid(row=0, column=0)
        ttk.Entry(channel_settings_frame, textvariable=self.distinct_channel_one).grid(row = 0, column = 1, sticky='WE')
        ttk.Label(channel_settings_frame, text = "Distinct name of channel 2 images:").grid(row=0, column=2)
        ttk.Entry(channel_settings_frame, textvariable=self.distinct_channel_two).grid(row = 0, column = 3, sticky='WE')

        info_label = tk.Text(channel_settings_frame, wrap='word', font='Arial 8', foreground="gray", height = 4)
        info_label.insert(1.0, "The distinct part describes, which part of the filename is unique. E.g. if your images in the channel 1 folder are named 'image_shank1.tif', and the channel 2 images are named 'image_psd95.tif', you would enter 'shank1' in the first input, and 'psd95' in the second input.\nBelow you can make sure that your paramteres are correct. Orange entries indicate, that no matching image was found. Green entries indicate, that a matching image was detected. To ensure that all images are present, make sure that all entries are green. Red entires point were matched to themselves. This can happen, when you select the same folder twice.")
        info_label.configure( bg=self.root.cget('bg'), relief='flat', state='disabled' )
        info_label.grid(row=1, column=0, columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W))

        check_settings_frame = ttk.LabelFrame(settings_frame, text="Check settings")

        ttk.Label(check_settings_frame, text="Channel 1 files:").grid(row=0, column=0, columnspan=2, sticky="W")
        ttk.Label(check_settings_frame, text="Channel 2 files:").grid(row=0, column=2, columnspan=2, sticky="W")

        self.files_one_listbox = tk.Listbox(check_settings_frame)
        self.files_two_listbox = tk.Listbox(check_settings_frame)

        self.files_one_listbox.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.files_two_listbox.grid(row=1, column=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        s_one = ttk.Scrollbar(check_settings_frame, orient=tk.VERTICAL, command=self.files_one_listbox.yview)
        self.files_one_listbox.configure(yscrollcommand=s_one.set)
        s_one.grid(row=1, column=1, sticky=(tk.N, tk.S))

        s_two = ttk.Scrollbar(check_settings_frame, orient=tk.VERTICAL, command=self.files_two_listbox.yview)
        self.files_two_listbox.configure(yscrollcommand=s_two.set)
        s_two.grid(row=1, column=3, sticky=(tk.N, tk.S))

        channel_settings_frame.grid(row=2, columnspan=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        check_settings_frame.grid(row=3, columnspan=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        channel_settings_frame.columnconfigure(0, weight = 0)
        channel_settings_frame.columnconfigure(1, weight = 1)
        channel_settings_frame.columnconfigure(2, weight = 0)
        channel_settings_frame.columnconfigure(3, weight = 1)
        channel_settings_frame.rowconfigure(0, weight = 0)
        channel_settings_frame.rowconfigure(1, weight = 0)

        settings_frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        settings_frame.columnconfigure(0, weight = 0)
        settings_frame.columnconfigure(1, weight = 1)
        settings_frame.columnconfigure(2, weight = 0)

        settings_frame.rowconfigure(0, weight = 0)
        settings_frame.rowconfigure(1, weight = 0)
        settings_frame.rowconfigure(2, weight = 0)
        settings_frame.rowconfigure(3, weight = 1)

        check_settings_frame.columnconfigure(0, weight = 1)
        check_settings_frame.columnconfigure(2, weight = 1)
        check_settings_frame.rowconfigure(0, weight = 0)
        check_settings_frame.rowconfigure(1, weight = 1)

        for child in settings_frame.winfo_children():
            child.grid_configure(padx=2, pady=3)

        for child in channel_settings_frame.winfo_children():
            child.grid_configure(padx=2, pady=3)

    def create_bottom_bar(self):
        bottom_frame = ttk.Frame(self.root)
        about_button = ttk.Button(bottom_frame, text="About", command=lambda: tkinter.messagebox.showinfo("About", "Colocalization Toolkit\n\nWritten by:\nChristian Jacob & Jan-Philipp Delling\n(c) 2016"))

        about_button.grid(row=0, column=0, sticky="E")
        bottom_frame.grid(row=1, column=0, sticky="NE")


if __name__ == '__main__':
    gui = ColocGUI()
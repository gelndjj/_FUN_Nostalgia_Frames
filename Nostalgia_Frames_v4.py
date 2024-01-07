import tkinter as tk
import os, shutil, csv
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from tkinter import ttk

class RetrogamingOverlayApp:
    def __init__(self, root):
        self.root = root
        root.title("Nostalgia Frames")
        root.geometry("830x385")

        # Right Frame for Image
        self.right_frame = tk.Frame(root)
        self.right_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=6)

        # Configure the main window grid columns for proportional sizing
        root.grid_columnconfigure(0, weight=1)  # Gives 1/3 space to the Treeview
        root.grid_columnconfigure(1, weight=2)  # Gives 2/3 space to the image display

        # Left Frame for Treeview and controls
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, sticky='nsew')
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=0)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Treeview setup
        self.file_treeview = ttk.Treeview(self.left_frame)
        self.file_treeview.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.file_treeview.bind("<<TreeviewSelect>>", self.on_file_select)

        # Create a LabelFrame for controls below the Treeview
        self.controls_frame = tk.LabelFrame(self.left_frame, text="Overlay Controls", padx=10, pady=10)
        self.controls_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        # Configure the grid within the left_frame to fill the space
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Width and Height Entry fields with "x" label between them, all within the controls_frame
        self.entry_frame = tk.Frame(self.controls_frame)
        self.entry_frame.grid(row=0, column=0, sticky='ew')

        self.width_entry = tk.Entry(self.entry_frame, width=5)
        self.width_entry.pack(side=tk.LEFT)

        self.label_x = tk.Label(self.entry_frame, text="x")
        self.label_x.pack(side=tk.LEFT)

        self.height_entry = tk.Entry(self.entry_frame, width=5)
        self.height_entry.pack(side=tk.LEFT)

        # "Create Overlay" button within the controls_frame
        self.create_overlay_button = tk.Button(self.controls_frame, text="Create Overlay", command=self.create_overlay)
        self.create_overlay_button.grid(row=1, column=0, sticky='ew')

        # "Load Pictures" button within the controls_frame
        self.load_pictures_button = tk.Button(self.controls_frame, text="Add Pictures", command=self.load_pictures)
        self.load_pictures_button.grid(row=2, column=0, sticky='ew')

        # "Edit CSV" button within the controls_frame
        self.edit_csv_button = tk.Button(self.controls_frame, text="Edit CSV", command=self.edit_csv)
        self.edit_csv_button.grid(row=3, column=0, sticky='ew')

        # Image label within the right frame for displaying the picture
        self.image_label = tk.Label(self.right_frame, borderwidth=2, relief="groove")
        self.image_label.pack(fill='both', expand=True)

        # Load images from the current working directory
        self.load_images(os.getcwd())

        # Bind the save function to the close event
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Bind 'r' key to the update_listbox method
        root.bind('r', lambda event: self.update_listbox())

        # Bind the Backspace key
        self.root.bind('<BackSpace>', lambda event: self.delete_selected_files())

        # System ComboBox
        self.system_combobox = ttk.Combobox(self.entry_frame, width=14)
        self.system_combobox.pack(side=tk.LEFT, padx=5)
        self.system_combobox.set("Select a system")
        self.system_resolutions = {}
        self.load_systems_from_csv()

        # Load and display the default image 'bg.png'
        default_image_path = os.path.join(os.getcwd(), 'bg.jpg')
        if os.path.exists(default_image_path):
            default_image = Image.open(default_image_path)
            default_photo = ImageTk.PhotoImage(default_image.resize((320, 180), Image.Resampling.LANCZOS))
            self.image_label.config(image=default_photo, text='')
            self.image_label.image = default_photo
        else:
            self.image_label.config(text="No Image Selected")

    def load_images(self, directory):
        # Clear existing items
        for i in self.file_treeview.get_children():
            self.file_treeview.delete(i)

        # List all PNG files and sort them
        files = [file for file in os.listdir(directory) if file.lower().endswith(".png")]
        sorted_files = sorted(files)

        # Add sorted files to the treeview
        for file in sorted_files:
            file_path = os.path.join(directory, file)
            with Image.open(file_path) as img:
                if img.size == (1920, 1080):
                    self.file_treeview.insert('', 'end', text=file, tags=('1080p',))
                else:
                    self.file_treeview.insert('', 'end', text=file, tags=('non1080p',))

        self.file_treeview.tag_configure('non1080p', foreground='gray')

    def load_systems_from_csv(self):
        csv_path = 'Resolutions integer scaling.csv'
        try:
            with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                systems = set()
                for row in reader:
                    try:
                        system_name = row['System']
                        width = row['viewport_width']
                        height = row['viewport_height']
                        systems.add(system_name)
                        self.system_resolutions[system_name] = (width, height)
                    except KeyError as e:
                        messagebox.showerror("CSV Format Error", f"Column missing in CSV: {e}")
                        return
                self.system_combobox['values'] = sorted(systems)
                self.system_combobox.bind("<<ComboboxSelected>>", self.on_system_select)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"CSV file not found: {csv_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the CSV file: {e}")

    def edit_csv(self):
        # Create a Toplevel window
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit CSV")

        # Create a Treeview to display the CSV data
        self.csv_treeview = ttk.Treeview(self.edit_window, columns=("System", "viewport_width", "viewport_height"))
        self.csv_treeview.heading('#0', text='ID')
        self.csv_treeview.heading('System', text='System')
        self.csv_treeview.heading('viewport_width', text='Width')
        self.csv_treeview.heading('viewport_height', text='Height')
        self.csv_treeview.column('#0', width=40)
        self.csv_treeview.column('System', width=100)
        self.csv_treeview.column('viewport_width', width=100)
        self.csv_treeview.column('viewport_height', width=100)
        self.csv_treeview.pack(fill='both', expand=True)

        # Add buttons for editing the CSV
        btn_frame = tk.Frame(self.edit_window)
        btn_frame.pack(fill='x', expand=False)
        add_btn = tk.Button(btn_frame, text="Add Row", command=self.add_row_to_csv)
        edit_btn = tk.Button(btn_frame, text="Edit Selected", command=self.edit_selected_row)
        del_btn = tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected_row)
        add_btn.pack(side='left', fill='x', expand=True)
        edit_btn.pack(side='left', fill='x', expand=True)
        del_btn.pack(side='left', fill='x', expand=True)

        # Load CSV data into the Treeview
        self.load_csv_into_treeview()

    def load_csv_into_treeview(self):
        # Clear the Treeview
        for row in self.csv_treeview.get_children():
            self.csv_treeview.delete(row)

        # Read the CSV and populate the Treeview
        try:
            with open('Resolutions integer scaling.csv', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for i, row in enumerate(reader):
                    self.csv_treeview.insert('', 'end', iid=i, text=str(i),
                                             values=(row['System'], row['viewport_width'], row['viewport_height']))
        except FileNotFoundError:
            messagebox.showerror("Error", "CSV file not found.")

    def update_csv_treeview(self):
        # Clear the current contents of the Treeview
        for item in self.csv_treeview.get_children():
            self.csv_treeview.delete(item)

        # Reload and repopulate the Treeview
        try:
            with open('Resolutions integer scaling.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Check if the expected columns exist in the row
                    if 'System' in row and 'viewport_width' in row and 'viewport_height' in row:
                        self.csv_treeview.insert('', 'end',
                                                 values=(row['System'], row['viewport_width'], row['viewport_height']))
                    else:
                        raise KeyError("CSV file does not contain the expected columns.")
        except FileNotFoundError:
            print("CSV file not found.")
        except KeyError as e:
            print(e)

    def add_row_to_csv(self):
        add_dialog = tk.Toplevel(self.root)
        add_dialog.title("Add New Row")

        labels = ['System', 'Width', 'Height']
        entries = {}

        # Create labels and entry widgets
        for idx, label in enumerate(labels):
            tk.Label(add_dialog, text=label).grid(row=idx, column=0)
            entry = tk.Entry(add_dialog)
            entry.grid(row=idx, column=1)
            entries[label] = entry

        def save_new_row():
            # Read values from entries
            new_row = [entries[label].get() for label in labels]

            # Append to CSV file
            with open('Resolutions integer scaling.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(new_row)

            # Refresh the combobox with systems
            self.load_systems_from_csv()
            self.update_csv_treeview()
            add_dialog.destroy()

        # Add a Save button
        save_btn = tk.Button(add_dialog, text="Save", command=save_new_row)
        save_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

        add_dialog.grab_set()  # Optional: make the dialog modal
        add_dialog.mainloop()

    def edit_selected_row(self):
        selected_item = self.csv_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No row selected.")
            return

        # Get the current values of the selected row
        current_values = self.csv_treeview.item(selected_item, 'values')

        # Create a Toplevel window
        edit_dialog = tk.Toplevel(self.root)
        edit_dialog.title("Edit Row")

        # Create labels and entry widgets for each field
        labels = ['System', 'Width', 'Height']
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(edit_dialog, text=label).grid(row=i, column=0)
            entry = tk.Entry(edit_dialog)
            entry.grid(row=i, column=1)
            entry.insert(0, current_values[i])
            entries[label] = entry

        # Function to save the edited values
        def save_edited_values():
            new_values = [entries['System'].get(), entries['Width'].get(), entries['Height'].get()]
            self.csv_treeview.item(selected_item, values=new_values)
            self.update_csv_file()  # Update the CSV file with new values
            self.load_systems_from_csv()
            edit_dialog.destroy()

        # Add a Save button
        save_btn = tk.Button(edit_dialog, text="Save", command=save_edited_values)
        save_btn.grid(row=len(labels), column=1)

    def update_csv_file(self):
        # Write the Treeview content back to the CSV file
        with open('Resolutions integer scaling.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['System', 'viewport_width', 'viewport_height'])
            writer.writeheader()
            for child in self.csv_treeview.get_children():
                writer.writerow(dict(zip(writer.fieldnames, self.csv_treeview.item(child)['values'])))

    def delete_selected_row(self):
        selected_item = self.csv_treeview.selection()

        # Check if an item is selected
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a row to delete.")
            return

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected row?"):
            return

        # Remove the selected rows from the treeview
        for item in selected_item:
            self.csv_treeview.delete(item)

        # Read the current data from the treeview
        updated_data = []
        for child in self.csv_treeview.get_children():
            updated_data.append(self.csv_treeview.item(child)['values'])

        # Rewrite the CSV file
        with open('Resolutions integer scaling.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['System', 'viewport_width', 'viewport_height'])
            for row in updated_data:
                writer.writerow(row)

        # Reload the CSV data
        self.load_systems_from_csv()

    def on_system_select(self, event=None):
        selected_system = self.system_combobox.get()
        if selected_system in self.system_resolutions:
            width, height = self.system_resolutions[selected_system]
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, width)
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, height)
    def load_pictures(self):
        # Clear the listbox
        self.file_treeview.delete(0, tk.END)

        # Let the user select a folder
        folder_path = filedialog.askdirectory()

        if folder_path:
            # List all PNG files in the selected folder
            for file in os.listdir(folder_path):
                if file.lower().endswith(".png"):
                    file_path = os.path.join(folder_path, file)
                    destination = os.path.join(os.getcwd(), file)

                    # Copy the file to the root directory
                    shutil.copy(file_path, destination)

        # Refresh the listbox
        self.update_listbox()

    def on_close(self):
        # Check if the FTP window and comboboxes exist before saving server history
        if hasattr(self, 'ftp_window') and self.ftp_window.winfo_exists():
            self.save_server_history()

        self.root.destroy()

    def find_transparent_square_size(self, image):
        # Ensure the image is in RGBA mode which contains an alpha channel
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        pixels = image.load()
        center_x, center_y = image.width // 2, image.height // 2

        # Transparency threshold, pixels with an alpha value below this are considered transparent
        alpha_threshold = 128

        # Find the bounds of the transparent square
        left, top, right, bottom = center_x, center_y, center_x, center_y

        # Scan left
        while left > 0 and pixels[left, center_y][3] < alpha_threshold:
            left -= 1
        # Scan right
        while right < image.width and pixels[right, center_y][3] < alpha_threshold:
            right += 1
        # Scan up
        while top > 0 and pixels[center_x, top][3] < alpha_threshold:
            top -= 1
        # Scan down
        while bottom < image.height and pixels[center_x, bottom][3] < alpha_threshold:
            bottom += 1

        # Calculate the transparent square size
        transparent_square_width = right - left
        transparent_square_height = bottom - top

        return transparent_square_width, transparent_square_height

    def on_file_select(self, event):
        selected_item = self.file_treeview.selection()

        if selected_item:
            filename = self.file_treeview.item(selected_item[0], 'text')
            image_path = os.path.join(os.getcwd(), filename)

            if 'non1080p' in self.file_treeview.item(selected_item[0], 'tags'):
                children = self.file_treeview.get_children()
                idx = children.index(selected_item[0])

                # Determine the next or previous item
                if idx < len(children) - 1:
                    next_item = children[idx + 1]
                else:
                    next_item = children[idx - 1] if idx > 0 else None

                if next_item:
                    self.file_treeview.selection_set(next_item)
                    self.file_treeview.see(next_item)

                return

            # Enable fields and button for a single selection
            self.width_entry.config(state='normal')
            self.height_entry.config(state='normal')
            self.create_overlay_button.config(state='normal')

            # Handle the display of a single selected image
            image = Image.open(image_path)

            # Calculate the transparent square size and multiply by 6
            transparent_square_width, transparent_square_height = self.find_transparent_square_size(image)
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, str(transparent_square_width))
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, str(transparent_square_height))

            # Resize image for display
            display_image = image.resize((image.width // 6, image.height // 6), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(display_image)
            self.image_label.config(image=photo, text='')
            self.image_label.image = photo
        else:
            # No selection, display default image
            default_image_path = os.path.join(os.getcwd(), 'bg.png')
            if os.path.exists(default_image_path):
                default_image = Image.open(default_image_path)
                default_photo = ImageTk.PhotoImage(default_image.resize((480, 300), Image.Resampling.LANCZOS))
                self.image_label.config(image=default_photo, text='')
                self.image_label.image = default_photo
            else:
                self.image_label.config(text="No Image Selected")

            # Disable fields and button
            self.width_entry.config(state='disabled')
            self.height_entry.config(state='disabled')
            self.create_overlay_button.config(state='disabled')

    def update_listbox(self):
        # Remember the current selection
        selected_item = self.file_treeview.selection()
        selected_filename = None
        if selected_item:
            selected_filename = self.file_treeview.item(selected_item[0], 'text')

        # Clear the Treeview
        for item in self.file_treeview.get_children():
            self.file_treeview.delete(item)

        # List and sort all png files in the current working directory
        sorted_files = sorted([file for file in os.listdir(os.getcwd()) if file.lower().endswith(".png")])

        # Update the Treeview with sorted files
        for file in sorted_files:
            file_path = os.path.join(os.getcwd(), file)
            with Image.open(file_path) as img:
                if img.size == (1920, 1080):
                    self.file_treeview.insert('', 'end', text=file, tags=('1080p',))
                else:
                    self.file_treeview.insert('', 'end', text=file, tags=('non1080p',))

        # Configure tag for non-1080p images
        self.file_treeview.tag_configure('non1080p', foreground='gray')

        # Reselect the previously selected item, if applicable
        if selected_filename:
            for item in self.file_treeview.get_children():
                if self.file_treeview.item(item, 'text') == selected_filename:
                    self.file_treeview.selection_set(item)
                    self.file_treeview.see(item)
                    break

    def delete_selected_files(self):
        selected_items = self.file_treeview.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a file to delete.")
            return

        # Ask for confirmation
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected file(s)?"):
            for selected_item in selected_items:
                filename = self.file_treeview.item(selected_item, 'text')
                image_path = os.path.join(os.getcwd(), filename)
                cfg_filename = os.path.splitext(filename)[0] + ".cfg"
                cfg_path = os.path.join(os.getcwd(), cfg_filename)

                if os.path.exists(image_path):
                    os.remove(image_path)  # Delete the image file
                    self.file_treeview.delete(selected_item)  # Delete the item from the Treeview

                if os.path.exists(cfg_path):
                    os.remove(cfg_path)  # Delete the corresponding .cfg file if it exists

        self.update_listbox()

    def create_overlay(self):
        selected_items = self.file_treeview.selection()
        if not selected_items:
            messagebox.showinfo("Selection Required", "Please select an image.")
            return

        selected_item = selected_items[0]
        filename = self.file_treeview.item(selected_item, 'text')
        image_path = os.path.join(os.getcwd(), filename)
        original_image = Image.open(image_path)

        try:
            desired_width = int(self.width_entry.get())
            desired_height = int(self.height_entry.get())
        except ValueError:
            messagebox.showinfo("Invalid Input", "Please enter valid width and height.")
            return

        # Calculate the original transparent square size
        original_transparent_width, original_transparent_height = self.find_transparent_square_size(original_image)

        # Calculate the ratio for resizing
        width_ratio = desired_width / original_transparent_width
        height_ratio = desired_height / original_transparent_height

        # Resize the original image to the new size
        resized_image = original_image.resize(
            (int(original_image.width * width_ratio), int(original_image.height * height_ratio)),
            Image.Resampling.LANCZOS)

        # Create a new image with black background and original dimensions
        new_image = Image.new("RGBA", original_image.size, (0, 0, 0, 0))

        # Calculate position to paste the resized image in the center
        x_position = (new_image.width - resized_image.width) // 2
        y_position = (new_image.height - resized_image.height) // 2

        # Paste the resized image onto the new black background image
        new_image.paste(resized_image, (x_position, y_position), resized_image)

        # Save the new image
        new_image_filename = f"{os.path.splitext(filename)[0]}_{desired_width}x{desired_height}.png"
        new_image.save(os.path.join(os.getcwd(), new_image_filename))

        # Create the .cfg file
        cfg_content = f"""overlays = 1\n
    overlay0_overlay = "{new_image_filename}"\n
    overlay0_full_screen = true\n
    overlay0_descs = 0"""
        cfg_filename = f"{os.path.splitext(new_image_filename)[0]}.cfg"
        with open(os.path.join(os.getcwd(), cfg_filename), 'w') as cfg_file:
            cfg_file.write(cfg_content)

        messagebox.showinfo("Overlay Created", f"Overlay and configuration file '{cfg_filename}' created.")
        self.update_listbox()

root = tk.Tk()
app = RetrogamingOverlayApp(root)
root.mainloop()

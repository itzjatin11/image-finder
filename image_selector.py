import tkinter as tk
from tkinter import messagebox, ttk, Label, filedialog
import pyodbc
import os
from PIL import Image, ImageTk
class SearchPage:
    def __init__(self, root):
        """Initializes the SearchPage object and creates the main window."""
        self.root = root
        self.create_ui()  # Create the user interface
        self.conn = None
        self.cursor = None

    def create_ui(self):
        """Creates the user interface for the search page."""
        self.root.title("Search Customers")
        self.root.geometry("500x350")
        self.root.configure(bg="#f0f0f0")

        title_label = tk.Label(self.root, text="SEARCH CUSTOMERS", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=20)

        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=10)

        fname_label = tk.Label(input_frame, text="Customer First Name:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        fname_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.fname_entry = tk.Entry(input_frame, font=("Arial", 12), width=30, bg="#ffffff")
        self.fname_entry.grid(row=0, column=1, padx=10, pady=5)

        bdate_label = tk.Label(input_frame, text="Customer Birthdate:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        bdate_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        bdate_frame = tk.Frame(input_frame, bg="#f0f0f0")
        bdate_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.year_entry = tk.Entry(bdate_frame, width=6, justify="center", font=("Arial", 12), bg="#ffffff")
        self.year_entry.grid(row=0, column=0, padx=5)
        self.year_entry.insert(0, "YYYY")

        self.month_entry = tk.Entry(bdate_frame, width=4, justify="center", font=("Arial", 12), bg="#ffffff")
        self.month_entry.grid(row=0, column=1, padx=5)
        self.month_entry.insert(0, "MM")

        self.day_entry = tk.Entry(bdate_frame, width=4, justify="center", font=("Arial", 12), bg="#ffffff")
        self.day_entry.grid(row=0, column=2, padx=5)
        self.day_entry.insert(0, "DD")

        search_button = tk.Button(self.root, text="Search", width=15, font=("Arial", 12), bg="#4CAF50", fg="white", command=self.search_customer)
        search_button.pack(pady=20)

    def setup_database_connection(self):
        """Sets up the database connection."""
        db_path = r'C:\Users\Admin\OneDrive - Auckland Institute of Studies\Documents\imagefinder.accdb'
        
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found at {db_path}")
        
        conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};'
        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()

    def search_customer(self):
        """Searches for customers based on input criteria."""
        if not self.conn or not self.cursor:
            self.setup_database_connection()  # Establish the database connection if not already done

        first_name = self.fname_entry.get().strip()
        birth_year = self.year_entry.get().strip()
        birth_month = self.month_entry.get().strip()
        birth_day = self.day_entry.get().strip()

        # If year, month, or day are still default values, treat them as empty
        if birth_year == "YYYY":
            birth_year = ""
        if birth_month == "MM":
            birth_month = ""
        if birth_day == "DD":
            birth_day = ""

        if not any([first_name, birth_year, birth_month, birth_day]):
            messagebox.showwarning("Warning", "At least one field must be filled out.")
            return

        # Build the query based on available input
        query = "SELECT [Photo Path] FROM image WHERE 1=1"
        params = []

        if first_name:
            query += " AND [First Name] LIKE ?"
            params.append(f"%{first_name}%")  # Allow partial matching for names

        if birth_year:
            query += " AND [Birth Year] = ?"
            params.append(int(birth_year))

        if birth_month:
            query += " AND [Birth Month] = ?"
            params.append(int(birth_month))

        if birth_day:
            query += " AND [Birth Day] = ?"
            params.append(int(birth_day))

        # Search for matching images
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()

            if results:
                self.display_images([result[0] for result in results])
            else:
                messagebox.showinfo("Not Found", "No matching customer found.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    def display_images(self, image_paths):
        """Displays the images in a grid with clickable thumbnails."""
        gallery_window = tk.Toplevel(self.root)
        gallery_window.title("Image Gallery")
        gallery_window.configure(bg="#f0f0f0")

        for idx, image_path in enumerate(image_paths):
            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img.thumbnail((100, 100))  # Create thumbnail

                    # Convert PIL image to ImageTk for displaying in tkinter
                    img_tk = ImageTk.PhotoImage(img)

                    # Create a button with the image that opens it in a larger view
                    image_button = tk.Button(gallery_window, image=img_tk, command=lambda path=image_path: self.open_image(path), bd=0)
                    image_button.image = img_tk  # Keep reference to avoid garbage collection
                    image_button.grid(row=idx // 5, column=idx % 5, padx=10, pady=10)

                except Exception as e:
                    messagebox.showerror("Image Error", f"Failed to load image at {image_path}: {str(e)}")
            else:
                messagebox.showerror("File Not Found", f"Image file not found at {image_path}")

    def open_image(self, image_path):
        """Opens a full-sized version of the image."""
        try:
            img = Image.open(image_path)
            img = img.resize((400, 400))  # Resize image to a larger size

            # Create a new window for the expanded image
            expanded_window = tk.Toplevel(self.root)
            expanded_window.title("Expanded Image")
            expanded_window.configure(bg="#f0f0f0")

            # Convert image to ImageTk format
            img_tk = ImageTk.PhotoImage(img)

            # Create a label to display the image
            image_label = tk.Label(expanded_window, image=img_tk, bg="#f0f0f0")
            image_label.image = img_tk  # Keep reference to avoid garbage collection
            image_label.pack()

        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to open image: {str(e)}")

class DeleteCustomerApp:

    def __init__(self, root):
        """Initialize the DeleteCustomerApp with improved visual design and layout."""
        self.root = root
        self.root.title("Customer ID Database System (Delete)")
        self.root.geometry("600x550")  # Adjusted size to accommodate UI elements
        self.root.configure(bg="#f0f0f0")

        # Setup database connection
        self.conn, self.cursor = self.setup_database_connection()

        # Add a title label with better styling
        title_label = tk.Label(root, text="Customer ID Database System (Delete)", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=20)

        # Create a frame for input fields with improved padding and layout
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # Add labels and entry fields for the filename with better font and spacing
        fname_label = tk.Label(input_frame, text="Enter Filename:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        fname_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry_filename = tk.Entry(input_frame, font=("Arial", 12), width=30, bg="#ffffff")
        self.entry_filename.grid(row=0, column=1, padx=10, pady=10)

        # Add search and delete buttons with improved styling and alignment
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=20)

        button_search = tk.Button(button_frame, text="Search", width=15, font=("Arial", 12), bg="#4CAF50", fg="white", command=self.search_customer)
        button_search.grid(row=0, column=0, padx=10, pady=10)

        button_delete = tk.Button(button_frame, text="Delete", width=15, font=("Arial", 12), bg="#F44336", fg="white", command=self.delete_customer)
        button_delete.grid(row=0, column=1, padx=10, pady=10)

        # Add a frame for the image display with improved background color
        self.image_frame = tk.Frame(root, bg="#f0f0f0", bd=1, relief="sunken")
        self.image_frame.pack(pady=20)

        # Placeholder for storing the image path after a search
        self.image_path = None

    def setup_database_connection(self):
        """Setup the database connection."""
        db_path = r'C:\Users\Admin\OneDrive - Auckland Institute of Studies\Documents\imagefinder.accdb'
        
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found at {db_path}")
        
        conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        return conn, cursor

    def search_customer(self):
        """Search for the customer by filename and display the corresponding image."""
        filename = self.entry_filename.get().strip()

        # Validate input
        if not filename:
            messagebox.showwarning("Warning", "Filename cannot be empty.")
            return

        # Query the database to search for the customer by filename
        try:
            query = "SELECT [Photo Path] FROM image WHERE [Photo Path] LIKE ?"
            self.cursor.execute(query, ('%' + filename + '%',))
            result = self.cursor.fetchone()

            if result:
                self.image_path = result[0]
                self.display_image(self.image_path)  # Display the image
                messagebox.showinfo("Customer Found", f"Image found for: {filename}")
            else:
                self.image_path = None
                for widget in self.image_frame.winfo_children():
                    widget.destroy()  # Clear the image display if not found
                messagebox.showwarning("Not Found", "No customer found with the specified filename.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search for customer: {str(e)}")

    def display_image(self, image_path):
        """Display the image in the image frame after searching."""
        # Clear the previous image (if any)
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Open and display the image in a label
        try:
            img = Image.open(image_path)
            img = img.resize((250, 250), Image.LANCZOS)  # Resize image to fit in the window
            img_tk = ImageTk.PhotoImage(img)

            image_label = tk.Label(self.image_frame, image=img_tk, bg="#f0f0f0")
            image_label.image = img_tk  # Keep a reference to avoid garbage collection
            image_label.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image: {str(e)}")

    def delete_customer(self):
        """Delete the selected customer and image from the system."""
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected for deletion.")
            return

        try:
            # Ask for confirmation
            confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete the file '{self.image_path}'?")
            if confirm:
                # Delete the image file
                if os.path.exists(self.image_path):
                    os.remove(self.image_path)

                # Delete the record from the database
                delete_query = "DELETE FROM image WHERE [Photo Path] = ?"
                self.cursor.execute(delete_query, (self.image_path,))
                self.conn.commit()

                messagebox.showinfo("Success", "Customer and image deleted successfully!")

                # Clear the image display and entry after deletion
                for widget in self.image_frame.winfo_children():
                    widget.destroy()
                self.entry_filename.delete(0, tk.END)
                self.image_path = None
            else:
                messagebox.showinfo("Cancelled", "Deletion cancelled.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete customer: {str(e)}")

class CustomerImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer ID Database System (Add Customer)")
        self.root.geometry("550x400")
        self.root.configure(bg="#f0f0f0")  # Softer background color

        # Setup database connection
        self.conn, self.cursor = self.setup_database_connection()

        # Add a title label with enhanced styling
        title_label = tk.Label(root, text="Add New Customer", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=20)

        # Create a frame for input fields with padding and layout improvements
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # First Name Label and Entry with better spacing
        fname_label = tk.Label(input_frame, text="First Name:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        fname_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry_first_name = tk.Entry(input_frame, font=("Arial", 12), width=30, bg="#ffffff")
        self.entry_first_name.grid(row=0, column=1, padx=10, pady=10)

        # Birthdate Label and Entry fields organized in a frame with placeholders and alignment
        bdate_label = tk.Label(input_frame, text="Birthdate (YYYY/MM/DD):", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        bdate_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        bdate_frame = tk.Frame(input_frame, bg="#f0f0f0")
        bdate_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Year Entry
        self.entry_year = tk.Entry(bdate_frame, width=5, justify="center", font=("Arial", 12), bg="#ffffff")
        self.entry_year.grid(row=0, column=0, padx=5)
        self.entry_year.insert(0, "YYYY")

        # Month Entry
        self.entry_month = tk.Entry(bdate_frame, width=3, justify="center", font=("Arial", 12), bg="#ffffff")
        self.entry_month.grid(row=0, column=1, padx=5)
        self.entry_month.insert(0, "MM")

        # Day Entry
        self.entry_day = tk.Entry(bdate_frame, width=3, justify="center", font=("Arial", 12), bg="#ffffff")
        self.entry_day.grid(row=0, column=2, padx=5)
        self.entry_day.insert(0, "DD")

        # Image File Type Label and Dropdown with improved styling
        label_file_type = tk.Label(input_frame, text="Image File Type:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        label_file_type.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.combo_file_type = ttk.Combobox(input_frame, values=["jpg", "png", "jpeg"], font=("Arial", 12), width=28)
        self.combo_file_type.grid(row=2, column=1, padx=10, pady=10)
        self.combo_file_type.current(0)

        # Add Button with updated styling
        button_add = tk.Button(root, text="Add Customer", width=20, font=("Arial", 12), bg="#4CAF50", fg="white", command=self.add_customer)
        button_add.pack(pady=30)

    def setup_database_connection(self):
        """Set up a connection to the database."""
        db_path = r'C:\Users\Admin\OneDrive - Auckland Institute of Studies\Documents\imagefinder.accdb'
        
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found at {db_path}")
        
        conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        return conn, cursor

    def add_customer(self):
        """Add a new customer to the database."""
        first_name = self.entry_first_name.get().strip()
        birth_year = self.entry_year.get().strip()
        birth_month = self.entry_month.get().strip()
        birth_day = self.entry_day.get().strip()
        file_type = self.combo_file_type.get().strip()

        # Validate input
        if not all([first_name, birth_year, birth_month, birth_day]):
            messagebox.showwarning("Warning", "All fields must be filled out.")
            return

        # Format the birthdate
        birthdate = f"{birth_year}{birth_month.zfill(2)}{birth_day.zfill(2)}"
        new_filename = f"{first_name.lower()}-{birthdate}.{file_type}"

        # Proceed to add the image and data
        self.add_image(new_filename, first_name, birth_year, birth_month, birth_day, file_type)

    def add_image(self, new_filename, first_name, birth_year, birth_month, birth_day, file_type):
        """Select an image file and add it to the database."""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
        )
        
        if file_path:
            try:
                destination_dir = "images"
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                
                destination_path = os.path.join(destination_dir, new_filename)

                # Check for existing files and prompt for overwrite
                if os.path.exists(destination_path):
                    overwrite = messagebox.askyesno("Overwrite?", f"File '{new_filename}' already exists. Do you want to overwrite it?")
                    if not overwrite:
                        return

                # Save the image to the destination folder
                with open(file_path, 'rb') as file_src:
                    with open(destination_path, 'wb') as file_dest:
                        file_dest.write(file_src.read())

                # Insert the record into the database
                self.cursor.execute(
                "INSERT INTO image ([First Name], [Birth Year], [Birth Month], [Birth Day], [Photoimage Type], [Photo Path]) VALUES (?, ?, ?, ?, ?, ?)",
                first_name, int(birth_year), int(birth_month), int(birth_day), file_type, destination_path
                )

                self.conn.commit()

                messagebox.showinfo("Success", f"Customer '{first_name}' added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add image: {str(e)}")

def open_delete_page():
    # Create a new window for the delete page
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Customer Image")
    DeleteCustomerApp(delete_window)  # Initialize the DeleteCustomerApp in the new window
    # Set focus and grab input to this window
    delete_window.grab_set()
    delete_window.focus_set()

def open_search_page():
    # Create a new window for the search page
    search_window = tk.Toplevel(root)
    search_window.title("Search Customers")
    SearchPage(search_window)  # Initialize the SearchPage in the new window
    # Set focus and grab input to this window
    search_window.grab_set()
    search_window.focus_set()

def open_add_page():
    # Create a new window for the add page
    add_window = tk.Toplevel(root)
    add_window.title("Add Customer Image")
    CustomerImageApp(add_window)  # Initialize the CustomerImageApp in the new window
    # Set focus and grab input to this window
    add_window.grab_set()
    add_window.focus_set()

# Create the main window
root = tk.Tk()
root.title("Customer ID Database System")
root.geometry("500x300")
root.configure(bg="#f7f7f7")  # Softer background color for better aesthetics

# Add a title label with enhanced styling
title_label = tk.Label(root, text="CUSTOMER ID DATABASE SYSTEM", font=("Arial", 18, "bold"), bg="#f7f7f7", fg="#333")
title_label.pack(pady=30)

# Create a frame for buttons to center them
button_frame = tk.Frame(root, bg="#f7f7f7")
button_frame.pack(pady=20)

# Button styles
button_style = {
    "font": ("Arial", 12),
    "width": 20,
    "bg": "#4CAF50",   # Soft green for buttons
    "fg": "white",
    "activebackground": "#45a049",  # Darker green when pressed
    "activeforeground": "white"
}

# Create buttons for different pages with improved styling
search_button = tk.Button(button_frame, text="Search Customers", **button_style, command=open_search_page)
search_button.pack(pady=10)

add_button = tk.Button(button_frame, text="Maintenance (Add)", **button_style, command=open_add_page)
add_button.pack(pady=10)

delete_button = tk.Button(button_frame, text="Maintenance (Delete)", **button_style, command=open_delete_page)
delete_button.pack(pady=10)

# Run the application
root.mainloop()
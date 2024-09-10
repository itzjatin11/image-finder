This project is a image finder Database System built using Python and Tkinter for a graphical user interface (GUI). The application allows users to add, search, and delete customer information, including their photos, which are stored and managed in a Microsoft Access database. The system provides a clean and user-friendly interface for managing customer images and details effectively.

Features
Add Customer:

Enter customer details such as First Name and Birthdate.
Choose the image format (jpg, png, jpeg).
Upload a customer photo that gets saved with a unique name format: firstname-yyyymmdd.filetype.

Search Customer:

Search for customers based on their First Name and Birthdate.
Display matching customer images in a gallery view with clickable thumbnails.
View full-sized versions of the images.

Delete Customer:

Search for a customer by their image filename.
Delete both the customer record and the image file from the system.

Technologies Used

Python for core logic.
Tkinter for the graphical user interface (GUI).
Pillow (PIL) for handling and displaying images.
PyODBC for connecting to the Microsoft Access database.
Microsoft Access as the database for storing customer data and image file paths.
Getting Started

Prerequisites

Python 3.x installed on your system.
Microsoft Access database (.accdb) with a table named image, containing the following fields:
[First Name]: The first name of the customer.
[Birth Year], [Birth Month], [Birth Day]: The customer's birthdate.
[Photo Path]: The path to the image file.

Usage

Add Customer

Open the application.
Enter the customer's First Name and Birthdate.
Choose the image format (jpg, png, jpeg).
Upload the customer's photo using the file dialog.
The system saves the photo in a designated folder (images/) and stores the path in the database.

Search Customer

Enter the First Name and Birthdate (optional fields).
Click Search to display the customer photos matching the criteria.
Click on a thumbnail to view the full-sized image.

Delete Customer

Enter the image filename.
Click Search to load the customer photo.
Click Delete to remove both the photo and the customer record from the system.

Future Enhancements

Implement better error handling for database connection and file operations.
Improve the image gallery with more advanced features (e.g., pagination, zoom).
Add input validation for date fields to prevent invalid date entries.

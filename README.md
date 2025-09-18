# 📖 Vulnerable Library Management System (VulnLib)

Vulnlib is a **deliberately vulnerable web application** designed to simulate a real-world **Library Management System (LMS)**.  
It is intended for **learning and practicing web penetration testing** in a safe and controlled environment.  
The system mimics the features of a typical library application while intentionally containing various security flaws for training purposes.  
Live Demo: https://vulnlib.helium.sh/

⚠️ **Warning!**  
This project is **for educational use only**. Do not deploy or expose Vulnlib to public/production environments.


<img width="1133" height="602" alt="image" src="https://github.com/user-attachments/assets/5da5f6c2-35da-40e3-b9d4-efc0c9348deb" />


## Roles and Features
There are 4 roles : Public, Member, Librarian, and Admin

### Public (No Authentication)
- **Home & Book Search**: Search books by title, category, author, or year.  
- **Book Details**: View detailed book information with external links.  
- **Reviews & Comments**: Submit and read public reviews for books.  
- **User Registration & Login**: Create a new account or log in as a member.

### Member
- **Borrowing History**: View personal loan records.  
- **Loan Requests**: Submit loan applications for books.  
- **Loan Extensions**: Request extensions for active loans.  
- **Fines Management**: View and pay outstanding fines. (Under Development)
- **Profile Update**: Edit personal information.  
- **Wishlist**: Maintain a personal wishlist of books.  

### Librarian
- **Book Management**: Add, edit, delete, or import books into the system.  
- **Loan Management**: Approve or reject loan requests, process returns, and calculate fines.  
- **Notifications**: Receive updates on pending requests.  
- **Slip/Barcode Generation**: Generate printable loan slips or barcodes.  
- **Backup & Restore**: Export and restore data from CSV/JSON files.  

### Admin
- **User Management**: Create, update, delete, and assign user roles.  
- **Role & Permission Configuration**: Manage access rights for different roles.  
- **Audit Logs**: Monitor system activity and user actions.  (Under Development)
- **System Configuration**: Adjust global settings such as fine rules and email templates.  
- **Database Management**: Reset or re-seed the application database.

### Live Demo
**https://vulnlib.helium.sh/** - (Thanks to Cyberacademy.id) 
Demo Account :
| Username   | Email                   | Password          | Role      |
|------------|-------------------------|-------------------|-----------|
| admin      | admin@vulnlib.edu       | PisangGorengYes!  | admin     |
| librarian  | librarian@vulnlib.edu   | PisangGorengYes!! | librarian |
| sarah_lib  | sarah@vulnlib.edu       | PisangGorengYes!! | librarian |
| member     | member@vulnlib.edu      | password123       | member    |
| john_doe   | john.doe@student.edu    | student123        | member    |

## Vulnerability Categories
Vulnlib intentionally includes multiple categories of vulnerabilities for pentesting practice, such as:

- **SQL Injection (SQLi)**  
- **Cross-Site Scripting (XSS)** – reflected and stored  
- **Insecure File Upload**  
- **Server-Side Request Forgery (SSRF)**  
- **Broken Access Control**
- **Insecure Direct Object Reference (IDOR)**    
- **Business Logic Flaws**  
- **Mass Assignment**  
- **Open Redirect**  
- **Sensitive Data Exposure**  
- **Grep Endpoint from app.js**
- etc.


## Installation (Docker Compose)

Ensure **Docker** and **Docker Compose** are installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/harrmahar/vulnlib.git
   cd vulnlib
   docker compose up -d
   ```

2. Access Vunlib at `http://localhost:8000`

## Still Not Working Features
- Fines Features
- File Upload (File Not Found)
- Log (Admin Dashboard)
- ....

## Detailed Walkthrough

Currently, there is no official walkthrough available for **VulnLib**.  
If you would like to contribute by creating a walkthrough or write-up, feel free to reach out to me.  
I would be more than happy to add your work here with proper credit. 🚀  


## App Preview 
<img width="574" height="300" alt="image" src="https://github.com/user-attachments/assets/f701bfb6-368a-4a7b-b638-fc2e2e4b3c7b" />

<img width="574" height="300" alt="image" src="https://github.com/user-attachments/assets/ccb4bda7-5c63-4e38-be9d-9c79d1702200" />


<img width="574" height="300" alt="image" src="https://github.com/user-attachments/assets/2dbc5f9f-ade9-47f8-aa5b-db3e35292b5e" />

## License
This project is licensed under the MIT License - see the LICENSE file for details.


## Contact
If you want to collaborate, contribute, or ask something, you can reach me via:  
- **LinkedIn**: [Harrmahar](https://www.linkedin.com/in/harrmahar)  


<p align='center'><sub>Made for community - Harrmahar , Sept 2025</sub></p>

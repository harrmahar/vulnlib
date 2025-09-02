# 📖 Vulnerable Library Management System (Vulnlib)

Vulnlib is a **deliberately vulnerable web application** designed to simulate a real-world **Library Management System (LMS)**.  
It is intended for **learning and practicing web penetration testing** in a safe and controlled environment.  
The system mimics the features of a typical library application while intentionally containing various security flaws for training purposes.  

> ⚠️ **Disclaimer**:  
> This project is **for educational use only**. Do not deploy or expose Vulnlib to public/production environments.

---

## 🔹 Features by Role Overview

### Public (No Authentication)
- **Home & Book Search**: Search books by title, category, author, or year.  
- **Book Details**: View detailed book information with external links.  
- **Reviews & Comments**: Submit and read public reviews for books.  
- **User Registration & Login**: Create a new account or log in as a member.

### Member
- **Borrowing History**: View personal loan records.  
- **Loan Requests**: Submit loan applications for books.  
- **Loan Extensions**: Request extensions for active loans.  
- **Fines Management**: View and pay outstanding fines.  
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
- **Audit Logs**: Monitor system activity and user actions.  
- **System Configuration**: Adjust global settings such as fine rules and email templates.  
- **Database Management**: Reset or re-seed the application database.  

---

## 🔹 Vulnerability Categories
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

---

## 🔹 Installation (Docker Compose)

Ensure **Docker** and **Docker Compose** are installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/stefan/vulnlib.git
   cd vulnlib
   ```



from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
import os
import json
import requests
import sqlite3
from datetime import datetime, timedelta
import csv
from io import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time

# Import seeder functions for database reset
try:
    from seeder import clear_database, create_users, create_books, create_loans, create_reviews, create_fines, create_wishlists, create_audit_logs, create_system_config
except ImportError:
    # Fallback if seeder import fails
    clear_database = None
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vuln-library-secret-key-2024'  # VULN: Weak secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnlib.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

from models import db, User, Book, Loan, Review, Fine, Wishlist, AuditLog, SystemConfig

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Ensure upload directory exists
os.makedirs('uploads', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# Helper functions
def log_action(action, resource_type=None, resource_id=None, details=None):
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None
    
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    # VULN: Reflected XSS - query is displayed without escaping
    return render_template('search.html', query=query, category=category)

@app.route('/books/<book_id>')
def book_detail(book_id):
    next_url = request.args.get('next')  # Check for next parameter
    if next_url:
        return redirect(next_url)
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book, next_url=next_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # VULN: Username enumeration - different response times and messages
    user = User.query.filter_by(username=username).first()
    
    if not user:
        time.sleep(0.1)  # Shorter delay for non-existent users
        return jsonify({'success': False, 'message': 'Invalid username'}), 401
    
    time.sleep(0.5)  # Longer delay when user exists
    
    if not check_password_hash(user.password_hash, password):
        return jsonify({'success': False, 'message': 'Invalid password'}), 401
    
    login_user(user)
    log_action('login', 'user', user.id)
    return jsonify({'success': True, 'message': 'Logged in successfully', 'redirect': url_for('home')})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Email already exists'}), 400
    
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role='member'
    )
    db.session.add(user)
    db.session.commit()
    
    log_action('register', 'user', user.id)
    return jsonify({'success': True, 'message': 'Account created successfully'})

@app.route('/logout')
@login_required
def logout():
    log_action('logout', 'user', current_user.id)
    logout_user()
    return redirect(url_for('home'))

# API Routes
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    return login()

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    return register()

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def api_logout():
    log_action('logout', 'user', current_user.id)
    logout_user()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# Book API endpoints
@app.route('/api/books')
def api_books():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    author = request.args.get('author', '')
    page = int(request.args.get('page', 1))
    per_page = 12
    
    query = Book.query
    
    if search:
        # VULN: Potential for SQL injection in search
        query = query.filter(
            Book.title.contains(search) |
            Book.author.contains(search) |
            Book.description.contains(search)
        )
    
    if category:
        query = query.filter(Book.category == category)
    
    if author:
        query = query.filter(Book.author.contains(author))
    
    books = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'books': [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'category': book.category,
            'description': book.description,
            'cover_url': book.cover_url,
            'year_published': book.year_published,
            'available_copies': book.available_copies,
            'total_copies': book.total_copies,
            'tags': book.tags
        } for book in books.items],
        'total': books.total,
        'page': page,
        'pages': books.pages
    })

@app.route('/api/books/<book_id>')
def api_book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'category': book.category,
        'description': book.description,
        'cover_url': book.cover_url,
        'year_published': book.year_published,
        'available_copies': book.available_copies,
        'total_copies': book.total_copies,
        'tags': book.tags,
        'created_at': book.created_at.isoformat()
    })

# Review endpoints
@app.route('/api/books/<book_id>/reviews')
def api_book_reviews(book_id):
    reviews = Review.query.filter_by(book_id=book_id).all()
    
    return jsonify({
        'reviews': [{
            'id': review.id,
            'user_id': review.user_id,
            'username': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.isoformat()
        } for review in reviews]
    })

@app.route('/api/books/<book_id>/reviews', methods=['POST'])
def api_create_review(book_id):
    data = request.get_json()
    
    # VULN: No authentication check for creating reviews
    user_id = data.get('user_id')
    rating = data.get('rating')
    comment = data.get('comment')
    
    review = Review(
        user_id=user_id,
        book_id=book_id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Review added successfully', 'review_id': review.id})

# Member features with IDOR vulnerabilities
@app.route('/api/users/<user_id>/loans')
def api_user_loans(user_id):
    # VULN: IDOR - No check if current user matches user_id
    loans = Loan.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'loans': [{
            'id': loan.id,
            'book_id': loan.book_id,
            'book_title': loan.book.title,
            'requested_at': loan.requested_at.isoformat(),
            'approved_at': loan.approved_at.isoformat() if loan.approved_at else None,
            'due_date': loan.due_date.isoformat() if loan.due_date else None,
            'returned_at': loan.returned_at.isoformat() if loan.returned_at else None,
            'status': loan.status,
            'notes': loan.notes
        } for loan in loans]
    })

@app.route('/api/loans', methods=['POST'])
@login_required
def api_create_loan():
    data = request.get_json()
    
    book_id = data.get('book_id')
    from_date = datetime.fromisoformat(data.get('from_date'))
    to_date = datetime.fromisoformat(data.get('to_date'))
    
    loan = Loan(
        user_id=current_user.id,
        book_id=book_id,
        due_date=to_date,
        status='pending'
    )
    
    db.session.add(loan)
    db.session.commit()
    
    log_action('create_loan', 'loan', loan.id)
    return jsonify({'success': True, 'message': 'Loan request submitted', 'loan_id': loan.id})

@app.route('/api/loans/<loan_id>/approve', methods=['PUT'])
def api_approve_loan(loan_id):
    # VULN: Business logic flaw - anyone can approve their own loan
    data = request.get_json()
    
    loan = Loan.query.get_or_404(loan_id)
    
    # VULN: No proper authorization check for approval
    loan.status = 'approved'
    loan.approved_at = datetime.utcnow()
    
    # Update book availability
    book = Book.query.get(loan.book_id)
    if book.available_copies > 0:
        book.available_copies -= 1
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Loan approved successfully'})

@app.route('/api/loans/<loan_id>/extend', methods=['POST'])
@login_required
def api_extend_loan(loan_id):
    # VULN: Business logic bypass - unlimited extensions
    data = request.get_json()
    
    loan = Loan.query.get_or_404(loan_id)
    
    # VULN: No limit on extensions
    extend_days = data.get('days', 7)
    reason = data.get('reason', 'No reason provided')
    
    # Log the extension request for librarian review
    log_action('extend_loan', 'loan', loan_id, f'Extended by {extend_days} days. Reason: {reason}')
    
    loan.due_date = loan.due_date + timedelta(days=extend_days)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Loan extended by {extend_days} days'})

# Fine management with business logic flaws
@app.route('/api/users/<user_id>/fines')
def api_user_fines(user_id):
    # VULN: IDOR - No authorization check
    fines = Fine.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'fines': [{
            'id': fine.id,
            'amount': fine.amount,
            'reason': fine.reason,
            'status': fine.status,
            'created_at': fine.created_at.isoformat(),
            'paid_at': fine.paid_at.isoformat() if fine.paid_at else None
        } for fine in fines]
    })

@app.route('/api/users/<user_id>/fines/pay', methods=['POST'])
def api_pay_fine(user_id):
    # VULN: Business logic flaw - client controls payment amount
    data = request.get_json()
    
    fine_id = data.get('fine_id')
    amount_paid = data.get('amount', 0)  # VULN: Client can set any amount
    
    fine = Fine.query.get_or_404(fine_id)
    
    # VULN: No verification of actual payment, just trust client data
    if amount_paid >= fine.amount:
        fine.status = 'paid'
        fine.paid_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Fine payment processed'})

# Profile update with mass assignment vulnerability
@app.route('/api/users/<user_id>', methods=['PUT'])
@login_required
def api_update_user(user_id):
    # VULN: No check if current user matches user_id
    data = request.get_json()
    
    user = User.query.get_or_404(user_id)
    
    # VULN: Mass assignment - accepts any field from JSON
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)  # VULN: Can set role, password_hash, etc.
    
    db.session.commit()
    
    log_action('update_profile', 'user', user_id)
    return jsonify({'success': True, 'message': 'Profile updated successfully'})

# Wishlist with IDOR
@app.route('/api/users/<user_id>/wishlist')
def api_user_wishlist(user_id):
    # VULN: IDOR - No authorization check
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'wishlist': [{
            'id': item.id,
            'book_id': item.book_id,
            'book_title': item.book.title,
            'book_author': item.book.author,
            'created_at': item.created_at.isoformat()
        } for item in wishlist_items]
    })

@app.route('/api/users/<user_id>/wishlist', methods=['POST'])
@login_required
def api_add_to_wishlist(user_id):
    data = request.get_json()
    
    book_id = data.get('book_id')
    
    # VULN: Can add to any user's wishlist
    wishlist_item = Wishlist(
        user_id=user_id,
        book_id=book_id
    )
    
    db.session.add(wishlist_item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Added to wishlist'})

@app.route('/api/users/<user_id>/wishlist/<item_id>', methods=['DELETE'])
@login_required
def api_remove_from_wishlist(user_id, item_id):
    # VULN: Can remove from any user's wishlist
    item = Wishlist.query.get_or_404(item_id)
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Removed from wishlist'})

# Librarian features with SSRF and file upload vulnerabilities
@app.route('/api/books', methods=['POST'])
def api_create_book():
    # VULN: Weak role check - should require librarian role
    if not current_user.is_authenticated or current_user.role not in ['librarian', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    # VULN: SSRF - application fetches URLs without validation
    cover_url = data.get('cover_url')
    metadata_url = data.get('metadata_url')
    
    # Fetch metadata if URL provided (VULN: SSRF)
    metadata = {}
    if metadata_url:
        try:
            response = requests.get(metadata_url, timeout=5)  # VULN: No URL validation
            if response.headers.get('content-type', '').startswith('application/json'):
                metadata = response.json()
        except:
            pass
    
    book = Book(
        title=data.get('title'),
        author=data.get('author'),
        isbn=data.get('isbn'),
        category=data.get('category'),
        description=data.get('description'),
        cover_url=cover_url,
        metadata_url=metadata_url,
        year_published=data.get('year_published'),
        total_copies=data.get('total_copies', 1),
        available_copies=data.get('available_copies', 1),
        tags=data.get('tags')
    )
    
    db.session.add(book)
    db.session.commit()
    
    log_action('create_book', 'book', book.id)
    return jsonify({'success': True, 'message': 'Book created successfully', 'book_id': book.id})

@app.route('/api/books/import', methods=['POST'])
def api_import_books():
    # VULN: Weak authorization check
    if not current_user.is_authenticated or current_user.role not in ['librarian', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400
    
    file = request.files['file']
    notes = request.form.get('notes', '')  # VULN: Notes stored without sanitization (Stored XSS)
    
    if file.filename.endswith('.csv'):
        # Process CSV
        content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(StringIO(content))
        
        imported_count = 0
        for row in csv_reader:
            book = Book(
                title=row.get('title'),
                author=row.get('author'),
                isbn=row.get('isbn'),
                category=row.get('category'),
                description=row.get('description')
            )
            db.session.add(book)
            imported_count += 1
        
        db.session.commit()
        
        # Store import log with notes (VULN: XSS in notes)
        log_action('import_books', 'book', None, f'Imported {imported_count} books. Notes: {notes}')
        
        return jsonify({'success': True, 'message': f'Imported {imported_count} books'})
    
    return jsonify({'success': False, 'message': 'Invalid file format'}), 400

@app.route('/api/books/<book_id>/upload', methods=['POST'])
def api_upload_book_file(book_id):
    # VULN: Weak authorization check
    if not current_user.is_authenticated or current_user.role not in ['librarian', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    # VULN: No file extension or content type validation
    filename = file.filename  # Could be malicious like script.php
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    file.save(file_path)
    
    log_action('upload_file', 'book', book_id, f'Uploaded: {filename}')
    return jsonify({'success': True, 'message': 'File uploaded successfully', 'filename': filename})

@app.route('/api/users/avatar/upload', methods=['POST'])
def api_upload_avatar():
    # VULN: Unrestricted file upload vulnerability - no file type restrictions
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400
    
    file = request.files['avatar']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    # VULN: No file extension or content type validation - allows any file type
    filename = f"{current_user.id}_{file.filename}"  # Add user ID to filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(file_path)
        
        # Update user avatar path in database
        current_user.avatar = f"/uploads/{filename}"
        db.session.commit()
        
        log_action('upload_avatar', 'user', current_user.id, f'Uploaded avatar: {filename}')
        return jsonify({'success': True, 'message': 'Avatar uploaded successfully', 'filename': filename})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Upload failed: {str(e)}'}), 500

@app.route('/api/loans/pending')
def api_pending_loans():
    # VULN: Weak authorization - should check if user is librarian
    pending_loans = Loan.query.filter_by(status='pending').all()
    
    return jsonify({
        'loans': [{
            'id': loan.id,
            'user_id': loan.user_id,
            'username': loan.user.username,
            'book_id': loan.book_id,
            'book_title': loan.book.title,
            'requested_at': loan.requested_at.isoformat(),
            'due_date': loan.due_date.isoformat() if loan.due_date else None,
            'notes': loan.notes
        } for loan in pending_loans]
    })

@app.route('/api/loans/all')
def api_all_loans():
    # For librarians to get all loans for management
    if not current_user.is_authenticated or current_user.role not in ['librarian', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    all_loans = Loan.query.order_by(Loan.requested_at.desc()).all()
    
    return jsonify({
        'loans': [{
            'id': loan.id,
            'user_id': loan.user_id,
            'username': loan.user.username,
            'book_id': loan.book_id,
            'book_title': loan.book.title,
            'requested_at': loan.requested_at.isoformat(),
            'approved_at': loan.approved_at.isoformat() if loan.approved_at else None,
            'due_date': loan.due_date.isoformat() if loan.due_date else None,
            'returned_at': loan.returned_at.isoformat() if loan.returned_at else None,
            'status': loan.status,
            'notes': loan.notes
        } for loan in all_loans]
    })

@app.route('/api/loans/<loan_id>/return', methods=['PUT'])
def api_return_loan(loan_id):
    # VULN: Weak authorization check
    data = request.get_json()
    
    loan = Loan.query.get_or_404(loan_id)
    
    # VULN: Client can manipulate return date for fine calculation
    return_date_str = data.get('return_date')
    if return_date_str:
        return_date = datetime.fromisoformat(return_date_str)
    else:
        return_date = datetime.utcnow()
    
    loan.returned_at = return_date
    loan.status = 'returned'
    
    # Update book availability
    book = Book.query.get(loan.book_id)
    book.available_copies += 1
    
    # Calculate fine based on client-provided return date (VULN: Business logic flaw)
    if return_date > loan.due_date:
        days_late = (return_date - loan.due_date).days
        fine_amount = days_late * 1.0  # $1 per day
        
        fine = Fine(
            user_id=loan.user_id,
            loan_id=loan.id,
            amount=fine_amount,
            reason=f'Late return: {days_late} days',
            status='unpaid'
        )
        db.session.add(fine)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Loan returned successfully'})

@app.route('/api/loans/<loan_id>/slip')
def api_loan_slip(loan_id):
    # VULN: No authorization check
    loan = Loan.query.get_or_404(loan_id)
    
    # Generate PDF slip
    from io import BytesIO
    buffer = BytesIO()
    
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"VulnLib - Loan Slip")
    p.drawString(100, 730, f"Loan ID: {loan.id}")
    p.drawString(100, 710, f"Book: {loan.book.title}")
    p.drawString(100, 690, f"User: {loan.user.username}")
    p.drawString(100, 670, f"Due Date: {loan.due_date}")
    p.save()
    
    buffer.seek(0)
    
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=loan_{loan_id}.pdf'
    
    return response

# Admin panel with broken access control
@app.route('/api/admin/users')
def api_admin_users():
    # VULN: Broken access control - insufficient role check
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    # VULN: Should check if user is admin, but this check can be bypassed
    users = User.query.all()
    
    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        } for user in users]
    })

@app.route('/api/admin/users', methods=['POST'])
def api_admin_create_user():
    # Proper access control
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        password_hash=generate_password_hash(data.get('password')),
        role=data.get('role', 'member')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User created successfully', 'user_id': user.id})

@app.route('/api/admin/users/<user_id>', methods=['PUT'])
def api_admin_update_user(user_id):
    # Proper access control
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    
    # Update user fields
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'role' in data:
        user.role = data['role']
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User updated successfully'})

@app.route('/api/admin/users/<user_id>', methods=['DELETE'])
def api_admin_delete_user(user_id):
    # Proper access control
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User deleted successfully'})

@app.route('/api/admin/logs')
def api_admin_logs():
    # Proper access control
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    
    return jsonify({
        'logs': [{
            'id': log.id,
            'user_id': log.user_id,
            'action': log.action,
            'resource_type': log.resource_type,
            'resource_id': log.resource_id,
            'details': log.details,  # VULN: Could contain XSS if log injection possible
            'ip_address': log.ip_address,
            'created_at': log.created_at.isoformat()
        } for log in logs]
    })

@app.route('/api/admin/db/clean', methods=['POST'])
def api_admin_clean_db():
    # Proper access control
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        # Clear all tables
        db.session.query(AuditLog).delete()
        db.session.query(Fine).delete()
        db.session.query(Review).delete()
        db.session.query(Wishlist).delete()
        db.session.query(Loan).delete()
        db.session.query(Book).delete()
        db.session.query(User).delete()
        db.session.query(SystemConfig).delete()
        
        db.session.commit()
        
        # Run seeder to repopulate with demo data
        if clear_database:  # Check if seeder functions are available
            print("🗑️  Database cleared, repopulating with demo data...")
            
            # Create demo data using seeder functions
            users = create_users()
            books = create_books()
            loans = create_loans(users, books)
            create_reviews(users, books)
            create_fines(users, loans)
            create_wishlists(users, books)
            create_audit_logs(users)
            create_system_config()
            
            print("✅ Database reset and repopulated successfully!")
            return jsonify({'success': True, 'message': 'Database cleaned and repopulated with demo data successfully'})
        else:
            return jsonify({'success': True, 'message': 'Database cleaned successfully (seeder not available)'})
            
    except Exception as e:
        db.session.rollback()
        print(f"Error during database cleanup: {str(e)}")
        return jsonify({'success': False, 'message': f'Error during database cleanup: {str(e)}'}), 500

@app.route('/api/loans/extensions')
def api_loan_extensions():
    # Allow librarians and admins to view extension logs
    if not current_user.is_authenticated or current_user.role not in ['librarian', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    # Get extension logs from audit table with user information
    extension_logs = AuditLog.query.filter_by(action='extend_loan').order_by(AuditLog.created_at.desc()).limit(50).all()
    
    extensions_with_user_info = []
    for log in extension_logs:
        user = User.query.get(log.user_id) if log.user_id else None
        extensions_with_user_info.append({
            'id': log.id,
            'user_id': log.user_id,
            'username': user.username if user else 'Unknown User',
            'loan_id': log.resource_id,
            'details': log.details,
            'created_at': log.created_at.isoformat(),
            'ip_address': log.ip_address
        })
    
    return jsonify({
        'extensions': extensions_with_user_info
    })

@app.route('/api/admin/scheduler/status')
def api_scheduler_status():
    # Proper access control
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    # Get current scheduler configuration
    cleanup_config = SystemConfig.query.filter_by(key='auto_cleanup_schedule').first()
    
    return jsonify({
        'success': True,
        'scheduler_enabled': cleanup_config.value if cleanup_config else 'disabled',
        'next_cleanup': 'Not scheduled' if not cleanup_config or cleanup_config.value == 'disabled' else f'Next cleanup in {cleanup_config.value} hours'
    })

@app.route('/api/admin/scheduler/configure', methods=['POST'])
def api_configure_scheduler():
    # Proper access control
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    hours = data.get('hours', 0)
    
    if hours < 1 or hours > 168:  # Between 1 hour and 1 week
        return jsonify({'success': False, 'message': 'Hours must be between 1 and 168 (1 week)'}), 400
    
    # Update or create scheduler configuration
    cleanup_config = SystemConfig.query.filter_by(key='auto_cleanup_schedule').first()
    if cleanup_config:
        cleanup_config.value = str(hours)
    else:
        cleanup_config = SystemConfig(
            key='auto_cleanup_schedule',
            value=str(hours),
            description=f'Automatic database cleanup every {hours} hours'
        )
        db.session.add(cleanup_config)
    
    db.session.commit()
    
    log_action('configure_scheduler', 'system', None, f'Set auto cleanup to every {hours} hours')
    return jsonify({'success': True, 'message': f'Scheduler configured for every {hours} hours'})

@app.route('/api/admin/scheduler/disable', methods=['POST'])
def api_disable_scheduler():
    # Proper access control
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    # Update scheduler configuration
    cleanup_config = SystemConfig.query.filter_by(key='auto_cleanup_schedule').first()
    if cleanup_config:
        cleanup_config.value = 'disabled'
        db.session.commit()
    
    log_action('disable_scheduler', 'system', None, 'Disabled auto cleanup scheduler')
    return jsonify({'success': True, 'message': 'Scheduler disabled successfully'})

# Report endpoint with SQL injection vulnerability
@app.route('/api/reports/loans')
def api_loan_reports():
    # VULN: Weak access control
    if not current_user.is_authenticated or current_user.role not in ['librarian', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    year = request.args.get('year', datetime.now().year)
    month = request.args.get('month', '1')
    
    # VULN: SQL Injection in month parameter
    query = f"""
        SELECT l.*, b.title, u.username 
        FROM loan l
        JOIN book b ON l.book_id = b.id
        JOIN user u ON l.user_id = u.id
        WHERE strftime('%Y', l.requested_at) = '{year}'
        AND strftime('%m', l.requested_at) = '{month}'
    """
    
    conn = sqlite3.connect('instance/vulnlib.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)  # VULN: Direct SQL execution with user input
        results = cursor.fetchall()
        
        # Convert to list of dicts (simplified)
        loans = []
        for row in results:
            loans.append({
                'loan_id': row[0],
                'user_id': row[1],
                'book_id': row[2],
                'requested_at': row[3],
                'status': row[6],
                'book_title': row[-2],
                'username': row[-1]
            })
        
        return jsonify({'loans': loans})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

# Member-specific routes
@app.route('/profile')
@login_required
def profile():
    return render_template('member/profile.html', user=current_user)

@app.route('/my-loans')
@login_required
def my_loans():
    return render_template('member/my_loans.html', user=current_user)

@app.route('/my-wishlist')
@login_required
def my_wishlist():
    return render_template('member/my_wishlist.html', user=current_user)

@app.route('/my-fines')
@login_required
def my_fines():
    return render_template('member/my_fines.html', user=current_user)

# Librarian-specific routes
@app.route('/librarian/dashboard')
@login_required
def librarian_dashboard():
    if current_user.role not in ['librarian', 'admin']:
        # VULN: Weak access control - only shows flash message but still renders page
        flash('Access denied', 'error')
    return render_template('librarian/dashboard.html', user=current_user)

@app.route('/librarian/books')
@login_required
def librarian_books():
    if current_user.role not in ['librarian', 'admin']:
        flash('Access denied', 'error')
    return render_template('librarian/books.html', user=current_user)

@app.route('/librarian/loans')
@login_required
def librarian_loans():
    if current_user.role not in ['librarian', 'admin']:
        flash('Access denied', 'error')
    return render_template('librarian/loans.html', user=current_user)

# Admin-specific routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Proper access control
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    return render_template('admin/dashboard.html', user=current_user)

@app.route('/admin/users')
@login_required
def admin_users():
    # This endpoint remains vulnerable (BAC) - only /admin/users should be vulnerable
    return render_template('admin/users.html', user=current_user)

@app.route('/admin/logs')
@login_required
def admin_logs():
    # Proper access control
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    return render_template('admin/logs.html', user=current_user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Configure for Docker environment
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

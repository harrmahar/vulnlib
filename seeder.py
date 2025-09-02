#!/usr/bin/env python3
"""
VulnLib Database Seeder
Seeds the database with demo data for library management system
"""

import os
import sys
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, Book, Loan, Review, Fine, Wishlist, AuditLog, SystemConfig

def clear_database():
    """Clear all data from the database"""
    print("🗑️  Clearing database...")
    
    with app.app_context():
        # Delete in correct order to avoid foreign key constraints
        db.session.query(AuditLog).delete()
        db.session.query(Fine).delete()
        db.session.query(Review).delete()
        db.session.query(Wishlist).delete()
        db.session.query(Loan).delete()
        db.session.query(Book).delete()
        db.session.query(User).delete()
        db.session.query(SystemConfig).delete()
        db.session.commit()
    
    print("✅ Database cleared")

def create_users():
    """Create demo users with different roles"""
    print("👥 Creating demo users...")
    
    users_data = [
        # Admin user
        {
            'username': 'admin',
            'email': 'admin@vulnlib.edu',
            'password': 'PisangGorengYes!',
            'role': 'admin'
        },
        # Librarian users
        {
            'username': 'librarian',
            'email': 'librarian@vulnlib.edu',
            'password': 'PisangGorengYes!!',
            'role': 'librarian'
        },
        {
            'username': 'sarah_lib',
            'email': 'sarah@vulnlib.edu',
            'password': 'PisangGorengYes!!',
            'role': 'librarian'
        },
        # Member users
        {
            'username': 'member',
            'email': 'member@vulnlib.edu',
            'password': 'password123',
            'role': 'member'
        },
        {
            'username': 'john_doe',
            'email': 'john.doe@student.edu',
            'password': 'student123',
            'role': 'member'
        },
        {
            'username': 'alice_smith',
            'email': 'alice.smith@student.edu',
            'password': 'alice2024',
            'role': 'member'
        },
        {
            'username': 'bob_wilson',
            'email': 'bob.wilson@faculty.edu',
            'password': 'faculty456',
            'role': 'member'
        },
        {
            'username': 'eva_brown',
            'email': 'eva.brown@research.edu',
            'password': 'research789',
            'role': 'member'
        },
        # Test user
        {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'test123',
            'role': 'member'
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password']),
            role=user_data['role']
        )
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    print(f"✅ Created {len(users)} demo users")
    return users

def create_books():
    """Create demo books"""
    print("📚 Creating demo books...")
    
    books_data = [
        {
            'title': 'Web Application Security',
            'author': 'Marcus Hartwell',
            'isbn': '978-0123456789',
            'category': 'Technology',
            'description': 'A comprehensive guide to web application security testing and vulnerability assessment.',
            'year_published': 2023,
            'total_copies': 5,
            'available_copies': 3,
            'tags': 'security,web,testing,cybersecurity'
        },
        {
            'title': 'The Art of Penetration Testing',
            'author': 'Sarah Johnson',
            'isbn': '978-0987654321',
            'category': 'Technology',
            'description': 'Learn ethical hacking techniques and penetration testing methodologies.',
            'year_published': 2022,
            'total_copies': 3,
            'available_copies': 2,
            'tags': 'hacking,pentesting,security,ethical'
        },
        {
            'title': 'Database Security Fundamentals',
            'author': 'Robert Chen',
            'isbn': '978-0456789123',
            'category': 'Technology',
            'description': 'Understanding database security, SQL injection, and data protection.',
            'year_published': 2023,
            'total_copies': 4,
            'available_copies': 4,
            'tags': 'database,sql,security,injection'
        },
        {
            'title': 'Modern Cryptography',
            'author': 'Dr. Emily Davis',
            'isbn': '978-0789123456',
            'category': 'Science',
            'description': 'An introduction to cryptographic algorithms and their applications.',
            'year_published': 2021,
            'total_copies': 2,
            'available_copies': 1,
            'tags': 'cryptography,algorithms,security'
        },
        {
            'title': 'Social Engineering Attacks',
            'author': 'Kevin Martinez',
            'isbn': '978-0321654987',
            'category': 'Technology',
            'description': 'Understanding human-based security threats and psychological manipulation.',
            'year_published': 2023,
            'total_copies': 3,
            'available_copies': 0,
            'tags': 'social engineering,psychology,security'
        },
        {
            'title': 'Network Security Protocols',
            'author': 'Lisa Anderson',
            'isbn': '978-0654987321',
            'category': 'Technology',
            'description': 'Deep dive into network security protocols and implementation.',
            'year_published': 2022,
            'total_copies': 6,
            'available_copies': 5,
            'tags': 'network,protocols,security,tcp'
        },
        {
            'title': 'History of Computing',
            'author': 'Michael Thompson',
            'isbn': '978-0147258369',
            'category': 'History',
            'description': 'The evolution of computers from mechanical calculators to modern systems.',
            'year_published': 2020,
            'total_copies': 2,
            'available_copies': 2,
            'tags': 'history,computing,technology'
        },
        {
            'title': 'Digital Forensics Handbook',
            'author': 'Jennifer White',
            'isbn': '978-0258369147',
            'category': 'Technology',
            'description': 'Comprehensive guide to digital forensics and incident response.',
            'year_published': 2023,
            'total_copies': 4,
            'available_copies': 3,
            'tags': 'forensics,investigation,cybercrime'
        },
        {
            'title': 'Advanced Python Programming',
            'author': 'David Rodriguez',
            'isbn': '978-0369147258',
            'category': 'Technology',
            'description': 'Advanced Python techniques for security professionals and developers.',
            'year_published': 2022,
            'total_copies': 8,
            'available_copies': 6,
            'tags': 'python,programming,scripting'
        },
        {
            'title': 'Mathematics for Computer Science',
            'author': 'Prof. Alan Kumar',
            'isbn': '978-0741852963',
            'category': 'Science',
            'description': 'Essential mathematical concepts for computer science students.',
            'year_published': 2021,
            'total_copies': 10,
            'available_copies': 8,
            'tags': 'mathematics,computer science,algorithms'
        },
        {
            'title': 'The Psychology of Security',
            'author': 'Dr. Rachel Green',
            'isbn': '978-0852963741',
            'category': 'Non-Fiction',
            'description': 'Understanding human behavior in cybersecurity contexts.',
            'year_published': 2023,
            'total_copies': 3,
            'available_copies': 2,
            'tags': 'psychology,security,behavior'
        },
        {
            'title': 'Cloud Security Architecture',
            'author': 'Thomas Lee',
            'isbn': '978-0963741852',
            'category': 'Technology',
            'description': 'Designing secure cloud infrastructures and services.',
            'year_published': 2023,
            'total_copies': 5,
            'available_copies': 4,
            'tags': 'cloud,security,architecture,aws'
        },
        # JavaScript security book
        {
            'title': 'JavaScript Security Fundamentals',
            'author': 'Alex Johnson',
            'isbn': '978-0000000000',
            'category': 'Technology',
            'description': 'A comprehensive guide to JavaScript security best practices.',
            'year_published': 2024,
            'total_copies': 1,
            'available_copies': 1,
            'tags': 'javascript,security,development'
        }
    ]
    
    books = []
    for book_data in books_data:
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            isbn=book_data['isbn'],
            category=book_data['category'],
            description=book_data['description'],
            year_published=book_data['year_published'],
            total_copies=book_data['total_copies'],
            available_copies=book_data['available_copies'],
            tags=book_data['tags']
        )
        db.session.add(book)
        books.append(book)
    
    db.session.commit()
    print(f"✅ Created {len(books)} demo books")
    return books

def create_loans(users, books):
    """Create demo loan records"""
    print("📋 Creating demo loans...")
    
    # Get some specific users
    admin = next(u for u in users if u.username == 'admin')
    member = next(u for u in users if u.username == 'member')
    john = next(u for u in users if u.username == 'john_doe')
    alice = next(u for u in users if u.username == 'alice_smith')
    
    # Create various loan scenarios
    loans_data = [
        # Approved loans
        {
            'user': member,
            'book': books[0],
            'status': 'approved',
            'requested_at': datetime.now() - timedelta(days=10),
            'approved_at': datetime.now() - timedelta(days=9),
            'due_date': datetime.now() + timedelta(days=4)
        },
        {
            'user': john,
            'book': books[1],
            'status': 'approved',
            'requested_at': datetime.now() - timedelta(days=15),
            'approved_at': datetime.now() - timedelta(days=14),
            'due_date': datetime.now() + timedelta(days=1)
        },
        # Overdue loan
        {
            'user': alice,
            'book': books[2],
            'status': 'approved',
            'requested_at': datetime.now() - timedelta(days=25),
            'approved_at': datetime.now() - timedelta(days=24),
            'due_date': datetime.now() - timedelta(days=3)  # 3 days overdue
        },
        # Pending loans
        {
            'user': member,
            'book': books[3],
            'status': 'pending',
            'requested_at': datetime.now() - timedelta(days=2),
            'due_date': datetime.now() + timedelta(days=14)
        },
        {
            'user': alice,
            'book': books[5],
            'status': 'pending',
            'requested_at': datetime.now() - timedelta(days=1),
            'due_date': datetime.now() + timedelta(days=21)
        },
        # Returned loans
        {
            'user': john,
            'book': books[6],
            'status': 'returned',
            'requested_at': datetime.now() - timedelta(days=30),
            'approved_at': datetime.now() - timedelta(days=29),
            'due_date': datetime.now() - timedelta(days=7),
            'returned_at': datetime.now() - timedelta(days=5)
        }
    ]
    
    loans = []
    for loan_data in loans_data:
        loan = Loan(
            user_id=loan_data['user'].id,
            book_id=loan_data['book'].id,
            status=loan_data['status'],
            requested_at=loan_data['requested_at'],
            approved_at=loan_data.get('approved_at'),
            due_date=loan_data['due_date'],
            returned_at=loan_data.get('returned_at'),
            notes=f"Demo loan for {loan_data['book'].title}"
        )
        db.session.add(loan)
        loans.append(loan)
    
    db.session.commit()
    print(f"✅ Created {len(loans)} demo loans")
    return loans

def create_reviews(users, books):
    """Create demo reviews"""
    print("💬 Creating demo reviews...")
    
    reviews_data = [
        {
            'user': next(u for u in users if u.username == 'member'),
            'book': books[0],
            'rating': 5,
            'comment': 'Excellent book on web security! Very comprehensive and up-to-date.'
        },
        {
            'user': next(u for u in users if u.username == 'john_doe'),
            'book': books[0],
            'rating': 4,
            'comment': 'Great resource for security professionals. Some chapters could be more detailed.'
        },
        {
            'user': next(u for u in users if u.username == 'alice_smith'),
            'book': books[1],
            'rating': 5,
            'comment': 'Best penetration testing book I have read. Practical examples are very helpful.'
        },
        # Additional review
        {
            'user': next(u for u in users if u.username == 'member'),
            'book': books[1],
            'rating': 3,
            'comment': 'Good book but some sections are outdated.'
        },
        {
            'user': next(u for u in users if u.username == 'bob_wilson'),
            'book': books[2],
            'rating': 4,
            'comment': 'Solid foundation for database security. Could use more real-world examples.'
        },
        # Critical review
        {
            'user': next(u for u in users if u.username == 'eva_brown'),
            'book': books[3],
            'rating': 2,
            'comment': 'Too theoretical for my taste. Needs more practical content.'
        },
        {
            'user': next(u for u in users if u.username == 'john_doe'),
            'book': books[4],
            'rating': 5,
            'comment': 'Eye-opening book about social engineering. Everyone should read this!'
        },
        {
            'user': next(u for u in users if u.username == 'alice_smith'),
            'book': books[8],
            'rating': 4,
            'comment': 'Great Python book for security applications. Code examples are excellent.'
        }
    ]
    
    reviews = []
    for review_data in reviews_data:
        review = Review(
            user_id=review_data['user'].id,
            book_id=review_data['book'].id,
            rating=review_data['rating'],
            comment=review_data['comment']
        )
        db.session.add(review)
        reviews.append(review)
    
    db.session.commit()
    print(f"✅ Created {len(reviews)} demo reviews")
    return reviews

def create_fines(users, loans):
    """Create demo fines for overdue books"""
    print("💰 Creating demo fines...")
    
    # Find overdue loans
    overdue_loans = [loan for loan in loans if loan.due_date and loan.due_date < datetime.now() and loan.status == 'approved']
    
    fines = []
    for loan in overdue_loans:
        days_overdue = (datetime.now() - loan.due_date).days
        fine_amount = days_overdue * 1.0  # $1 per day
        
        fine = Fine(
            user_id=loan.user_id,
            loan_id=loan.id,
            amount=fine_amount,
            reason=f'Late return of "{loan.book.title}" - {days_overdue} days overdue',
            status='unpaid'
        )
        db.session.add(fine)
        fines.append(fine)
    
    # Add some paid fines from history
    paid_fine = Fine(
        user_id=next(u for u in users if u.username == 'john_doe').id,
        amount=5.0,
        reason='Late return - historical fine',
        status='paid',
        created_at=datetime.now() - timedelta(days=20),
        paid_at=datetime.now() - timedelta(days=18)
    )
    db.session.add(paid_fine)
    fines.append(paid_fine)
    
    db.session.commit()
    print(f"✅ Created {len(fines)} demo fines")
    return fines

def create_wishlists(users, books):
    """Create demo wishlist items"""
    print("❤️  Creating demo wishlist items...")
    
    wishlist_data = [
        {
            'user': next(u for u in users if u.username == 'member'),
            'books': [books[3], books[5], books[7]]
        },
        {
            'user': next(u for u in users if u.username == 'john_doe'),
            'books': [books[2], books[4]]
        },
        {
            'user': next(u for u in users if u.username == 'alice_smith'),
            'books': [books[1], books[6], books[8], books[10]]
        }
    ]
    
    wishlists = []
    for data in wishlist_data:
        for book in data['books']:
            wishlist = Wishlist(
                user_id=data['user'].id,
                book_id=book.id
            )
            db.session.add(wishlist)
            wishlists.append(wishlist)
    
    db.session.commit()
    print(f"✅ Created {len(wishlists)} wishlist items")
    return wishlists

def create_audit_logs(users):
    """Create demo audit log entries"""
    print("📝 Creating demo audit logs...")
    
    log_entries = [
        {
            'user': next(u for u in users if u.username == 'admin'),
            'action': 'login',
            'resource_type': 'user',
            'ip_address': '192.168.1.100',
            'created_at': datetime.now() - timedelta(hours=2)
        },
        {
            'user': next(u for u in users if u.username == 'librarian'),
            'action': 'create_book',
            'resource_type': 'book',
            'resource_id': books[0].id if 'books' in locals() else None,
            'details': 'Added new book: Web Application Security',
            'ip_address': '192.168.1.101',
            'created_at': datetime.now() - timedelta(hours=5)
        },
        {
            'user': next(u for u in users if u.username == 'member'),
            'action': 'login',
            'resource_type': 'user',
            'ip_address': '10.0.0.50',
            'created_at': datetime.now() - timedelta(minutes=30)
        },
        # Book import log
        {
            'user': next(u for u in users if u.username == 'admin'),
            'action': 'import_books',
            'resource_type': 'book',
            'details': 'Imported books with notes: Quarterly book collection update',
            'ip_address': '192.168.1.100',
            'created_at': datetime.now() - timedelta(hours=1)
        }
    ]
    
    logs = []
    for log_data in log_entries:
        log = AuditLog(
            user_id=log_data['user'].id,
            action=log_data['action'],
            resource_type=log_data['resource_type'],
            resource_id=log_data.get('resource_id'),
            details=log_data.get('details'),
            ip_address=log_data['ip_address'],
            created_at=log_data['created_at']
        )
        db.session.add(log)
        logs.append(log)
    
    db.session.commit()
    print(f"✅ Created {len(logs)} audit log entries")
    return logs

def create_system_config():
    """Create demo system configuration"""
    print("⚙️  Creating system configuration...")
    
    config_data = [
        {
            'key': 'fine_per_day',
            'value': '1.00',
            'description': 'Fine amount per day for overdue books'
        },
        {
            'key': 'max_loan_days',
            'value': '14',
            'description': 'Maximum loan period in days'
        },
        {
            'key': 'email_template_overdue',
            'value': 'Dear {username}, your book is overdue. Please return it as soon as possible.',
            'description': 'Email template for overdue notifications'
        },
        {
            'key': 'library_name',
            'value': 'VulnLib Education Center',
            'description': 'Library name for system display'
        },
        {
            'key': 'admin_email',
            'value': 'admin@vulnlib.edu',
            'description': 'Administrator email address'
        }
    ]
    
    configs = []
    for config in config_data:
        sys_config = SystemConfig(
            key=config['key'],
            value=config['value'],
            description=config['description']
        )
        db.session.add(sys_config)
        configs.append(sys_config)
    
    db.session.commit()
    print(f"✅ Created {len(configs)} system configuration entries")
    return configs

def main():
    """Main seeder function"""
    print("🌱 Starting VulnLib database seeding...")
    print("📚 Creating demo data for library management system")
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Clear existing data
        clear_database()
        
        # Create all demo data
        users = create_users()
        books = create_books()
        loans = create_loans(users, books)
        reviews = create_reviews(users, books)
        fines = create_fines(users, loans)
        wishlists = create_wishlists(users, books)
        logs = create_audit_logs(users)
        configs = create_system_config()
    
    print("\n🎉 Database seeding completed successfully!")
    print("\n📋 Demo Accounts Created:")
    print("┌─────────────┬──────────────────────────┬─────────────┬──────────────┐")
    print("│ Role        │ Username                 │ Email                    │ Password     │")
    print("├─────────────┼──────────────────────────┼─────────────────────────┼──────────────┤")
    print("│ Admin       │ admin                    │ admin@vulnlib.edu        │ password123  │")
    print("│ Librarian   │ librarian                │ librarian@vulnlib.edu    │ password123  │")
    print("│ Librarian   │ sarah_lib                │ sarah@vulnlib.edu        │ library2024  │")
    print("│ Member      │ member                   │ member@vulnlib.edu       │ password123  │")
    print("│ Member      │ john_doe                 │ john.doe@student.edu     │ student123   │")
    print("│ Member      │ alice_smith              │ alice.smith@student.edu  │ alice2024    │")
    print("│ Member      │ bob_wilson               │ bob.wilson@faculty.edu   │ faculty456   │")
    print("│ Member      │ eva_brown                │ eva.brown@research.edu   │ research789  │")
    print("└─────────────┴──────────────────────────┴─────────────────────────┴──────────────┘")
    
    print("\n📋 Database populated with:")
    print("• Demo user accounts for testing")
    print("• Sample book catalog")
    print("• Example loan requests and history")
    print("• User reviews and ratings")
    print("• System configuration entries")
    
    print("\n✅ Setup complete! Ready for development and testing.")

if __name__ == '__main__':
    main()

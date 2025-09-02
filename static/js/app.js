// VulnLib JavaScript Application

// Global configuration
const API_BASE = '/api';
const ITEMS_PER_PAGE = 12;

// Utility functions
const utils = {
    // Format date
    formatDate: (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // Format datetime
    formatDateTime: (dateString) => {
        return new Date(dateString).toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Sanitize HTML (basic - intentionally weak for educational purposes)
    sanitizeHtml: (str) => {
        // VULN: Weak sanitization - can be bypassed
        return str.replace(/<script>/gi, '').replace(/<\/script>/gi, '');
    },

    // Debounce function
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Generate UUID (basic implementation)
    generateUUID: () => {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0,
                v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },

    // Get current user from session (if available)
    getCurrentUser: () => {
        // This would normally be handled server-side, but for demo purposes
        return window.currentUser || null;
    },

    // Check if user has role
    hasRole: (role) => {
        const user = utils.getCurrentUser();
        return user && user.role === role;
    }
};

// API wrapper
const api = {
    // Generic request handler
    request: async (endpoint, options = {}) => {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(`${API_BASE}${endpoint}`, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || `HTTP ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    },

    // Auth endpoints
    auth: {
        login: (credentials) => api.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        }),
        
        register: (userData) => api.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        }),
        
        logout: () => api.request('/auth/logout', { method: 'POST' })
    },

    // Book endpoints
    books: {
        list: (params = {}) => {
            const queryString = new URLSearchParams(params).toString();
            return api.request(`/books${queryString ? '?' + queryString : ''}`);
        },
        
        get: (id) => api.request(`/books/${id}`),
        
        create: (bookData) => api.request('/books', {
            method: 'POST',
            body: JSON.stringify(bookData)
        }),
        
        update: (id, bookData) => api.request(`/books/${id}`, {
            method: 'PUT',
            body: JSON.stringify(bookData)
        }),
        
        delete: (id) => api.request(`/books/${id}`, { method: 'DELETE' }),
        
        // Reviews
        getReviews: (bookId) => api.request(`/books/${bookId}/reviews`),
        
        addReview: (bookId, reviewData) => api.request(`/books/${bookId}/reviews`, {
            method: 'POST',
            body: JSON.stringify(reviewData)
        })
    },

    // User endpoints
    users: {
        get: (id) => api.request(`/users/${id}`),
        
        update: (id, userData) => api.request(`/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        }),
        
        // Loans
        getLoans: (userId) => api.request(`/users/${userId}/loans`),
        
        // Fines
        getFines: (userId) => api.request(`/users/${userId}/fines`),
        
        payFine: (userId, fineData) => api.request(`/users/${userId}/fines/pay`, {
            method: 'POST',
            body: JSON.stringify(fineData)
        }),
        
        // Wishlist
        getWishlist: (userId) => api.request(`/users/${userId}/wishlist`),
        
        addToWishlist: (userId, bookId) => api.request(`/users/${userId}/wishlist`, {
            method: 'POST',
            body: JSON.stringify({ book_id: bookId })
        }),
        
        removeFromWishlist: (userId, itemId) => api.request(`/users/${userId}/wishlist/${itemId}`, {
            method: 'DELETE'
        })
    },

    // Loan endpoints
    loans: {
        create: (loanData) => api.request('/loans', {
            method: 'POST',
            body: JSON.stringify(loanData)
        }),
        
        approve: (loanId) => api.request(`/loans/${loanId}/approve`, {
            method: 'PUT',
            body: JSON.stringify({})
        }),
        
        extend: (loanId, days) => api.request(`/loans/${loanId}/extend`, {
            method: 'POST',
            body: JSON.stringify({ days })
        }),
        
        return: (loanId, returnDate) => api.request(`/loans/${loanId}/return`, {
            method: 'PUT',
            body: JSON.stringify({ return_date: returnDate })
        }),
        
        getPending: () => api.request('/loans/pending'),
        
        getSlip: (loanId) => fetch(`${API_BASE}/loans/${loanId}/slip`)
    },

    // Admin endpoints
    admin: {
        getUsers: () => api.request('/admin/users'),
        
        createUser: (userData) => api.request('/admin/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        }),
        
        updateUser: (userId, userData) => api.request(`/admin/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        }),
        
        deleteUser: (userId) => api.request(`/admin/users/${userId}`, {
            method: 'DELETE'
        }),
        
        getLogs: () => api.request('/admin/logs'),
        
        cleanDatabase: () => api.request('/admin/db/clean', { method: 'POST' })
    }
};

// Toast notifications
const notifications = {
    show: (message, type = 'success', duration = 5000) => {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) return;

        const toastId = `toast-${Date.now()}`;
        const iconClass = {
            success: 'bi-check-circle-fill text-success',
            error: 'bi-exclamation-triangle-fill text-danger',
            warning: 'bi-exclamation-triangle text-warning',
            info: 'bi-info-circle-fill text-info'
        };

        const toastHTML = `
            <div class="toast" role="alert" id="${toastId}" data-bs-autohide="true" data-bs-delay="${duration}">
                <div class="toast-header">
                    <i class="${iconClass[type]} me-2"></i>
                    <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">${message}</div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        
        toast.show();

        // Remove element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    },

    success: (message) => notifications.show(message, 'success'),
    error: (message) => notifications.show(message, 'error'),
    warning: (message) => notifications.show(message, 'warning'),
    info: (message) => notifications.show(message, 'info')
};

// Loading indicator
const loading = {
    show: (element, text = 'Loading...') => {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (!element) return;

        element.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">${text}</span>
                </div>
                <div class="mt-2">${text}</div>
            </div>
        `;
    },

    hide: (element) => {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (!element) return;

        element.innerHTML = '';
    }
};

// Form helpers
const forms = {
    // Serialize form data to object
    serialize: (form) => {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        return data;
    },

    // Reset form and remove validation classes
    reset: (form) => {
        form.reset();
        form.querySelectorAll('.is-valid, .is-invalid').forEach(el => {
            el.classList.remove('is-valid', 'is-invalid');
        });
    },

    // Validate required fields
    validate: (form) => {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
                field.classList.add('is-valid');
            }
        });

        return isValid;
    }
};

// Modal helpers
const modals = {
    show: (modalId) => {
        const modal = document.getElementById(modalId);
        if (modal) {
            const bsModal = bootstrap.Modal.getOrCreateInstance(modal);
            bsModal.show();
        }
    },

    hide: (modalId) => {
        const modal = document.getElementById(modalId);
        if (modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        }
    },

    confirm: (message, callback) => {
        // Simple confirm dialog - in production, use a custom modal
        if (confirm(message)) {
            callback();
        }
    }
};

// Search functionality
const search = {
    // Highlight search terms in text
    highlight: (text, terms) => {
        if (!terms || !text) return text;
        
        const regex = new RegExp(`(${terms.split(' ').join('|')})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    },

    // Debounced search
    debounced: utils.debounce((query, callback) => {
        callback(query);
    }, 300)
};

// Book management
const bookManager = {
    // Create book card element
    createCard: (book) => {
        const card = document.createElement('div');
        card.className = 'col-md-4 col-lg-3 mb-4';
        
        const availabilityClass = book.available_copies > 0 ? 'text-success' : 'text-danger';
        const availabilityText = book.available_copies > 0 ? 'Available' : 'Not Available';

        card.innerHTML = `
            <div class="card h-100 book-card">
                <div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
                    ${book.cover_url ? 
                        `<img src="${book.cover_url}" class="img-fluid" style="max-height: 180px;" alt="${book.title}">` :
                        `<i class="bi bi-book display-4 text-muted"></i>`
                    }
                </div>
                <div class="card-body d-flex flex-column">
                    <h6 class="card-title">${book.title}</h6>
                    <p class="card-text text-muted flex-grow-1">${book.author}</p>
                    <div class="mt-auto">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <small class="text-muted">${book.category || 'Uncategorized'}</small>
                            <span class="${availabilityClass}">${availabilityText}</span>
                        </div>
                        <div class="d-flex justify-content-between">
                            <a href="/books/${book.id}" class="btn btn-primary btn-sm">
                                <i class="bi bi-eye"></i> View
                            </a>
                            <span class="badge bg-secondary">${book.available_copies}/${book.total_copies}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        return card;
    },

    // Render books in container
    render: (books, containerId) => {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';
        
        if (books.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-book display-4 text-muted"></i>
                    <h4 class="mt-3 text-muted">No books found</h4>
                    <p class="text-muted">Try adjusting your search criteria</p>
                </div>
            `;
            return;
        }

        books.forEach(book => {
            container.appendChild(bookManager.createCard(book));
        });
    }
};

// Pagination
const pagination = {
    render: (currentPage, totalPages, onPageClick, containerId) => {
        const container = document.getElementById(containerId);
        if (!container || totalPages <= 1) {
            container.innerHTML = '';
            return;
        }

        let html = '<ul class="pagination justify-content-center">';

        // Previous button
        html += `
            <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a>
            </li>
        `;

        // Page numbers
        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, currentPage + 2);

        if (startPage > 1) {
            html += '<li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>';
            if (startPage > 2) {
                html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            html += `
                <li class="page-item ${i === currentPage ? 'active' : ''}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                </li>
            `;
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
            }
            html += `<li class="page-item"><a class="page-link" href="#" data-page="${totalPages}">${totalPages}</a></li>`;
        }

        // Next button
        html += `
            <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${currentPage + 1}">Next</a>
            </li>
        `;

        html += '</ul>';
        container.innerHTML = html;

        // Add click handlers
        container.querySelectorAll('[data-page]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = parseInt(link.dataset.page);
                if (page >= 1 && page <= totalPages && page !== currentPage) {
                    onPageClick(page);
                }
            });
        });
    }
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Global error handler for fetch requests
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        notifications.error('An unexpected error occurred. Please try again.');
    });
});

// Export to global scope
window.VulnLib = {
    utils,
    api,
    notifications,
    loading,
    forms,
    modals,
    search,
    bookManager,
    pagination
};
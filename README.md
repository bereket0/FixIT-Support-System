# FixIT - Internal IT Support System

A comprehensive Django-based internal IT support system designed for organizations to manage IT support tickets, share tech tips, and conduct monthly quizzes.

## Features

### 🎫 **IT Support Tickets**
- Create, view, edit, and delete support tickets
- Role-based access control (IT Admin vs Employee)
- Ticket status tracking (Pending, In Progress, Solved)
- File attachments support
- Change tracking and employee update notes
- Advanced filtering and search capabilities

### 💡 **Weekly Tech Tips**
- Share and manage weekly technology tips
- Categorized tips for better organization
- Public access for all employees

### 🧠 **Monthly Quizzes**
- Create and manage monthly technology quizzes
- Multiple choice questions with explanations
- Track quiz participation and results

### 👥 **User Management**
- Role-based user system (IT Admin & Employee)
- Admin dashboard for user management
- Employee account creation by admins
- Secure authentication system

### 🎨 **Modern UI/UX**
- Responsive Bootstrap 5 design
- Beautiful, user-friendly interface
- Mobile-friendly design
- Intuitive navigation

## Technology Stack

- **Backend**: Django 5.2
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Authentication**: Django's built-in authentication system
- **File Storage**: Local file system

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fixit.git
cd fixit
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Create User Groups and Admin User
```bash
python manage.py create_admin_user
```

### 8. Run Development Server
```bash
python manage.py runserver
```

### 9. Access the Application
- **Employee Dashboard**: http://127.0.0.1:8000/
- **Admin Dashboard**: http://127.0.0.1:8000/admin-dashboard/
- **Django Admin**: http://127.0.0.1:8000/admin/

## Default Users

### Admin User
- **Username**: FixIT
- **Password**: Zion1@mercy
- **Role**: IT Admin

### Employee User
- **Username**: employee
- **Password**: employee123
- **Role**: Employee

## Project Structure

```
fixit/
├── fixit/                 # Main Django project
│   ├── settings.py       # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── tickets/             # Ticket management app
├── tips/               # Tech tips app
├── quiz/               # Quiz management app
├── users/              # User management app
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploaded files
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Usage

### For Employees
1. Access the employee dashboard (public, no login required)
2. Create new support tickets
3. View and edit your own tickets
4. Access weekly tech tips and monthly quizzes
5. Update ticket information (except status)

### For IT Admins
1. Login with admin credentials
2. Access the admin dashboard
3. Manage all tickets across the organization
4. Create and manage tech tips and quizzes
5. Create employee accounts
6. Assign tickets to team members
7. Update ticket status and priority

## Key Features

### Role-Based Access Control
- **IT Admins**: Full access to all features
- **Employees**: Limited access to their own tickets and public content

### Ticket Management
- Create tickets with categories and priority levels
- Attach files to tickets
- Track ticket status and updates
- Employee update notes for better communication

### Security Features
- Secure authentication system
- Role-based permissions
- Input validation and sanitization
- CSRF protection

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions, please contact the development team or create an issue in the GitHub repository.

## Acknowledgments

- Django Framework
- Bootstrap 5
- Font Awesome Icons
- All contributors and testers

---

**FixIT** - Making IT support simple and efficient! 🚀 
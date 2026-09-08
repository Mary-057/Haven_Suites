Haven_Suites

A secure, lightweight hotel management and guest registration web application built with Django. Designed for front-desk operations with strict role-based access controls and a clean enterprise-slate interface.

Key Features
- Role-Based Access Control (RBAC): Front-desk staff can view and manage active bookings, but creating new staff accounts is restricted exclusively to managers/superusers using custom decorators (@user_passes_test).

- Guest Management (CRUD): Complete create, read, update, and delete workflows for tracking guest logs, including strict operational fields like mandatory phone numbers, room assignments, stay durations, and check-in dates.

- Modern Enterprise UI: Styled with Tailwind CSS, featuring custom form rendering that strips out clunky default Django helper text for a clean, professional look.

- Automated Unit Testing: Includes robust test coverage (tests.py) verifying model string representations, view security barriers, and authentication redirection rules.

Tech Stack
Backend: Python, Django

Database: SQLite (Local development)

Frontend: HTML5, Tailwind CSS

Testing: Django TestCase Framework

ollow these steps to set up and run the project on your local machine:

1. Clone the repository using 'git clone https://github.com/Mary-057/Haven_Suites.git' and 'cd Haven_Suites'
   
2. Set up a virtual environment using:
'python -m venv venv'
# On Windows:
'venv\Scripts\activate'
# On macOS/Linux:
'source venv/bin/activate'

3. Install dependencies using 'pip install -r requirements.txt'

4. Run database migrations:
'python manage.py makemigrations'
'python manage.py migrate'

5. Create a superuser (Manager account)
To access restricted routes like adding new staff, you must create an admin superuser:
'python manage.py createsuperuser'
(Follow the prompts to enter your username, email, and password).

7. Run the development server using 'python manage.py runserver'
Open your browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Running Tests
To verify that all models, views, and security checks are passing correctly, run the built-in test suite:
'python manage.py test'

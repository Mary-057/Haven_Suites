Haven_Suites Guest Registration System (CRUD Application)

This is a professional-grade web application built using the Django framework. Its primary purpose is to provide hotel staff with a secure, simple dashboard to manage guest check-ins, registration details, and booking information.

This project demonstrates core skills including database management, form validation, and securing user data.

Features Implemented (CRUD)

This application fully implements the Create, Read, Update, and Delete lifecycle using Django's Model-View-Template (MVT) architecture.

- Secure Authentication: Staff must log in to access any registration or viewing functionality.
- Create (C): Staff can register new guests via a dedicated web form (/register/).
- Read (R): The Staff Dashboard (/dashboard/) displays all guest entries in a single, sortable table.
- Update (U): Staff can edit existing guest details (e.g., changing room numbers or check-out dates) via a unique link per guest.
- Delete (D):Staff can securely delete outdated guest records.
- Database Management: Uses Django’s built-in ORM (Object-Relational Mapper) for stable data handling.

Technologies Used

- Backend Framework:Django (Python)
- Database:SQLite (Default for development)
- Frontend: HTML/CSS (Inline styling for structure)
- Version Control: Git

How to Run the Project Locally

Follow these steps to set up and run the application:

- Setup Environment (Create a Sandbox)

i. Create Security Key (.env File)
This project requires a private security key (SECRET_KEY) which is managed externally for security.


ii. Create the Vault: Create a new file named `.env` in the project's root directory (next to `manage.py`).


iii. Navigate to the project root directory and set up a virtual environment (Venv):

```bash
python -m venv venv

.\venv\Scripts\Activate.ps1


iv. Generate a Key: Open your terminal (with the venv active) and run the following commands to generate a unique, secure key:

    ```bash
    python manage.py shell
    >>> from django.core.management.utils import get_random_secret_key
    >>> print(get_random_secret_key())
    >>> exit()
    ```
    (Copy the long string of text that is printed.)

v. Paste the Key: Open the new `.env` file and paste the key you generated inside it, following this exact format:
    ```text
    SECRET_KEY=PASTE_YOUR_GENERATED_KEY_HERE
    ```

(Note: This process must be completed before running the server for the first time.)



# Django Job Portal

A full-featured Job Portal web application built using Python, Django, and SQLite. This platform connects job seekers with employers, enabling users to search and apply for jobs while allowing recruiters to post vacancies and manage applications.

---

## Key Features

* **User Authentication & Roles:** Custom user profiles for Job Seekers and Employers.
* **Job Listings & Search:** Browse, filter, and search job openings by keyword, location, or category.
* **Employer Dashboard:** Post, edit, and manage job openings; view incoming applications.
* **Applicant Portal:** Apply for jobs, upload resumes, and track application status.
* **Admin Interface:** Full Django admin management for users, listings, and platform data.

---

## Tech Stack

* **Backend:** Python, Django
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap

---

## Project Structure

```text
├── job_portal/         # Main project configuration
├── jobs/               # App for handling job posts, applications, and search
├── users/              # App for authentication and user profiles
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, Images)
├── media/              # User-uploaded files (Resumes, Profile pictures)
├── db.sqlite3          # SQLite Database
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies

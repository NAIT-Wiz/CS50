## Aninymous Tip Off (ATO) Reporting System


## CS50
>This was my final project to conclude the CS50 Introduction to Computer Sciense course.

>CS, python, flask, flask web framework, web development, CS50, sqlite3, flask-session, Jinja2

## Features

I've used Flask web framework based in Python

## Explaining the project and the database
My final project is a Flask-based web application that allow the users to  submit crime incidents tips offs This is a for reporting and managing various types of incidents. The system  two applications,

## public.py
One for general users/public where they can log tips or criminal activity reports, track the reports or see latest news regarding crime, all this is done anonymously. Contains predefined categories

## admin.py
Allows users to log in, view  and process the reports, view or update the status of reports. Only users with role admin can create and manage the users. Contains predefined categories

All information about reports, users, news, notes and stored in messages.db.

I used cs50 sqlite3 to connect the database to the application and to manager it.

## How to start
Project is ready to run (with some requirements). You need to clone and run:


$ mkdir aproject
$ cd aproject
$cd aproject export FLASK_APP=public_app/app_public.py ### for the Public app
### OR
cd aproject export FLASK_APP=admin_app/app_admin.py ### for the Admin app

```

Open http://127.0.0.1:5000/, customize project files and **have fun**.

#### Sqlachemy and sqlite3:
I needed seven tables for my database:

- users: Stores user information and roles.
- reports: Stores incident reports.
- notes: Stores updates associated with reports.
- news: Stores news articles and notices.
- audit_trail: stores logs of user activities.
- roles: Stores user roles.
- support: Stores Support queries


## Demonstration on youtube
[My Final Project presentation](https://youtu.be/ZNVXVmspA3k?si=cwIciITmxyPEKnMu)


### Layout, JavaScript and CSS
The layout was adapted from the course’s final problem set (Finance)

The idea behind the design was to created an interactive, where the user could perform almost any operation within the same route. This was achieved with the use of JavaScript methods and Bootstrap components

The CSS file was not heavily utilized, mainly because Bootstrap provided appealing default styles. Nevertheless, some HTML elements required specific positioning adjustments.

### Directory Structure
/aproject
  /public_app
    app_public.py
    /templates
      ...other public app templates here...
  /admin_app
    app_admin.py
    /templates
      ...admin app templates here..
  /static
   style.css
 messages.db
 helpers.py

## Routes

## Front End - public.py
- /: Renders the landing page. with reports displayed by latest.
- /incident_report: Displays the incident report form and handles form submissions. The incident report form includes a hidden honeypot field to detect bot submissions. If the field is filled out, the submission is rejected.
- /track_report: Allows users to track the status of their incident reports.
- /faq: Displays the FAQ page.
- /headlines: Shows the latest headlines.
- /article/<int:article_id>: Displays detailed content of a selected article.
- /contact: Displays the contact page.
- /apology: Displays apology for errors.
- /Layout: the basic fixed layout structure

## Backe-End - admin.py
- /login: Renders the login page. Log the user in.
- /logout: Log the user out.
- /create_user: Render the create user page only accessible to admin.
- /manage_users: Display and manage users only accessible to admin.
- /suspend_account/<int:user_id>: Suspend a user account only accessible to admin.
- /change_role/<int:user_id>: Change a user's role only accessible to admin.
- /dashboard: Render the admin dashboard page.
- /faq: Render the FAQ page.
- /audit_trail: Display the audit trail.
- /search: Render the search page Under construction


## Manage Reports Received
- /: Render the index page with reports displayed by latest.
- /view_report/<int:report_id>: View a specific report.
- /view_report/<int:report_id>: Update the status of a report.
- /report/<int:report_id>/process: Render the process report page.
- /report/<int:report_id>/process: Process a report.
- /report/<int:report_id>/add_notes: Render the add notes page.
/report/<int:report_id>/add_notes: Add notes to a report.
- /status/<int:report_id>: Render the status update page.
 Update the status of a report.
- /report_details: Display report details with pagination.

### News and Notices
- /post_news: Render the post news page. Post news and notices.
- GET /headlines: Display the latest headlines.
- GET /article/<int:article_id>: Show a specific article.
- GET /edit_article/<int:article_id>: Render the edit article page.
- POST /edit_article/<int:article_id>: Edit an article.

### Support and Messages
- /support: Render the support page.
- /support: Submit a support message.
- /messages: Display support messages with pagination.

## Ideas for improvement
For a starting project can't be perfect. with noone to ask  i had to model it around the finance pset. Future work could include:
- Search to be completed
- Task assignments to various users.
- Print labels for selected specimen.
- more styling.
- create departments
- adjust the reference number genaration as th current one is not ideal


## About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you for all CS50.

- Where I get CS50 course?
https://cs50.harvard.edu/x/2024/project/


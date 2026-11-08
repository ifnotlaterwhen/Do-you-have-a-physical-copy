# CFG Group Project

For our CFG group project, we were tasked with developing a Flask-based application connected to a MySQL database to address a real-world problem. We reviewed a few options from our team before moving forward with Cinefiles.

**Cinefiles** is a home entertainment management application that helps the user track films, manage their streaming subscriptions, and keep a record of owned physical media (DVD, Blu-ray, 4k Blu-ray). It was developed to address the growing difficulty of navigating streaming platforms and keep track of your physical collection.

### 1: Installation instructions

1. Run `python -m venv .venv` at the root of the repository to create a virtual environment.
2. Run `source .venv/bin/activate` to start the virtual environment.
2. Run `pip install -r requirements.txt` to install the packages needed for this project.

### 2. Setup instructions

1. Create a `.env` file and paste the following lines:

<p>DB_HOST=localhost <br>
DB_PORT=3306<br>
DB_USER=$YOUR_USER_NAME<br>
DB_PW=$YOUR_MYSQL_SERVER_PASSWORD<br>
API_KEY=$YOUR_TMDB_API_KEY<br></p>

2. Replace the values of DB_USER, DB_PW, and API_KEY with your own credentials. You can get a personal TMDB API key here: <https://www.themoviedb.org/settings/api>

### 3. Running the app

Once installation and setting up is completed, follow the instruction below every time you wish to start the application.  
***Important note to project marker***:   
If you wish to start the app with a database seeded with sample data, **follow section 4 before coming back to section 3**
1. Run `python app.py` at the root of the repository to start the server.
2. Run `python main.py` to start the application.

### 4. Optional: Seeding the DB with sample data

We have mock data to save you the trouble of adding film manually, so you can start experiencing the app straight away.  
1. Follow section 1 and section 2
1. Run `python DButils.py` at the root of the repo.
2. Continue with section 3
<br>
<br>
       


### 5. Meet the team!↓

## Reid intro


* Acted as project lead, coordinating efforts across the team and leading regular meetings
* Worked with the team on the initial database schema
* Developed the Add physical copy feature


## Reese intro


* Led project architecture, database setup and module organisation.
* Established testing infrastructure, GitHub Actions and MySQL integration.
* Reviewed code, supported debugging and coordinated integration across branches.
* Developed the See tracked films feature.


## Olivia intro
* Fixed query bugs (missing joins, duplicates, SQL injection risk) and identified duplicate classes and methods
* Set up the initial config.py database connection


## Tansy Intro

* Worked alongside on initial functions setup in DButils.py
* Contributed to refactoring repeated queries and organising database functions with teammates streamline.


## Carina Intro

* Developed the Find where to watch feature, which returns physical copies  the user owns and where to stream Movies.
* Developed a Film recommendations feature based on viewing preferences.


## Stéphanie Intro

* Developed the Track a new film feature
* Worked on the initial database schema with the team
* Contributed in creating and tracking activity project log


## Roxann Intro 

* Developed the Subscription feature, allowing users to view, add and remove streaming subscriptions.
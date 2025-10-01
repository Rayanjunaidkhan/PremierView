# PremierView
=======




# PremierView – A Premier League Web Application
#### Description
Introduction

PremierView is a Flask-based web application that provides fans of the Premier League with an accessible way to follow fixtures, statistics, standings, and personalized team information. The project integrates with the free Football-Data.org API
 to fetch real-time data about matches, players, and standings.

At its core, the application allows users to:

View all upcoming fixtures in the Premier League for the next month.

Create an account and log in to track their favorite teams.

Access a dedicated statistics page to look up performance details of Premier League players.

View the live Premier League table standings.

Enjoy a dynamic navigation bar that updates based on login status.

The goal of this project is to create a simple but robust website where the essential aspects of following the Premier League are centralized. The site emphasizes usability, a clear structure, and personalization through user accounts and favorite teams.

File Descriptions
1. app.py

This is the central file of the project. It contains all the Flask route definitions, session handling logic, database interactions, and integration with the Football-Data.org API. Key functionalities include:

Homepage route (/): Displays all matches in the next month and, if the user is logged in, also shows matches for their favorite teams.

Login and registration routes: Allow users to securely log in, register, and log out. Login status is tracked via Flask sessions.

Player statistics route: Handles form input where users can enter a player’s name to retrieve and display data such as goals, assists, and matches played.

Favorite teams management: Lets logged-in users add or remove teams and ensures their upcoming fixtures appear on the homepage.

Table route: Displays the live Premier League standings by pulling structured data from the API.

In addition to routes, app.py also manages session state, ensuring that only logged-in users can access certain features.

2. helpers.py

contains the single funstion @login_required took direct inspiration from the @login_required function inside cs50 finance

3. templates/

This folder contains all HTML files used to render views for the site. The project uses Jinja2 templating, which allows dynamic content insertion from Flask.

layout.html: The base template shared across all pages. It includes the navbar, common styles, and logic to show different links depending on whether the user is logged in. Other templates extend from this layout.

index.html: Displays all upcoming Premier League matches for the next 30 days. If the user is logged in, it also includes a dedicated “Favorite Matches” section.

login.html: Provides a login form where users can enter their credentials. If they don’t have an account, they can navigate to the register page.

register.html: Allows new users to create an account. Once registered, users can log in and start adding favorite teams.

favoriteteams.html: A page where logged-in users can manage their favorite teams, adding or removing clubs as desired.

player_statistics.html: Displays details for a player searched by the user, including name, team, goals, assists, and matches played.

table.html: Shows the live Premier League standings, including club positions, matches played, wins, draws, losses, and points.

4. static/

Contains static assets such as CSS files.

styles.css: Custom styles that define the site’s overall look, including formatting for match cards, navigation, and other UI elements.

5. users.db

A SQLite3 database that stores user credentials and favorite team data. Using SQLite makes the project lightweight and easy to set up without requiring a separate database server.

Tables include:

users: Stores usernames and securely hashed passwords.

favorite_teams: Stores relationships between users and the teams they follow.

6. requirements.txt

Lists all dependencies required to run the project. This ensures reproducibility: another developer can quickly set up the same environment with pip install -r requirements.txt.

7. README.md

This document — providing a thorough explanation of the project, its purpose, and its structure.

Design Choices

A few important decisions shaped this project:

API Choice
The project relies on Football-Data.org because it was the only free API that provided the full range of features needed: fixtures, standings, player stats, venues, and referees. Alternatives were considered, but they were either incomplete or required paid subscriptions.

Session-based Authentication
Flask sessions were chosen to manage user authentication because they integrate smoothly with Flask, are lightweight, and keep track of login state effectively without requiring a full authentication service.

Database
SQLite was chosen over other databases like MySQL or PostgreSQL because it is file-based, portable, and simple to configure. This matches the project’s scale and makes it beginner-friendly to run.

Template Inheritance
By using a layout.html with Jinja2 inheritance, the project avoids code duplication across HTML files. The navbar and base layout only need to be defined once, making future modifications easier.

Conclusion

PremierView provides a clean, user-friendly interface for following the Premier League. The application’s architecture balances simplicity with functionality: Flask as the web framework, SQLite for persistence, and Football-Data.org for live data. By organizing the code into separate files for routes, helpers, templates, and static assets, the project remains maintainable and easy to extend.

Whether you want to quickly check the next set of fixtures, track your favorite team’s matches, analyze player stats, or see how the league table is shaping up, PremierView brings all of this together into one cohesive platform.
>>>>>>> 42b1586 (First commit)

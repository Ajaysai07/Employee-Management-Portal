# Employee Management Portal

This project is a simple employee management system built using **Python, Streamlit, and Pandas**.
It provides separate dashboards for **Admin** and **Employees**, allowing basic management of employees, tasks, support tickets, and feedback.

The goal of this project was to build a lightweight internal portal that can handle common workplace workflows without relying on a complex database or backend framework.

---
 Features

 Admin Dashboard

* Create new employee accounts
* View, edit, or remove employees
* Assign tasks to employees
* Review submitted tasks and update status
* View employee tickets and respond
* Read employee recommendations and add comments
* Update admin profile and password

 Employee Dashboard

* View and update personal profile
* See assigned tasks
* Raise support tickets
* Track ticket status
* Submit recommendations or feedback
* Change account password


Tech Stack

* **Python**
* **Streamlit**
* **Pandas**
* **CSV files** used as a lightweight data store

---

## Project Structure

```
Employee-Management-Portal
│
├── app.py
├── admin_dashboard.py
├── user_dashboard.py
├── employees.csv
├── tasks.csv
├── tickets.csv
├── recommendations.csv
└── README.md
```

The application uses CSV files to store data such as employees, tasks, and tickets. This keeps the project simple and easy to run locally.

---

 Running the Project

Clone the repository:

```
git clone https://github.com/Ajaysai07/Employee-Management-Portal.git
```

Navigate into the project directory:

```
cd Employee-Management-Portal
```

Install dependencies:

```
pip install streamlit pandas
```

Run the application:

```
streamlit run app.py
```

The application will open in your browser.

---

 Notes

This project was created as a practice project to explore:

* Streamlit dashboards
* Basic role-based interfaces
* Handling simple data storage using CSV files

It can easily be extended by replacing CSV storage with a database like **SQLite or PostgreSQL** and adding authentication features.

---

 Future Improvements

Some ideas for improvement:

* Use a database instead of CSV files
* Add file uploads for task submissions
* Implement role-based authentication
* Add analytics for admin dashboard
* Improve UI styling

---

 Author

Ajay Sai

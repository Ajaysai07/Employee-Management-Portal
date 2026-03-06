import streamlit as st
import pandas as pd
import os
import hashlib
import secrets
import string

CSV_FILE = "employees.csv"
TASKS_FILE = "tasks.csv"
TICKETS_FILE = "tickets.csv"
RECOMMEND_FILE = "recommendations.csv"
ADMIN_FILE = "admin.csv"


class AdminDashboard:

    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))

    def run(self):

        admin_name = st.session_state.get("admin_name", "Admin")

        st.markdown("# 🛠️ Admin Dashboard")
        st.success(f"Welcome {admin_name}")

        if st.sidebar.button("🔄 Reload Page"):
            st.rerun()

        st.sidebar.title("Admin Menu")

        menu = st.sidebar.radio(
            "Navigation",
            [
                "Create Employee",
                "View Employees",
                "Edit Employee",
                "Remove Employee",
                "Assign Task",
                "Task Status",
                "Tickets",
                "Recommendations",
                "Admin Settings",
                "Logout"
            ]
        )

        #  CREATE EMPLOYEE 
        if menu == "Create Employee":

            st.subheader("Create Employee")

            col1, col2 = st.columns(2)

            with col1:
                emp_id = st.text_input("Employee ID")
                name = st.text_input("Name")

                email = ""
                if name:
                    email = name.lower().replace(" ", ".") + "@company.com"

                st.text_input("Email", value=email, disabled=True)

                contact = st.text_input("Contact")

            with col2:

                department = st.selectbox(
                    "Department",
                    ["Select Department","HR","Finance","IT","Sales","Marketing","Operations"]
                )

                roles = {
                    "HR": ["HR Manager","Recruiter","HR Executive"],
                    "Finance": ["Accountant","Finance Analyst","Payroll Specialist"],
                    "IT": ["Software Engineer","Data Analyst","System Administrator","DevOps Engineer"],
                    "Sales": ["Sales Executive","Sales Manager","Business Development Executive"],
                    "Marketing": ["Marketing Executive","SEO Specialist","Content Manager"],
                    "Operations": ["Operations Manager","Logistics Coordinator","Process Analyst"]
                }

                role_options = roles.get(department, [])

                role = st.selectbox(
                    "Role",
                    role_options if role_options else ["Select Department First"]
                )

                salary_structure = {
                    "HR Manager": ["60000","70000","80000"],
                    "Recruiter": ["35000","40000","45000"],
                    "HR Executive": ["30000","35000","40000"],
                    "Accountant": ["40000","50000","60000"],
                    "Finance Analyst": ["50000","60000","70000"],
                    "Payroll Specialist": ["35000","40000","45000"],
                    "Software Engineer": ["60000","80000","100000"],
                    "Data Analyst": ["50000","70000","90000"],
                    "System Administrator": ["50000","65000","80000"],
                    "DevOps Engineer": ["70000","90000","110000"],
                    "Sales Executive": ["30000","40000","50000"],
                    "Sales Manager": ["60000","75000","90000"],
                    "Business Development Executive": ["35000","45000","55000"],
                    "Marketing Executive": ["35000","45000","55000"],
                    "SEO Specialist": ["40000","50000","60000"],
                    "Content Manager": ["45000","55000","65000"],
                    "Operations Manager": ["60000","75000","90000"],
                    "Logistics Coordinator": ["35000","45000","55000"],
                    "Process Analyst": ["40000","50000","60000"]
                }

                salary_options = salary_structure.get(role, [])

                salary = st.selectbox(
                    "Salary",
                    salary_options if salary_options else ["Select Role First"]
                )

                joining_date = st.date_input("Joining Date")

            if st.button("Add Employee"):

                if department == "Select Department":
                    st.error("Please select a department")

                elif os.path.exists(CSV_FILE):

                    df = pd.read_csv(CSV_FILE)

                    if emp_id in df["Employee ID"].astype(str).values:
                        st.error("Employee ID already exists")
                        return

                password = self.generate_random_password()
                hashed = hashlib.sha256(password.encode()).hexdigest()

                new_emp = pd.DataFrame([{
                    "Employee ID": emp_id,
                    "Name": name,
                    "Email": email,
                    "Contact": contact,
                    "Department": department,
                    "Role": role,
                    "Salary": salary,
                    "Joining Date": joining_date,
                    "Password": hashed
                }])

                new_emp.to_csv(
                    CSV_FILE,
                    mode="a",
                    header=not os.path.exists(CSV_FILE),
                    index=False
                )

                st.success("Employee Created Successfully")
                st.info(f"Temporary Password: {password}")

        #  VIEW EMPLOYEES 
        elif menu == "View Employees":

            st.subheader("All Employees")

            if os.path.exists(CSV_FILE):

                df = pd.read_csv(CSV_FILE)

                st.dataframe(
                    df.drop(columns=["Password"], errors="ignore"),
                    use_container_width=True
                )

            else:
                st.info("No employees yet.")

        #  EDIT EMPLOYEE 
        elif menu == "Edit Employee":

            if not os.path.exists(CSV_FILE):
                st.info("No employees available")
                return

            df = pd.read_csv(CSV_FILE)

            emp = st.selectbox("Select Employee", df["Employee ID"].astype(str))

            idx = df[df["Employee ID"].astype(str) == emp].index[0]

            emp_data = df.loc[idx]

            name = st.text_input("Name", emp_data["Name"])
            email = st.text_input("Email", emp_data["Email"])
            contact = st.text_input("Contact", emp_data["Contact"])
            department = st.text_input("Department", emp_data["Department"])
            role = st.text_input("Role", emp_data["Role"])
            salary = st.text_input("Salary", emp_data["Salary"])

            new_password = st.text_input("Reset Password (optional)", type="password")

            if st.button("Update"):

                df.at[idx, "Name"] = name
                df.at[idx, "Email"] = email
                df.at[idx, "Contact"] = contact
                df.at[idx, "Department"] = department
                df.at[idx, "Role"] = role
                df.at[idx, "Salary"] = salary

                if new_password:
                    df.at[idx, "Password"] = hashlib.sha256(new_password.encode()).hexdigest()

                df.to_csv(CSV_FILE, index=False)

                st.success("Employee Updated Successfully")

        #  REMOVE EMPLOYEE 
        elif menu == "Remove Employee":

            st.subheader("Remove Employee")

            if not os.path.exists(CSV_FILE):
                st.info("No employees available")
                return

            df = pd.read_csv(CSV_FILE)

            emp = st.selectbox(
                "Select Employee to Remove",
                df["Employee ID"].astype(str)
            )

            if st.button("Delete Employee"):

                df = df[df["Employee ID"].astype(str) != str(emp)]

                df.to_csv(CSV_FILE, index=False)

                st.success(f"Employee {emp} removed successfully")
                st.rerun()

        #  ASSIGN TASK 
        elif menu == "Assign Task":

            if not os.path.exists(CSV_FILE):
                st.info("No employees available")
                return

            employees = pd.read_csv(CSV_FILE)

            emp_id = st.selectbox(
                "Select Employee",
                employees["Employee ID"].astype(str)
            )

            task = st.text_area("Task Description")

            if st.button("Assign Task"):

                task_data = pd.DataFrame([{
                    "Employee ID": emp_id,
                    "Task": task,
                    "Status": "Pending",
                    "Submission": ""
                }])

                task_data.to_csv(
                    TASKS_FILE,
                    mode="a",
                    header=not os.path.exists(TASKS_FILE),
                    index=False
                )

                st.success("Task Assigned Successfully")

        # TASK STATUS
        elif menu == "Task Status":

            st.subheader("Update Task Status")

            if os.path.exists(TASKS_FILE):

                tasks = pd.read_csv(TASKS_FILE)

                if tasks.empty:
                    st.info("No tasks available")

                else:

                    task_index = st.selectbox(
                        "Select Task",
                        tasks.index,
                        format_func=lambda x: f"{tasks.loc[x,'Employee ID']} - {tasks.loc[x,'Task']}"
                    )

                    st.write("Employee ID:", tasks.loc[task_index, "Employee ID"])
                    st.write("Task:", tasks.loc[task_index, "Task"])

                    if "Submission" in tasks.columns:
                        st.write("Submission:", tasks.loc[task_index, "Submission"])

                    status = st.selectbox(
                        "Update Status",
                        ["Pending", "Submitted", "Approved", "Rejected"]
                    )

                    if st.button("Update Task Status"):

                        tasks.loc[task_index, "Status"] = status
                        tasks.to_csv(TASKS_FILE, index=False)

                        st.success("Task Status Updated")
                        st.rerun()

                    st.dataframe(tasks, use_container_width=True)

            else:
                st.info("No tasks yet.")

        #  LOGOUT 
        elif menu == "Logout":

            st.session_state.clear()
            st.session_state["page"] = "login"
            st.rerun()
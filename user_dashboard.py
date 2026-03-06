import streamlit as st
import pandas as pd
import os
import hashlib

CSV_FILE = "employees.csv"
TASKS_FILE = "tasks.csv"
TICKETS_FILE = "tickets.csv"
RECOMMEND_FILE = "recommendations.csv"


class UserDashboard:

    def run(self):

        emp_id = st.session_state.get("emp_id")

        if not os.path.exists(CSV_FILE):
            st.error("Employee database missing")
            return

        df = pd.read_csv(CSV_FILE)

        user_rows = df[df["Employee ID"].astype(str) == str(emp_id)]

        if user_rows.empty:
            st.error("User not found")
            return

        user_index = user_rows.index[0]
        user_data = df.loc[user_index]

        # -------- ADDED SECTION (fix .0 in phone numbers) --------
        contact_clean = str(user_data["Contact"]).replace(".0", "")
        # ---------------------------------------------------------

        st.markdown("# 👨‍💼 Employee Dashboard")
        st.success(f"Welcome {user_data['Name']}")

        if st.sidebar.button("🔄 Reload Page"):
            st.rerun()

        st.sidebar.title("Employee Menu")

        menu = st.sidebar.radio(
            "Navigation",
            [
                "My Profile",
                "Tasks",
                "Raise Ticket",
                "My Tickets",
                "Recommendations",
                "Change Password",
                "Logout"
            ]
        )

        #  PROFILE 
        if menu == "My Profile":

            with st.form("profile"):

                name = st.text_input("Name", user_data["Name"])
                contact = st.text_input("Mobile Number", value=f"+91 {contact_clean}" if not str(contact_clean).startswith("+91") else contact_clean)

                st.text_input("Email", user_data["Email"], disabled=True)
                st.text_input("Department", user_data["Department"], disabled=True)
                st.text_input("Role", user_data["Role"], disabled=True)
                st.text_input("Salary", user_data["Salary"], disabled=True)

                submit = st.form_submit_button("Update Profile")

                if submit:

                    df.at[user_index, "Name"] = name
                    df.at[user_index, "Contact"] = contact

                    df.to_csv(CSV_FILE, index=False)

                    st.success("Profile Updated Successfully")

        # TASKS 
        elif menu == "Tasks":

            if os.path.exists(TASKS_FILE):

                tasks = pd.read_csv(TASKS_FILE)

                my_tasks = tasks[
                    tasks["Employee ID"].astype(str) == str(emp_id)
                ]

                if my_tasks.empty:
                    st.info("📭 No tasks assigned yet.")
                else:
                    st.dataframe(my_tasks, use_container_width=True)

            else:
                st.info("📭 No tasks assigned yet.")

        #  RAISE TICKET 
        elif menu == "Raise Ticket":

            with st.form("ticket_form"):

                title = st.text_input("Ticket Title")
                description = st.text_area("Description")

                submit = st.form_submit_button("Submit Ticket")

                if submit:

                    ticket = pd.DataFrame([{
                        "Employee ID": emp_id,
                        "Employee Name": user_data["Name"],
                        "Title": title,
                        "Description": description,
                        "Status": "Open"
                    }])

                    ticket.to_csv(
                        TICKETS_FILE,
                        mode="a",
                        header=not os.path.exists(TICKETS_FILE),
                        index=False
                    )

                    st.success("🎫 Ticket Raised Successfully!")

        #  MY TICKETS 
        elif menu == "My Tickets":

            if os.path.exists(TICKETS_FILE):

                tickets = pd.read_csv(TICKETS_FILE)

                my_tickets = tickets[
                    tickets["Employee ID"].astype(str) == str(emp_id)
                ]

                if my_tickets.empty:
                    st.info("You have not raised any tickets.")
                else:
                    st.dataframe(my_tickets, use_container_width=True)

            else:
                st.info("No tickets available yet.")

        #  RECOMMENDATIONS 
        elif menu == "Recommendations":

            st.subheader("Submit Recommendation")

            with st.form("recommend_form"):

                message = st.text_area("Your Recommendation")

                submit = st.form_submit_button("Submit")

                if submit and message:

                    rec = pd.DataFrame([{
                        "Employee ID": emp_id,
                        "Employee Name": user_data["Name"],
                        "Recommendation": message
                    }])

                    rec.to_csv(
                        RECOMMEND_FILE,
                        mode="a",
                        header=not os.path.exists(RECOMMEND_FILE),
                        index=False
                    )

                    st.success("Thank you for your feedback!")

        #  CHANGE PASSWORD 
        elif menu == "Change Password":

            new_pass = st.text_input("New Password", type="password")

            if st.button("Update Password"):

                if new_pass:

                    hashed = hashlib.sha256(new_pass.encode()).hexdigest()

                    df.at[user_index, "Password"] = hashed

                    df.to_csv(CSV_FILE, index=False)

                    st.success("Password Updated Successfully")

                else:
                    st.error("Enter a new password")

        #  LOGOUT 
        elif menu == "Logout":

            st.session_state.clear()
            st.session_state["page"] = "login"
            st.rerun()
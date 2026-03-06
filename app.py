import streamlit as st
import pandas as pd
import hashlib
import os

from admin_dashboard import AdminDashboard
from user_dashboard import UserDashboard

CSV_FILE = "employees.csv"

#  PAGE CONFIG 
st.set_page_config(
    page_title="Employee Portal",
    page_icon="🏢",
    layout="wide"
)

#  STYLE 
st.markdown("""
<style>

.stApp{
background: linear-gradient(to right,#4da6ff,#b3d9ff,#ffffff);
}

.title{
text-align:center;
color:#003366;
font-size:42px;
font-weight:bold;
}

.subtitle{
text-align:center;
font-size:18px;
color:#333333;
}

.card{
background:white;
padding:25px;
border-radius:12px;
box-shadow:0px 4px 12px rgba(0,0,0,0.08);
}

div.stButton > button{
height:55px;
font-size:17px;
font-weight:600;
border-radius:10px;
}

</style>
""", unsafe_allow_html=True)


class App:

    #  WELCOME PAGE 
    def role_page(self):

        st.markdown("<div class='title'>🏢 User Management Portal</div>", unsafe_allow_html=True)

        st.markdown(
            "<div class='subtitle'>Manage employees, tasks and support tickets in one place.</div>",
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            st.markdown("""
            <div class="card">

            **Portal Features**

            • Employee management  
            • Task assignment & tracking  
            • Ticket management  
            • Employee recommendations  

            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("### 🛠 Admin")

                if st.button("Admin Login", use_container_width=True):
                    st.session_state["role"] = "admin"
                    st.session_state["page"] = "login"
                    st.rerun()

            with c2:
                st.markdown("### 👨‍💼 Employee")

                if st.button("Employee Login", use_container_width=True):
                    st.session_state["role"] = "employee"
                    st.session_state["page"] = "login"
                    st.rerun()

    #  LOGIN PAGE 
    def login_page(self):

        role = st.session_state.get("role")

        if role is None:
            st.session_state["page"] = "role"
            st.rerun()

        st.markdown(f"<h2 style='text-align:center'>{role.capitalize()} Login</h2>", unsafe_allow_html=True)

        st.write("")
        st.write("")

        left, center, right = st.columns([2,1.2,2])

        with center:

            emp_id = st.text_input("Username / Employee ID")
            password = st.text_input("Password", type="password")

            st.write("")

            if st.button("Login", use_container_width=True):

                # ADMIN LOGIN (FIXED) 
                if role == "admin":

                    ADMIN_FILE = "admin.csv"

                    if not os.path.exists(ADMIN_FILE):
                        st.error("Admin database missing")
                        return

                    admin_df = pd.read_csv(ADMIN_FILE)

                    admin_row = admin_df[admin_df["Username"] == emp_id]

                    if admin_row.empty:
                        st.error("Invalid Admin Credentials")
                        return

                    stored_password = admin_row.iloc[0]["Password"]

                    hashed_input = hashlib.sha256(password.encode()).hexdigest()

                    if hashed_input == stored_password:
                        st.session_state["admin_name"] = admin_row.iloc[0]["Name"]
                        st.session_state["page"] = "admin"
                        st.rerun()
                    else:
                        st.error("Invalid Admin Credentials")

                #  EMPLOYEE LOGIN
                else:

                    if not os.path.exists(CSV_FILE):
                        st.error("Employee database missing")
                        return

                    df = pd.read_csv(CSV_FILE)

                    hashed = hashlib.sha256(password.encode()).hexdigest()

                    user = df[
                        (df["Employee ID"].astype(str) == emp_id) &
                        (df["Password"] == hashed)
                    ]

                    if not user.empty:
                        st.session_state["emp_id"] = emp_id
                        st.session_state["page"] = "user"
                        st.rerun()
                    else:
                        st.error("Invalid Credentials")

            st.write("")

            if st.button("⬅ Back", use_container_width=True):
                st.session_state["page"] = "role"
                st.rerun()

    #  ROUTER 
    def run(self):

        if "page" not in st.session_state:
            st.session_state["page"] = "role"

        if st.session_state["page"] == "role":
            self.role_page()

        elif st.session_state["page"] == "login":
            self.login_page()

        elif st.session_state["page"] == "admin":
            AdminDashboard().run()

        elif st.session_state["page"] == "user":
            UserDashboard().run()


App().run()
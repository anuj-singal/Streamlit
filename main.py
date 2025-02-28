import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

def connectdb():
    conn = sqlite3.connect("mydb.db")
    return conn

def createTable():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(name text,password text,roll int primary key,branch text)")
        conn.commit()

def addRecord(data):
    with connectdb() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO student(name,password,roll,branch) VALUES(?,?,?,?)",data)
            conn.commit()
        except sqlite3.IntegrityError:
            st.error("student already registered...")

def display():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        result = cur.fetchall()
        return result

def signup():
    st.title("Registeration Page")
    name = st.text_input("Enter your username")
    password = st.text_input("Enter the Password",type='password')
    repassword = st.text_input("Retype your password",type='password')
    roll = st.number_input("Enter the Roll Number",format="%0.0f")
    branch = st.selectbox("Branch",options=["CSE","AIML","ECE","RA"])
    if st.button('signin'):
        if password != repassword:
            st.warning("Password Mismatch")
        else:
            addRecord((name,password,roll,branch))
            st.success("Student Registered Successfully...")

def updatepassword(roll,password):
    try:
        with connectdb() as conn:
            cur = conn.cursor()
            cur.execute("SELECT roll FROM student")
            allroll = [tup[0] for tup in cur.fetchall()]
            if(int(roll) in allroll):
                cur.execute("UPDATE student SET password = ? where roll = ?",(password,roll))
                conn.commit()
                return True
            else:
                st.error("Invalid Roll Number")
                return False
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return False

def ResetPassword():
    roll = st.text_input("Enter your Roll number")
    newpassword = st.text_input("Enter the new Password",type="password")
    renewpassword = st.text_input("Re-enter Password",type="password")
    if st.button("Reset") :
        if newpassword != renewpassword :
            st.warning("Password Mismatched...")
        else:
            message = updatepassword(roll,newpassword)
            if message :
                st.success("Password successfully updated.")

def Filter():
    branch = st.selectbox("Branch",options=["CSE","AIML","ECE","RA"])
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE branch = ?",(branch,))
        data = cur.fetchall()
        if(data == []):
            st.warning("No Record Found!")
        else:
            st.table(data)

def Search():
    roll = st.text_input("Enter the roll number to search")
    if st.button("Search"):
        with connectdb() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM student WHERE roll = ?",(roll,))
            data = cur.fetchall()
            if(data == []):
                st.warning("No Record Found!")
            else:
                st.table(data)

# Create a Reset password page , create a filter option on branch , a search option based on rollno , delete student record 

with st.sidebar:
    selected = option_menu("My App",['Signup','Display ALl Record','Reset Password','Filter','Search'])

createTable()

if selected == "Signup":
    signup()
elif selected == "Reset Password":
    ResetPassword()
elif selected == "Filter":
    Filter()
elif selected == "Search":
    Search()
else:
    data = display()
    st.table(data)
import streamlit as st
import pandas as pd


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def predict():      
    st.title("STORM PREDICTION FOR FARMERS")
    html_temp = """
    <div style="background-color:green;text-align:center;padding:15px">
    <h3 style="color:white;text-align:center;">This app shows storm prediction for farmers </h3>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    location = st.text_input("LOCATION")
    begintime = st.text_input("BEGIN Time")
    endtime = st.text_input("END TIME")


def main():
	"""Simple Login App"""

	st.title("Simple Login App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("username")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):

			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Add Post"])
				if task == "Add Post":
					predict()

			else:
				st.warning("Incorrect Username/Password")

	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()
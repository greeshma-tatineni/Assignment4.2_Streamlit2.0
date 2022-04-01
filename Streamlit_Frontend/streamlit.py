import streamlit as st
#import tensorflow as tf
#from PIL import Image
import pickle
import numpy as np
import pandas as pd
import requests

def predict_weather(location,begintime,endtime):

    data ={
    "LOCATION": location,
    "BEGIN TIME": begintime,
    "END TIME": endtime
    }
    response = requests.post('http://127.0.0.1:8000/predict',json=data)
    return response
    


def main1():
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

    result=""
	#if st.selectbox('Fresh'):
    if st.button("Predict"):
        #result=
        img = predict_weather(location,begintime,endtime)
    st.success('The output is {}'.format(result))
    st.image(img.content)
 


def main():
	"""Weather Nowcasting"""
    

	st.title("Weather Nowcasting")

    

	menu = ["Login","SignUp"]
	choice = st.selectbox("Menu",menu)

	if choice == "Login":
		st.subheader("Login Section")
		email = st.text_input("Email")
		password = st.text_input("Password",type='password')
		login_data = {
            "email": email,
            "password": password
		}
		if st.button("Login"):
			#Post Request for Login
			response = requests.post('http://127.0.0.1:8000/user/login',json=login_data)
			if response.reason == 200:
				st.success("Logged In as {}".format(email))
				main1()
			else:
				st.warning("Incorrect Username/Password")


	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_fullname = st.text_input("Full Name")
		new_email= st.text_input("Email")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			#Post Request for Signup
			signup_data = {
			"fullname":	new_fullname,
            "email":new_email,
            "password": new_password
		}
			response = requests.post('http://127.0.0.1:8000/user/signup',json=login_data)
			if response.reason == 200:
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()

    



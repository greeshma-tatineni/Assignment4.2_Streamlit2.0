
#export const COMPONENT_READY_WARNING_TIME_MS = 3000
import streamlit as st
#import tensorflow as tf
from PIL import Image
import pickle
import numpy as np
import pandas as pd
import requests
from cached_data import locator
import gcsfs
from google.cloud import storage
import json
from google.oauth2 import service_account
from google.cloud import storage
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

source= r"C:\Users\16178\Downloads\Final_App\Final_App\Streamlit_Frontend\premium-strata-340618-745287f8fd66.json"
projectid = 'premium-strata-340618'
gcs = gcsfs.GCSFileSystem(project=projectid, token=source)
print("hello")

def predict_weather(location,begintime,endtime):

    data ={
    "location": location,
    "begintime": begintime,
    "endtime": endtime
    }
    response = requests.post('https://nowcastserviceapi-dot-premium-strata-340618.uk.r.appspot.com/predict',json=data)
    return response

st.title("STORM PREDICTION FOR FARMERS")
html_temp = """
<div style="background-color:green;text-align:center;padding:15px">
<h3 style="color:white;text-align:center;">This app shows storm prediction for farmers </h3>
</div>
"""
st.markdown(html_temp,unsafe_allow_html=True)

def predict():
    

        
        location = st.text_input("LOCATION")
        begintime = st.text_input("BEGIN Time")
        endtime = st.text_input("END TIME")

        result=""
        r = st.radio("Pick one", ('Fresh', 'Cache'),index =1)
        
        #if st.selectbox('Fresh'):
        if st.button("Predict"):

            if(r == "Fresh"):
                img = predict_weather(location,begintime,endtime)
                st.success('The output is {}'.format(result))
                st.image(img.content)
            if(r == "Cache"):
                loc = locator(location)
                if(loc=="hitapi"):
                    img = predict_weather(location,begintime,endtime)
                else:
                    #get loc image from gcs
                    filename = 'gcs://cache_loc_images/' +str(loc)+".png"
                    with gcs.open(filename,'rb') as f:
                        st.image(f.read())

                    print("get loc image from gcs")
                    

#@st.cache(suppress_st_warning=True)
#@st.experimental_memo
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
            response = requests.post('https://nowcastserviceapi-dot-premium-strata-340618.uk.r.appspot.com/user/login',json=login_data)
            if(response.content.decode()[2:7] == "error"):
                st.warning("Incorrect Username/Password")
            elif(response.content.decode()[2:8] == "detail"):
                st.warning("Invalid Email")
            
            else:
                st.success("Logged In as {}".format(email))
    
                predict()
            

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_fullname = st.text_input("Full Name")
        new_email= st.text_input("Email")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            #Post Request for Signup
            signup_data = {
            "fullname": new_fullname,
            "email":new_email,
            "password": new_password
        }
            response = requests.post('https://nowcastserviceapi-dot-premium-strata-340618.uk.r.appspot.com/user/signup',json=signup_data)
            if (response.content.decode()[2:8] == "access"):
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")
            else:
                st.warning("Value is not a valid email address")

if __name__ == '__main__':
    main()

    



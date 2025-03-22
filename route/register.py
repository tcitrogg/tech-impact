import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
# from random import choice as rd_choice
import hashlib
import base64
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import pyshorteners

st.set_page_config(page_title="Registration | CGT'S2", page_icon="assets/favicon.png")

# Configuration       
cloudinary.config( 
    cloud_name = "dodxto0d1", 
    api_key = st.secrets["database"]["api_key"], 
    api_secret = st.secrets["database"]["image_api_secret"],
    secure=True
)
SheetConn = st.connection("gsheets", type=GSheetsConnection)
EXISTINGDATA = SheetConn.read(worksheet="RegistrationResponse", ttl=5)

shortener = pyshorteners.Shortener()

st.image("assets/CGT-TOP-BANNER.png")

st.header("CGT'S2")

st.write("""
### Chapel's Got Talent Season 2
😃 Would you like to show case your amazing talent?
Register Now!!!, we anticipate to see you 🤩

- :red[Registration ends by **26th of April**]
- 🖋 Note: **Auditioning is compulsory for all participants.**
""")

def make_id():
    timestamp = datetime.now().timestamp()
    return f"CGT-S2P{str(hashlib.md5(str(timestamp).encode()).hexdigest())[:7]}"

@st.dialog("🤩 Successful!!")
def handle_submission():
    st.text("Great!! 😁 Your submission has be recieved")
    st.divider()
    st.write("""
    😃 Follow this link the join the WhatsApp group, where you will be informed more about the audition and rehearsal.
    > *https://chat.whatsapp.com/Bng1rPXEQd0JWRdrK3P6wX*
    """)

with st.form(key="registration_form"):
    # with st.container(border=True):
    participant_name = st.text_input("Name :red[*]")
    st.caption("If it is a group? what is the name of your group?")
        # handle = st.text_input("Stage alias")
    participant_phone_number = st.text_input("📞 Phone number :red[*]")
    st.caption("Preferable WhatsApp number")

    participant_talent = st.text_input("😎 What talent would you be showcasing? :red[*]")
    participant_reason = st.text_input("😃 Why do you want to participant? :red[*]")
    is_participant_firsttime = st.radio("😉 Is this your first time showcasing this talent? :red[*]", ["Yes", "No"], index=1)
    participant_portrait = st.file_uploader("🎴 Portrait of yourself :red[*]")
    st.caption("Your picture or image of your group")
    
    submit_button = st.form_submit_button("Submit")
    if submit_button:
        if (not participant_name) or (not participant_phone_number) or (not participant_talent) or (not participant_reason) or (not is_participant_firsttime) or (not participant_portrait):
            st.toast(":red[*] Please fill all required fields")
            st.stop()
        else:
            participant_id = make_id()
            with st.spinner():
                # Upload an image
                uploaded_participant_portrait = cloudinary.uploader.upload(participant_portrait.getvalue(), public_id=participant_id)
                uploaded_participant_portrait_url = shortener.isgd.short(uploaded_participant_portrait["secure_url"])
                NEWDATA = pd.DataFrame([
                            {
                                "ID": participant_id,
                                "Name": participant_name,
                                "Phone number": participant_phone_number,
                                "Talent": participant_talent,
                                "Reason": participant_reason,
                                "First time": is_participant_firsttime,
                                "Portrait": uploaded_participant_portrait_url,
                                "Timestamp": datetime.now().strftime("%d-%h-%y %H:%M:%S")
                            }
                        ])
            # Updated Data
            UPDATED_DATA = pd.concat([EXISTINGDATA, NEWDATA])
            
            # Updated Sheets with updated data
            SheetConn.update(worksheet="RegistrationResponse", data=UPDATED_DATA)
            # st.code(uploaded_participant_portrait_url)
            # print(f"Success + {participant_name} submitted response")
            handle_submission()


st.divider()
_, middle, _ = st.columns([0.3, 0.4, 0.15])
with middle:
    st.link_button(label="@chapelunilorin", url="https://zaap.bio/Chapelunilorin")
    st.image("assets/social_mark.png", width=200)
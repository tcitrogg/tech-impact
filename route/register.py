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

st.set_page_config(page_title="Registration | CGT'S2", page_icon="assets/favicon.png")

# Configuration       
cloudinary.config( 
    cloud_name = "dodxto0d1", 
    api_key = "252441329872367", 
    api_secret = st.secrets["database"]["image_api_secret"],
    secure=True
)
SheetConn = st.connection("gsheets", type=GSheetsConnection)
EXISTINGDATA = SheetConn.read(worksheet="RegistrationResponse", ttl=5)

st.image("assets/CGT-TOP-BANNER.png")

st.header("CGT'S2")

st.write("""
### Chapel's Got Talent Season 2
😃 Would you like to show case your amazing talent?
Register Now!!!, we anticipate to see you 🤩

- Registration ends by 8th of May
- Audition will take place on the ⌚️ 11th of May
See you on 17th of May
at Chapel Of The Light, Main Campus, Unilorin

🖋 Note: **Auditioning is compulsory for all participants.**
""")

def make_id():
    timestamp = datetime.now().timestamp()
    return f"CGT-S2P{str(hashlib.md5(str(timestamp).encode()).hexdigest())[:7]}"

@st.dialog("Submitted")
def handle_submission():
    st.header("🤩 Successful")
    st.write("Your submission has be recieved")

with st.form(key="registration_form"):
    # with st.container(border=True):
    participate_name = st.text_input("Name :red[*]")
    st.caption("If it is a group? what is the name of your group?")
        # handle = st.text_input("Stage alias")
    participate_phone_number = st.text_input("📞 Phone number :red[*]")
    st.caption("Preferable WhatsApp number")

    participate_talent = st.text_input("😎 What talent would you be showcasing? :red[*]")
    participate_reason = st.text_input("😃 Why do you want to participate? :red[*]")
    is_participate_firsttime = st.radio("😉 Is this your first time showcasing this talent? :red[*]", ["Yes", "No"], index=1)
    participate_portrait = st.file_uploader("🎴 Portrait of yourself :red[*]")
    st.caption("Your picture or image of your group")
    
    submit_button = st.form_submit_button("Submit")
    if submit_button:
        if (not participate_name) or (not participate_phone_number) or (not participate_talent) or (not participate_reason) or (not is_participate_firsttime) or (not participate_portrait):
            st.toast(":red[*] Please fill all required fields")
            st.stop()
        else:
            participate_id = make_id()
            with st.spinner():
                # Upload an image
                uploaded_participate_portrait = cloudinary.uploader.upload(participate_portrait.getvalue(), public_id=participate_id)
                uploaded_participate_portrait_url = uploaded_participate_portrait["secure_url"]
                NEWDATA = pd.DataFrame([
                            {
                                "ID": participate_id,
                                "Name": participate_name,
                                "Phone number": participate_phone_number,
                                "Talent": participate_talent,
                                "Reason": participate_reason,
                                "First time": is_participate_firsttime,
                                "Portrait": uploaded_participate_portrait_url,
                                "Timestamp": datetime.now().strftime("%d-%h-%y %H:%M:%S")
                            }
                        ])
            # Updated Data
            UPDATED_DATA = pd.concat([EXISTINGDATA, NEWDATA])
            
            # Updated Sheets with updated data
            SheetConn.update(worksheet="RegistrationResponse", data=UPDATED_DATA)
            # st.code(uploaded_participate_portrait_url)
            # print(f"Success + {participate_name} submitted response")
            handle_submission()
    
        st.divider()
        st.text("Great!! 😁")
        st.write("""
    😃 See you on the **📆 11th of May**
    at the **⛪️ Chapel Of The Light** for your audition!!
    """)


st.divider()
_, middle, _ = st.columns([0.3, 0.4, 0.15])
with middle:
    st.link_button(label="@chapelunilorin", url="https://zaap.bio/Chapelunilorin")
    st.image("assets/social_mark.png", width=200)
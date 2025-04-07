import streamlit as st
import pandas as pd
import hashlib
import pyshorteners
import folium
# from random import choice as rd_choice
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
from streamlit_folium import st_folium

st.set_page_config(page_title="Save a seat | Tech Impact 1.0", page_icon="assets/favicon.png")

# Configuration
SheetConn = st.connection("gsheets", type=GSheetsConnection)
EXISTINGDATA = SheetConn.read(worksheet="Response", ttl=5)

shortener = pyshorteners.Shortener()

st.image("assets/tech-impact-form-banner.png")

st.header("☄ Tech Impact 1.0")

st.write("""
### There is a space for everyone in tech.

Join us for an exciting evening of tech inspiration, at [Chapel Of The Light, Unilorin](https://maps.app.goo.gl/5cNUJYwaHAq8EmoF9), as we celebrate our youth week. This lively gathering is all about sparking your creativity and empowering you to become solution-oriented in today's fast-paced digital world. Whether you're passionate about AI, intrigued by innovative Design, or curious about Web3, there's something here for everyone.

Come ready to connect, learn, and have fun as we explore how technology can shape our future. Let's celebrate innovation together—see you there!
""")

st.markdown("#### 📅 Date: 14th of May")

st.markdown("#### 📍 Location")
st.html("""<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3946.241936509288!2d4.6736017!3d8.4758397!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x10364b3d082f5acd%3A0xf22cc9c204615c61!2sUnilorin%20Chapel%20of%20the%20Light!5e0!3m2!1sen!2sng!4v1743971143963!5m2!1sen!2sng" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""")
m = folium.Map(location=[8.4758397,4.6736017], zoom_start=16)
folium.Marker(
    [8.4758397,4.6736017], popup="Chapel Of The Light, Unilorin", tooltip="Chapel Of The Light, Unilorin"
).add_to(m)
st_data = st_folium(m, width=725)

# ------------

@st.dialog("🤩 See you on the 14th of May!!")
def handle_submission():
    st.text("Great!! 😁 Your submission has be recieved")
    st.divider()


def make_id(wing_id: str):
    timestamp = datetime.now().timestamp()
    return f"TI-{wing_id}25{str(hashlib.md5(str(timestamp).encode()).hexdigest())[:7]}"

with st.form(key="registration_form"):
    attendee_name = st.text_input("Name :red[*]")
    attendee_phone_number = st.text_input("📞 Phone number :red[*]")
    st.caption("Preferable WhatsApp number")

    attendee_wing = st.radio("🛠️ What **Solution Wing** would you like to save a seat for? :red[*]", ["AI", "Design", "Web3"])
    attendee_expectation = st.text_input("😃 What are your expectations for this event?")
    
    submit_button = st.form_submit_button("Submit")
    if submit_button:
        if (not attendee_name) or (not attendee_phone_number) or (not attendee_wing):
            st.toast(":red[*] Please fill all required fields")
            st.stop()
        else:
            if attendee_wing == "AI":
                wing_id = "A"
            elif attendee_wing == "Design":
                wing_id = "D"
            else:
                wing_id = "W"
            attendee_id = make_id(wing_id=wing_id)
            with st.spinner():
                # Upload an image
                NEWDATA = pd.DataFrame([
                            {
                                "ID": attendee_id,
                                "Name": attendee_name,
                                "Phone number": attendee_phone_number,
                                "Wing": attendee_wing,
                                "Expectation": attendee_expectation,
                                "Timestamp": datetime.now().strftime("%d-%h-%y %H:%M:%S")
                            }
                        ])
            # Updated Data
            UPDATED_DATA = pd.concat([EXISTINGDATA, NEWDATA])
            
            # Updated Sheets with updated data
            SheetConn.update(worksheet="Response", data=UPDATED_DATA)
            handle_submission()


st.divider()
_, middle, _ = st.columns([0.3, 0.4, 0.15])
with middle:
    st.link_button(label="@chapelunilorin", url="https://bit.ly/chapelunilorin")
    st.image("assets/social_mark.png", width=200)
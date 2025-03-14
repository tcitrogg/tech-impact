import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import base64
# import io

st.set_page_config(page_title="View | CGT'S2", page_icon="assets/favicon.png")


st.write("bankai")

# Display stored image
# decoded_image = base64.b64decode(encoded_image)
# st.image(io.BytesIO(decoded_image), caption="Stored Image", use_column_width=True)
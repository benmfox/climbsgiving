import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import random, os
import time, base64
sys.path.append(str(Path(__file__).parent.parent))
from utils import (
    init_session_state,
    get_all_participants,
    get_participant_count,
    sign_in_participant,
    on_this_day_message,
    log_climb_completion
)

if os.path.exists(".maintenance_mode"):
    st.error("Someone broke the app!")
    st.image('assets/logo2.png', width=1000)
    st.write(on_this_day_message())
    st.markdown("""LOOK HOW GOOD I (AI) AM AT CODING""")
    st.code("""def womens_salary(mens_salary):
    return mens_salary * 0.82""")
    st.stop()

logo_choice = random.choice(['assets/logo.jpg', 'assets/logo2.png', 'assets/logo3.jpeg'])
st.logo(logo_choice)
st.set_page_config(page_title="Sign In", page_icon="🥸", layout="wide")

init_session_state()

st.header("Sign Up Sheet")
st.markdown("> Sponsored by Palantir Technologies")

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("sign_in_form"):
        name = st.text_input("Your Name", help="Enter your full name", key="name_input")
        #ssn = st.text_input("Social Security Number", type="password", help="Enter your SSN for verification purposes")
        submitted = st.form_submit_button("Sign In", type="primary")
        
        if submitted and name:
            name = name.strip()
            if not name:
                st.error("Please enter a valid name")
            else:
                if 'austin' in name.lower():
                    name = 'Catlord5'
                if 'emily' in name.lower():
                    name = 'Dr. Emily Bramel PhD'
                success, message = sign_in_participant(name)
                if success:
                    if name == 'Catlord5':
                        log_climb_completion("bonus", "V10000", [name])
                        st.success("Special welcome to our esteemed leader, Catlord5!")
                    else:
                        st.success(f"Welcome, {name}! Thank you for sharing your data with us.")
                    #st.image('assets/IMG_0190.jpeg', width=600)
                elif message == "Already signed in":
                    st.info(f"Welcome back, {name}! You're already being watched.")
                    if name == 'Catlord5':
                        st.toast("Special welcome to our esteemed leader, Catlord5!")
                    #st.image('assets/IMG_0190.jpeg', width=600)
                else:
                    st.error("Failed to sign in. I'm a bot and bad at coding. Maybe try again.")

with col2:
    participant_count = get_participant_count()
    st.metric("Total Participants", participant_count)
    if submitted:
        st.image('assets/IMG_0190.jpeg', width=100)
        time.sleep(3)
        st.rerun()

# Display participants
participants = get_all_participants()
if participants:
    st.subheader("Climbers")
    
    participants_df = pd.DataFrame([
        {
            "Name": p["name"], 
            "Sign In Time": pd.to_datetime(p["sign_in_time"]).strftime("%I:%M %p"),
            "Social Security Number": f"{random.randint(100,999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}",
            "Friend Tier": "First Tier" if p['name'].lower() in ["iris,"ben","benson","abby","Catlord5"] else "Dead to me"  
        }
        for p in sorted(participants, key=lambda x: x["name"], reverse=True)
    ])
    st.dataframe(participants_df, width="stretch", hide_index=True)

    if participants_df['Name'].str.lower().str.contains('iris').any():
        st.subheader("Hikers")
        st.dataframe(participants_df[participants_df['Name'].str.lower().str.contains('iris')], width="stretch", hide_index=True)
else:
    st.info("No participants signed in yet. Get some friends.")

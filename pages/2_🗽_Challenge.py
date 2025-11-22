import streamlit as st
import pandas as pd
import sys, os
from pathlib import Path
import random, time

sys.path.append(str(Path(__file__).parent.parent))
from utils import (
    init_session_state,
    get_participant_names,
    get_all_participants,
    log_climb_completion,
    get_completions_for_location,
    on_this_day_message
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
st.set_page_config(page_title="Challenge Tracker", page_icon="🎯", layout="wide")

init_session_state()

st.title("Challenge Progress Tracker")
st.markdown("> With inspiration from Luigi Mangione")

participants = get_participant_names()

if not participants:
    st.warning("No participants signed in yet! You have no friends.")
else:
    location = st.selectbox("Select Location", [
        "Location 1: West Harlem Vital",
        "Location 2: Upper East Side Vital",
        "Location 3: Lower East Side Vital",
        "Location 4: Brooklyn Vital"
    ])
    
    loc_num = int(location.split(":")[0].split()[-1])
    loc_key = f"location_{loc_num}"
    
    # ===== LOCATIONS 1 & 2: V-GRADE TRACKING =====
    if loc_num in [1, 2]:
        st.subheader(f"{location.split(':')[0].strip()}")
        st.markdown(f"**Goal:** 1 V8, 2 V7s, 3 V6s, 4 V5s, 5 V4s, 8 V3s")
        
        @st.fragment
        def show_climb_tracking():
            grades = ["V8", "V7", "V6", "V5", "V4", "V3"]
            targets = [1, 2, 3, 4, 5, 8]
            
            # Get completions
            all_completions = get_completions_for_location(loc_key)
            
            # Summary table
            st.markdown("#### Overall Progress")
            summary_data = []
            for grade, target in zip(grades, targets):
                grade_count = len([c for c in all_completions if c["grade"] == grade])
                status = "✅" if grade_count >= target else "🔄"
                summary_data.append({
                    "Grade": grade,
                    "Target": target,
                    "Completed": grade_count,
                    "Status": status
                })
            
            st.dataframe(pd.DataFrame(summary_data), width="stretch", hide_index=True)
            
            st.divider()
            
            # Simple form for adding climbs
            st.markdown("#### Log New Climb")
            
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                selected_grade = st.selectbox("Grade", grades, key=f"grade_{loc_key}")
            
            with col2:
                selected_participants = st.multiselect(
                    "Who completed it?",
                    participants,
                    key=f"participants_{loc_key}"
                )
            
            with col3:
                st.write("")  # Spacing
                st.write("")  # Spacing
                if st.button("➕ Add", type="primary",  width="stretch"):
                    if not selected_participants:
                        st.error("Select at least one participant")
                    else:
                        if log_climb_completion(loc_key, selected_grade, selected_participants):
                            st.toast(f"✅ Logged {selected_grade} for {len(selected_participants)} climber(s)!")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("Failed to log climb")
            
            # Show recent completions
            if all_completions:
                st.divider()
                st.markdown("#### Recent Completions")
                recent = sorted(all_completions, key=lambda x: x["completed_at"], reverse=True)[:10]
                
                recent_data = []
                for comp in recent:
                    recent_data.append({
                        "Grade": comp["grade"],
                        "Participant": comp["participant_name"],
                        "Time": pd.to_datetime(comp["completed_at"]).strftime("%Y-%m-%d %H:%M") # 2025-11-17T07:57:34.144850
                    })
                recent_dataframe = pd.DataFrame(recent_data)
                recent_dataframe = recent_dataframe.groupby('Time').agg({'Grade': 'first', 'Participant': ', '.join}).reset_index()
                recent_dataframe['Time'] = pd.to_datetime(recent_dataframe['Time']).dt.strftime("%I:%M %p")
                st.dataframe(recent_dataframe,  width="stretch", hide_index=True)
        
        show_climb_tracking()
    
    # ===== LOCATION 3: PERSONAL CHALLENGES =====
    elif loc_num == 3:
        st.subheader(f"{location.split(':')[0].strip()}")
        st.markdown("**Goal:** Each person chooses one climb. Everyone attempts each person's climb.")
        
        @st.fragment
        def show_location3_challenges():
            grades = [f"V{i}" for i in range(1, 13)]  # V1 to V12
            
            # Get completions
            all_completions = get_completions_for_location(loc_key)
            
            st.markdown("#### Log Personal Challenge Climbs")
            
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                selected_grade = st.selectbox("Grade", grades, key=f"grade_{loc_key}")
            
            with col2:
                selected_participants = st.multiselect(
                    "Who completed it?",
                    participants,
                    default=participants,
                    key=f"participants_{loc_key}"
                )
            
            with col3:
                st.write("")  # Spacing
                st.write("")  # Spacing
                if st.button("➕ Add", type="primary",  width="stretch"):
                    if not selected_participants:
                        col2.error("Select at least one participant")
                    elif set(selected_participants) != set(participants):
                        bitches = set(participants) - set(selected_participants)
                        col2.error(f"HAHA nice try {bitches}. Everyone must complete the climbs.")
                    else:
                        if log_climb_completion(loc_key, selected_grade, selected_participants):
                            st.toast(f"✅ Logged {selected_grade} for {len(selected_participants)} climber(s)!")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("Failed to log climb")
            # Show recent completions
            if all_completions:
                st.divider()
                st.markdown("#### Recent Completions")
                recent = sorted(all_completions, key=lambda x: x["completed_at"], reverse=True)
                
                recent_data = []
                for comp in recent:
                    recent_data.append({
                        "Grade": comp["grade"],
                        "Participant": comp["participant_name"],
                        "Time": pd.to_datetime(comp["completed_at"]).strftime("%Y-%m-%d %H:%M:%S")
                    })
                recent_dataframe = pd.DataFrame(recent_data)
                recent_dataframe = recent_dataframe.groupby('Time').agg({'Grade': 'first', 'Participant': ', '.join}).reset_index()
                recent_dataframe['Time'] = pd.to_datetime(recent_dataframe['Time']).dt.strftime("%I:%M %p")
                st.dataframe(recent_dataframe,  width="stretch", hide_index=True)
        
        show_location3_challenges()
    
    # ===== LOCATION 4: ROOF SESSION =====
    elif loc_num == 4:
        st.subheader(f"{location.split(':')[0].strip()}")
        st.markdown("**Goal:** Roof climbing. Jason will judge you if you don't climb at least a red.")
        
        @st.fragment
        def show_location4_status():
            # Get completions (all V4s)
            all_completions = get_completions_for_location(loc_key)
            
            st.markdown("#### Log Red Route Climbs (V4)")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected_participants = st.multiselect(
                    "Who completed a red route?",
                    participants,
                    key=f"participants_{loc_key}"
                )
            
            with col2:
                st.write("")  # Spacing
                if st.button("➕ Add V4", type="primary",  width="stretch"):
                    if not selected_participants:
                        st.error("Select at least one participant")
                    else:
                        if log_climb_completion(loc_key, "V4", selected_participants):
                            st.toast(f"✅ Logged V4 for {len(selected_participants)} climber(s)!")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("Failed to log climb")
            
            # Show who has climbed red routes
            if all_completions:
                st.divider()
                st.markdown("#### Who Climbed Red Routes")
                
                # Group by participant
                climbers = {}
                for comp in all_completions:
                    name = comp["participant_name"]
                    if name not in climbers:
                        climbers[name] = 0
                    climbers[name] += 1
                
                status_data = []
                for p in participants:
                    count = climbers.get(p, 0)
                    status = "✅ You climbed a Red, after how many years?" if count > 0 else "❌ Not a real climber"
                    status_data.append({
                        "Participant": p,
                        "Status": status,
                        "Red Routes": count
                    })
                
                st.dataframe(pd.DataFrame(status_data),  width="stretch", hide_index=True)
        
        show_location4_status()

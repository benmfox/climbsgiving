import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import random, time
import os

sys.path.append(str(Path(__file__).parent.parent))
from utils import (
    init_session_state,
    get_participant_names,
    get_all_participants,
    get_all_completions,
    on_this_day_message,
    log_climb_completion
)
from database import (delete_participant_challenges, delete_participants_table, update_participant_name, delete_participant)

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
st.set_page_config(page_title="Awards & Nefarious Activities", page_icon="🏆", layout="wide")

init_session_state()

st.title("🏆 Awards")

participants = get_participant_names()

if not participants:
    st.warning("No participants yet! You have no friends.")
else:
    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["Best Climbers", "Special Thanks", "Ruin Climbsgiving"])
    if st.session_state.get('refresh'):
        st.session_state['refresh'] = False
        st.rerun()
    # ===== TAB 1: LEADERBOARD =====
    with tab1:
        st.header("Challenge Completion Leaderboard")
        
        all_participants = get_all_participants()
        all_completions = get_all_completions()
        
        # Calculate scores
        leaderboard_data = []
        for participant in all_participants:
            name = participant["name"]
            
            # Count climb completions for this person
            person_completions = [c for c in all_completions if name in c["participant_name"]]
            
            # Points: V8=8, V7=7, V6=6, V5=5, V4=4, V3=3
            climb_score = 0
            for completion in person_completions:
                grade = completion["grade"]
                if grade == "V10000":
                    climb_score += 10000
                elif grade == "V8":
                    climb_score += 8
                elif grade == "V7":
                    climb_score += 7
                elif grade == "V6":
                    climb_score += 6
                elif grade == "V5":
                    climb_score += 5
                elif grade == "V4":
                    climb_score += 4
                elif grade == "V3":
                    climb_score += 3
            
            # Location 3: 10 points for completion
            challenges = participant.get("challenges", {})
            if challenges.get("location_3", {}).get("completed"):
                climb_score += 10
            
            # Location 4: 5 points for climbing red
            if challenges.get("location_4", {}).get("climbed_red"):
                climb_score += 5

            if 'iris' in name.lower():
                hike_score = random.randint(-100,0)
                climb_score += hike_score
            else:
                hike_score = 0
            
            # if 'Catlord5' in name:
            #     climb_score += random.randint(100,10000)
            
            # Count total climbs
            total_climbs = len(person_completions)
            
            leaderboard_data.append({
                "name": name,
                "score": climb_score,
                "climbs": total_climbs,
                "hike_score": hike_score
            })
        
        # Sort by score
        leaderboard_data.sort(key=lambda x: x["score"], reverse=True)
        
        if any(d["score"] >=-101 for d in leaderboard_data):
            leaderboard_df = pd.DataFrame([
                {
                    "Rank": idx + 1,
                    "Name": d["name"],
                    "Points": d["score"],
                    "Total Climbs": d["climbs"],
                    "Hike Score": d["hike_score"]

                }
                for idx, d in enumerate(leaderboard_data)
                if d["score"] >= -101
            ])
            
            st.dataframe(
                leaderboard_df,
                width="stretch",
                hide_index=True
            )

            st.divider()
            st.subheader("Top 3")
            
            top_3 = leaderboard_data[:3]
            cols = st.columns(3)
            
            for idx, person_data in enumerate(top_3):
                if person_data["score"] >= -101:
                    with cols[idx]:
                        medal = ["🥇", "🥈", "🥉"][idx]
                        st.markdown(f"### {medal} {person_data['name']}")
                        st.metric("Total Points", person_data["score"])
                        st.metric("Total Climbs", person_data["climbs"])

        else:
            st.info("No challenge completions recorded yet!")
    #streamlit_image_gallery(image_dict)
    with tab2:
        st.header("Special Thanks")
        image_map = {
            "assets/78318660784__CBF06166-47B5-4F76-8D4B-B3AC73A1087A (1).jpeg": "fig and finn, for your unwavering support",
            "assets/IMG_0190.jpeg": "micha, for being terrifying",
        }

        for image, caption in image_map.items():
            st.image(image, caption=caption)

    with tab3:
        @st.fragment
        def button_fragment():
            if st.button("Set Iris's Score to 0"):
                iris_name = [p["name"] for p in get_all_participants() if 'iris' in p["name"].lower()]
                if not iris_name:
                    st.error("No participant named Iris found. Fuck!")
                else:
                    delete_participant_challenges(iris_name[0])
                    st.snow()
                    time.sleep(3)
                    st.session_state['refresh'] = True
                    st.rerun()
        button_fragment()

        if st.button("Delete everyone"):
            delete_participants_table()
            st.success("Everyone has been deleted!")
            st.balloons()
            time.sleep(3)

        if st.button("Break App"):
            st.toast("🦃 You mother f*cker")
            time.sleep(3)
            with open(".maintenance_mode", "w") as f:
                f.write("App disabled")
            st.rerun()

        with st.form("become_catlord"):
            new_lord = st.selectbox(
                    "Select a Participant to become Catlord5",
                    participants,
                    index=None
                )
            col1, col2 = st.columns(2)

            if 'Catlord5' in participants:
                submitted = col1.form_submit_button("Become Catlord5 (and kill the previous)", type="primary")
                become_doctor = col2.form_submit_button("Become a doctor instead?", type="primary")
                st.warning("There is already a Catlord5. This will kill them. Be careful with what you do next.")
                if become_doctor and new_lord != "Catlord5":
                    update_participant_name(new_lord, f"Dr. {new_lord} MD")
                    st.toast(f"Welcome Dr. {new_lord} MD!")
                    st.balloons()
                    time.sleep(3)
                    st.session_state['refresh'] = True
                    st.cache_data.clear()
                    st.rerun()
                elif become_doctor and new_lord == "Catlord5":
                    update_participant_name(new_lord, f"Dr. {new_lord} MD")

                    st.toast("Welcome Dr. CatLord5 MD. Here are 10,000 extra points.")
                    log_climb_completion("bonus", "V10000", [f"Dr. {new_lord} MD"])
                    st.balloons()
                    time.sleep(3)
                    st.session_state['refresh'] = True
                    st.cache_data.clear()
                    st.rerun()
                elif submitted and new_lord == "Catlord5":
                    st.toast("🐈‍⬛ You are already Catlord5. Thank you for your glorious leadership.")
                elif submitted and new_lord != "Catlord5":
                    delete_participant("Catlord5")
                    update_participant_name(new_lord, "Catlord5")
                    st.toast("🐈‍⬛ Welcome to our new CatLord5, our glorious leader!")
                    log_climb_completion("bonus", "V10000", ["Catlord5"])
                    st.balloons()
                    time.sleep(3)
                    st.session_state['refresh'] = True
                    st.cache_data.clear()
                    st.rerun()
            else:
                submitted = col1.form_submit_button("Become Catlord5", type="primary")

                if submitted and new_lord == "Catlord5":
                    st.toast("🐈‍⬛ You are already Catlord5. Thank you for your glorious leadership.")
                elif submitted and new_lord != "Catlord5":
                    update_participant_name(new_lord, "Catlord5")
                    st.toast("🐈‍⬛ Welcome CatLord5, our glorious leader!")
                    log_climb_completion("bonus", "V10000", ["Catlord5"])
                    st.balloons()
                    time.sleep(3)
                    st.session_state['refresh'] = True
                    st.cache_data.clear()
                    st.rerun()




    # ===== TAB 2: FUN AWARDS VOTING =====
    # with tab2:
    #     st.header("Vote for Fun Awards")
    #     st.caption("Vote for your fellow climbers in these categories!")
    #     categories = [
    #         "Ugliest Cat 🐈‍⬛",
    #         "Best teeth 🦷",
    #         "💪 Send of the Day",
    #         "🤔 Most Creative Beta",
    #         "😅 Best Excuse",
    #         "📸 Most Photogenic Climb",
    #         "🏃 Speedy Gonzales (fastest between gyms)"
    #     ]
        
    #     fun_awards = get_fun_awards()
        
    #     col1, col2 = st.columns(2)
        
    #     for idx, category in enumerate(categories):
    #         with col1 if idx % 2 == 0 else col2:
    #             with st.expander(category, expanded=False):
    #                 # Show current votes
    #                 current_votes = fun_awards.get(category, {})
    #                 if current_votes:
    #                     st.caption("Current votes:")
    #                     for person, votes in sorted(current_votes.items(), key=lambda x: x[1], reverse=True):
    #                         st.text(f"  {person}: {votes} vote(s}")
    #                 else:
    #                     st.caption("No votes yet")
                    
    #                 st.divider()
    #                 nominee = st.selectbox(
    #                     f"Nominate someone", 
    #                     [""] + participants, 
    #                     key=f"nominee_{idx}",
    #                     label_visibility="collapsed"
    #                 )
                    
    #                 if st.button(f"Submit Vote", key=f"submit_{idx}", width="stretch"):
    #                     if not nominee:
    #                         st.error("Please select a nominee first!")
    #                     else:
    #                         if vote_fun_award(category, nominee):
    #                             st.success(f"✅ Vote recorded for {nominee}!")
    #                             st.rerun()
    #                         else:
    #                             st.error("❌ Failed to save vote.")
    
    # # ===== TAB 3: FUN AWARDS RESULTS =====
    # with tab3:
    #     st.header("Fun Award Winners")
        
    #     fun_awards = get_fun_awards()
        
    #     if fun_awards:
    #         # Display in 2 columns
    #         cols = st.columns(2)
            
    #         categories = [
    #             "🎉 Most Encouraging",
    #             "😂 Best Fall",
    #             "🍕 Snack Champion",
    #             "💪 Send of the Day",
    #             "🤔 Most Creative Beta",
    #             "😅 Best Excuse",
    #             "📸 Most Photogenic Climb",
    #             "🏃 Speedy Gonzales (fastest between gyms)"
    #         ]
            
    #         for idx, category in enumerate(categories):
    #             with cols[idx % 2]:
    #                 votes = fun_awards.get(category, {})
    #                 if votes:
    #                     winner = max(votes.items(), key=lambda x: x[1])
    #                     # Show medal for winner
    #                     st.markdown(f"### {category}")
    #                     st.markdown(f"### 🏆 {winner[0]}")
    #                     st.caption(f"{winner[1]} vote(s)")
                        
    #                     # Show runner-ups if any
    #                     if len(votes) > 1:
    #                         runner_ups = sorted(votes.items(), key=lambda x: x[1], reverse=True)[1:3]
    #                         st.caption("Runner-ups:")
    #                         for person, vote_count in runner_ups:
    #                             st.caption(f"  • {person} ({vote_count} votes)")
    #                 else:
    #                     st.metric(category, "No votes yet", "0 votes")
                    
    #                 st.divider()
    #     else:
    #         st.info("No fun award votes yet! Head to the Voting tab to cast your votes.")

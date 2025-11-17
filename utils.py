import streamlit as st
from database import (
    get_cached_participants,
    participant_exists,
    add_participant,
    update_participant_challenges,
    add_climb_completion_to_participant,
    get_climb_completions_by_location,
    get_cached_climb_completions
)

def init_session_state():
    """Initialize session state"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = True
    return True

def get_all_participants():
    """Get all participants from database"""
    return get_cached_participants()

def get_participant_names():
    """Get list of all participant names"""
    participants = get_all_participants()
    return [p["name"] for p in participants]

def get_participant_count():
    """Get total number of participants"""
    return len(get_all_participants())

def get_participant_data(name):
    """Get specific participant's data"""
    participants = get_all_participants()
    for p in participants:
        if p["name"] == name:
            return p
    return None

def sign_in_participant(name):
    """Sign in a new participant"""
    if participant_exists(name):
        return False, "Already signed in"
    
    if add_participant(name):
        # Clear cache to show new participant
        get_cached_participants.clear()
        return True, "Success"
    return False, "Error saving"

def save_challenge_progress(name, location_key, challenges_data):
    """Save challenge progress for a participant"""
    if update_participant_challenges(name, location_key, challenges_data):
        get_cached_participants.clear()
        return True
    return False

def log_climb_completion(location_key, grade, participant_names):
    """Log a climb completion for one or more participants"""
    if add_climb_completion_to_participant(location_key, grade, participant_names):
        get_cached_participants.clear()
        get_cached_climb_completions.clear()
        return True
    return False

def get_completions_for_location(location_key):
    """Get all climb completions for a location"""
    return get_climb_completions_by_location(location_key)

def get_all_completions():
    """Get all climb completions with caching"""
    return get_cached_climb_completions()

def on_this_day_message():
    """Return a historical message for today"""
    import datetime, pytz
    est = pytz.timezone('America/New_York')
    current_time = datetime.datetime.now(est)
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return f"In November of 1620, the Mayflower arrived in the New World, carrying the Pilgrims who would later celebrate the first Thanksgiving and lay the foundation for what would become the United States of America (I am a stupid bot). Today, on {current_time} EST, we celebrated Climbsgiving, and I personally had a great time."
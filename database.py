import os
from supabase import create_client, Client
import streamlit as st
from datetime import datetime
import json

# Get Supabase credentials from Streamlit secrets or environment
def get_supabase_client():
    """Initialize Supabase client"""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
    except:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        st.error("⚠️ Supabase credentials not found. Please configure in .streamlit/secrets.toml")
        return None
    
    return create_client(url, key)

# Initialize client
supabase: Client = get_supabase_client()

# Participant functions
def get_all_participants():
    """Get all participants from database"""
    if not supabase:
        return []
    try:
        response = supabase.table("participants").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching participants: {e}")
        return []

def add_participant(name):
    """Add a new participant"""
    if not supabase:
        return False
    try:
        data = {
            "name": name,
            "sign_in_time": datetime.now().isoformat(),
            "challenges": {f"location_{i}": {} for i in range(1, 5)}
        }
        supabase.table("participants").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error adding participant: {e}")
        return False

def participant_exists(name):
    """Check if participant already exists"""
    if not supabase:
        return False
    try:
        response = supabase.table("participants").select("name").eq("name", name).execute()
        return len(response.data) > 0
    except:
        return False

def delete_participant(name):
    """Delete a participant by name"""
    if not supabase:
        return False
    try:
        supabase.table("participants").delete().eq("name", name).execute()
        return True
    except Exception as e:
        st.error(f"Error deleting participant: {e}")
        return False

def update_participant_name(name, new_name):
    """Update participant's name"""
    if not supabase:
        return False
    try:
        # Get current participant data
        response = supabase.table("participants").select("name").eq("name", name).execute()
        if response.data:
            supabase.table("participants").update({
                "name": new_name
            }).eq("name", name).execute()
            return True
    except Exception as e:
        st.error(f"Error updating name: {e}")
        return False

def delete_participant_challenges(name):
    """Delete all challenges for a participant"""
    if not supabase:
        return False
    try:
        supabase.table("participants").update({
            "challenges": {}
        }).eq("name", name).execute()
        return True
    except Exception as e:
        st.error(f"Error deleting challenges: {e}")
        return False

def add_climb_completion_to_participant(location_key, grade, participant_names):
    """Add a climb completion to participant(s) challenges"""
    if not supabase:
        return False
    try:
        # Handle both single name and list of names
        if isinstance(participant_names, str):
            participant_names = [participant_names]
        
        for name in participant_names:
            # Get current participant data
            response = supabase.table("participants").select("challenges").eq("name", name).execute()
            if response.data:
                current_challenges = response.data[0].get("challenges", {})
                
                # Initialize location if doesn't exist
                if location_key not in current_challenges:
                    current_challenges[location_key] = {}
                
                # Initialize completions array if doesn't exist
                if "completions" not in current_challenges[location_key]:
                    current_challenges[location_key]["completions"] = []
                
                # Add new completion
                current_challenges[location_key]["completions"].append({
                    "grade": grade,
                    "completed_at": datetime.now().isoformat()
                })
                
                # Update database
                supabase.table("participants").update({
                    "challenges": current_challenges
                }).eq("name", name).execute()
        
        return True
    except Exception as e:
        st.error(f"Error adding climb completion: {e}")
        return False

def get_all_climb_completions_from_participants():
    """Get all climb completions from participants table"""
    if not supabase:
        return []
    try:
        response = supabase.table("participants").select("name, challenges").execute()
        completions = []
        
        for participant in response.data:
            name = participant["name"]
            challenges = participant.get("challenges", {})

            # Extract completions from location_1, location_2, location_3, and location_4
            for location_key in ["location_1", "location_2", "location_3", "location_4", "bonus"]:
                if location_key in challenges:
                    location_completions = challenges[location_key].get("completions", [])
                    for comp in location_completions:
                        completions.append({
                            "location": location_key,
                            "grade": comp.get("grade"),
                            "participant_name": name,
                            "completed_at": comp["completed_at"]
                        })
        
        return completions
    except Exception as e:
        st.error(f"Error fetching climb completions: {e}")
        return []

def get_climb_completions_by_location(location_key):
    """Get climb completions for a specific location"""
    if not supabase:
        return []
    try:
        all_completions = get_all_climb_completions_from_participants()
        return [c for c in all_completions if c["location"] == location_key]
    except Exception as e:
        st.error(f"Error fetching completions: {e}")
        return []

def delete_participants_table():
    """Delete all participants (for testing purposes or not)"""
    if not supabase:
        return False
    try:
        supabase.table("participants").delete().neq("id", 0).execute()
        return True
    except Exception as e:
        st.error(f"Error deleting participants table: {e}")
        return False

# Cache with TTL for better performance
@st.cache_data(ttl=5)  # Cache for 5 seconds
def get_cached_participants():
    """Get participants with caching"""
    return get_all_participants()

@st.cache_data(ttl=5)
def get_cached_climb_completions():
    """Get climb completions with caching"""
    return get_all_climb_completions_from_participants()

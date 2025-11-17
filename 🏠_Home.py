import streamlit as st
import folium
from streamlit_folium import st_folium
from utils import init_session_state, get_participant_count, on_this_day_message
from datetime import datetime
import pytz
import random
import os
# Page config
st.set_page_config(
    page_title="Climbsgiving 2025",
    page_icon="🧗",
    layout="wide"
)

# Initialize session state
init_session_state()

if os.path.exists(".maintenance_mode"):
    st.error("Someone broke the app!")
    st.image('assets/logo2.png', width=1000)
    st.write(on_this_day_message())
    st.markdown("""LOOK HOW GOOD I (AI) AM AT CODING""")
    st.code("""def womens_salary(mens_salary):
    return mens_salary * 0.82""")
    st.stop()

# Get current time in EST
est = pytz.timezone('America/New_York')
current_time = datetime.now(est)

logo_choice = random.choice(['assets/logo.jpg', 'assets/logo2.png', 'assets/logo3.jpeg'])
st.logo(logo_choice)
# Title with current time
st.title("🦃 Climbsgiving 2025")
st.markdown("> Funding provided by Curtis Sliwa and the Guardian Angels")
col_date, col_time = st.columns([2, 1])
with col_date:
    st.markdown("**9:00 AM @ Dear Mama (or 9:30 AM @ West Harlem Vital) | November 22, 2025 | New York City, NY**")
with col_time:
    st.markdown(f"**🕐 Current Time: {current_time.strftime('%I:%M %p EST')}**")

st.image('assets/IMG_7132.jpg', width=300)
# Event Details Page
st.header("Event Details")

st.markdown("""
### Climbsgiving (United States)

Climbsgiving is an annual holiday celebrated by climbers primarily residing in the Upper East Side (UES) of Manhattan in New York City, New York, USA. Its first occurrence was Nov 22, 2025. The original idea was proposed by local UES residents while camping in Rumney, New Hampshire after a day of climbing only 5.9s at Rattlesnake Mountain. Despite only climbing 5.9s, which to some of the UES group consider “not real climbing”, the residents were determined to “climb” again together before the holiday season. 

### History
On September 20, 2025, the initial plans for Climbsgiving were first conceived while grasping for conversation topics to avoid going to bed at 8 PM during the trip to Rumney, New Hampshire. Iris Parke, a climber and hiker, first suggested that the group should all get together for a “crawl” of sorts. Many ideas were proposed, including but not limited to, biking or running to various locations throughout New York City. Austin Baggetta, who is better known as Catlord5 and the leader of the United Clan of ROBLOX and an Eagle Scout, suggested that a focused event, perhaps around climbing, would draw more interest from their acquaintances (not really friends) back in New York City. The group generally agreed on the concept. Some people within the group doubted that other members could plan such an event. However, as one can see, “Climbsgiving” was planned.
""")

# Define locations with coordinates and times
climbing_locations = [
    {"name": "1. West Harlem Vital", "address": "3225 Broadway, New York, NY 10027", 
     "lat": 40.8175, "lon": -73.9586, "type": "climbing", "icon": "🧗", "time": "9:30 AM"},
    {"name": "2. Upper East Side Vital", "address": "1506 Lexington Ave, New York, NY 10029", 
     "lat": 40.7856, "lon": -73.9514, "type": "climbing", "icon": "🧗", "time": "11:00 AM"},
    {"name": "3. Lower East Side Vital", "address": "182 Broome St, New York, NY 10002", 
     "lat": 40.7178, "lon": -73.9903, "type": "climbing", "icon": "🧗", "time": "1:00 PM"},
    {"name": "4. Brooklyn Vital", "address": "221 N 14th St, Brooklyn, NY 11249", 
     "lat": 40.7192, "lon": -73.9573, "type": "climbing", "icon": "🧗", "time": "2:30 PM"}
]

food_locations = [
    {"name": "Dear Mama", "address": "611 W 129th St, New York, NY 10027", 
     "lat": 40.8161, "lon": -73.9588, "type": "food", "icon": "🍽️", "time": "9:00 AM"},
    {"name": "Bo's Bagels", "address": "235 W 116th St, New York, NY 10026", 
     "lat": 40.8051, "lon": -73.9547, "type": "food", "icon": "🥯"},
    {"name": "Unregular Pizza", "address": "88 Essex St, New York, NY 10002", 
     "lat": 40.7182, "lon": -73.9877, "type": "food", "icon": "🍕"},
    {"name": "Talea Beer Co", "address": "87 Richardson St, Brooklyn, NY 11211", 
     "lat": 40.7147, "lon": -73.9580, "type": "food", "icon": "🍺"},
    {"name": "Blinky's", "address": "609 Grand St, Brooklyn, NY 11211", 
     "lat": 40.7129, "lon": -73.9438, "type": "food", "icon": "🍻"}
]

all_locations = climbing_locations + food_locations

# Create map centered on NYC
st.markdown("""
### Proposed Locations
""")

m = folium.Map(location=[40.760475, -73.900183], zoom_start=12)
# Add climbing locations with times
for loc in climbing_locations:
    popup_html = f"<b>{loc['name']}</b><br>{loc['address']}<br><b>⏰ Arrival: {loc['time']}</b>"
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=popup_html,
        tooltip=f"{loc['name']} - {loc['time']}",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Add food locations
for loc in food_locations:
    popup_html = f"<b>{loc['name']}</b><br>{loc['address']}"
    if "time" in loc:
        popup_html += f"<br><b>⏰ {loc['time']}</b>"
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=popup_html,
        tooltip=loc["name"],
        icon=folium.Icon(color="green", icon="cutlery", prefix='fa')
    ).add_to(m)


# Display map
st_folium(m, width=1400, height=500)

st.markdown("**Legend:** 🔴 Climbing Gyms | 🟢 Food/Drink")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧗 Climbing Locations")
    locations = [
        "1. West Harlem Vital - 3225 Broadway @ **9:30 AM**",
        "2. Upper East Side Vital - 1506 Lexington Ave @ **11:00 AM**",
        "3. Lower East Side Vital - 182 Broome St @ **1:00 PM**",
        "4. Brooklyn Vital - 221 N 14th St, Brooklyn @ **2:30 PM**"
    ]
    for loc in locations:
        st.markdown(f"- {loc}")

with col2:
    st.subheader("🥔 Food/Drink Stops")
    food_stops = [
        "1. Dear Mama (before loc 1) - 611 W 129th St @ **9:00 AM**",
        "2. Bo's Bagels (after loc 1) - 235 W 116th St",
        "3. Unregular Pizza (before/after loc 3) - 88 Essex St",
        "4. Talea Beer Co - 87 Richardson St, Brooklyn OR Blinky's - 609 Grand St, Brooklyn"
    ]
    for stop in food_stops:
        st.markdown(f"- {stop}")

st.subheader("🚔 Transport")
st.markdown("""
- Food stop (1) → Climbing (1): **Walk**
- Climbing (1) → Climbing (2): **M4 Bus** or bike (pick up Bo's bagels)
- Climbing (2) → Climbing (3): **6 to F subway**
- Climbing (3) → Climbing (4): **Bike**
""")

st.subheader("🥛 Challenges at Each Location")

with st.expander("Locations 1 & 2: West Harlem & Upper East Side Vital"):
    st.markdown("""
    Complete the following climbs (V3-V8):
    - **1x V8** 
    - **2x V7**
    - **3x V6**
    - **4x V5**
    - **5x V4**
    - **8x V3**
    
    *If a climb cannot be completed, just do every move or maybe go for a hike and that could count too*
    """)

with st.expander("Location 3: Lower East Side Vital"):
    st.markdown("""
    - Each person chooses **one climb**
    - **Everyone must attempt that climb** and help others
    - Work through every move, even if you can't complete it
    - Choose kindly or be mean!
    """)

with st.expander("Location 4: Brooklyn Vital"):
    st.markdown("""
    - Head to the **roof** (weather permitting)
    - No strict requirements... but Jason will make you feel bad if you don't climb at least one red
    """)
# Footer
st.sidebar.markdown("---")
st.sidebar.metric("Total Climbers", get_participant_count())

#st.image('assets/acquaintance.jpeg')
#st.markdown("![Alt Text](https://media1.tenor.com/m/qTaIAACZ9BsAAAAC/gas-gas-pumper.gif)")
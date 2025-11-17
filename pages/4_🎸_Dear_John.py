import streamlit as st, time
from utils import on_this_day_message
import random
import os
import base64
from google import genai

client = genai.Client(api_key=st.secrets["gemini"]["GOOGLE_API_KEY"])

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true" loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

autoplay_audio("assets/dear_john.mp3")

st.set_page_config(
    page_title="🎸 Dear John",
    page_icon="🎸",
    layout="wide"
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

dear_john_lyrics = """
Long were the nights when
My days once revolved around you
Counting my footsteps
Praying the floor won't fall through again
And my mother accused me of losing my mind
But I swore I was fine
You paint me a blue sky
Then go back and turn it to rain
And I lived in your chess game
But you changed the rules everyday
Wondering which version of you I might get on the phone tonight
Well, I stopped pickin' up and this song is to let you know why

Dear John, I see it all now that you're gone
Don't you think I was too young to be messed with?
The girl in the dress cried the whole way home
I should've known

Well, maybe it's me
And my blind optimism to blame
Or maybe it's you and your sick need
To give love and take it away
And you'll add my name to your long list of traitors
Who don't understand
And I look back in regret how I ignored when they said
"Run as fast as you can"

Dear John, I see it all now that you're gone
Don't you think I was too young to be messed with?
The girl in the dress cried the whole way home
Dear John, I see it all now, it was wrong
Don't you think nineteen's too young
To be played by your dark, twisted games when I loved you so?
I should've known


You are an expert at sorry and keeping lines blurry
Never impressed by me acing your tests
All the girls that you've run dry have tired lifeless eyes
'Cause you burned them out
But I took your matches before fire could catch me
So don't look now
I'm shining like fireworks over your sad empty town
Oh, oh


Dear John, I see it all now that you're gone
Don't you think I was too young to be messed with?
The girl in the dress cried the whole way home
I see it all now that you're gone
Don't you think I was too young to be messed with?
The girl in the dress wrote you a song
You should've known

You should've known
Don't you think I was too young?
You should've known
"""

dear_john_ai = """
Long were the mornings when
I'd see you out on the bike lanes
You'd climb the walls, you'd never stop,
But you'd roll your eyes at tech in the shop
And your friends all laughed, saying “John's lost his mind”
But I swear you were fine
You'd send me the skyline,
Then turn away when I brought up AI
You say you're a purist, you won't be swayed
And I wonder which John I'll get today
Are you free soloing? Or back to the grind?
So I stopped calling, and now I'm writing this rhyme

Dear John, I see it all now that you're gone
Don't you think it's too much to pretend like you don't care?
Micha's still a jerk, and your climbing's elite
But it's like you're stuck in some old-world retreat

Well, maybe it's me
And my trust in the future to blame
Or maybe it's you and your climb-your-own-way
You push through the streets but you never change
And I'm on your list of things you don't understand
While I try to respect you, there's no common ground
You hate on AI, and I know it's profound
But we can't all just pretend the world's standing still
When you ride your bike through the city up the hill

Dear John, I see it all now that you're gone
Don't you think it's too much to pretend like you don't care?
Micha's still a jerk, your bike's still your ride
But your view on tech's way too fried
I should've known

You're an expert at keeping things tough
Ignoring progress and acting rough
All the times you've dodged what's new
Has left you a little bit through
But I won't fight the future, I won't be burned
While you're too busy with your chalk-stained hands
So don't look now
I'm climbing higher, free as the sky
While you're stuck at the base of your old-world climb

Dear John, I see it all now that you're gone
Don't you think it's too much to pretend like you don't care?
Micha's still a jerk, your climbing's elite
But you're missing out, stuck in some obsolete beat
I should've known

You should've known
That you can't stay in the past
You should've known
Technology's moving too fast
You should've known
"""

# Create placeholders for each column
col1, col2 = st.columns([1, 1])
placeholder1 = col1.empty()
placeholder2 = col2.empty()
placeholder3 = col1.empty()
placeholder4 = col2.empty()

def get_new_response(dear_john_lyrics):
    try:
        response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=st.secrets['prompt']['dear_john_prompt'] + dear_john_lyrics,
            ).text
        return response
    except:
        return dear_john_ai

# Split into words
prev_dear_john_ai_lyrics = dear_john_ai
words1 = dear_john_lyrics.split(" ")
words2 = dear_john_ai.split(" ")

while True:
    # Build text incrementally
    text1 = ""
    text2 = ""
    placeholder1.empty()
    placeholder2.empty()
    placeholder3.markdown(f"![Alt Text](https://raw.githubusercontent.com/benmfox/climbsgiving/refs/heads/main/assets/66DE1C84-604C-44B8-ADB3-990BC4B94202.gif?t={time.time()})")
    placeholder4.markdown(f"![Alt Text](https://raw.githubusercontent.com/benmfox/climbsgiving/refs/heads/main/assets/66DE1C84-604C-44B8-ADB3-990BC4B94202.gif?t={time.time()})")
    time.sleep(4)
    placeholder3.empty()
    placeholder4.empty()
    # Stream both simultaneously by alternating updates
    max_length = max(len(words1), len(words2))
    for i in range(max_length):
        if i == 0:
            text1 += "### Dear John\n"
            text2 += "### ⬅️ Dear John, sincerely chatgpt\n"
            placeholder1.markdown(text1)
            placeholder2.markdown(text2)
        if i < len(words1):
            text1 += words1[i] + " "
            placeholder1.markdown(text1)
        if i < len(words2):
            text2 += words2[i] + " "
            placeholder2.markdown(text2)
        time.sleep(0.09)
    words1 = prev_dear_john_ai_lyrics.split(" ")
    prev_dear_john_ai_lyrics = get_new_response(prev_dear_john_ai_lyrics)
    words2 = prev_dear_john_ai_lyrics.split(" ")
    
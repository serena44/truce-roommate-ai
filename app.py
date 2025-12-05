import streamlit as st
from datetime import datetime
import random
import uuid
import traceback


# Configuration & Defaults
INITIAL_MOCK_USER_ID = "user_123"
PROFILE_IMAGE_OPTIONS = {
    "Blue A": "https://placehold.co/100x100/1E3A8A/FFFFFF?text=A",
    "Red B": "https://placehold.co/100x100/B91C1C/FFFFFF?text=B",
    "Green C": "https://placehold.co/100x100/065F46/FFFFFF?text=C",
    "Purple D": "https://placehold.co/100x100/7E22CE/FFFFFF?text=D",
}

# SESSION STATE INIT
if 'profiles' not in st.session_state:
    st.session_state.profiles = {
        INITIAL_MOCK_USER_ID: {"name": "Alex", "vibe_score": 4, "img_url": PROFILE_IMAGE_OPTIONS["Blue A"], "email": "alex@home.com"},
        "roomie_A": {"name": "Jordan", "vibe_score": 3, "img_url": PROFILE_IMAGE_OPTIONS["Red B"], "email": "jordan@home.com"},
        "roomie_B": {"name": "Taylor", "vibe_score": 5, "img_url": PROFILE_IMAGE_OPTIONS["Green C"], "email": "taylor@home.com"}
    }

if 'chores' not in st.session_state:
    st.session_state.chores = [
        "Clean Kitchen Counters",
        "Empty Dishwasher",
        "Vacuum Living Room",
        "Take out Trash & Recycling",
        "Wipe Down Bathroom Sink",
        "Clean Toilet",
        "Sweep Kitchen Floor",
        "Water House Plants"
    ]

if 'apt_name_input' not in st.session_state:
    st.session_state.apt_name_input = "Apt 14"

if 'hub_code' not in st.session_state:
    st.session_state.hub_code = str(random.randint(1000, 9999))

if 'chore_history' not in st.session_state:
    st.session_state.chore_history = {name: 0 for name in [p['name'] for p in st.session_state.profiles.values()]}

# ANNOUNCEMENTS
if 'announcements' not in st.session_state:
    st.session_state.announcements = [{
        "id": str(uuid.uuid4()),
        "text": "Welcome to your Roomi Hub! Post your first important announcement here.",
        "author": "Roomi Admin",
        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "urgent": False,
        "pinned": True
    }]

# FEEDBACK
if 'feedback' not in st.session_state:
    st.session_state.feedback = []

# CURRENT USER
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True
if 'current_active_user_id' not in st.session_state:
    st.session_state.current_active_user_id = INITIAL_MOCK_USER_ID

# User session init
def initialize_user_session_data(user_id):
    profile = st.session_state.profiles.get(user_id, {})
    st.session_state.current_user_name = profile.get('name', 'New User')
    st.session_state.current_user_vibe = profile.get('vibe_score', 3)
    st.session_state.current_user_img_url = profile.get('img_url', list(PROFILE_IMAGE_OPTIONS.values())[0])
initialize_user_session_data(st.session_state.current_active_user_id)

if "page" not in st.session_state:
    st.session_state.page = "Home"

# UI HELPERS
def get_vibe_style(score):
    if score >= 4.5:
        return {"color": "#16A34A", "emoji": "😄"}
    elif score >= 3.5:
        return {"color": "#FBBF24", "emoji": "🙂"}
    elif score >= 2.5:
        return {"color": "#F97316", "emoji": "😐"}
    else:
        return {"color": "#DC2626", "emoji": "😟"}

def generate_chore_schedule(profiles, chores):
    names = [p['name'] for p in profiles.values()]
    history = st.session_state.chore_history
    sorted_names = sorted(names, key=lambda name: history.get(name, 0))
    week_number = datetime.now().isocalendar()[1]
    random.seed(week_number)
    random.shuffle(chores)
    schedule = {name: [] for name in names}
    new_counts = {name: 0 for name in names}
    for i, chore in enumerate(chores):
        person = sorted_names[i % len(sorted_names)]
        schedule[person].append(chore)
        new_counts[person] += 1
    st.session_state.chore_history = new_counts
    return schedule

def sign_out():
    for k in ['current_user_name', 'current_user_vibe', 'current_user_img_url']:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state.logged_in = False
    st.session_state.page = "Home"
    st.rerun()

#PAGE DISPLAY
st.markdown("""
<style>
.profile-pic { border-radius: 50%; object-fit: cover; border: 3px solid #F97316; }
.vibe-box { padding: 15px; background-color: #F3F4F6; border-radius: 10px; text-align: center; margin-top: 20px; }
.chore-list { list-style: none; padding-left: 0; }
.chore-list li { background-color: #FEF3C7; margin-bottom: 8px; padding: 10px; border-radius: 6px;
                 border-left: 5px solid #EA580C; color: #000; display:flex; align-items:center;}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.markdown("<div style='padding-top:10px;text-align:center;'><h1 style='color:#ebc334;font-size:48px;margin:0;'>Roomi</h1></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Profile"):
    st.session_state.page = "Profile"
if st.sidebar.button("Settings"):
    st.session_state.page = "Settings"
st.sidebar.markdown("---")
st.sidebar.write(f"Logged in as: **{st.session_state.current_user_name}**")
st.sidebar.write(f"Hub code: **{st.session_state.hub_code}**")
st.sidebar.markdown("---")

#MAIN PAGES
CURRENT_USER_ID = st.session_state.current_active_user_id

if not st.session_state.logged_in:
    st.title("Welcome — Join a Roomi Hub")
    st.write("This app expects a logged-in state for the demo. Set `logged_in` to True in session_state to continue.")
    st.stop()

# HOME PAGE
if st.session_state.page == "Home":
    st.header(st.session_state.apt_name_input)
    st.markdown("---")

    # Profile + Roommates
    col_profile, col_roomies = st.columns([1, 2])
    with col_profile:
        st.markdown(f"<div style='text-align:center;'>"
                    f"<img src='{st.session_state.current_user_img_url}' class='profile-pic' style='width:100px;height:100px;'>"
                    f"<h3 style='margin-top:10px;color:#5B21B6'>{st.session_state.current_user_name}</h3>"
                    f"</div>", unsafe_allow_html=True)
    with col_roomies:
        roommate_keys = [k for k in st.session_state.profiles if k != CURRENT_USER_ID]
        st.subheader(f"Roommates ({len(roommate_keys)})")
        cols = st.columns(max(1, len(roommate_keys)))
        for i, rk in enumerate(roommate_keys):
            prof = st.session_state.profiles[rk]
            with cols[i]:
                st.markdown(f"<div style='text-align:center;'>"
                            f"<img src='{prof['img_url']}' class='profile-pic' style='width:50px;height:50px;border:2px solid #9CA3AF;'>"
                            f"<p style='font-size:12px;margin-top:6px'>{prof['name']}</p>"
                            f"</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ANNOUNCEMENTS 
    st.subheader("Announcements")

    with st.expander("Post Announcement"):
        announcement_input = st.text_area("Write announcement:", key="announcement_input")
        urgent_flag = st.checkbox("Mark as urgent", key="announcement_urgent_checkbox")

        if st.button("Submit Announcement"):
            if announcement_input.strip():
                try:
                    st.session_state.announcements.insert(0, {
                        "id": str(uuid.uuid4()),
                        "text": announcement_input.strip(),
                        "author": st.session_state.current_user_name,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                        "urgent": urgent_flag
                    })
                    st.success("Announcement posted successfully!")
                    st.session_state.announcement_input = ""
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to post announcement: {e}")
            else:
                st.warning("Please write an announcement before submitting.")

    with st.expander("Open Announcements"):
        for ann in st.session_state.announcements:
            prefix = "[URGENT] " if ann['urgent'] else ""
            st.markdown(f"**{prefix}{ann['text']}**  \n*— {ann['author']}, {ann['timestamp']}*")
            st.markdown("---")
    # FEEDBACK (WRITE + VIEW — with AI neutralizer)
    
    from google import genai
    
    # Initialize Gemini client 
    if "gemini_ready" not in st.session_state:
        try:
            st.session_state.gemini_client = genai.Client()
            st.session_state.gemini_ready = True
        except:
            st.session_state.gemini_ready = False
    
    def rephrase_feedback(text):
        """Makes feedback neutral & constructive when needed."""
        prompt = f"""
        You are a conflict-resolution assistant. 
        Rephrase the following feedback into:
        - neutral
        - concise
        - constructive  
        ONLY rewrite it if it is hostile, rude, or aggressive.
        If the message is already neutral: return it unchanged but improve clarity.
    
        Original: "{text}"
        """
    
        if not st.session_state.gemini_ready:
            return text  # fallback if Gemini is not available
    
        try:
            resp = st.session_state.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            cleaned = resp.text.strip()
            return cleaned if cleaned else text
        except:
            return text


    st.markdown("---")
    st.subheader("Feedback")

    # WRITE FEEDBACK WITH AI REWORDING
    with st.expander("Write Feedback"):
        fb_input = st.text_area(
            "Share feedback:",
            key="fb_text_input",
            value=st.session_state.get("fb_draft", "")
        )
    
        fb_anonymous = st.checkbox("Submit anonymously")
    
        if st.button("Submit Feedback"):
            if fb_input.strip():
    
                # AI reword it BEFORE storing
                final_text = rephrase_feedback(fb_input.strip())
    
                st.session_state.feedback.insert(0, {
                    "id": str(uuid.uuid4()),
                    "text": final_text,
                    "author": "Anonymous" if fb_anonymous else st.session_state.current_user_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p")
                })
    
                st.success("Feedback submitted!")
    
                # reset draft text only (NOT the widget key!)
                st.session_state.fb_draft = ""
    
                st.rerun()
            else:
                st.warning("Please write feedback before submitting.")

    # VIEW FEEDBACK
    with st.expander("View Feedback"):
        if not st.session_state.feedback:
            st.info("No feedback yet.")
        else:
            for fb in st.session_state.feedback:
                st.markdown(f"**{fb['text']}**  \n*— {fb['author']}, {fb['timestamp']}*")
                st.markdown("---")

    # VIBE TRACKER
    dashboard_vibe_average = round(sum(p['vibe_score'] for p in st.session_state.profiles.values()) / len(st.session_state.profiles), 1)
    vibe_style = get_vibe_style(dashboard_vibe_average)
    col_vibe, col_check_in = st.columns(2)
    with col_vibe:
        st.markdown(f"<div class='vibe-box'><p style='font-size:18px;color:#4B5563;'>Overall Vibe in Hub:</p>"
                    f"<h2 style='font-size:36px;color:{vibe_style['color']};margin:0;'>{vibe_style['emoji']} {dashboard_vibe_average}/5.0</h2></div>", unsafe_allow_html=True)
    with col_check_in:
        with st.form("vibe_check_in_form"):
            new_vibe_score = st.slider("How satisfied are you with the hub this week?", min_value=1, max_value=5, value=st.session_state.current_user_vibe)
            if st.form_submit_button("Report My Vibe Score"):
                st.session_state.current_user_vibe = new_vibe_score
                st.session_state.profiles[CURRENT_USER_ID]['vibe_score'] = new_vibe_score
                st.success(f"Vibe Score ({new_vibe_score}/5) reported successfully!")
                st.rerun()

    st.markdown("---")

    # CHORE SCHEDULE
    st.subheader("Weekly Chore Schedule")
    curr_schedule = generate_chore_schedule(st.session_state.profiles, st.session_state.chores)
    schedule_cols = st.columns(len(curr_schedule))
    for i, (name, chores) in enumerate(curr_schedule.items()):
        with schedule_cols[i]:
            st.markdown(f"**{name}**")
            chore_html = "".join([f'<li>{c}</li>' for c in chores])
            st.markdown(f"<ul class='chore-list'>{chore_html}</ul>", unsafe_allow_html=True)
    st.info("The chore schedule updates every Monday.", icon="ℹ️")

# PROFILE PAGE
elif st.session_state.page == "Profile":
    st.header("Your Profile")
    st.markdown("Edit display name and view avatar.")
    st.image(st.session_state.current_user_img_url, width=100)
    with st.form("profile_form", clear_on_submit=False):
        new_name = st.text_input("Your Display Name", value=st.session_state.current_user_name)
        if st.form_submit_button("Save Profile Changes"):
            st.session_state.current_user_name = new_name
            st.session_state.profiles[CURRENT_USER_ID]['name'] = new_name
            st.success("Profile updated successfully!")
            st.rerun()

# SETTINGS PAGE
elif st.session_state.page == "Settings":
    st.header("Settings")

    # Apartment Name
    st.subheader("Apartment Name")
    new_apt_name = st.text_input("Apartment Name", value=st.session_state.apt_name_input)
    if st.button("Update Apartment Name"):
        st.session_state.apt_name_input = new_apt_name
        st.success("Apartment Name updated!")
        st.rerun()

    st.subheader("Hub Code")
    st.markdown(f"""<div style="background-color:#ECFDF5;padding:12px;border-radius:8px;border:2px dashed #059669;text-align:center;">
                    <p style="margin:0;font-size:14px;color:#059669;">Your Shared Hub Code</p>
                    <h1 style="margin:6px 0 0 0;font-size:48px;color:#064E3B;font-weight:bold;font-family:monospace;">{st.session_state.hub_code}</h1>
                    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("Manage Chore List")
    current_chores_text = "\n".join(st.session_state.chores)
    new_chores_text = st.text_area("Edit Chore List (one chore per line):", value=current_chores_text, height=200)
    if st.button("Update Chore List"):
        updated_chores = [c.strip() for c in new_chores_text.split('\n') if c.strip()]
        if updated_chores:
            st.session_state.chores = updated_chores
            st.success("Chore list updated!")
            st.rerun()
        else:
            st.error("Chore list cannot be empty.")

    st.markdown("---")
    st.subheader("Account & Logout")
    st.markdown("Securely sign out from here.")
    if st.button("Sign Out of Roomi Hub"):
        sign_out()
        st.success("Signed out.")

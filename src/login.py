# login.py
import streamlit as st
import base64
import os
from utils import login_user

# -------------------------------------------------
# Set background image with premium glass overlays
# -------------------------------------------------
def set_background(image_path):
    if not os.path.exists(image_path):
        st.error(f"Image not found: {image_path}")
        return

    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
        <style>
        /* Cyberpunk Ambient Neon Shaded Matrix */
        .stApp {{
            background-image: linear-gradient(rgba(9, 13, 22, 0.75), rgba(2, 4, 8, 0.9)), url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #e2e8f0 !important;
        }}

        /* Center container: Cyberpunk Bento Shading */
        .center-box {{
            width: 320px;
            margin: 0 auto;
            margin-top: 40px;
            padding: 30px;
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(0, 242, 254, 0.2);
            border-radius: 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 0 30px rgba(0, 242, 254, 0.15);
        }}

        /* Luminous Glowing Title */
        .title {{
            text-align: center;
            font-size: 46px;
            font-weight: 900;
            background: linear-gradient(90deg, #00e676, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 25px rgba(0, 230, 118, 0.35);
            margin-top: 50px;
            letter-spacing: -1px;
        }}

        /* OR separator text */
        .or-text {{
            text-align: center;
            font-size: 16px;
            font-weight: 800;
            margin-top: 25px;
            color: #64748b;
            letter-spacing: 3px;
        }}

        /* Telegram button: Luminous Neon Crimson styling */
        .telegram-btn {{
            display: block;
            width: 100%;
            max-width: 340px;
            margin: 20px auto;
            background: linear-gradient(90deg, #ff1744, #d50000);
            padding: 14px;
            border-radius: 12px;
            text-align: center;
            color: white !important;
            font-size: 16px;
            font-weight: bold;
            text-decoration: none;
            box-shadow: 0 4px 15px rgba(255,23,68,0.4);
            transition: all 0.3s ease;
            letter-spacing: 0.5px;
        }}
        .telegram-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 0 25px rgba(255,23,68,0.65);
        }}

        /* Transparent Cyber Input Field Overrides */
        div[data-baseweb="input"] > div {{
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
        }}
        div[data-baseweb="input"] input {{
            color: #ffffff !important;
            font-size: 15px !important;
        }}
        div[data-baseweb="input"] > div:focus-within {{
            border-color: #00f2fe !important;
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.3) !important;
        }}
        label p {{
            color: #94a3b8 !important;
            font-weight: 600 !important;
        }}
        </style>
    """, unsafe_allow_html=True)


# -------------------------------------------------
# LOGIN PAGE UI
# -------------------------------------------------
def login_page():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "backgrounds", "bg4.jpg")
    set_background(image_path)

    # Luminous Header Title Matrix
    st.markdown("<div class='title'>🌴 Coconut Disease Detection</div>", unsafe_allow_html=True)

    # Login Container Box
    with st.container():
        st.markdown("<div class='center-box'>", unsafe_allow_html=True)

        username = st.text_input("👤 Username", key="user")
        password = st.text_input("🔒 Password", type="password", key="pass")
        
        # 2026 REPLACEMENT STANDARD: Configured with native width parameters
        login_btn = st.button("Sign In Framework", width='stretch')

        st.markdown("</div>", unsafe_allow_html=True)

    # Login Authentication Logic Pipeline
    if login_btn:
        if username == "admin" and password == "admin":
            login_user(username)
            st.query_params.update({"page": "home"})
            st.rerun()
        else:
            st.error("Invalid corporate credentials entered.")

    # OR Break Pane
    st.markdown("<div class='or-text'>— OR —</div>", unsafe_allow_html=True)

    # Isolated System Environment Token Loading
    TELEGRAM_LINK = st.secrets["telegram"]["BOT_USER_LINK"]
    st.markdown(
        f"<a class='telegram-btn' href='{TELEGRAM_LINK}' target='_blank'>🚀 Open Telegram Instant Coconut Doctor</a>",
        unsafe_allow_html=True,
    )
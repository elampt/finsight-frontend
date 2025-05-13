import streamlit as st
from services.api import login_user, signup_user
from custom_pages.holdings import holdings_page
from custom_pages.sentiment import sentiment_page

# Set the page configuration
st.set_page_config(
    page_title="FinSight",  # Title of the browser tab
    page_icon="logo.png",  # Path to your favicon file
    layout="centered",         # Optional: Set layout to wide
)


# Initialize sesssion state for token
if "token" not in st.session_state:
    st.session_state.token = None

# Home Page
def home():
    st.title("🌟 Welcome to FinSight")
    st.markdown(
        """
        ### Your personal financial insights platform 💡
        **Gain valuable insights into your portfolio, track market sentiment, and make informed decisions**
        """
    )

    # Login or Signup options
    st.markdown("### Get Started")
    option = st.radio(
        "Choose an option:",
        ["🔑 Login", "📝 Signup"],
        label_visibility="collapsed"
    )

    if option == "📝 Signup":
        signup()
    elif option == "🔑 Login":
        login()

# Signup Page
def signup():
    st.subheader("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        response = signup_user(name, email, password)
        if response:
            st.success("Sign up successful! Please log in.")
        else:
            st.error("Sign up failed. Please try again.")

# Login Page
def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        token = login_user(email, password)
        if token:
            st.session_state.token = token
            st.session_state.user_email = email  # Store user email in session state
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")

# Logout Button
def logout():
    if st.button("Log Out"):
        st.session_state.token = None
        st.rerun()

# Main App Logic
if st.session_state.token:
    # Sidebar Enhancements
    st.sidebar.image("logo.png", use_container_width=True)  # Add a logo or placeholder image
    st.sidebar.title("📊 FinSight Dashboard")
    st.sidebar.markdown("---")

    # Sidebar Navigation
    st.sidebar.subheader("📂 Navigate to:")
    page = st.sidebar.radio("Pages", ["🏠 Holdings", "📰 News Sentiment"], label_visibility="collapsed")

    st.sidebar.markdown("---")


    # User Information
    st.sidebar.markdown("**Logged in as:**")
    st.sidebar.markdown(f"👤 **User:** {st.session_state.get('user_email', 'Unknown')}")  # Replace with actual user info if available
    st.sidebar.markdown("---")


    # Logout Button
    if st.sidebar.button("🚪 Log Out"):
        st.session_state.token = None
        st.session_state.user_email = None
        st.rerun()

    if page == "🏠 Holdings":
        holdings_page()
    elif page == "📰 News Sentiment":
        sentiment_page()

else:
    # Show home page if not logged in
    home()

import streamlit as st
import datetime
import requests

# Suppose you have your actual API key stored somewhere
OPENWEATHER_API_KEY = "32cea45226c067e85ada1ce66773d070"

def get_weather(city: str, api_key: str) -> str:
    """
    Fetches current weather for the specified city using OpenWeatherMap.
    Returns a string like 'Clouds | 23°C' or an error message.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        resp = requests.get(base_url, params=params, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            desc = data["weather"][0]["main"] 
            temp = data["main"]["temp"]           
            return f"{desc} | {temp:.0f}°C"
        else:
            return "Weather Unavailable"
    except Exception:
        return "Weather Error"

def show_top_header():
    # -- Inline CSS to style the header --
    st.markdown(
        """
        <style>
        .top-header-container {
            background-color: #2B547E;  /* A darker blue background */
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .header-text {
            color: #ffffff;            /* White text for readability */
            font-size: 1rem;
            font-weight: 500;
            margin: 0.2rem 0;
        }
        /* Style the Streamlit buttons within the header */
        .stButton button {
            background-color: #ffffff !important; 
            color: #2B547E !important;
            border: none !important;
            padding: 0.45rem 0.8rem !important;
            border-radius: 4px !important;
            margin: 0.4rem !important;
            cursor: pointer !important;
            font-weight: 600 !important;
        }
        .stButton button:hover {
            background-color: #1d3c57 !important;
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Gather dynamic info
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    city_name = "Ankara"
    weather_data = get_weather(city_name, OPENWEATHER_API_KEY)

    # Create the top header container
    st.markdown("<div class='top-header-container'>", unsafe_allow_html=True)

    # Two main columns: left for info, right for buttons
    col_left, col_right = st.columns([7,3])  # Adjust the ratio if needed

    with col_left:
        st.markdown(f"<div class='header-text'>Developed by: Ilyas Nayle</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='header-text'>Time: {now_str}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='header-text'>City: {city_name}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='header-text'>Weather: {weather_data}</div>", unsafe_allow_html=True)

    with col_right:
        # Create two columns for side-by-side buttons
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Login"):
                st.info("Login not implemented yet.")
        with c2:
            if st.button("Sign Up"):
                st.info("Sign Up not implemented yet.")

    st.markdown("</div>", unsafe_allow_html=True)  # Close the container

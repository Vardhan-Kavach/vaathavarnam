import streamlit as st
import requests

# Setting the OpenWeatherMap API key
WEATHER_API_KEY = 'c072be6082a637189669ea81ea570824'

st.set_page_config(page_title="Precise Weather & AQI Tracker", page_icon="🌎", layout="centered")
st.title("🌎 Precise Weather & Air Quality Tracker for Locations")
st.markdown("Select your **Country → State → City/District** to get real-time **Weather** and **Air Quality** information! 🌟")

# Countries List (expandable)
countries_list = ["India", "United States", "Australia"]

# Select Country
country = st.selectbox("Select Country", countries_list)

state = None
city = None

def get_states_of_country(country_name):
    url = "https://countriesnow.space/api/v0.1/countries/states"
    payload = {"country": country_name}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        states = [state["name"] for state in data["data"]["states"]]
        return states
    return []

def get_cities_of_state(country_name, state_name):
    url = "https://countriesnow.space/api/v0.1/countries/state/cities"
    payload = {"country": country_name, "state": state_name}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        cities = data["data"]
        return cities
    return []

# Fetch states dynamically
if country:
    states = get_states_of_country(country)
    state = st.selectbox("Select State", states) if states else None

# Fetch cities/districts dynamically
if state:
    cities = get_cities_of_state(country, state)
    city = st.selectbox("Select District/City", cities) if cities else None

# Get weather and air quality
def get_weather_and_aqi(city_name):
    try:
        # Get Weather Info
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()

        if weather_data.get('cod') != 200:
            return None  # Location not found

        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']

        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        description = weather_data['weather'][0]['description'].title()

        # Get Air Quality Info
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
        aqi_data = requests.get(aqi_url).json()

        aqi = aqi_data['list'][0]['main']['aqi']
        components = aqi_data['list'][0]['components']

        pm2_5 = components['pm2_5']
        pm10 = components['pm10']
        no2 = components['no2']
        o3 = components['o3']

        return {
            "temp": temp,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "description": description,
            "aqi": aqi,
            "pm2_5": pm2_5,
            "pm10": pm10,
            "no2": no2,
            "o3": o3
        }

    except Exception as e:
        print(e)
        return None

# Human understandable AQI interpretation
def interpret_aqi_detailed(aqi_value):
    if aqi_value == 1:
        return "🟢 Good — Excellent air quality! Enjoy your day outside. 🌳"
    elif aqi_value == 2:
        return "🟡 Fair — Acceptable air quality. Sensitive individuals should take care. 🚶"
    elif aqi_value == 3:
        return "🟠 Moderate — Air is somewhat polluted. Elderly, kids should be careful. 😐"
    elif aqi_value == 4:
        return "🔴 Poor — Unhealthy air. Limit outdoor activities, use masks if needed. 😷"
    elif aqi_value == 5:
        return "🟣 Very Poor — Hazardous! Stay indoors, use air purifiers. ⚠️"
    else:
        return "⚪ Unknown — Data unavailable."

# Button to get weather and AQI
if st.button("Get Weather and AQI Info"):
    if city:
        result = get_weather_and_aqi(city)
        if result:
            st.success(f"📍 Location: {city}, {state}, {country}")
            st.write(f"🌡 Temperature: {result['temp']} °C")
            st.write(f"💧 Humidity: {result['humidity']}%")
            st.write(f"🔵 Pressure: {result['pressure']} hPa")
            st.write(f"☁️ Weather: {result['description']}")
            st.write(f"🌬 Wind Speed: {result['wind_speed']} m/s")

            st.markdown("---")
            st.subheader("🧪 Air Quality Details")
            st.write(f"**AQI Level:** {result['aqi']}")
            st.info(interpret_aqi_detailed(result['aqi']))
            st.write(f"🫧 PM2.5 (fine dust): {result['pm2_5']} μg/m³ ➔ *Fine particles harmful for lungs*")
            st.write(f"🫧 PM10 (coarse dust): {result['pm10']} μg/m³ ➔ *Larger dust particles, cause breathing irritation*")
            st.write(f"🧪 NO₂ (Nitrogen Dioxide): {result['no2']} μg/m³ ➔ *Pollutant from traffic and factories*")
            st.write(f"🧪 O₃ (Ozone): {result['o3']} μg/m³ ➔ *Good at high altitudes, bad at ground level*")
        else:
            st.error("❌ Weather or Air Quality data unavailable for this location. Please try another city/district!")
    else:
        st.warning("⚠️ Please complete selection first (Country → State → City/District).")

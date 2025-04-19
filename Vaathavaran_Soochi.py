# import streamlit as st
# import requests

# # My OpenWeatherMap API key
# API_KEY = 'c072be6082a637189669ea81ea570824'

# st.set_page_config(page_title="Weather & Air Quality Tracker", page_icon="🌏", layout="centered")
# st.title("🌏 Live Weather & Air Quality Tracker for Indian Cities 🇮🇳")
# st.markdown("Get real-time **Weather** and **Air Pollution** information easily!")

# city = st.text_input("Enter City Name (e.g., Delhi, Mumbai, Bangalore):")

# def get_weather_and_aqi(city_name):
#     try:
#         # Getting the Weather Info
#         weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
#         weather_data = requests.get(weather_url).json()

#         lat = weather_data['coord']['lat']
#         lon = weather_data['coord']['lon']

#         temp = weather_data['main']['temp']
#         humidity = weather_data['main']['humidity']
#         pressure = weather_data['main']['pressure']
#         wind_speed = weather_data['wind']['speed']
#         description = weather_data['weather'][0]['description'].title()

#         # Getting the Air Quality Info
#         aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
#         aqi_data = requests.get(aqi_url).json()

#         aqi = aqi_data['list'][0]['main']['aqi']
#         components = aqi_data['list'][0]['components']

#         pm2_5 = components['pm2_5']
#         pm10 = components['pm10']
#         no2 = components['no2']
#         o3 = components['o3']

#         return {
#             "temp": temp,
#             "humidity": humidity,
#             "pressure": pressure,
#             "wind_speed": wind_speed,
#             "description": description,
#             "aqi": aqi,
#             "pm2_5": pm2_5,
#             "pm10": pm10,
#             "no2": no2,
#             "o3": o3
#         }

#     except Exception as e:
#         return None

# def interpret_aqi(aqi_value):
#     mapping = {
#         1: "Good 🙂 - Air quality is ideal for everyone.",
#         2: "Fair 🙂 - Air quality is acceptable.",
#         3: "Moderate 😐 - Sensitive people should limit outdoor activities.",
#         4: "Poor 😷 - Health risks for sensitive groups, avoid heavy outdoor work.",
#         5: "Very Poor 😵 - Health warnings, everyone should reduce outdoor exposure!"
#     }
#     return mapping.get(aqi_value, "Unknown")

# if st.button("Get Weather and AQI Info"):
#     if city:
#         result = get_weather_and_aqi(city)
#         if result:
#             st.success(f"📍 City: {city.title()}")
#             st.write(f"🌡 **Temperature:** {result['temp']} °C")
#             st.write(f"💧 **Humidity:** {result['humidity']}%")
#             st.write(f"🔵 **Pressure:** {result['pressure']} hPa")
#             st.write(f"☁️ **Weather:** {result['description']}")
#             st.write(f"🌬 **Wind Speed:** {result['wind_speed']} m/s")

#             st.markdown("---")
#             st.subheader("🏭 Air Quality Information:")

#             st.write(f"🧪 **Air Quality Index (AQI):** {result['aqi']} ({interpret_aqi(result['aqi'])})")

#             if result['aqi'] == 5:
#                 st.error("🔴 Very Poor AQI! It is advised to stay indoors and use air purifiers if possible.")
#             elif result['aqi'] == 4:
#                 st.warning("🟠 Poor AQI! Sensitive groups should minimize outdoor activities.")
#             elif result['aqi'] == 3:
#                 st.info("🟡 Moderate AQI! People with breathing issues should be cautious.")
#             else:
#                 st.success("🟢 Good/Fair AQI! Air quality is good for everyone.")

#             st.write(f"🫧 **PM2.5:** {result['pm2_5']} μg/m³")
#             st.caption("→ Fine particles causing breathing problems. High PM2.5 is very harmful for lungs.")

#             st.write(f"🫧 **PM10:** {result['pm10']} μg/m³")
#             st.caption("→ Dust and pollen-sized particles. High PM10 can cause coughing and sneezing.")

#             st.write(f"🧪 **Nitrogen Dioxide (NO₂):** {result['no2']} μg/m³")
#             st.caption("→ Gas mainly from vehicles and industries. High NO₂ can irritate lungs and eyes.")

#             st.write(f"🧪 **Ozone (O₃):** {result['o3']} μg/m³")
#             st.caption("→ Harmful gas at ground level. High O₃ can trigger asthma and breathing difficulties.")

#         else:
#             st.error("City not found or API issue! 🚫")
#     else:
#         st.warning("Please enter a city name! 📍")


# Install required libraries:
# pip install streamlit requests

import streamlit as st
import requests

st.set_page_config(page_title="Precise Weather & AQI Tracker", page_icon="🌎", layout="centered")
st.title("🌎 Precise Weather & Air Quality Tracker for Locations")
st.markdown("Select your **Country → State → City/District** to get real-time **Weather** and **Air Quality** information!")

# API Keys
WEATHER_API_KEY = "c072be6082a637189669ea81ea570824"

# Countries List (You can expand manually if you want worldwide)
countries_list = ["India", "United States", "Australia"]

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

def get_weather_and_aqi(city_name):
    try:
        # Get Weather Info
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()

        if weather_data.get('cod') != 200:
            return None

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

def interpret_aqi(aqi_value):
    mapping = {
        1: "Good 🙂",
        2: "Fair 🙂",
        3: "Moderate 😐",
        4: "Poor 😷",
        5: "Very Poor 😵"
    }
    return mapping.get(aqi_value, "Unknown")

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
            st.write(f"**AQI Level:** {result['aqi']} ({interpret_aqi(result['aqi'])})")
            st.write(f"🫧 PM2.5 (fine dust): {result['pm2_5']} μg/m³ ➔ *Tiny particles causing respiratory issues*")
            st.write(f"🫧 PM10 (coarse dust): {result['pm10']} μg/m³ ➔ *Larger dust particles, irritate lungs*")
            st.write(f"🧪 NO₂ (Nitrogen Dioxide): {result['no2']} μg/m³ ➔ *Major pollutant from vehicles*")
            st.write(f"🧪 O₃ (Ozone): {result['o3']} μg/m³ ➔ *Good in upper atmosphere, bad at ground level*")
        else:
            st.error("Location not found or data unavailable!")
    else:
        st.warning("Please complete selection first.")


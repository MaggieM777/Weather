import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 🗝️ Въведи своя API ключ тук
API_KEY = "4ac274aa678b073aa1511d3de8f777cc"
CITY = "Plovdiv"

# 📍 Координати за Пловдив
lat = 42.1354
lon = 24.7453

# 🌦️ URL за прогноза за времето (5 дни)
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

# 🌍 URL за замърсеност на въздуха
AIR_URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

# 🧠 Изтегляне на прогнозни метео данни
def get_weather_data():
    response = requests.get(WEATHER_URL)
    data = response.json()
    weather = []

    for entry in data["list"]:
        date = datetime.fromtimestamp(entry["dt"]).date()
        temp = entry["main"]["temp"]
        rain = entry.get("rain", {}).get("3h", 0)
        humidity = entry["main"]["humidity"]
        weather.append({
            "date": date,
            "temp": temp,
            "rain": rain,
            "humidity": humidity
        })

    df = pd.DataFrame(weather)
    df = df.groupby("date").agg({
        "temp": "mean",
        "rain": "sum",
        "humidity": "mean"
    })
    return df

# 📐 Данни за обичайните стойности за май (пример)
NORMALS = {
    "May": {
        "temp": 17.0,
        "rain_days": 8
    }
}

# 🏭 Замърсеност – извличане на данни
def get_air_quality_data():
    response = requests.get(AIR_URL)
    data = response.json()

    if "list" in data and len(data["list"]) > 0:
        aqi = data["list"][0]["main"]["aqi"]
        components = data["list"][0]["components"]
        return aqi, components
    else:
        return None, None

# 🖥️ Streamlit интерфейс
st.set_page_config("Прогноза и въздух", layout="centered")
st.title(f"🌤️ Времето и замърсеността в {CITY}")

df = get_weather_data()

# 📅 Прогноза по дни
st.subheader("📈 Температури по дни")
st.line_chart(df["temp"])

st.subheader("🌧️ Валежи по дни (в мм)")
st.bar_chart(df["rain"])

# 📊 Анализ
st.subheader("📊 Анализ на времето за месеца")
month = "May"  # фиксирано, може да се направи динамично
avg_temp = df["temp"].mean()
rain_days = (df["rain"] > 0).sum()

st.write(f"📌 Средна температура: **{avg_temp:.1f}°C**")
st.write(f"📌 Дни с валежи: **{rain_days} дни**")

if avg_temp > NORMALS[month]["temp"] + 2:
    st.warning("⚠️ Температурите са по-високи от обичайното за месеца.")
elif avg_temp < NORMALS[month]["temp"] - 2:
    st.warning("⚠️ Температурите са по-ниски от обичайното за месеца.")
else:
    st.success("✅ Температурите са в нормалните граници.")

if rain_days > NORMALS[month]["rain_days"]:
    st.warning("🌧️ Повече дъждовни дни от обичайното.")
else:
    st.success("✅ Валежите са в нормата.")

# 🧪 Качество на въздуха
st.subheader("🧪 Качество на въздуха")
aqi, components = get_air_quality_data()

if aqi:
    aqi_levels = {
        1: "Добро",
        2: "Задоволително",
        3: "Умерено",
        4: "Лошо",
        5: "Много лошо"
    }

    st.markdown(f"**AQI (Air Quality Index):** {aqi} – {aqi_levels[aqi]}")
    st.markdown("**Компоненти (μg/m³):**")
    st.json(components)

    # Визуализация
    fig, ax = plt.subplots()
    ax.bar(components.keys(), components.values(), color='teal')
    ax.set_ylabel("μg/m³")
    ax.set_title("Концентрации на замърсители")
    st.pyplot(fig)
else:
    st.warning("⚠️ Няма налични данни за замърсеността на въздуха.")

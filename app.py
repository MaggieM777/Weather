import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 🗝️ Въведи своя API ключ тук
API_KEY = "4ac274aa678b073aa1511d3de8f777cc"
CITY = "Plovdiv"
LAT = 42.1354   # ширина за Пловдив
LON = 24.7453   # дължина за Пловдив

# 🌦️ URL за времето (5-дневна прогноза)
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

# 🌍 URL за замърсеност на въздуха
AIR_URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

# 🧠 Изтегляне на данни за времето
def get_weather_data():
    response = requests.get(WEATHER_URL)
    data = response.json()
    weather = []

    for entry in data["list"]:
        date = datetime.fromtimestamp(entry["dt"]).date()
        temp = entry["main"]["temp"]
        rain = entry.get("rain", {}).get("3h", 0)
        weather.append({"date": date, "temp": temp, "rain": rain})

    df = pd.DataFrame(weather)
    df = df.groupby("date").agg({"temp": "mean", "rain": "sum"})
    return df

# 🧑‍🔬 Изтегляне на данни за замърсеността на въздуха
def get_air_quality():
    response = requests.get(AIR_URL)
    data = response.json()
    air_data = data["list"][0]["components"]
    aqi = data["list"][0]["main"]["aqi"]
    
    return air_data, aqi

# 📊 Сравнителни данни за май (можеш да ги разшириш и за други месеци)
NORMALS = {
    "May": {
        "temp": 17.0,
        "rain_days": 8
    }
}

# 🚀 Streamlit UI
st.title("🌦️ Анализ на времето и замърсеността на въздуха в Пловдив")
st.write("Данни от OpenWeatherMap за 5 дни напред")

# Вземаме данни за времето
df = get_weather_data()

# 📈 Визуализации за времето
st.subheader("📈 Температури по дни")
st.line_chart(df["temp"])

st.subheader("🌧️ Валежи по дни (в мм)")
st.bar_chart(df["rain"])

# 📐 Средни стойности и сравнение
month = "May"  # Тук е фиксирано, но може да се направи динамично
avg_temp = df["temp"].mean()
rain_days = (df["rain"] > 0).sum()

st.subheader("📊 Анализ на времето")
st.write(f"📌 Средна температура: **{avg_temp:.1f}°C**")
st.write(f"📌 Дни с валежи: **{rain_days} дни**")

# 🔍 Интерпретация на времето
if avg_temp > NORMALS[month]["temp"] + 2:
    st.warning("⚠️ Температурите са неочаквано високи за този месец!")
elif avg_temp < NORMALS[month]["temp"] - 2:
    st.warning("⚠️ Температурите са по-ниски от обичайното!")
else:
    st.success("✅ Температурите са в обичайните граници.")

if rain_days > NORMALS[month]["rain_days"]:
    st.warning("🌧️ Има повече валежи от обичайното.")
else:
    st.success("✅ Валежите са в нормата.")

# 🌍 Данни за замърсеност на въздуха
air_data, aqi = get_air_quality()

# 📊 Визуализация на замърсеността
st.subheader("🌬️ Замърсеност на въздуха в Пловдив")
st.write(f"📌 Индекс на замърсеността (AQI): **{aqi}**")

# 📊 Бар графика за замърсеността на въздуха
components = list(air_data.keys())
values = list(air_data.values())

fig, ax = plt.subplots()
ax.bar(components, values, color='skyblue')
ax.set_title('Компоненти на замърсеността на въздуха (µg/m³)')
ax.set_ylabel('Концентрация')
st.pyplot(fig)

# 🔍 Интерпретация на замърсеността
if aqi == 1:
    st.success("✅ Въздухът е много чист (Добро).")
elif aqi == 2:
    st.success("✅ Въздухът е приемлив (Приемливо).")
elif aqi == 3:
    st.warning("⚠️ Въздухът е умерено замърсен (Умерено).")
elif aqi == 4:
    st.warning("⚠️ Въздухът е замърсен (Лошо).")
else:
    st.error("⚠️ Въздухът е много замърсен (Много лошо).")

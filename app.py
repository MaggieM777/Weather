import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 🗝️ Въведи своя API ключ тук
API_KEY = "ТУК_ВЪВЕДИ_СВОЯ_API_KEY"
CITY = "Plovdiv"
URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

# 🧠 Изтегляне на данните от API
def get_weather_data():
    response = requests.get(URL)
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

# 📊 Сравнителни данни за май (можеш да ги разшириш и за други месеци)
NORMALS = {
    "May": {
        "temp": 17.0,
        "rain_days": 8
    }
}

# 🚀 Streamlit UI
st.title("🌦️ Анализ на времето в Пловдив")
st.write("Данни от OpenWeatherMap за 5 дни напред")

df = get_weather_data()

# 📈 Визуализации
st.subheader("📈 Температури по дни")
st.line_chart(df["temp"])

st.subheader("🌧️ Валежи по дни (в мм)")
st.bar_chart(df["rain"])

# 📐 Средни стойности и сравнение
month = "May"  # Тук е фиксирано, но може да се направи динамично
avg_temp = df["temp"].mean()
rain_days = (df["rain"] > 0).sum()

st.subheader("📊 Анализ")
st.write(f"📌 Средна температура: **{avg_temp:.1f}°C**")
st.write(f"📌 Дни с валежи: **{rain_days} дни**")

# 🔍 Интерпретация
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

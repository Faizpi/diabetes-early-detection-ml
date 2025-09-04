import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# =======================
# 🎨 Custom Style
# =======================
st.set_page_config(page_title="Prediksi Diabetes", page_icon="💻", layout="centered")

st.markdown("""
    <style>
    body {
        background: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
        color: #333;
    }
    .stButton>button {
        background: #2a5298;
        color: white;
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #1e3c72;
        transform: scale(1.02);
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 6px;
        padding: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# =======================
# 📂 Load Dataset
# =======================
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset_Diabetes.csv")
    return df

df = load_data()

# =======================
# 🧠 Training Model
# =======================
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

acc = accuracy_score(y_test, model.predict(X_test))

# =======================
# 🌐 Tampilan Streamlit
# =======================
st.title("Prediksi Diabetes")
st.markdown("Model Machine Learning menggunakan **Logistic Regression**")

st.info(f"Akurasi Model pada data uji: **{acc*100:.2f}%**")

st.markdown("### Form Input Data Pasien")

# rata-rata nilai dari dataset untuk hint
mean_values = df.mean().to_dict()

kolom = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
         'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

user_input = {}
col1, col2 = st.columns(2)

for i, k in enumerate(kolom):
    if i % 2 == 0:
        val = col1.number_input(f"{k}", value=0.0)
        col1.caption(f"💡 Rata-rata: {mean_values[k]:.1f}")
    else:
        val = col2.number_input(f"{k}", value=0.0)
        col2.caption(f"💡 Rata-rata: {mean_values[k]:.1f}")
    user_input[k] = val

if st.button("Prediksi"):
    user_data = np.array([list(user_input.values())])
    user_data_scaled = scaler.transform(user_data)
    prediction = model.predict(user_data_scaled)
    prediction_proba = model.predict_proba(user_data_scaled)

    st.markdown("### Hasil Prediksi")
    if prediction[0] == 1:
        st.error("Prediksi: POSITIF Diabetes")
    else:
        st.success("Prediksi: TIDAK Diabetes")

    st.write("Probabilitas:")
    st.progress(float(prediction_proba[0][1]))
    st.write(f"- Tidak Diabetes = {prediction_proba[0][0]:.2f}")
    st.write(f"- Diabetes = {prediction_proba[0][1]:.2f}")

# =======================
# 📊 Visualisasi Data
# =======================
st.markdown("### Insight Data")

tab1, tab2 = st.tabs(["Distribusi Glucose", "Distribusi BMI"])

with tab1:
    chart_glucose = alt.Chart(df).mark_bar(opacity=0.7).encode(
        alt.X("Glucose:Q", bin=alt.Bin(maxbins=40), title="Glucose"),
        alt.Y("count()", title="Jumlah Pasien"),
        alt.Color("Outcome:N", scale=alt.Scale(domain=[0,1], range=["#2a5298", "#e63946"]),
                  title="Outcome")
    ).properties(width=600, height=400, title="Distribusi Glucose berdasarkan Outcome")
    st.altair_chart(chart_glucose, use_container_width=True)

with tab2:
    chart_bmi = alt.Chart(df).mark_bar(opacity=0.7).encode(
        alt.X("BMI:Q", bin=alt.Bin(maxbins=40), title="BMI"),
        alt.Y("count()", title="Jumlah Pasien"),
        alt.Color("Outcome:N", scale=alt.Scale(domain=[0,1], range=["#2a5298", "#e63946"]),
                  title="Outcome")
    ).properties(width=600, height=400, title="Distribusi BMI berdasarkan Outcome")
    st.altair_chart(chart_bmi, use_container_width=True)

import streamlit as st
import pandas as pd
import datetime
import io
import matplotlib.pyplot as plt

# Title
st.set_page_config(page_title="Lab Automation App", layout="centered")
st.title("🧪 Lab Automation Project")

# Session state setup
if "experiments" not in st.session_state:
    st.session_state.experiments = []

# Input section
st.header("Enter Experiment Details")
exp_name = st.text_input("Experiment Name")
concentration = st.number_input("Chemical Concentration (mol/L)", min_value=0.0, step=0.1)
temperature = st.number_input("Temperature (°C)", min_value=0.0, step=0.1)
notes = st.text_area("Notes (Optional)")

# Reaction rate calculation
def calculate_rate(conc, temp):
    k = 0.01  # Rate constant
    return k * conc * temp

if st.button("Run Experiment"):
    if not exp_name:
        st.warning("Please enter an experiment name.")
    else:
        rate = calculate_rate(concentration, temperature)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.experiments.append({
            "Date": timestamp,
            "Experiment": exp_name,
            "Concentration": concentration,
            "Temperature": temperature,
            "Rate": round(rate, 4),
            "Notes": notes
        })
        st.success(f"✅ Reaction Rate: {rate:.4f} mol/L·s")

# Show table
if st.session_state.experiments:
    st.subheader("Experiment History")
    df = pd.DataFrame(st.session_state.experiments)
    st.dataframe(df, use_container_width=True)

    # Plot
    st.subheader("📈 Reaction Rate vs Concentration")
    fig, ax = plt.subplots()
    ax.plot(df["Concentration"], df["Rate"], marker="o")
    ax.set_xlabel("Concentration (mol/L)")
    ax.set_ylabel("Reaction Rate (mol/L·s)")
    st.pyplot(fig)

    # Download buttons
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    def generate_txt(df):
        txt_buffer = io.StringIO()
        for _, row in df.iterrows():
            txt_buffer.write(f"Date: {row['Date']}\nExperiment: {row['Experiment']}\nConcentration: {row['Concentration']}\nTemperature: {row['Temperature']}\nRate: {row['Rate']}\nNotes: {row['Notes']}\n---\n")
        return txt_buffer.getvalue().encode("utf-8")

    st.download_button("⬇️ Download CSV Report", convert_df_to_csv(df), file_name="lab_report.csv")
    st.download_button("⬇️ Download TXT Report", generate_txt(df), file_name="lab_report.txt")

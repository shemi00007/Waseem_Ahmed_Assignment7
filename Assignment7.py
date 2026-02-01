import streamlit as st
import pandas as pd
from datetime import date

st.title("Personal Information & Exact Age App")

# -----------------------------
# Defaults
# -----------------------------
defaults = {
    "name": "",
    "parent_name": "",
    "dob": date.today(),
    "sex": "Male",
    "married": False,
    "unmarried": False,
    "kids": 0
}

# Initialize session state
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "records" not in st.session_state:
    st.session_state.records = []


# -----------------------------
# Exact Age Calculation
# -----------------------------
def calculate_exact_age(dob):
    today = date.today()

    years = today.year - dob.year
    months = today.month - dob.month
    days = today.day - dob.day

    if days < 0:
        months -= 1
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month != 1 else today.year - 1
        days += (date(prev_year, prev_month % 12 + 1, 1) - date(prev_year, prev_month, 1)).days

    if months < 0:
        years -= 1
        months += 12

    return years, months, days


# -----------------------------
# Submit callback (IMPORTANT)
# -----------------------------
def submit_form():
    years, months, days = calculate_exact_age(st.session_state.dob)

    record = {
        "Name": st.session_state.name,
        "Parent Name": st.session_state.parent_name,
        "DOB": st.session_state.dob.strftime("%Y-%m-%d"),
        "Exact Age": f"{years} Years {months} Months {days} Days",
        "Sex": st.session_state.sex,
        "Marital Status": "Married" if st.session_state.married else "Unmarried",
        "Kids": st.session_state.kids
    }

    st.session_state.records.append(record)

    # Reset all fields safely
    for key, value in defaults.items():
        st.session_state[key] = value


# -----------------------------
# Form Inputs
# -----------------------------
st.subheader("Enter Personal Details")

st.text_input("Full Name", key="name")
st.text_input("Parent Name", key="parent_name")

st.date_input(
    "Date of Birth",
    min_value=date.today().replace(year=date.today().year - 100),
    max_value=date.today(),
    key="dob"
)

st.radio("Sex", ["Male", "Female"], key="sex")

st.checkbox("Married", key="married")
st.checkbox("Unmarried", key="unmarried")

# Ensure only one marital status
if st.session_state.married and st.session_state.unmarried:
    st.warning("Please select only one marital status")
    st.session_state.unmarried = False

# Kids dropdown logic
if st.session_state.married and not st.session_state.unmarried:
    st.selectbox("Number of Kids", [0, 1, 2, 3, 4, 5], key="kids")
else:
    st.session_state.kids = 0


# -----------------------------
# Submit Button (with callback)
# -----------------------------
st.button("Submit", on_click=submit_form)


# -----------------------------
# Display & Download Data
# -----------------------------
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)

    st.subheader("Stored Records")
    st.dataframe(df)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="personal_data.csv",
        mime="text/csv"
    )

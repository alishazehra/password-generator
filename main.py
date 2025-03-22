import re
import streamlit as st

import random
import string
import requests
import hashlib

from io import BytesIO
from PIL import Image

st.set_page_config(page_title="🔐 Password Security Checker ", layout="centered")

# Added a custom background color using markdown and CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, pink, pink);
    }
    </style>
    """,
    unsafe_allow_html=True
)


def check_password(password):
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    sha1_prefix, sha1_suffix = sha1_password[:5], sha1_password[5:]
    
    response = requests.get(f"https://api.pwnedpasswords.com/range/{sha1_prefix}")
    if sha1_suffix in response.text:
        return True
    return False



# Password  Checker
def check_password_strengths(password):
    score = 0
    feedback = []

    if check_password(password):
        feedback.append("❌ Your password was found in a data breach! Choose another one.")
        return 0, feedback

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Use both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*()_+{}|:<>?]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    return score, feedback

# Strong Password Generator
def strong_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+{}|:<>?"
    return "".join(random.choice(chars) for _ in range(length))

# Generate a Secure 2FA Code
def generate_2ba_code():
    return random.randint(100000, 999999)

# Generate MFA QR Code
# def generate_qr_code(secret):
#     qr = qrcode.make(f"otpauth://totp/YourApp?secret={secret}")
#     buffer = BytesIO()
#     qr.save(buffer, format="PNG")
#     buffer.seek(0)
#     return buffer

# Streamlit UI
# st.set_page_config(page_title="🔐 Password Security Checker", layout="centered")

st.title("🔐 Password Security App")
st.write("Check your password strength & security in real-time!")

# Password Input
password = st.text_input("Enter your password:", type="password")

if password:
    score, feedback = check_password_strengths(password)
    
    if score >= 5:
        st.success("✅ Ultra Secure Password!")
    elif score == 4:
        st.success("✅ Strong Password!")
    elif score == 3:
        st.warning("⚠️ Moderate Password - Consider improving it.")
    else:
        st.error("❌ Weak Password! Improve using these tips:")
        for msg in feedback:
            st.write(msg)

    st.progress(score / 5)


st.subheader("🔑 Generate a Strong Password")
length = st.slider("Password Length", 8, 32, 16)
if st.button("Generate Password"):
    strong_password = strong_password(length)
    st.code(strong_password, language="")


st.subheader("🔓 Generate a Secure 2BA Code")
if st.button("Generate 2BA Code"):
    st.success(f"Your 2BA Code: {generate_2ba_code()}")

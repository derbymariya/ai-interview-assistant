import streamlit as st
import requests
import os

# ✅ Correct working HF router endpoint
API_URL = "https://router.huggingface.co/hf-inference/models/HuggingFaceH4/zephyr-7b-beta"

# ✅ Token from environment variable
headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json"
}

# ✅ API call function (safe handling)
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        return response.json()
    except:
        return {"error": response.text}

# ✅ UI
st.title("🎯 AI Interview Assistant")

role = st.text_input("Enter Job Role")

if st.button("Generate"):
    if role:
        prompt = f"""
        You are an expert interviewer.

        Generate 5 interview questions with clear answers for the role: {role}.

        Keep answers simple and structured.
        """

        with st.spinner("Generating... please wait"):
            output = query({
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 300
                }
            })

        # ✅ Safe output handling
        if isinstance(output, list):
            st.write(output[0].get("generated_text", "No output generated"))

        elif isinstance(output, dict):
            if "error" in output:
                st.error(output["error"])
            else:
                st.write(output)

        else:
            st.write("Unexpected response, try again")

    else:
        st.warning("Enter a job role")
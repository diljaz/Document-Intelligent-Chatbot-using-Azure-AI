import streamlit as st #streamlit is a python library used for creating the frontend
import requests
import os

# Set up the Streamlit app
st.title("File Upload and Chatbot")

# File upload section
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    # Save the uploaded file
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File uploaded successfully: {uploaded_file.name}")

    # Send the file name to the /api/upload endpoint
    upload_url = "http://localhost:8000/api/upload"
    data = {"file_name": file_path}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(upload_url, json=data, headers=headers)
        response.raise_for_status()
        st.success("File name sent to API successfully")
    except requests.exceptions.RequestException as e:
        st.error(f"Error sending file name to API: {str(e)}")
        st.error(f"Response content: {response.text}")

# Chatbot section
st.header("Chatbot")
user_input = st.text_input("Enter your message:")

if st.button("Send"):
    if user_input:
        # Send only the user input to the /api/query endpoint
        query_url = "http://localhost:8000/api/query"
        data = {"query": user_input}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(query_url, json=data, headers=headers)
            response.raise_for_status()
            bot_response = response.json().get("response", "No response from the chatbot")
            st.text_area("Chatbot:", value=bot_response, height=500)
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting response from the chatbot: {str(e)}")
            st.error(f"Response content: {response.text}")
    else:
        st.warning("Please enter a message")


import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="The Dawg Catalog Advisor", page_icon="📋", layout="wide")

# 2. Main Dashboard UI
st.title("📋 The Dawg Catalog Advisor")
st.write("Perform strict, year-over-year comparative policy tracking across Adrian College academic catalogs.")

# 3. Initialize Secure API Context
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("Missing OpenAI API Key in Streamlit Secrets dashboard.")
    st.stop()

# 4. User Input and Execution Stream
user_query = st.text_input(
    "What historical requirement or policy are you tracking?", 
    placeholder="e.g., For a Baccalaureate degree does a student have to take a Modern Language?"
)

if st.button("Run Historical Analysis", type="primary"):
    if not user_query.strip():
        st.warning("Please submit a specific question first.")
    else:
        with st.spinner("Deep scanning catalog databases..."):
            try:
                # Create a fresh conversational context thread
                thread = client.beta.threads.create()
                client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=user_query
                )
                
                # Execute the live multi-catalog search run
                # Paste your exact Assistant ID string right below:
                run = client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id,
                    assistant_id="OcJ1slvpExnLvqYCJjQ0VsxT" 
                )
                
                # Render results natively upon completion
                if run.status == 'completed':
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    answer = messages.data[0].content[0].text.value
                    st.success("Historical Audit Complete:")
                    st.markdown(answer)
                else:
                    st.error(f"Execution run stopped with unexpected status: {run.status}")
            except Exception as e:
                st.error(f"An API handshake error occurred: {str(e)}")
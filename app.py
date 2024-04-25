import streamlit as st
from unify import ChatBot

# Initialize session state for chatbots if not already present
if 'chatbot1' not in st.session_state:
    st.session_state['chatbot1'] = None
if 'chatbot2' not in st.session_state:
    st.session_state['chatbot2'] = None

# Function to input API keys and endpoints
def input_fields():
    with st.sidebar:
        st.header("Configuration")
        unify_api_key = st.secrets.get('unify_api_key', st.text_input("Unify API Key*", type="password", placeholder="Enter Unify API Key"))
        endpoint1 = st.text_input("Endpoint 1*", placeholder="model@provider", value="claude-3-haiku@anthropic")
        endpoint2 = st.text_input("Endpoint 2*", placeholder="model@provider", value="mixtral-8x7b-instruct-v0.1@together-ai")
        show_credits = st.toggle("Show Credit Usage", value=False)
        return unify_api_key, endpoint1, endpoint2, show_credits

# Function to display chat interface and handle game logic
def chat_interface(prompt, chatbot1, chatbot2):
    if prompt:
        # Assuming the method to get a response is named 'process_input' or accessing '_process_input' directly
        response1 = chatbot1.process_input(prompt, show_credits=False, show_provider=False)
        response2 = chatbot2.process_input(prompt, show_credits=False, show_provider=False)
        st.write("AI 1 Response:", response1)
        st.write("AI 2 Response:", response2)
        
        # Implement response verification and judge logic here
        if response1 != response2:  # Simplified example of a verification
            st.error("Responses do not match! Game Over.")
            return True  # Indicates game over
    return False  # Game continues

def main():
    st.set_page_config(page_title="LLM Wars")
    st.title("LLM Wars")

    unify_api_key, endpoint1, endpoint2, show_credits = input_fields()

    if unify_api_key and endpoint1 and endpoint2:
        if not st.session_state.chatbot1 or st.session_state.chatbot1.endpoint != endpoint1:
            st.session_state.chatbot1 = ChatBot(unify_api_key, endpoint1)
        if not st.session_state.chatbot2 or st.session_state.chatbot2.endpoint != endpoint2:
            st.session_state.chatbot2 = ChatBot(unify_api_key, endpoint2)

        user_input = st.text_input("Enter your prompt:")
        game_over = chat_interface(user_input, st.session_state.chatbot1, st.session_state.chatbot2)
        if game_over:
            st.success("Game has ended.")

if __name__ == "__main__":
    main()
import streamlit as st
from unify import Unify
import requests
from gtts import gTTS
from io import BytesIO
import base64

class ChatBot:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint
        self.client = Unify(api_key=api_key, endpoint=endpoint)
        self.message_history = []

    def send_message(self, message):
        """Send a message to the Unify API and store the conversation history."""
        self.message_history.append({'role': 'user', 'content': message})
        try:
            response = self.client.generate(messages=self.message_history)
            self.message_history.append({'role': 'assistant', 'content': response})
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def _get_credits(self):
        """Retrieve the credit balance using the Unify API."""
        url = 'https://api.unify.ai/v0/get_credits'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['credits']
        else:
            return f"Error fetching credits: {response.json().get('error', 'Unknown error')}"

    def text_to_speech(self, text):
        """Convert text to speech and return HTML audio element."""
        tts = gTTS(text, lang='en')
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode("utf-8")
        audio_html = f"<audio controls><source src='data:audio/mp3;base64,{audio_base64}' type='audio/mpeg'></audio>"
        return audio_html

def input_fields():
    """Create sidebar for input fields."""
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("API Key*", type="password")
        endpoint1 = st.text_input("LLM1 Endpoint*", "model@provider")
        endpoint2 = st.text_input("LLM2 Endpoint*", "model@provider")
        judge_endpoint = st.text_input("Judge Endpoint*", "model@provider")
        show_credits = st.checkbox("Show Credit Usage", value=False)
        return api_key, endpoint1, endpoint2, judge_endpoint, show_credits

def llm_battle(chatbot1, chatbot2, judge, show_credits):
    """Simulate a battle between two language models with a judge."""
    prompt = "Generate a random question that you need to get answered."
    round_number = 1

    while True:
        question = chatbot1.send_message(prompt)
        answer_llm2 = chatbot2.send_message(question)
        evaluation_llm1 = chatbot1.send_message(f"Evaluating LLM2's response: {answer_llm2}")
        answer_llm1 = chatbot1.send_message(question)

        judge_response = judge.send_message(f"Judge the responses: Original Question: {question}\nLLM2's Answer: {answer_llm2}\nLLM1's Evaluation of LLM2: {evaluation_llm1}\nLLM1's Answer: {answer_llm1}")

        st.write(f"Round {round_number}:")
        st.markdown(f"**LLM1 Question:** {question}")
        st.markdown(f"**LLM2's Answer:** {answer_llm2}")
        st.markdown(f"**LLM1's Evaluation of LLM2:** {evaluation_llm1}")
        st.markdown(f"**LLM1's Answer:** {answer_llm1}")
        st.markdown(f"**Judge's Evaluation:** {judge_response}")

        # Play the audio for each text
        st.markdown(chatbot1.text_to_speech(question), unsafe_allow_html=True)
        st.markdown(chatbot2.text_to_speech(answer_llm2), unsafe_allow_html=True)
        st.markdown(chatbot1.text_to_speech(evaluation_llm1), unsafe_allow_html=True)
        st.markdown(chatbot1.text_to_speech(answer_llm1), unsafe_allow_html=True)
        st.markdown(judge.text_to_speech(judge_response), unsafe_allow_html=True)

        if show_credits:
            credits = chatbot1._get_credits()
            st.sidebar.write(f"Credit Balance: ${credits}")

        if not st.button("Next Round", key=f"next{round_number}"):
            break

        round_number += 1
        prompt = "Generate another random question."

def main():
    """Main function to run the Streamlit app."""
    st.title("LLM Wars")
    api_key, endpoint1, endpoint2, judge_endpoint, show_credits = input_fields()

    if api_key and endpoint1 and endpoint2 and judge_endpoint:
        chatbot1 = ChatBot(api_key, endpoint1)
        chatbot2 = ChatBot(api_key, endpoint2)
        judge = ChatBot(api_key, judge_endpoint)

        if st.button("Start Battle"):
            llm_battle(chatbot1, chatbot2, judge, show_credits)

if __name__ == "__main__":
    main()
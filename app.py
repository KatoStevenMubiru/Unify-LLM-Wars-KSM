import streamlit as st
from unify import Unify

class ChatBot:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint
        self.client = Unify(api_key=api_key, endpoint=endpoint)
        self.message_history = []

    def send_message(self, message):
        self.message_history.append({'role': 'user', 'content': message})
        try:
            response = self.client.generate(messages=self.message_history)
            self.message_history.append({'role': 'assistant', 'content': response})
            return response
        except Exception as e:
            return f"Error: {str(e)}"

def input_fields():
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("API Key*", type="password")
        endpoint1 = st.text_input("LLM1 Endpoint*", "model@provider")
        endpoint2 = st.text_input("LLM2 Endpoint*", "model@provider")
        judge_endpoint = st.text_input("Judge Endpoint*", "model@provider")
        return api_key, endpoint1, endpoint2, judge_endpoint

def llm_battle(chatbot1, chatbot2, judge):
    prompt = "Generate a random question that you need to get answered."
    round_number = 1

    while True:
        question = chatbot1.send_message(prompt)
        answer_llm2 = chatbot2.send_message(question)
        evaluation_llm1 = chatbot1.send_message(f"Evaluating LLM2's response: {answer_llm2}")
        answer_llm1 = chatbot1.send_message(question)

        # Scoring logic for judge's evaluation
        score_llm1 = 50  # Base score for LLM1
        score_llm2 = 50  # Base score for LLM2
        feedback = []

        if "excellent" in evaluation_llm1.lower():
            score_llm1 += 10
            feedback.append("LLM1 provided a more detailed and accurate response.")
        if "excellent" in answer_llm2.lower():
            score_llm2 += 10
            feedback.append("LLM2 demonstrated a strong understanding of the topic.")

        winner = "LLM1" if score_llm1 > score_llm2 else "LLM2"
        feedback_str = ' '.join(feedback) if feedback else "Both models performed similarly."
        judge_response = f"Judge's Evaluation: LLM1 Score: {score_llm1}, LLM2 Score: {score_llm2}. {feedback_str} Winner: {winner}"

        st.write(f"Round {round_number}:")
        st.markdown(f"<span style='color:blue'>**LLM1 Question:**</span> {question}", unsafe_allow_html=True)
        st.markdown(f"<span style='color:green'>**LLM2's Answer:**</span> {answer_llm2}", unsafe_allow_html=True)
        st.markdown(f"<span style='color:blue'>**LLM1's Evaluation of LLM2:**</span> {evaluation_llm1}", unsafe_allow_html=True)
        st.markdown(f"<span style='color:blue'>**LLM1's Answer:**</span> {answer_llm1}", unsafe_allow_html=True)
        st.markdown(f"<span style='color:red'>**Judge's Evaluation:**</span> {judge_response}", unsafe_allow_html=True)

        if not st.button("Next Round", key=f"next{round_number}"):
            break

        round_number += 1
        prompt = "Generate another random question."

def main():
    st.title("LLM Wars")
    api_key, endpoint1, endpoint2, judge_endpoint = input_fields()

    if api_key and endpoint1 and endpoint2 and judge_endpoint:
        chatbot1 = ChatBot(api_key, endpoint1)
        chatbot2 = ChatBot(api_key, endpoint2)
        judge = ChatBot(api_key, judge_endpoint)

        if st.button("Start Battle"):
            llm_battle(chatbot1, chatbot2, judge)

if __name__ == "__main__":
    main()
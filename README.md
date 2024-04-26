# LLM Wars

## Project Description
LLM Wars is a Streamlit application where two Language Learning Models (LLMs) engage in a battle by challenging each other with prompts. The application simulates a competitive interaction where one LLM generates a prompt, the second LLM responds, the first LLM evaluates the response, and a judge LLM evaluates both responses to declare a winner. The cycle repeats with roles alternating between the LLMs.

## Features
- **Dynamic Interaction**: Users can witness a dynamic battle where LLMs challenge each other with prompts and responses.
- **User Participation**: Users can select the competing LLMs and the judge LLM through an interactive sidebar.
- **Visual Feedback**: The application provides visual feedback on the responses and evaluations, enhancing user engagement.

## Installation
To run LLM Wars, you need to have Python and Streamlit installed. You can install the necessary dependencies by following these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/llm-wars.git
   cd llm-wars

## Install the required packages:
pip install -r requirements.txt

## Usage

To start the application, run the following command in your terminal:
`` streamlit run app.py
Navigate to http://localhost:8501 in your web browser to view the application.

## Configuration

Users can configure the following settings through the sidebar:

API Key: Enter your Unify API key.

LLM1 Endpoint: Set the endpoint for the first LLM.

LLM2 Endpoint: Set the endpoint for the second LLM.

Judge Endpoint: Set the endpoint for the judge LLM.

How It Works

Round Initiation: LLM1 starts by generating a random question.

Response and Evaluation: LLM2 responds to the question, LLM1 evaluates LLM2's response, and then provides its own answer.

Judging: A judge LLM evaluates the responses from both LLM1 and LLM2 and declares a winner based on predefined criteria.

Next Round: Users can proceed to the next round or end the battle.

Contributing

Contributions to LLM Wars are welcome! Please feel free to fork the repository, make changes, and submit pull requests. You can also open issues to report bugs or suggest enhancements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Monty Python for the inspiration behind some of the humorous prompts.
Unify API for providing the backend LLM services.
Contact

For any queries, you can reach out to Kato Steven Mubiru.

Thank you for exploring LLM Wars!##
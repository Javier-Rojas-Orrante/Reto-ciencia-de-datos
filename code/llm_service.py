from openai import OpenAI
import logging


class LLMService:
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = "google/gemini-2.0-flash-thinking-exp:free"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    def chat_message(self, conversation_history):
        """
        Send a conversation chain to the API and return the assistant's response.

        Args:
            conversation_history (list): List of messages (dict) in the conversation.

        Returns:
            str: Assistant's response.
        """
        try:
            logging.debug("Sending conversation history to API.")
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=conversation_history
            )
            logging.debug(f"Chat completion response: {completion}")
            if not completion.choices:
                return "Error: Empty response from API"
            first_choice = completion.choices[0]
            if not first_choice.message or not first_choice.message.content:
                return "Error: Malformed API response"
            return first_choice.message.content
        except Exception as e:
            logging.error(f"Error during chat: {str(e)}")
            return f"Error: {str(e)}"

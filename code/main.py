import json
import logging
from llm_service import LLMService
from parser import TicketParser
LLM = LLMService('apikey')

print(LLM.chat_message([{"role": "user", "content": "Hola, ¿cómo estás?"}]))




# def load_config(config_path="code/config.json"):
#     try:
#         with open(config_path, 'r') as f:
#             config = json.load(f)
#         return config
#     except FileNotFoundError:
#         logging.error(f"Config file not found at {config_path}")
#         return {}
#     except json.JSONDecodeError:
#         logging.error(f"Error decoding JSON from {config_path}")
#         return {}


#parser = TicketParser("Tickets de atencion a socios (1).json", "Tickets de atencion a socios (2).json")
#print(parser.get_info_conversation(1))
#print(parser.get_formatted_string(1)) 


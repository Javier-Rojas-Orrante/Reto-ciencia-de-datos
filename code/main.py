import json
import logging
from llm_service import LLMService
from parser import TicketParser
# image_analysis_service = LLMService(api_key)


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


parser = TicketParser("Tickets de atencion a socios (1).json")
print(parser.get_ticket_data(1))  # Get as chat-like format
import json
from datetime import datetime
import pprint

class TicketParser:
    def __init__(self, filepath1, filepath2):
        self.filepath1 = filepath1
        self.filepath2 = filepath2
        self.parsed_tickets = {}
        self._load_data()


    def _load_data(self):
        with open(self.filepath1, encoding="utf-8") as f:
            data1 = json.load(f)
        with open(self.filepath2, encoding="utf-8") as f:
            data2 = json.load(f)

        for item in data1 + data2:
            ticket = item["helpdesk_ticket"]
            ticket_id = ticket["id"]

            requester_id = ticket["requester_id"]
            responder_id = ticket["responder_id"]
            requester_name = ticket.get("requester_name", "Unknown")
            responder_name = ticket.get("responder_name", "Unknown")

            conversation = []

            for note in sorted(ticket["notes"], key=lambda x: x["created_at"]):
                sender_type = "Customer" if note["user_id"] == requester_id else "Agent"
                sender_name = requester_name if sender_type == "Customer" else responder_name
                message = note["body"]
                sent_at = note["created_at"]
                sent_at = datetime.fromisoformat(sent_at).strftime("%Y-%m-%d %H:%M:%S")
                agent = False if note['incoming'] else True  # True if the message is from the agent, False if it's from the customer

                conversation.append({
                    "name": sender_name,
                    "message": message,
                    "sent_at": sent_at,
                    "agent": agent
                })

            self.parsed_tickets[ticket_id] = {
                "conversation": conversation
            }


    def get_formatted_string(self, ticket_index=0):
        '''
        Devuelve el parsed_tickets en un string con formato de diccionario.
        '''
        try:
            ticket_id = list(self.parsed_tickets.keys())[ticket_index]
            ticket_data = self.parsed_tickets[ticket_id]
            return pprint.pformat(ticket_data, indent=2, width=100)
        except IndexError:
            return f"Ticket index {ticket_index} out of range."

    def get_info_conversation(self, ticket_index=0):
        '''
        Returns the conversation of a ticket in a list of dictionaries with the following keys:
        - name: the name of the sender
        - message: the message of the sender
        - sent_at: the date and time the message was sent
        - agent: True if the message is from the agent, False if it's from the customer
        '''
        try:
            ticket_id = list(self.parsed_tickets.keys())[ticket_index]
            return self.parsed_tickets[ticket_id]
        except IndexError:
            return None
        
    def get_text_conversation(self, ticket_index=0):
        '''
        Returns the conversation of a ticket in a string with the following format:
        - name: the name of the sender
        - message: the message of the sender
        '''
        try:
            ticket_id = list(self.parsed_tickets.keys())[ticket_index]
            conversation = self.parsed_tickets[ticket_id]["conversation"]
            lines = []
            for entry in conversation:
                lines.append(f"{entry['name']}:\n{entry['message']}\n")
            return {"id": ticket_id, "conversation": "\n".join(lines)}
        except IndexError:
            return f"Ticket index {ticket_index} out of range."

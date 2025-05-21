import json
import pprint

class TicketParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.parsed_tickets = {}
        self._load_data()

    def _load_data(self):
        with open(self.filepath, encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
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

                conversation.append({
                    "name": sender_name,
                    "message": message
                })

            self.parsed_tickets[ticket_id] = {
                "conversation": conversation
            }


    def get_formatted_string(self, ticket_index=0):
        try:
            ticket_id = list(self.parsed_tickets.keys())[ticket_index]
            ticket_data = self.parsed_tickets[ticket_id]
            return pprint.pformat(ticket_data, indent=2, width=100)
        except IndexError:
            return f"Ticket index {ticket_index} out of range."

    def get_ticket_data(self, ticket_index=0):
        try:
            ticket_id = list(self.parsed_tickets.keys())[ticket_index]
            return self.parsed_tickets[ticket_id]
        except IndexError:
            return None
        
    def get_text_conversation(self, ticket_index=0):
        try:
            ticket_id = list(self.parsed_tickets.keys())[ticket_index]
            conversation = self.parsed_tickets[ticket_id]["conversation"]
            lines = []
            for entry in conversation:
                lines.append(f"{entry['name']}:\n{entry['message']}\n")
            return "\n".join(lines)
        except IndexError:
            return f"Ticket index {ticket_index} out of range."

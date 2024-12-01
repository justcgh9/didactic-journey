from datetime import datetime


class Message:
    def __init__(self, from_, message):
        self.from_ = from_
        self.message = message
        self.created_at = datetime.now()

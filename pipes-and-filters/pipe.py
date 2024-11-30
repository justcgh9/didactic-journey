from multiprocessing import Queue

from message import Message


class Pipe:
    def __init__(self) -> None:
        self.queue: Queue = Queue()

    def send(self, data: Message) -> None:
        self.queue.put(data)

    def recv(self) -> Message:
        return self.queue.get()

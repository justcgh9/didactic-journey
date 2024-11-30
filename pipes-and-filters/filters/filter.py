import multiprocessing

from filters.protocol import Filter
from pipe import Pipe

class FilterFilter(Filter):
    def __init__(self, inputs: list[Pipe], outputs: list[Pipe], stopwords: list[str]):
        super().__init__()
        self.inputs, self.outputs = inputs, outputs
        self.stopwords = stopwords


    def run(self):
        self._process = multiprocessing.Process(target=self.target)
        self.process.start()

    def target(self):
        while True:
            for input_pipe in self.inputs:
                message = input_pipe.recv()
                print(f"filter {message}")
                if any(word in message.message for word in self.stopwords):
                    return
                for output_pipe in self.outputs:
                    output_pipe.send(message)

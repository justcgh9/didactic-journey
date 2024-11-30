
import multiprocessing

from filters.protocol import Filter
from pipe import Pipe


class ScreamingFilter(Filter):
    def __init__(self, inputs: list[Pipe], outputs: list[Pipe]):
        super().__init__()
        self.inputs, self.outputs = inputs, outputs
        


    def run(self):
        self._process = multiprocessing.Process(target=self.target)
        self.process.start()

    def target(self):
        while True:
            for input_pipe in self.inputs:
                message = input_pipe.recv()
                message.message = message.message.upper()
                print(f"scream {message}")
                for output_pipe in self.outputs:
                    output_pipe.send(message)

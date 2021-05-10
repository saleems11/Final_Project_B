class ProcessBar:
    def __init__(self):
        self.status: str = ''
        self.process: float = 0.0
        self.finished:bool = False

    def inc(self):
        self.process += 0.1
        if self.process> 1.0:
            self.process = 0
from threading import Thread


class WorkedThread(Thread):
    def __init__(self, scenario, **kwargs):
        super(WorkedThread, self).__init__()
        self.scenario = scenario
        self.data = kwargs
        self.start()

    def run(self):
        self.scenario(self.data).run_scenario()

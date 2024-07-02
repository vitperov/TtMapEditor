class GeneratorPluginBase:
    def __init__(self):
        pass

    def generate(self):
        raise NotImplementedError("Each plugin must implement the run method.")

from autobi.core import AutobiJVM


class TrainDefault:
    def __init__(self, jvm: AutobiJVM):
        self._jvm = jvm
        self._object = jvm._jvm.edu.leidenuniv.AuToBIAdapter.TrainDefault()

    def run(self, args: str):
        self._object.run(args)

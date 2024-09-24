from py4j.java_gateway import JVMView


class AutobiJVM:
    _jvm: JVMView


class AutobiJVMHandler:
    def __init__(self, name: str) -> None:
        ...

    def __enter__(self) -> AutobiJVM:
        ...

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        ...

from autobi.core import AutobiJVMHandler
from autobi import RunDefault, TrainDefault


class TestRunDefault:
    def test_runs_at_all(self):
        with AutobiJVMHandler("test") as jvm:
            RunDefault(jvm).run("")

    def test_trains_at_al(self):
        with AutobiJVMHandler("test") as jvm:
            TrainDefault(jvm).run("")

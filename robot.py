
class Robot:
    STATES = ["IDLE", "MOVING", "ERROR", "RECOVERY"]

    def __init__(self):
        self.state = "IDLE"

    def start(self):
        if self.state == "IDLE":
            self.state = "MOVING"
        else:
            raise Exception(f"Cannot start from state: {self.state}")

    def trigger_error(self):
        if self.state == "MOVING":
            self.state = "ERROR"
        else:
            raise Exception(f"Cannot trigger error from state: {self.state}")

    def recover(self):
        if self.state == "ERROR":
            self.state = "RECOVERY"
        else:
            raise Exception(f"Cannot recover from state: {self.state}")

    def reset(self):
        if self.state == "RECOVERY":
            self.state = "IDLE"
        else:
            raise Exception(f"Cannot reset from state: {self.state}")

    def get_state(self):
        return self.state
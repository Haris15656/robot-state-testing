class Robot:
    STATES = ["IDLE", "CHARGING", "MOVING", "OBSTACLE_DETECTED", 
              "ERROR", "RECOVERY", "EMERGENCY_STOP"]

    def __init__(self):
        self.state = "IDLE"

    def charge(self):
        if self.state == "IDLE":
            self.state = "CHARGING"
        else:
            raise Exception(f"Cannot charge from state: {self.state}")

    def finish_charging(self):
        if self.state == "CHARGING":
            self.state = "IDLE"
        else:
            raise Exception(f"Cannot finish charging from state: {self.state}")

    def start(self):
        if self.state == "IDLE":
            self.state = "MOVING"
        else:
            raise Exception(f"Cannot start from state: {self.state}")

    def detect_obstacle(self):
        if self.state == "MOVING":
            self.state = "OBSTACLE_DETECTED"
        else:
            raise Exception(f"Cannot detect obstacle from state: {self.state}")

    def clear_obstacle(self):
        if self.state == "OBSTACLE_DETECTED":
            self.state = "MOVING"
        else:
            raise Exception(f"Cannot clear obstacle from state: {self.state}")

    def trigger_error(self):
        if self.state in ["MOVING", "OBSTACLE_DETECTED"]:
            self.state = "ERROR"
        else:
            raise Exception(f"Cannot trigger error from state: {self.state}")

    def emergency_stop(self):
        if self.state in ["MOVING", "OBSTACLE_DETECTED", "ERROR"]:
            self.state = "EMERGENCY_STOP"
        else:
            raise Exception(f"Cannot emergency stop from state: {self.state}")

    def recover(self):
        if self.state in ["ERROR", "EMERGENCY_STOP"]:
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
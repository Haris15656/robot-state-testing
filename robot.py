from datetime import datetime

class Robot:
    STATES = ["IDLE", "CHARGING", "MOVING", "OBSTACLE_DETECTED",
              "ERROR", "EMERGENCY_STOP", "RECOVERY"]

    def __init__(self, robot_id="ROBOT-1"):
        self.robot_id = robot_id
        self.state = "IDLE"
        self.logs = []

    def _log(self, action, from_state, to_state):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {self.robot_id}: {from_state} → {to_state} ({action})"
        self.logs.append(entry)

    def charge(self):
        if self.state == "IDLE":
            self._log("CHARGE", self.state, "CHARGING")
            self.state = "CHARGING"
        else:
            raise Exception(f"Cannot charge from state: {self.state}")

    def finish_charging(self):
        if self.state == "CHARGING":
            self._log("FINISH_CHARGE", self.state, "IDLE")
            self.state = "IDLE"
        else:
            raise Exception(f"Cannot finish charging from state: {self.state}")

    def start(self):
        if self.state == "IDLE":
            self._log("START", self.state, "MOVING")
            self.state = "MOVING"
        else:
            raise Exception(f"Cannot start from state: {self.state}")

    def detect_obstacle(self):
        if self.state == "MOVING":
            self._log("OBSTACLE", self.state, "OBSTACLE_DETECTED")
            self.state = "OBSTACLE_DETECTED"
        else:
            raise Exception(f"Cannot detect obstacle from state: {self.state}")

    def clear_obstacle(self):
        if self.state == "OBSTACLE_DETECTED":
            self._log("CLEAR", self.state, "MOVING")
            self.state = "MOVING"
        else:
            raise Exception(f"Cannot clear obstacle from state: {self.state}")

    def trigger_error(self):
        if self.state in ["MOVING", "OBSTACLE_DETECTED"]:
            self._log("ERROR", self.state, "ERROR")
            self.state = "ERROR"
        else:
            raise Exception(f"Cannot trigger error from state: {self.state}")

    def emergency_stop(self):
        if self.state in ["MOVING", "OBSTACLE_DETECTED", "ERROR"]:
            self._log("E-STOP", self.state, "EMERGENCY_STOP")
            self.state = "EMERGENCY_STOP"
        else:
            raise Exception(f"Cannot emergency stop from state: {self.state}")

    def recover(self):
        if self.state in ["ERROR", "EMERGENCY_STOP"]:
            self._log("RECOVER", self.state, "RECOVERY")
            self.state = "RECOVERY"
        else:
            raise Exception(f"Cannot recover from state: {self.state}")

    def reset(self):
        if self.state == "RECOVERY":
            self._log("RESET", self.state, "IDLE")
            self.state = "IDLE"
        else:
            raise Exception(f"Cannot reset from state: {self.state}")

    def get_state(self):
        return self.state

    def get_logs(self):
        return self.logs


class RobotFleet:
    def __init__(self, size=3):
        self.robots = {
            f"ROBOT-{i+1}": Robot(f"ROBOT-{i+1}") 
            for i in range(size)
        }

    def get_robot(self, robot_id):
        return self.robots[robot_id]

    def get_all_states(self):
        return {rid: r.get_state() for rid, r in self.robots.items()}

    def get_all_logs(self):
        all_logs = []
        for robot in self.robots.values():
            all_logs.extend(robot.get_logs())
        return sorted(all_logs)

    def are_independent(self):
        for rid, robot in self.robots.items():
            other_states = [
                r.get_state() for oid, r in self.robots.items() if oid != rid
            ]
            if robot.get_state() in other_states:
                continue
        return True
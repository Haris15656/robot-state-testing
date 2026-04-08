from robot import Robot
from datetime import datetime

class Mission:
    def __init__(self, mission_id, robot):
        self.mission_id = mission_id
        self.robot = robot
        self.status = "PENDING"
        self.logs = []

    def _log(self, event):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] Mission {self.mission_id} ({self.robot.robot_id}): {event}"
        self.logs.append(entry)

    def execute(self):
        if self.status != "PENDING":
            raise Exception(f"Mission {self.mission_id} already {self.status}")
        self._log("STARTED")
        self.robot.start()
        self.status = "IN_PROGRESS"
        self._log("IN_PROGRESS")

    def complete(self):
        if self.status != "IN_PROGRESS":
            raise Exception(f"Cannot complete mission in status: {self.status}")
        self.robot.reset() if self.robot.get_state() == "RECOVERY" else None
        self.status = "COMPLETED"
        self._log("COMPLETED")

    def fail(self):
        if self.status != "IN_PROGRESS":
            raise Exception(f"Cannot fail mission in status: {self.status}")
        self.robot.trigger_error()
        self.status = "FAILED"
        self._log("FAILED")

    def get_status(self):
        return self.status

    def get_logs(self):
        return self.logs


class MissionScheduler:
    def __init__(self, fleet):
        self.fleet = fleet
        self.missions = {}
        self.mission_counter = 0

    def assign_mission(self, robot_id):
        robot = self.fleet.get_robot(robot_id)
        if robot.get_state() != "IDLE":
            raise Exception(f"{robot_id} is not IDLE, cannot assign mission")
        self.mission_counter += 1
        mission_id = f"MSN-{self.mission_counter:03d}"
        mission = Mission(mission_id, robot)
        self.missions[mission_id] = mission
        return mission

    def get_mission(self, mission_id):
        return self.missions[mission_id]

    def get_all_missions(self):
        return self.missions

    def get_summary(self):
        total = len(self.missions)
        completed = sum(1 for m in self.missions.values() if m.status == "COMPLETED")
        failed = sum(1 for m in self.missions.values() if m.status == "FAILED")
        in_progress = sum(1 for m in self.missions.values() if m.status == "IN_PROGRESS")
        pending = sum(1 for m in self.missions.values() if m.status == "PENDING")
        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "in_progress": in_progress,
            "pending": pending
        }
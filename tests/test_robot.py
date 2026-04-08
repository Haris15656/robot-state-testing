import pytest
from robot import Robot, RobotFleet
from mission import Mission, MissionScheduler

# ── Single Robot State Tests ──────────────────────────────────────────────────

def test_initial_state():
    robot = Robot()
    assert robot.get_state() == "IDLE"

def test_start_from_idle():
    robot = Robot()
    robot.start()
    assert robot.get_state() == "MOVING"

def test_charging_cycle():
    robot = Robot()
    robot.charge()
    assert robot.get_state() == "CHARGING"
    robot.finish_charging()
    assert robot.get_state() == "IDLE"

def test_cannot_charge_while_moving():
    robot = Robot()
    robot.start()
    with pytest.raises(Exception, match="Cannot charge from state: MOVING"):
        robot.charge()

def test_obstacle_detected_while_moving():
    robot = Robot()
    robot.start()
    robot.detect_obstacle()
    assert robot.get_state() == "OBSTACLE_DETECTED"

def test_clear_obstacle_resumes_moving():
    robot = Robot()
    robot.start()
    robot.detect_obstacle()
    robot.clear_obstacle()
    assert robot.get_state() == "MOVING"

def test_error_from_obstacle():
    robot = Robot()
    robot.start()
    robot.detect_obstacle()
    robot.trigger_error()
    assert robot.get_state() == "ERROR"

def test_emergency_stop_from_moving():
    robot = Robot()
    robot.start()
    robot.emergency_stop()
    assert robot.get_state() == "EMERGENCY_STOP"

def test_emergency_stop_from_obstacle():
    robot = Robot()
    robot.start()
    robot.detect_obstacle()
    robot.emergency_stop()
    assert robot.get_state() == "EMERGENCY_STOP"

def test_recovery_from_emergency_stop():
    robot = Robot()
    robot.start()
    robot.emergency_stop()
    robot.recover()
    assert robot.get_state() == "RECOVERY"

def test_full_cycle():
    robot = Robot()
    robot.start()
    robot.trigger_error()
    robot.recover()
    robot.reset()
    assert robot.get_state() == "IDLE"

def test_full_cycle_with_obstacle():
    robot = Robot()
    robot.start()
    robot.detect_obstacle()
    robot.clear_obstacle()
    robot.trigger_error()
    robot.recover()
    robot.reset()
    assert robot.get_state() == "IDLE"

def test_cannot_start_from_error():
    robot = Robot()
    robot.start()
    robot.trigger_error()
    with pytest.raises(Exception, match="Cannot start from state: ERROR"):
        robot.start()

def test_cannot_recover_from_idle():
    robot = Robot()
    with pytest.raises(Exception, match="Cannot recover from state: IDLE"):
        robot.recover()

def test_cannot_emergency_stop_from_idle():
    robot = Robot()
    with pytest.raises(Exception, match="Cannot emergency stop from state: IDLE"):
        robot.emergency_stop()

def test_robot_logging():
    robot = Robot("ROBOT-1")
    robot.start()
    robot.trigger_error()
    robot.recover()
    logs = robot.get_logs()
    assert len(logs) == 3
    assert "IDLE → MOVING" in logs[0]
    assert "MOVING → ERROR" in logs[1]
    assert "ERROR → RECOVERY" in logs[2]

def test_robot_id_in_logs():
    robot = Robot("ROBOT-TEST")
    robot.start()
    logs = robot.get_logs()
    assert "ROBOT-TEST" in logs[0]

# ── Fleet Tests ───────────────────────────────────────────────────────────────

def test_fleet_initialization():
    fleet = RobotFleet(3)
    states = fleet.get_all_states()
    assert len(states) == 3
    assert all(s == "IDLE" for s in states.values())

def test_fleet_robots_are_independent():
    fleet = RobotFleet(3)
    fleet.get_robot("ROBOT-1").start()
    fleet.get_robot("ROBOT-2").charge()
    assert fleet.get_robot("ROBOT-1").get_state() == "MOVING"
    assert fleet.get_robot("ROBOT-2").get_state() == "CHARGING"
    assert fleet.get_robot("ROBOT-3").get_state() == "IDLE"

def test_fleet_all_logs():
    fleet = RobotFleet(2)
    fleet.get_robot("ROBOT-1").start()
    fleet.get_robot("ROBOT-2").charge()
    logs = fleet.get_all_logs()
    assert len(logs) == 2

def test_fleet_simultaneous_errors():
    fleet = RobotFleet(3)
    for robot in fleet.robots.values():
        robot.start()
        robot.trigger_error()
    states = fleet.get_all_states()
    assert all(s == "ERROR" for s in states.values())

# ── Mission Tests ─────────────────────────────────────────────────────────────

def test_mission_assignment():
    fleet = RobotFleet(3)
    scheduler = MissionScheduler(fleet)
    mission = scheduler.assign_mission("ROBOT-1")
    assert mission.get_status() == "PENDING"

def test_mission_execution():
    fleet = RobotFleet(3)
    scheduler = MissionScheduler(fleet)
    mission = scheduler.assign_mission("ROBOT-1")
    mission.execute()
    assert mission.get_status() == "IN_PROGRESS"
    assert fleet.get_robot("ROBOT-1").get_state() == "MOVING"

def test_mission_failure():
    fleet = RobotFleet(3)
    scheduler = MissionScheduler(fleet)
    mission = scheduler.assign_mission("ROBOT-1")
    mission.execute()
    mission.fail()
    assert mission.get_status() == "FAILED"
    assert fleet.get_robot("ROBOT-1").get_state() == "ERROR"

def test_cannot_assign_mission_to_busy_robot():
    fleet = RobotFleet(3)
    scheduler = MissionScheduler(fleet)
    mission = scheduler.assign_mission("ROBOT-1")
    mission.execute()
    with pytest.raises(Exception, match="is not IDLE"):
        scheduler.assign_mission("ROBOT-1")

def test_multiple_missions_different_robots():
    fleet = RobotFleet(3)
    scheduler = MissionScheduler(fleet)
    m1 = scheduler.assign_mission("ROBOT-1")
    m2 = scheduler.assign_mission("ROBOT-2")
    m3 = scheduler.assign_mission("ROBOT-3")
    m1.execute()
    m2.execute()
    m3.execute()
    assert fleet.get_robot("ROBOT-1").get_state() == "MOVING"
    assert fleet.get_robot("ROBOT-2").get_state() == "MOVING"
    assert fleet.get_robot("ROBOT-3").get_state() == "MOVING"

def test_mission_scheduler_summary():
    fleet = RobotFleet(3)
    scheduler = MissionScheduler(fleet)
    m1 = scheduler.assign_mission("ROBOT-1")
    m2 = scheduler.assign_mission("ROBOT-2")
    m1.execute()
    m2.execute()
    m2.fail()
    summary = scheduler.get_summary()
    assert summary["total"] == 2
    assert summary["in_progress"] == 1
    assert summary["failed"] == 1

def test_mission_logs():
    fleet = RobotFleet(3)
    scheduler = MissionScheduler(fleet)
    mission = scheduler.assign_mission("ROBOT-1")
    mission.execute()
    mission.fail()
    logs = mission.get_logs()
    assert len(logs) == 3
    assert "STARTED" in logs[0]
    assert "IN_PROGRESS" in logs[1]
    assert "FAILED" in logs[2]
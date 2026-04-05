import pytest
from robot import Robot

def test_initial_state():
    robot = Robot()
    assert robot.get_state() == "CHARGING"

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
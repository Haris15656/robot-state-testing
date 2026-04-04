import pytest
from robot import Robot

def test_initial_state():
    robot = Robot()
    assert robot.get_state() == "IDLE"

def test_start_from_idle():
    robot = Robot()
    robot.start()
    assert robot.get_state() == "MOVING"

def test_trigger_error_from_moving():
    robot = Robot()
    robot.start()
    robot.trigger_error()
    assert robot.get_state() == "ERROR"

def test_recovery_from_error():
    robot = Robot()
    robot.start()
    robot.trigger_error()
    robot.recover()
    assert robot.get_state() == "RECOVERY"

def test_full_cycle():
    robot = Robot()
    robot.start()
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
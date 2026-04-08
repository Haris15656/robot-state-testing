Here's the updated README. Replace everything in README.md with this:
markdown# Robot State Testing

A comprehensive automated testing suite simulating a real-world autonomous robot operations system.
Built to explore how robotics QA works in practice — inspired by the belief that complex systems
are only as good as their reliability.

## What This Simulates
A fleet of 3 autonomous robots receiving missions, navigating environments, handling obstacles,
recovering from faults, and reporting state changes — all validated through automated tests.

## Tech Stack
- Python 3.12
- Pytest
- pytest-html
- Custom auto-updating dark dashboard

## System Architecture
robot.py          — Robot state machine + RobotFleet manager
mission.py        — Mission lifecycle + MissionScheduler
conftest.py       — Auto-injects results into dashboard after every run
tests/            — 28 automated test cases
dashboard.html    — Live futuristic dark dashboard

## Robot States (7)
| State | Description |
|-------|-------------|
| IDLE | Robot is waiting, ready for mission |
| MOVING | Robot is actively navigating |
| CHARGING | Robot is recharging battery |
| OBSTACLE_DETECTED | Robot has detected a blockage |
| ERROR | Robot has encountered a fault |
| EMERGENCY_STOP | Robot has been force-stopped |
| RECOVERY | Robot is recovering before reset |

## State Machine Flows
Main:       IDLE → MOVING → ERROR → RECOVERY → IDLE
Charging:   IDLE → CHARGING → IDLE
Obstacle:   MOVING → OBSTACLE_DETECTED → MOVING or ERROR
Emergency:  MOVING → EMERGENCY_STOP → RECOVERY → IDLE

## Fleet & Mission System
- **RobotFleet** — manages 3 independent robots simultaneously
- **MissionScheduler** — assigns, tracks, and summarizes missions per robot
- **Logging** — every state transition is timestamped and logged per robot
- **Independence** — robots operate without affecting each other's state

## Test Coverage (28 Tests)

### Single Robot State Tests (17)
| # | Test | Description | Status |
|---|------|-------------|--------|
| 01 | test_initial_state | Robot starts in IDLE | ✅ |
| 02 | test_start_from_idle | IDLE → MOVING | ✅ |
| 03 | test_charging_cycle | IDLE → CHARGING → IDLE | ✅ |
| 04 | test_cannot_charge_while_moving | Invalid transition blocked | ✅ |
| 05 | test_obstacle_detected_while_moving | MOVING → OBSTACLE_DETECTED | ✅ |
| 06 | test_clear_obstacle_resumes_moving | OBSTACLE → MOVING | ✅ |
| 07 | test_error_from_obstacle | OBSTACLE → ERROR | ✅ |
| 08 | test_emergency_stop_from_moving | MOVING → EMERGENCY_STOP | ✅ |
| 09 | test_emergency_stop_from_obstacle | OBSTACLE → EMERGENCY_STOP | ✅ |
| 10 | test_recovery_from_emergency_stop | EMERGENCY → RECOVERY | ✅ |
| 11 | test_full_cycle | Full IDLE→MOVING→ERROR→RECOVERY→IDLE | ✅ |
| 12 | test_full_cycle_with_obstacle | Full cycle including obstacle | ✅ |
| 13 | test_cannot_start_from_error | Invalid transition raises exception | ✅ |
| 14 | test_cannot_recover_from_idle | Invalid transition raises exception | ✅ |
| 15 | test_cannot_emergency_stop_from_idle | Invalid transition raises exception | ✅ |
| 16 | test_robot_logging | State changes are logged correctly | ✅ |
| 17 | test_robot_id_in_logs | Robot ID appears in all log entries | ✅ |

### Fleet Tests (4)
| # | Test | Description | Status |
|---|------|-------------|--------|
| 18 | test_fleet_initialization | All 3 robots start in IDLE | ✅ |
| 19 | test_fleet_robots_are_independent | Robots don't affect each other | ✅ |
| 20 | test_fleet_all_logs | Combined logs from all robots | ✅ |
| 21 | test_fleet_simultaneous_errors | All robots can error simultaneously | ✅ |

### Mission Tests (7)
| # | Test | Description | Status |
|---|------|-------------|--------|
| 22 | test_mission_assignment | Mission assigned to IDLE robot | ✅ |
| 23 | test_mission_execution | Mission moves robot to MOVING | ✅ |
| 24 | test_mission_failure | Failed mission triggers ERROR state | ✅ |
| 25 | test_cannot_assign_mission_to_busy_robot | Busy robot rejects new mission | ✅ |
| 26 | test_multiple_missions_different_robots | 3 robots run missions simultaneously | ✅ |
| 27 | test_mission_scheduler_summary | Summary tracks all mission statuses | ✅ |
| 28 | test_mission_logs | Mission lifecycle is fully logged | ✅ |

## How to Run
```bash
pip install pytest pytest-html
pytest tests/ -v --html=reports/report.html
```

## Dashboard
Open `dashboard.html` in your browser to view live test results.
The dashboard auto-updates every time tests are run via conftest injection.

## Motivation
Built after realizing that my AI fitness app OptiFit would fail silently
when MediaPipe misdetected exercises — I wanted to understand how to properly
test systems that cannot afford to fail. Autonomous robots face the same problem
at much higher stakes.
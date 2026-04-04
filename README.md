# Robot State Testing

Automated test suite for validating autonomous robot state transitions using pytest.
Simulates real-world robotic system behavior including fault handling and recovery mechanisms.

## Tech Stack
- Python 3.12
- Pytest
- pytest-html

## State Machine
IDLE → MOVING → ERROR → RECOVERY → IDLE

## Project Structure
robot-state-testing/
├── robot.py
├── tests/
│   └── test_robot.py
└── reports/
└── report.html

## Test Cases
| Test | Description | Status |
|------|-------------|--------|
| test_initial_state | Robot starts in IDLE state | ✅ |
| test_start_from_idle | Robot moves to MOVING from IDLE | ✅ |
| test_trigger_error_from_moving | Robot transitions to ERROR from MOVING | ✅ |
| test_recovery_from_error | Robot enters RECOVERY from ERROR | ✅ |
| test_full_cycle | Full state cycle IDLE→MOVING→ERROR→RECOVERY→IDLE | ✅ |
| test_cannot_start_from_error | Invalid transition raises exception | ✅ |
| test_cannot_recover_from_idle | Invalid transition raises exception | ✅ |

## How to Run
```bash
pip install pytest pytest-html
pytest tests/ -v --html=reports/report.html
```
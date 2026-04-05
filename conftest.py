import pytest
import json
import time

results = {"tests": [], "summary": {"passed": 0, "failed": 0, "total": 0, "duration": 0}}
start_time = None

def pytest_sessionstart(session):
    global start_time
    start_time = time.time()

def pytest_runtest_logreport(report):
    if report.when == "call":
        results["tests"].append({
            "name": report.nodeid.split("::")[-1],
            "status": "PASSED" if report.passed else "FAILED",
            "duration": round(report.duration, 3)
        })
        if report.passed:
            results["summary"]["passed"] += 1
        else:
            results["summary"]["failed"] += 1

def pytest_sessionfinish(session, exitstatus):
    results["summary"]["total"] = len(results["tests"])
    results["summary"]["duration"] = round(time.time() - start_time, 2)

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    with open("dashboard.html", "r") as f:
        html = f.read()

    data_js = f"const data = {json.dumps(results, indent=2)};"
    import re
    html = re.sub(r"const data = \{.*?\};", data_js, html, flags=re.DOTALL)

    with open("dashboard.html", "w") as f:
        f.write(html)
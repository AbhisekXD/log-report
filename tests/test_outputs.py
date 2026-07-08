import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected():
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def test_report_exists():
    """Success criterion 1: the report is saved to /app/report.json."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"


def test_report_is_valid_json_object():
    """Success criterion 2: the report is a JSON object with the required fields."""
    data = json.loads(REPORT_PATH.read_text())
    assert isinstance(data, dict)
    for key in ("total_requests", "unique_ips", "top_path"):
        assert key in data, f"missing key: {key}"


def test_total_requests_correct():
    """Success criterion 3: total_requests matches the number of log lines."""
    data = json.loads(REPORT_PATH.read_text())
    assert data["total_requests"] == _expected()["total_requests"]


def test_unique_ips_correct():
    """Success criterion 4: unique_ips matches the number of distinct client IPs."""
    data = json.loads(REPORT_PATH.read_text())
    assert data["unique_ips"] == _expected()["unique_ips"]


def test_top_path_correct():
    """Success criterion 5: top_path matches the most frequently requested path."""
    data = json.loads(REPORT_PATH.read_text())
    assert data["top_path"] == _expected()["top_path"]

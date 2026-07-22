import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")

REQUEST_RE = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH|OPTIONS)\s+(\S+)\s+HTTP/\d\.\d"')


def _expected_stats():
    """Independently recompute total_requests, unique_ips, top_path from the raw log."""
    total = 0
    ips = set()
    paths = Counter()
    for line in LOG_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        match = REQUEST_RE.search(line)
        if match:
            paths[match.group(1)] += 1
    top_path = paths.most_common(1)[0][0] if paths else None
    return total, len(ips), top_path


def _load_report():
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    text = REPORT_PATH.read_text()
    assert text.strip(), "report.json is empty"
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"report.json is not valid JSON: {exc}")


def test_report_is_valid_json():
    """Success criterion 1: /app/report.json exists and contains valid JSON."""
    _load_report()


def test_report_has_exactly_expected_keys():
    """Success criterion 2: the JSON object has exactly total_requests, unique_ips, top_path."""
    report = _load_report()
    assert set(report.keys()) == {"total_requests", "unique_ips", "top_path"}, (
        f"expected exactly total_requests, unique_ips, top_path, got {sorted(report.keys())}"
    )


def test_total_requests_matches_log():
    """Success criterion 3: total_requests equals the number of non-blank lines in access.log."""
    report = _load_report()
    expected_total, _, _ = _expected_stats()
    assert report["total_requests"] == expected_total


def test_unique_ips_matches_log():
    """Success criterion 4: unique_ips equals the number of distinct client IPs in access.log."""
    report = _load_report()
    _, expected_unique_ips, _ = _expected_stats()
    assert report["unique_ips"] == expected_unique_ips


def test_top_path_matches_log():
    """Success criterion 5: top_path equals the most frequently requested path in access.log."""
    report = _load_report()
    _, _, expected_top_path = _expected_stats()
    assert report["top_path"] == expected_top_path

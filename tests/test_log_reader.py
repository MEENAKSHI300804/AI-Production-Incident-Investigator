
from src.log_reader import (
    extract_errors,
    count_errors,
    find_most_frequent_error,
    generate_incident_report
)


def test_extract_errors():
    logs = [
        "2026-11-26 10:00:01 INFO Application started",
        "2026-11-26 10:01:10 ERROR Database connection timeout",
        "2026-11-26 10:01:12 ERROR Payment processing failed"
    ]

    result = extract_errors(logs)

    assert len(result) == 2
    assert "ERROR Database connection timeout" in result[0]


def test_count_errors():
    error_logs = [
        "2026-11-26 10:01:10 ERROR Database connection timeout",
        "2026-11-26 10:01:12 ERROR Payment processing failed",
        "2026-11-26 10:01:30 ERROR Database connection timeout"
    ]

    result = count_errors(error_logs)

    assert result["Database connection timeout"] == 2
    assert result["Payment processing failed"] == 1


def test_find_most_frequent_error():
    error_count = {
        "Database connection timeout": 4,
        "Payment processing failed": 1,
        "Order creation failed": 1
    }

    error, count = find_most_frequent_error(error_count)

    assert error == "Database connection timeout"
    assert count == 4


def test_find_most_frequent_error_empty():
    error, count = find_most_frequent_error({})

    assert error is None
    assert count == 0


def test_generate_incident_report():
    logs = [
        "2026-11-26 10:00:01 INFO Application started",
        "2026-11-26 10:01:10 ERROR Database connection timeout",
        "2026-11-26 10:01:20 ERROR Payment processing failed",
        "2026-11-26 10:01:40 ERROR Database connection timeout"
    ]

    error_logs = extract_errors(logs)
    error_count = count_errors(error_logs)

    report = generate_incident_report(
        logs,
        error_logs,
        error_count
    )

    assert report["total_logs"] == 4
    assert report["total_errors"] == 3
    assert report["error_frequency"]["Database connection timeout"] == 2
    assert report["most_frequent_error"] == "Database connection timeout"
    assert report["occurrences"] == 2
    assert report["duration_seconds"] == 30.0

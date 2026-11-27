
from src.analysis.error_pattern_detector import (
    detect_repeated_errors,
    detect_errors_close_in_time
)


def test_detect_repeated_errors():

    error_logs = [
        "2026-11-27 10:01:10 ERROR Database connection timeout",
        "2026-11-27 10:01:12 ERROR Payment processing failed",
        "2026-11-27 10:01:30 ERROR Database connection timeout",
        "2026-11-27 10:01:35 ERROR Database connection timeout"
    ]

    result = detect_repeated_errors(error_logs)

    assert result == {
        "Database connection timeout": 3
    }


def test_detect_errors_close_in_time():

    error_logs = [
        "2026-11-27 10:01:10 ERROR Database connection timeout",
        "2026-11-27 10:01:12 ERROR Payment processing failed",
        "2026-11-27 10:01:15 ERROR Order creation failed",
        "2026-11-27 10:02:00 ERROR Service unavailable"
    ]

    result = detect_errors_close_in_time(
        error_logs,
        time_window=10
    )

    assert len(result) == 2

    assert len(result[0]["related_errors"]) == 2

    assert len(result[1]["related_errors"]) == 1


def test_no_repeated_errors():

    error_logs = [
        "2026-11-27 10:01:10 ERROR Database connection timeout",
        "2026-11-27 10:01:12 ERROR Payment processing failed"
    ]

    result = detect_repeated_errors(error_logs)

    assert result == {}


def test_no_errors_close_in_time():

    error_logs = [
        "2026-11-27 10:01:10 ERROR Database connection timeout",
        "2026-11-27 10:02:00 ERROR Payment processing failed"
    ]

    result = detect_errors_close_in_time(
        error_logs,
        time_window=10
    )

    assert result == []

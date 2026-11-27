
from datetime import datetime, timedelta


def detect_repeated_errors(error_logs):
    error_frequency = {}

    for log in error_logs:
        message = log.split("ERROR", 1)[1].strip()

        error_frequency[message] = (
            error_frequency.get(message, 0) + 1
        )

    repeated_errors = {}

    for message, count in error_frequency.items():
        if count > 1:
            repeated_errors[message] = count

    return repeated_errors


def detect_errors_close_in_time(error_logs, time_window=10):
    detected_groups = []

    for i in range(len(error_logs)):
        current_time = get_timestamp(error_logs[i])

        nearby_errors = []

        for j in range(i + 1, len(error_logs)):
            next_time = get_timestamp(error_logs[j])

            difference = (next_time - current_time).total_seconds()

            if difference <= time_window:
                nearby_errors.append(error_logs[j])
            else:
                break

        if nearby_errors:
            detected_groups.append({
                "starting_error": error_logs[i],
                "related_errors": nearby_errors
            })

    return detected_groups


def get_timestamp(error):
    timestamp_text = error.split(" ERROR", 1)[0]

    return datetime.strptime(
        timestamp_text,
        "%Y-%m-%d %H:%M:%S"
    )

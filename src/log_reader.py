
from datetime import datetime
import json


def read_logs(file_path):
    with open(file_path, "r") as file:
        return file.readlines()


def extract_errors(logs):
    error_logs = []

    for log in logs:
        if "ERROR" in log:
            error_logs.append(log.strip())

    return error_logs


def count_errors(error_logs):
    error_count = {}

    for error in error_logs:
        message = error.split("ERROR", 1)[1].strip()
        error_count[message] = error_count.get(message, 0) + 1

    return error_count


def get_timestamp(error):
    timestamp_text = error.split(" ERROR", 1)[0]

    return datetime.strptime(
        timestamp_text,
        "%Y-%m-%d %H:%M:%S"
    )


def find_most_frequent_error(error_count):
    if not error_count:
        return None, 0

    error = max(error_count, key=error_count.get)

    return error, error_count[error]


def generate_incident_report(logs, error_logs, error_count):

    if not error_logs:
        return {
            "total_logs": len(logs),
            "total_errors": 0,
            "error_frequency": {},
            "first_observed_error": None,
            "most_frequent_error": None,
            "occurrences": 0,
            "duration_seconds": 0
        }

    most_frequent_error, frequency = find_most_frequent_error(error_count)

    first_error = error_logs[0]
    last_error = error_logs[-1]

    start_time = get_timestamp(first_error)
    end_time = get_timestamp(last_error)

    duration = (end_time - start_time).total_seconds()

    report = {
        "total_logs": len(logs),
        "total_errors": len(error_logs),
        "error_frequency": error_count,
        "first_observed_error": first_error,
        "most_frequent_error": most_frequent_error,
        "occurrences": frequency,
        "duration_seconds": duration,
        "investigation_note": "Most frequent error requires further investigation."
    }

    return report


def save_report(report, output_file):
    with open(output_file, "w") as file:
        json.dump(report, file, indent=4)

    print("\nIncident report saved successfully:", output_file)


# MAIN PROGRAM

file_path = "data/incident_001.log"
output_file = "data/incident_report.json"

logs = read_logs(file_path)
error_logs = extract_errors(logs)
error_count = count_errors(error_logs)

report = generate_incident_report(logs, error_logs, error_count)

print("\nINCIDENT REPORT")
print("====================")
print(json.dumps(report, indent=4))

save_report(report, output_file)

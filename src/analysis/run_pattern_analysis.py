
import json

from src.log_reader import read_logs, extract_errors

from src.analysis.error_pattern_detector import (
    detect_repeated_errors,
    detect_errors_close_in_time
)


def run_analysis():

    file_path = "data/incident_001.log"

    logs = read_logs(file_path)

    error_logs = extract_errors(logs)

    repeated_errors = detect_repeated_errors(error_logs)

    time_patterns = detect_errors_close_in_time(
        error_logs,
        time_window=10
    )

    report = {
        "incident_file": file_path,
        "total_errors": len(error_logs),
        "repeated_errors": repeated_errors,
        "time_based_patterns": time_patterns,
        "investigation_note": (
            "These patterns are investigation clues, "
            "not confirmed root causes."
        )
    }

    print("\nINTELLIGENT ERROR PATTERN REPORT")
    print("================================")

    print(json.dumps(report, indent=4))

    with open("data/pattern_report.json", "w") as file:
        json.dump(report, file, indent=4)

    print("\nPattern report saved successfully!")


if __name__ == "__main__":
    run_analysis()

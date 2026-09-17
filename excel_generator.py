import pandas as pd


def create_excel(test_cases, output_file="test_cases.xlsx"):
    """
    Create an Excel file from generated test cases.
    """

    rows = []

    for test_case in test_cases:
        rows.append({
            "Test Case ID": test_case.get("test_case_id", ""),
            "Module": test_case.get("module", ""),
            "Requirement": test_case.get("requirement", ""),
            "Test Scenario": test_case.get("test_scenario", ""),
            "Test Type": test_case.get("test_type", ""),
            "Preconditions": test_case.get("preconditions", ""),
            "Test Steps": "\n".join(
                test_case.get("test_steps", [])
            ),
            "Test Data": test_case.get("test_data", ""),
            "Expected Result": test_case.get("expected_result", ""),
            "Priority": test_case.get("priority", "")
        })

    df = pd.DataFrame(rows)

    df.to_excel(
        output_file,
        index=False,
        engine="openpyxl"
    )

    return output_file
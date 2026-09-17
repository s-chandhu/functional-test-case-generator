from document_parser import extract_text
from test_case_generator import generate_test_cases


# Read the sample requirements
requirements = extract_text("sample.txt")

print("\nRequirements extracted successfully.")
print("Sending requirements to local AI...\n")


# Generate test cases
result = generate_test_cases(requirements)


print("=" * 70)
print("GENERATED FUNCTIONAL TEST CASES")
print("=" * 70)


for test_case in result["test_cases"]:

    print("\n" + "-" * 70)

    print("Test Case ID :", test_case["test_case_id"])
    print("Module       :", test_case["module"])
    print("Test Type    :", test_case["test_type"])
    print("Requirement  :", test_case["requirement"])
    print("Scenario     :", test_case["test_scenario"])
    print("Preconditions:", test_case["preconditions"])

    print("\nTest Steps:")

    for number, step in enumerate(
        test_case["test_steps"],
        start=1
    ):
        print(f"  {number}. {step}")

    print("\nTest Data    :", test_case["test_data"])
    print("Expected     :", test_case["expected_result"])
    print("Priority     :", test_case["priority"])
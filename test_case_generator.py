import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_test_cases(requirements_text):
    """
    Generate functional test cases using a local Ollama model.
    """

    prompt = f"""
You are a senior software QA engineer.

Analyze the requirements below and generate functional test cases.

STRICT RULES:

1. Use ONLY information explicitly stated in the requirements.

2. Never invent requirements, features, screens, buttons,
   error messages, business rules, preconditions, or system behavior.

3. Do not add "internet access", "database access", "browser",
   "server", or similar assumptions unless explicitly stated.

4. If a precondition is not explicitly stated, use:
   "No specific precondition stated in the requirement."

5. If an exact error message is not provided, use:
   "Appropriate error message should be displayed."

6. Generate only FUNCTIONAL test cases.

7. Do not generate performance, load, security, penetration,
   usability, compatibility, or unit tests unless explicitly
   required by the document.

8. Generate positive tests when valid behavior is specified.

9. Generate negative tests when invalid behavior is specified.

10. For mandatory fields, the negative test MUST use an empty
    value for that field.

11. For validation rules, use test data that directly represents
    the stated validation condition.

12. Generate boundary tests when an explicit boundary exists.

13. For a minimum length of N characters, generate at least:
    - one test with fewer than N characters
    - one test with exactly N characters

14. Generate business-rule tests when an explicit business rule exists.

15. Generate workflow tests when a workflow is explicitly described.

16. Do not create duplicate test cases.

17. Every test case must map to a specific requirement.

18. Do not assume behavior that is not stated.

19. For numeric rules, test the boundary values explicitly.

20. Test steps must be detailed enough to execute the test case.

21. Never replace multiple required actions with a vague step such as
    "Perform the required actions."

22. If a requirement specifies 5 attempts, explicitly list all 5 attempts
    in the test steps.

TEST TYPES:

- Positive
- Negative
- Validation
- Boundary
- Business Rule
- Workflow
- Error Handling

PRIORITY RULES:

- High: critical login, business rule, or workflow behavior
- Medium: normal validation or negative behavior
- Low: minor functional behavior

Return ONLY valid JSON.

Do not include markdown.
Do not include ```json.
Do not include explanations outside the JSON.

Use exactly this structure:

{{
    "test_cases": [
        {{
            "test_case_id": "TC-001",
            "module": "Login",
            "requirement": "Requirement text",
            "test_scenario": "Scenario description",
            "test_type": "Positive",
            "preconditions": "Precondition",
            "test_steps": [
                "Step 1",
                "Step 2",
                "Step 3"
            ],
            "test_data": "Test data",
            "expected_result": "Expected result",
            "priority": "High"
        }}
    ]
}}

REQUIREMENTS:

-----------------------------
{requirements_text}
-----------------------------
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    ai_output = data["response"]

    result = json.loads(ai_output)

    return result
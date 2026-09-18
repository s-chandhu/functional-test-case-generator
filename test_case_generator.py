import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError


# Load environment variables from .env
load_dotenv()


# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )


# Create Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Gemini model
MODEL_NAME = "gemini-3.6-flash"


# Expected JSON structure
TEST_CASE_SCHEMA = {
    "type": "object",
    "properties": {
        "test_cases": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "test_case_id": {
                        "type": "string"
                    },
                    "module": {
                        "type": "string"
                    },
                    "requirement": {
                        "type": "string"
                    },
                    "test_scenario": {
                        "type": "string"
                    },
                    "test_type": {
                        "type": "string"
                    },
                    "preconditions": {
                        "type": "string"
                    },
                    "test_steps": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "test_data": {
                        "type": "string"
                    },
                    "expected_result": {
                        "type": "string"
                    },
                    "priority": {
                        "type": "string"
                    }
                },
                "required": [
                    "test_case_id",
                    "module",
                    "requirement",
                    "test_scenario",
                    "test_type",
                    "preconditions",
                    "test_steps",
                    "test_data",
                    "expected_result",
                    "priority"
                ]
            }
        }
    },
    "required": [
        "test_cases"
    ]
}


def generate_test_cases(requirements_text):
    """
    Generate functional test cases from requirement text
    using Gemini.
    """

    prompt = f"""
You are a senior software QA engineer.

Analyze the requirements below and generate functional test cases.

STRICT RULES:

1. Use ONLY information explicitly stated in the requirements.

2. Never invent requirements, features, screens, buttons,
error messages, business rules, preconditions, or system behavior.

3. Do not assume internet access, database access, browser,
server, or any other environment requirement.

4. If a precondition is not explicitly stated, use:
"No specific precondition stated in the requirement."

5. If an exact error message is not provided, use:
"Appropriate error message should be displayed."

6. Generate ONLY functional test cases.

7. Do not generate performance, load, security, penetration,
usability, compatibility, or unit tests.

8. Generate positive tests when valid behavior is specified.

9. Generate negative tests when invalid behavior is specified.

10. For mandatory fields, use an empty value for that field
when creating the negative test.

11. For validation rules, use test data that directly represents
the stated validation condition.

12. Generate boundary tests when an explicit boundary exists.

13. For a minimum length of N characters, generate:
- one test with fewer than N characters
- one test with exactly N characters.

14. Generate business-rule tests when an explicit business rule exists.

15. Generate workflow tests when a workflow is explicitly described.

16. Do not create duplicate test cases.

17. Every test case must map to a specific requirement.

18. Each test case must map to ONE specific numbered requirement only.

19. Do not combine multiple requirements in the "requirement" field.

20. If one requirement naturally leads to another requirement's result,
map the test case to the primary requirement only.

21. Test steps must NOT contain step numbers.

Return steps like:
"Enter a valid registered email address."

Do NOT return:
"1. Enter a valid registered email address."

22. Do not use vague steps such as:
"Perform the required action."
"Perform action to view previous orders."
"Perform log out action."

23. When the requirement states a specific action, describe that
action directly using only information from the requirement.

24. Do not invent names of buttons, links, screens, menus, fields,
pages, or other UI elements unless explicitly stated.

25. Test steps must be detailed enough to execute the test case.

26. Never replace multiple required actions with:
"Perform the required actions."

27. If a requirement specifies multiple actions,
explicitly list every required action.

28. If the document does NOT contain software/application/system
functional requirements, return an empty test_cases list.

29. Do not convert financial, business, marketing, management,
or company information into software test cases.

30. Only generate a test case when the requirement describes
software behavior that can actually be functionally tested.

31. Do not invent UI elements or system behavior.

32. Do not invent exact error messages.

33. Do not create test cases simply because the document contains
numbers, percentages, financial values, or business statements.

34. Keep the requirement field faithful to the original requirement.
Do not merge multiple numbered requirements.

35. Do not create tests for information that is not a software
functional requirement.

REQUIREMENTS:

{requirements_text}
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:
            print(
                f"\nCalling Gemini "
                f"(attempt {attempt + 1}/{max_retries})...",
                flush=True
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": TEST_CASE_SCHEMA
                }
            )

            print(
                "Gemini response received.",
                flush=True
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            ai_output = response.text.strip()

            if not ai_output:
                raise ValueError(
                    "Gemini returned empty response text."
                )

            result = json.loads(
                ai_output
            )

            # Clean step numbering if Gemini adds it
            for test_case in result.get(
                "test_cases",
                []
            ):

                cleaned_steps = []

                for step in test_case.get(
                    "test_steps",
                    []
                ):

                    step = str(step).strip()

                    step = re.sub(
                        r"^\s*\d+[\.\)]\s*",
                        "",
                        step
                    )

                    cleaned_steps.append(
                        step
                    )

                test_case["test_steps"] = cleaned_steps

            print(
                "\nJSON parsed successfully.",
                flush=True
            )

            return result

        except ServerError as e:

            error_text = str(e)

            print(
                f"\nGemini server error: {error_text}",
                flush=True
            )

            # Retry temporary Gemini 503 errors
            if (
                "503" in error_text
                and attempt < max_retries - 1
            ):

                wait_time = (
                    attempt + 1
                ) * 3

                print(
                    f"Retrying in {wait_time} seconds...",
                    flush=True
                )

                time.sleep(
                    wait_time
                )

            else:
                raise

        except json.JSONDecodeError as e:

            raise ValueError(
                "Gemini returned invalid JSON.\n"
                f"Raw response:\n{repr(response.text)}"
            ) from e

        except Exception as e:

            error_text = str(e)

            # Handle Gemini quota exhaustion
            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):

                raise RuntimeError(
                    "Gemini free-tier quota has been reached. "
                    "Please try again after the quota resets "
                    "or use a Gemini API project with available quota."
                ) from e

            # Handle all other unexpected errors
            raise
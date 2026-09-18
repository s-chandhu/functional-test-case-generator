import os

import streamlit as st

from document_parser import extract_text
from test_case_generator import generate_test_cases
from excel_generator import create_excel


st.set_page_config(
    page_title="Functional Test Case Generator",
    page_icon="🧪",
    layout="wide"
)


st.title("🧪 Functional Test Case Generator")

st.write(
    "Upload a requirements document and generate "
    "functional test cases using AI."
)


uploaded_file = st.file_uploader(
    "Upload your requirement document",
    type=["pdf", "docx", "txt"]
)


if uploaded_file is not None:

    st.success(
        f"File uploaded successfully: {uploaded_file.name}"
    )

    if st.button(
        "🧪 Generate Functional Test Cases",
        type="primary"
    ):

        temp_file_path = None

        try:

            # Get uploaded file extension
            file_extension = os.path.splitext(
                uploaded_file.name
            )[1].lower()

            # Create temporary file path
            temp_file_path = (
                f"uploaded_document{file_extension}"
            )

            # Save uploaded file temporarily
            with open(
                temp_file_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            # -----------------------------------
            # STEP 1: Extract document text
            # -----------------------------------

            with st.spinner(
                "📄 Reading requirements document..."
            ):

                extracted_text = extract_text(
                    temp_file_path
                )

            if not extracted_text.strip():

                st.warning(
                    "No readable text was found in the document."
                )

            else:

                st.success(
                    "Requirements extracted successfully."
                )

                # Show extracted requirements
                with st.expander(
                    "📄 View Extracted Requirements"
                ):

                    st.text_area(
                        "Document Content",
                        extracted_text,
                        height=350
                    )

                # -----------------------------------
                # STEP 2: Generate test cases
                # -----------------------------------

                with st.spinner(
                    "🤖 Gemini is generating functional test cases..."
                ):

                    result = generate_test_cases(
                        extracted_text
                    )

                test_cases = result.get(
                    "test_cases",
                    []
                )

                # -----------------------------------
                # STEP 3: Check generated cases
                # -----------------------------------

                if not test_cases:

                    st.warning(
                        "No functional software requirements "
                        "were identified in the document."
                    )

                else:

                    st.success(
                        f"Generated {len(test_cases)} "
                        "functional test cases."
                    )

                    # -----------------------------------
                    # STEP 4: Display test case summary
                    # -----------------------------------

                    st.subheader(
                        "🧪 Generated Functional Test Cases"
                    )

                    display_rows = []

                    for test_case in test_cases:

                        display_rows.append({

                            "Test Case ID":
                                test_case.get(
                                    "test_case_id",
                                    ""
                                ),

                            "Module":
                                test_case.get(
                                    "module",
                                    ""
                                ),

                            "Test Type":
                                test_case.get(
                                    "test_type",
                                    ""
                                ),

                            "Requirement":
                                test_case.get(
                                    "requirement",
                                    ""
                                ),

                            "Test Scenario":
                                test_case.get(
                                    "test_scenario",
                                    ""
                                ),

                            "Priority":
                                test_case.get(
                                    "priority",
                                    ""
                                )
                        })

                    st.dataframe(
                        display_rows,
                        use_container_width=True,
                        hide_index=True
                    )

                    # -----------------------------------
                    # STEP 5: Display detailed cases
                    # -----------------------------------

                    st.subheader(
                        "🔍 Test Case Details"
                    )

                    for test_case in test_cases:

                        test_case_id = test_case.get(
                            "test_case_id",
                            ""
                        )

                        test_scenario = test_case.get(
                            "test_scenario",
                            ""
                        )

                        with st.expander(
                            f"{test_case_id} - {test_scenario}"
                        ):

                            st.write(
                                "**Module:**",
                                test_case.get(
                                    "module",
                                    ""
                                )
                            )

                            st.write(
                                "**Test Type:**",
                                test_case.get(
                                    "test_type",
                                    ""
                                )
                            )

                            st.write(
                                "**Requirement:**",
                                test_case.get(
                                    "requirement",
                                    ""
                                )
                            )

                            st.write(
                                "**Preconditions:**",
                                test_case.get(
                                    "preconditions",
                                    ""
                                )
                            )

                            st.write(
                                "**Test Data:**",
                                test_case.get(
                                    "test_data",
                                    ""
                                )
                            )

                            st.write(
                                "**Expected Result:**",
                                test_case.get(
                                    "expected_result",
                                    ""
                                )
                            )

                            st.write(
                                "**Priority:**",
                                test_case.get(
                                    "priority",
                                    ""
                                )
                            )

                            st.write(
                                "**Test Steps:**"
                            )

                            for number, step in enumerate(
                                test_case.get(
                                    "test_steps",
                                    []
                                ),
                                start=1
                            ):

                                st.write(
                                    f"{number}. {step}"
                                )

                    # -----------------------------------
                    # STEP 6: Create Excel file
                    # -----------------------------------

                    output_file = (
                        "generated_test_cases.xlsx"
                    )

                    create_excel(
                        test_cases,
                        output_file
                    )

                    # Read Excel file
                    with open(
                        output_file,
                        "rb"
                    ) as file:

                        excel_data = file.read()

                    # -----------------------------------
                    # STEP 7: Download Excel
                    # -----------------------------------

                    st.subheader(
                        "📥 Download"
                    )

                    st.download_button(
                        label="📥 Download Excel Test Cases",

                        data=excel_data,

                        file_name="functional_test_cases.xlsx",

                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.spreadsheetml.sheet"
                        )
                    )


        except RuntimeError as e:

            # -----------------------------------
            # Gemini quota error
            # -----------------------------------

            error_message = str(e)

            if "quota" in error_message.lower():

                st.error(
                    "⚠️ Gemini free-tier quota has been reached."
                )

                st.info(
                    "Please try again after the Gemini quota "
                    "resets or use a Gemini API project with "
                    "available quota."
                )

            else:

                st.error(
                    f"An error occurred: {error_message}"
                )


        except Exception as e:

            # -----------------------------------
            # Other errors
            # -----------------------------------

            st.error(
                f"An unexpected error occurred: {e}"
            )


        finally:

            # Delete temporary uploaded file
            if (
                temp_file_path is not None
                and os.path.exists(
                    temp_file_path
                )
            ):

                os.remove(
                    temp_file_path
                )
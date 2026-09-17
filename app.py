import os
import tempfile
import requests

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
    "Upload a requirements document and generate functional "
    "test cases automatically using AI."
)


# ---------------------------------------------------------
# Upload document
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your requirement document",
    type=["pdf", "docx", "txt"]
)


if uploaded_file is not None:

    st.success(
        f"File uploaded successfully: {uploaded_file.name}"
    )

    # -----------------------------------------------------
    # Generate test cases
    # -----------------------------------------------------

    if st.button(
        "🧪 Generate Functional Test Cases",
        type="primary"
    ):

        temp_file_path = None

        try:

            # Get file extension
            file_extension = os.path.splitext(
                uploaded_file.name
            )[1]

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_file_path = temp_file.name


            # -------------------------------------------------
            # Extract requirements
            # -------------------------------------------------

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

                # -------------------------------------------------
                # Show extracted requirements
                # -------------------------------------------------

                st.subheader(
                    "📄 Extracted Requirements"
                )

                with st.expander(
                    "View document content",
                    expanded=False
                ):

                    st.text_area(
                        "Requirements",
                        extracted_text,
                        height=300
                    )


                # -------------------------------------------------
                # Generate AI test cases
                # -------------------------------------------------

                with st.spinner(
                    "🤖 AI is generating functional test cases..."
                ):

                    result = generate_test_cases(
                        extracted_text
                    )


                test_cases = result.get(
                    "test_cases",
                    []
                )


                if not test_cases:

                    st.warning(
                        "The AI did not generate any test cases."
                    )

                else:

                    # -------------------------------------------------
                    # Display results
                    # -------------------------------------------------

                    st.success(
                        f"Successfully generated "
                        f"{len(test_cases)} functional test cases."
                    )


                    st.subheader(
                        "🧪 Generated Functional Test Cases"
                    )


                    # Create a simplified table for display
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


                    # -------------------------------------------------
                    # Detailed test cases
                    # -------------------------------------------------

                    st.subheader(
                        "🔍 Test Case Details"
                    )


                    for test_case in test_cases:

                        with st.expander(
                            f"{test_case.get('test_case_id', '')} - "
                            f"{test_case.get('test_scenario', '')}"
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


                    # -------------------------------------------------
                    # Create Excel
                    # -------------------------------------------------

                    output_file = "generated_test_cases.xlsx"

                    create_excel(
                        test_cases,
                        output_file
                    )


                    # -------------------------------------------------
                    # Download Excel
                    # -------------------------------------------------

                    with open(
                        output_file,
                        "rb"
                    ) as file:

                        excel_data = file.read()


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


        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to Ollama. "
                "Please make sure Ollama is running."
            )


        except Exception as e:

            st.error(
                f"An error occurred: {e}"
            )


        finally:

            # Delete temporary uploaded file
            if temp_file_path and os.path.exists(
                temp_file_path
            ):

                os.remove(
                    temp_file_path
                )
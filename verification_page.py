import streamlit as st
from predefined_datasets import predefined_datasets
from utils import perform_test
import numpy as np

def verification_page():
    st.title("🔍 Test Verification")

    # Track the previously selected test
    if "selected_test" not in st.session_state:
        st.session_state["selected_test"] = None
        st.session_state["run_verification"] = False

    # -- Select a test for verification (no longer using the sidebar) --
    test = st.selectbox("Select a test to verify", list(predefined_datasets.keys()))

    # Reset session state if the test changes
    if st.session_state["selected_test"] != test:
        st.session_state["selected_test"] = test
        st.session_state["run_verification"] = False

    # Validate predefined dataset
    if test not in predefined_datasets:
        st.error(f"Predefined dataset for '{test}' is missing or invalid.")
        return

    data = predefined_datasets[test]["data"]
    expected_result = predefined_datasets[test]["expected_result"]

    if not data or not expected_result:
        st.error(f"Predefined data or expected result is incomplete for '{test}'.")
        return

    # Create layout with columns
    col1, col2 = st.columns([2, 3])

    # Display Predefined Dataset and Expected Result on the left
    with col1:
        st.subheader("📋 Predefined Dataset")
        if isinstance(data, dict):
            for key, values in data.items():
                st.write(f"- **{key}**: {values}")
        else:
            st.write(data)

        st.subheader("✔️ Expected Result")
        st.markdown(f"**Expected Outcome:** {expected_result}")

        # Add the Run Verification button
        if st.button("Run Verification"):
            st.session_state["run_verification"] = True

    # Display Actual Result and Outcome on the right after clicking the button
    if st.session_state.get("run_verification", False):
        with col2:
            try:
                # Run the test
                st.subheader("🚀 Actual Result")
                actual_result = perform_test(test, data)
                st.write(actual_result)

                # Compare actual and expected results
                comparison_passed = True
                if isinstance(actual_result, dict) and isinstance(expected_result, dict):
                    # Compare dict keys one by one
                    for key in expected_result:
                        actual_value = actual_result.get(key)
                        expected_value = expected_result[key]

                        # Normalize numpy arrays for comparison
                        if isinstance(actual_value, np.ndarray):
                            actual_value = actual_value.tolist()
                        if isinstance(expected_value, np.ndarray):
                            expected_value = expected_value.tolist()

                        if isinstance(actual_value, dict) and isinstance(expected_value, dict):
                            # Compare nested dictionaries (e.g., critical_values)
                            for sub_key in expected_value:
                                sub_actual_value = actual_value.get(sub_key)
                                sub_expected_value = expected_value.get(sub_key)
                                if isinstance(sub_actual_value, np.ndarray):
                                    sub_actual_value = sub_actual_value.tolist()
                                if isinstance(sub_expected_value, np.ndarray):
                                    sub_expected_value = sub_expected_value.tolist()

                                comparison_passed &= np.isclose(
                                    sub_actual_value, sub_expected_value, atol=1e-6
                                )

                        elif isinstance(actual_value, list) and isinstance(expected_value, list):
                            # Compare lists element-wise
                            comparison_passed &= np.allclose(actual_value, expected_value, atol=1e-6)
                        elif isinstance(actual_value, (float, int)) and isinstance(expected_value, (float, int)):
                            # Compare scalar numbers with a tolerance
                            comparison_passed &= np.isclose(actual_value, expected_value, atol=1e-6)
                        else:
                            # Compare other types directly
                            comparison_passed &= (actual_value == expected_value)
                else:
                    comparison_passed = False

                # Display the success or error message
                if comparison_passed:
                    st.success("🎉 The test result matches the expected output!")
                else:
                    st.error("⚠️ The test result does not match the expected output.")

            except Exception as e:
                st.error(f"An error occurred while running the test: {e}")

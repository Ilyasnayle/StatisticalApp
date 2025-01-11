import streamlit as st
# Set the page layout and title
st.set_page_config(page_title="Statistical Analysis App - Developed by: Ilyas Nayle", layout="wide")

from utils import perform_test, display_graph
from constants import test_groups
from test_info import get_test_info
from verification_page import verification_page
from top_header import show_top_header
from datetime import datetime

# ---- Optional: Custom Styling with Inline CSS ----
st.markdown(
    """
    <style>
    /* Center the main container for better aesthetics */
    .main {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem 1rem;
        background-color: #f9f9f9;
        border-radius: 8px;
    }
    /* Custom style for titles */
    .title h1 {
        text-align: center;
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #2B547E;
    }
    /* Custom style for images */
    img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    /* Style for subheaders */
    .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #2B547E;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# -----------------------------------------------------------------------------
#                    HELPER FUNCTION TO CAPTURE USER DATA
# -----------------------------------------------------------------------------
def get_user_input(selected_test):
    data_input = None

    # ---------------------------------------------------------------------------
    # 1. Normality Tests (single list of numeric values)
    # ---------------------------------------------------------------------------
    if selected_test in [
        "Shapiro-Wilk Test",
        "D'Agostino's K² Test",
        "Anderson-Darling Test",
    ]:
        st.markdown("""
        **Example**: `1.2, 2.4, 3.5, 2.1`  
        Enter a single sequence of numeric values, separated by commas:
        """)
        data_str = st.text_area("Values for Normality Test", value="")
        if data_str:
            try:
                data_input = [float(x.strip()) for x in data_str.split(",") if x.strip()]
            except ValueError:
                st.error("⚠️ Please enter valid numeric data separated by commas.")

    # ---------------------------------------------------------------------------
    # 2. Kolmogorov-Smirnov Test (2-sample)
    # ---------------------------------------------------------------------------
    elif selected_test == "Kolmogorov-Smirnov Test":
        st.markdown("""
        **Example**:  
        - Sample 1: `1.5, 2.3, 3.7, 2.1, 4.0`  
        - Sample 2: `2.4, 3.5, 3.0, 3.7, 1.9`
        
        Enter two lists of comma-separated values:
        """)
        col1, col2 = st.columns(2)
        with col1:
            sample1_str = st.text_area("Sample 1", value="")
        with col2:
            sample2_str = st.text_area("Sample 2", value="")

        if sample1_str and sample2_str:
            try:
                sample1 = [float(x.strip()) for x in sample1_str.split(",") if x.strip()]
                sample2 = [float(x.strip()) for x in sample2_str.split(",") if x.strip()]
                data_input = {"Sample 1": sample1, "Sample 2": sample2}
            except ValueError:
                st.error("⚠️ Please enter valid numeric data for both samples.")

    # ---------------------------------------------------------------------------
    # 3. Student's T-test (unpaired, two groups)
    # ---------------------------------------------------------------------------
    elif selected_test == "Student's T-test":
        st.markdown("""
        **Example**:  
        - Group 1: `10, 12, 9, 14`  
        - Group 2: `8, 7, 11, 9`
        
        Enter two groups of comma-separated values:
        """)
        col1, col2 = st.columns(2)
        with col1:
            g1_str = st.text_area("Group 1", value="")
        with col2:
            g2_str = st.text_area("Group 2", value="")

        if g1_str and g2_str:
            try:
                group1 = [float(x.strip()) for x in g1_str.split(",") if x.strip()]
                group2 = [float(x.strip()) for x in g2_str.split(",") if x.strip()]
                data_input = {"Group 1": group1, "Group 2": group2}
            except ValueError:
                st.error("⚠️ Please enter valid numeric data for both groups.")

    # ---------------------------------------------------------------------------
    # 4. Paired Student's T-test (Before/After)
    # ---------------------------------------------------------------------------
    elif selected_test == "Paired Student's T-test":
        st.markdown("""
        **Example**:  
        - Before: `10, 12, 9, 14`  
        - After: `12, 14, 10, 15`
        
        Enter two paired datasets of comma-separated values:
        """)
        col1, col2 = st.columns(2)
        with col1:
            before_str = st.text_area("Before", value="")
        with col2:
            after_str = st.text_area("After", value="")

        if before_str and after_str:
            try:
                before = [float(x.strip()) for x in before_str.split(",") if x.strip()]
                after = [float(x.strip()) for x in after_str.split(",") if x.strip()]
                data_input = {"Before": before, "After": after}
            except ValueError:
                st.error("⚠️ Please enter valid numeric data for both 'Before' and 'After'.")

    # ---------------------------------------------------------------------------
    # 5. One-Way ANOVA (multiple groups in a dict)
    # ---------------------------------------------------------------------------
    elif selected_test == "One-Way ANOVA":
        st.markdown("""
        **Example**: For 3 groups  
        - Group 1: `10, 12, 9, 14`  
        - Group 2: `8, 7, 11, 9`  
        - Group 3: `15, 17, 14, 16`
        
        Enter data for each group (comma-separated):
        """)
        num_groups = st.number_input("Number of groups", min_value=2, max_value=10, value=3)
        anova_data = {}
        for i in range(num_groups):
            label = f"Group {i+1}"
            group_str = st.text_area(label, value="", key=f"oneway_group_{i}")
            if group_str:
                try:
                    anova_data[label] = [float(x.strip()) for x in group_str.split(",") if x.strip()]
                except ValueError:
                    st.error(f"⚠️ Please enter valid numeric data for {label}.")
        if anova_data:
            data_input = anova_data

    # ---------------------------------------------------------------------------
    # 6. Two-Way ANOVA (placeholder)
    # ---------------------------------------------------------------------------
    elif selected_test == "Two-Way ANOVA":
        st.markdown("""
        **Placeholder** for Two-Way ANOVA.  
        Typically, you'd have Factor A with several levels, Factor B with several levels,
        and multiple observations for each combination.

        **Example**: If Factor A has 2 levels (A1, A2), Factor B has 2 levels (B1, B2),
        you might enter:
        - A1, B1: `10, 12, 9, 14`
        - A1, B2: `8, 7, 11, 9`
        - A2, B1: `11, 9, 10, 13`
        - A2, B2: `15, 17, 14, 16`
        """)
        factorA = st.number_input("Levels in Factor A", min_value=2, max_value=5, value=2)
        factorB = st.number_input("Levels in Factor B", min_value=2, max_value=5, value=2)

        two_way_data = {}
        for a in range(int(factorA)):
            for b in range(int(factorB)):
                label = f"A{a+1}, B{b+1}"
                group_str = st.text_area(label, value="", key=f"twoway_{a}_{b}")
                if group_str:
                    try:
                        two_way_data[label] = [float(x.strip()) for x in group_str.split(",") if x.strip()]
                    except ValueError:
                        st.error(f"⚠️ Please enter valid numeric data for {label}.")

        if two_way_data:
            data_input = two_way_data

    # ---------------------------------------------------------------------------
    # 7. Repeated Measures ANOVA (placeholder)
    # ---------------------------------------------------------------------------
    elif selected_test == "Repeated Measures ANOVA":
        st.markdown("""
        **Placeholder** for Repeated Measures ANOVA.  
        Typically, you'd have multiple subjects, each measured under multiple conditions or time points.

        **Example**: If you have 5 subjects and 3 time points, each subject row might look like:  
        `10, 12, 14`  (Subject 1)  
        `8, 7, 9`     (Subject 2)  
        `15, 17, 16`  (Subject 3) etc.
        """)
        num_subjects = st.number_input("Number of subjects", min_value=2, max_value=20, value=5)
        num_conditions = st.number_input("Number of repeated conditions", min_value=2, max_value=10, value=3)

        repeated_data = {}
        for s in range(int(num_subjects)):
            label = f"Subject {s+1}"
            cond_str = st.text_area(label, value="", key=f"repeated_{s}")
            if cond_str:
                try:
                    vals = [float(x.strip()) for x in cond_str.split(",") if x.strip()]
                    if len(vals) != num_conditions:
                        st.warning(f"You entered {len(vals)} values, but expected {num_conditions} for {label}.")
                    repeated_data[label] = vals
                except ValueError:
                    st.error(f"⚠️ Please enter valid numeric data for {label}.")

        if repeated_data:
            data_input = repeated_data

    # ---------------------------------------------------------------------------
    # 8. Mann-Whitney U Test (2 independent samples, non-parametric)
    # ---------------------------------------------------------------------------
    elif selected_test == "Mann-Whitney U Test":
        st.markdown("""
        **Example**:  
        - Sample 1: `10, 12, 9, 14`  
        - Sample 2: `8, 7, 11, 9`
        
        Enter two independent samples (comma-separated):
        """)
        col1, col2 = st.columns(2)
        with col1:
            s1_str = st.text_area("Sample 1", value="")
        with col2:
            s2_str = st.text_area("Sample 2", value="")

        if s1_str and s2_str:
            try:
                sample1 = [float(x.strip()) for x in s1_str.split(",") if x.strip()]
                sample2 = [float(x.strip()) for x in s2_str.split(",") if x.strip()]
                data_input = {"Sample 1": sample1, "Sample 2": sample2}
            except ValueError:
                st.error("⚠️ Please enter valid numeric data for both samples.")

    # ---------------------------------------------------------------------------
    # 9. Wilcoxon Signed-Rank Test (paired, non-parametric)
    # ---------------------------------------------------------------------------
    elif selected_test == "Wilcoxon Signed-Rank Test":
        st.markdown("""
        **Example**:  
        - Data 1: `10, 12, 9, 14`  
        - Data 2: `12, 14, 10, 15`
        
        Enter two paired datasets of comma-separated values:
        """)
        col1, col2 = st.columns(2)
        with col1:
            before_str = st.text_area("Data 1", value="")
        with col2:
            after_str = st.text_area("Data 2", value="")

        if before_str and after_str:
            try:
                before = [float(x.strip()) for x in before_str.split(",") if x.strip()]
                after = [float(x.strip()) for x in after_str.split(",") if x.strip()]
                data_input = {"Before": before, "After": after}
            except ValueError:
                st.error("⚠️ Please enter valid numeric data for both sets.")

    # ---------------------------------------------------------------------------
    # 10. Kruskal-Wallis Test (multiple groups, non-parametric)
    # ---------------------------------------------------------------------------
    elif selected_test == "Kruskal-Wallis Test":
        st.markdown("""
        **Example**: For 3 groups  
        - Group 1: `10, 12, 9, 14`  
        - Group 2: `8, 7, 11, 9`  
        - Group 3: `15, 17, 14, 16`
        
        Enter data for multiple groups (comma-separated):
        """)
        num_groups = st.number_input("Number of groups", min_value=2, max_value=10, value=3)
        kw_data = {}
        for i in range(num_groups):
            label = f"Group {i+1}"
            group_str = st.text_area(label, value="", key=f"kw_group_{i}")
            if group_str:
                try:
                    kw_data[label] = [float(x.strip()) for x in group_str.split(",") if x.strip()]
                except ValueError:
                    st.error(f"⚠️ Please enter valid numeric data for {label}.")
        if kw_data:
            data_input = kw_data

    # ---------------------------------------------------------------------------
    # 11. Friedman Test (repeated measures, non-parametric)
    # ---------------------------------------------------------------------------
    elif selected_test == "Friedman Test":
        st.markdown("""
        **Example**: If you have 5 participants and 3 conditions, each participant row might be:  
        `10, 12, 14` (Participant 1)  
        `8, 7, 9`    (Participant 2)  
        ...
        
        Enter numeric data for each subject (comma-separated).
        """)
        num_subjects = st.number_input("Number of subjects", min_value=2, max_value=50, value=5)
        num_conditions = st.number_input("Number of conditions", min_value=2, max_value=10, value=3)

        friedman_data = {}
        for s in range(int(num_subjects)):
            label = f"Subject {s+1}"
            cond_str = st.text_area(label, value="", key=f"friedman_{s}")
            if cond_str:
                try:
                    vals = [float(x.strip()) for x in cond_str.split(",") if x.strip()]
                    if len(vals) != num_conditions:
                        st.warning(f"Row for {label} has {len(vals)} values, expected {num_conditions}.")
                    friedman_data[label] = vals
                except ValueError:
                    st.error(f"⚠️ Please enter valid numeric data for {label}.")
        if friedman_data:
            data_input = friedman_data

    # ---------------------------------------------------------------------------
    # 12. Chi-Squared Test (for A/B Tests)
    # ---------------------------------------------------------------------------
    elif selected_test == "Chi-Squared Test":
        st.markdown("""
        **Example** (2x2 table):  
        ```
        10, 5
        4,  6
        ```
        - This corresponds to 2 rows and 2 columns.
        
        Enter your contingency table, with rows separated by new lines and
        columns separated by commas:
        """)
        table_str = st.text_area("Contingency Table", value="")
        if table_str:
            try:
                rows = table_str.strip().split("\n")
                contingency_table = []
                for row in rows:
                    row_vals = [float(x.strip()) for x in row.split(",")]
                    contingency_table.append(row_vals)
                data_input = {"Contingency Table": contingency_table}
            except ValueError:
                st.error("⚠️ Please ensure all values in the table are numeric.")

    # ---------------------------------------------------------------------------
    # 13. Linear Regression => {"Predictors": 2D list, "Response": list}
    # ---------------------------------------------------------------------------
    elif selected_test == "Linear Regression":
        st.markdown("""
        **Example**: 3 observations with 1 predictor column  
        - Predictors:
          ```
          1
          2
          3
          ```
        - Response:
          ```
          5
          7
          9
          ```
        
        Enter predictor values (rows=observations, columns=variables) and response values:
        """)
        predictors_str = st.text_area("Predictors (each row is one observation)", value="")
        response_str = st.text_area("Response (one value per line)", value="")

        if predictors_str and response_str:
            try:
                pred_rows = predictors_str.strip().split("\n")
                predictors = []
                for row in pred_rows:
                    row_vals = [float(x.strip()) for x in row.split(",") if x.strip()]
                    predictors.append(row_vals)

                resp_vals = [float(x.strip()) for x in response_str.strip().split("\n") if x.strip()]

                if len(predictors) != len(resp_vals):
                    st.error("⚠️ The number of predictor rows must match the number of response values.")
                else:
                    data_input = {"Predictors": predictors, "Response": resp_vals}
            except ValueError:
                st.error("⚠️ Ensure all entries are numeric.")

    # ---------------------------------------------------------------------------
    # 14. Multiple Linear Regression => {"Predictors": 2D list, "Response": list}
    # ---------------------------------------------------------------------------
    elif selected_test == "Multiple Linear Regression":
        st.markdown("""
        **Example**: 3 observations, 2 predictor columns  
        - Predictors:
          ```
          1, 2
          2, 3
          3, 4
          ```
        - Response:
          ```
          5
          7
          9
          ```
        """)
        mlr_predictors_str = st.text_area("Predictors (rows=observations, columns=variables)", value="")
        mlr_response_str = st.text_area("Response (one value per line)", value="")

        if mlr_predictors_str and mlr_response_str:
            try:
                pred_rows = mlr_predictors_str.strip().split("\n")
                predictors = []
                for row in pred_rows:
                    row_vals = [float(x.strip()) for x in row.split(",") if x.strip()]
                    predictors.append(row_vals)

                resp_vals = [float(x.strip()) for x in mlr_response_str.strip().split("\n") if x.strip()]

                if len(predictors) != len(resp_vals):
                    st.error("⚠️ The number of predictor rows must match the number of response rows.")
                else:
                    data_input = {"Predictors": predictors, "Response": resp_vals}
            except ValueError:
                st.error("⚠️ Ensure all entries are numeric.")

    # ---------------------------------------------------------------------------
    # 15. Augmented Dickey-Fuller / KPSS => single time series
    # ---------------------------------------------------------------------------
    elif selected_test in [
        "Augmented Dickey-Fuller Test",
        "Kwiatkowski-Phillips-Schmidt-Shin (KPSS) Test",
    ]:
        st.markdown("""
        **Example**: `10.5, 10.7, 9.8, 11.0, 10.2`  
        Enter a single time series (comma-separated):
        """)
        ts_str = st.text_area("Time Series Data", value="")
        if ts_str:
            try:
                data_input = [float(x.strip()) for x in ts_str.split(",") if x.strip()]
            except ValueError:
                st.error("⚠️ Please enter valid numeric data for the time series.")

    # ---------------------------------------------------------------------------
    # 16. Pearson / Spearman / Kendall Correlation => X & Y lists
    # ---------------------------------------------------------------------------
    elif selected_test in [
        "Pearson Correlation",
        "Spearman's Rank Correlation",
        "Kendall's Rank Correlation",
    ]:
        st.markdown("""
        **Example**:  
        - X: `1, 2, 3, 4, 5`  
        - Y: `2.1, 3.5, 4.7, 5.0, 6.2`
        
        Enter two lists of comma-separated values:
        """)
        col1, col2 = st.columns(2)
        with col1:
            x_str = st.text_area("X values", value="")
        with col2:
            y_str = st.text_area("Y values", value="")

        if x_str and y_str:
            try:
                x_vals = [float(x.strip()) for x in x_str.split(",") if x.strip()]
                y_vals = [float(x.strip()) for x in y_str.split(",") if x.strip()]
                data_input = {"X": x_vals, "Y": y_vals}
            except ValueError:
                st.error("⚠️ Please enter valid numeric data for X and Y.")

    # ---------------------------------------------------------------------------
    # Fallback if the test name is not recognized
    # ---------------------------------------------------------------------------
    else:
        st.info("No specific input form for this test. Please modify the code to handle it.")
        st.markdown("If needed, enter your data below (comma-separated or otherwise):")
        fallback_data = st.text_area("Data", value="")
        if fallback_data:
            data_input = fallback_data

    return data_input


# -----------------------------------------------------------------------------
#                             PAGE FUNCTIONS
# -----------------------------------------------------------------------------

def welcome_page():
    st.markdown("<div class='title'>", unsafe_allow_html=True)
    st.title("📊 Statistical Analysis App - Developed by: Ilyas Nayle")
    st.markdown("</div>", unsafe_allow_html=True)

    st.image("Screenshot 2025-01-02 111627.png", width=400)

    st.markdown("""
    Welcome to the **Statistical Analysis App**!

    Here’s what you can do:
    - **Perform** various statistical tests on your data.
    - **Visualize** your results with easy-to-understand graphs.
    - **Interpret** statistical outputs to draw meaningful conclusions.
    
    Use the **tabs at the top** to navigate through the different features of the app.
    """)

    st.markdown("Feel free to explore, and let us know if you have any questions or feedback!")

def statistical_page():
    st.title("🔍 Statistical Tests")
    st.markdown("Explore statistical tests and visualize results interactively.")

    input_col, result_col = st.columns([2, 3])

    with input_col:
        st.subheader("📂 Menu")
        group = st.selectbox("Select a test group", list(test_groups.keys()))
        tests = test_groups[group]
        selected_test = st.selectbox("Select a specific test", tests)

        # Fetch and display test information
        test_name, description, details = get_test_info(selected_test)
        st.subheader(f"ℹ️ About {test_name}")
        st.write(description)
        with st.expander("Detailed Information"):
            st.markdown(details)

        st.markdown("---")
        st.subheader("📝 Enter Data for the Test")

        # -- Capture the user input dynamically (assuming get_user_input is defined) --
        data_input = get_user_input(selected_test)

        st.markdown("---")
        if st.button("Run Test"):
            if data_input:
                with result_col:
                    st.subheader("📈 Test Result")
                    with st.spinner("Running the test, please wait..."):
                        result = perform_test(selected_test, data_input)
                        st.success("✅ Test completed successfully!")
                    st.write(result)

                    st.markdown("### 📊 Interpretation")
                    # Try to pull a p_value from the result dictionary (if it exists)
                    if isinstance(result, dict) and "p_value" in result:
                        p_value = result["p_value"]
                        if p_value < 0.05:
                            st.markdown(
                                "The result is **statistically significant** "
                                f"(p-value = {p_value:.4f} < 0.05). We can reject the null hypothesis."
                            )
                        else:
                            st.markdown(
                                "The result is **not statistically significant** "
                                f"(p-value = {p_value:.4f} ≥ 0.05). We fail to reject the null hypothesis."
                            )
                    else:
                        st.write("No p-value found in the results. Please interpret accordingly.")

                    # Visualization
                    st.subheader("📊 Visualization")
                    display_graph(selected_test, data_input)
            else:
                st.error("⚠️ Please enter valid data.")

def about_page():
    """Displays an About page with general information about the project and author."""
    st.title("ℹ️ About This App")
    st.markdown("""
    ### What is this app about?
    This app helps users perform various **statistical tests** quickly and easily, 
    providing both **results** and **visualizations**.

    ### Technologies Used
    - **Streamlit** for the web interface
    - **scipy**, **statsmodels**, **sklearn** for statistical analysis
    - **pandas**, **numpy** for data manipulation
    - **matplotlib**, **seaborn** for visualization

    ### Author
    - **Ilyas Nayle** -  Machine Learning Engineer and Data Analyst

    ### References
                
    * https://streamlit.io/ 
    * https://www.python.org/ 
    * https://en.wikipedia.org/wiki/List_of_statistical_tests
    * https://medium.com/@anushka.da3/types-of-statistical-tests-b8ceb90e13b3
    * https://www.scribbr.com/statistics/statistical-tests/
    """)

def contact_page():
    """Displays a Contact page where users can reach out or find your info."""
    st.title("📩 Contact Us")

    st.markdown("""
    If you have any **questions**, **feedback**, or **bug reports**, please feel free to get in touch!

    **Email**: ilyasnayle5@gmail.com / ilyas.nayle@tedu.edu.tr  
    **Phone**: +90-501-341-6344 / 537-796-63 86 
    **Address**: Ankara, Turkiye

    Alternatively, you can fill out the form below:
    """)

    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send")
        if submitted:
            if name and email and message:
                st.success("Thank you for your message! We'll get back to you soon.")
            else:
                st.error("Please fill out all fields before submitting.")

def main():
     # Show topbar (name, time, weather, login+sign-up)
    show_top_header()
    # Create tabs at the top for navigation
    tabs = st.tabs(["Welcome", "Statistical Tests", "Verification", "About", "Contact"])

    with tabs[0]:
        welcome_page()
    with tabs[1]:
        statistical_page()
    with tabs[2]:
        verification_page()
    with tabs[3]:
        about_page()
    with tabs[4]:
        contact_page()

if __name__ == "__main__":
    main()

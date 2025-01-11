import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss
from sklearn.linear_model import LinearRegression
import streamlit as st
from predefined_datasets import predefined_datasets

def perform_test(test_name, data):
    print(f"DEBUG: Running {test_name} with data: {data}")

    try:
        # Shapiro-Wilk Test
        if test_name == "Shapiro-Wilk Test":
            from scipy.stats import shapiro
            stat, p_value = shapiro(data)
            result = {"statistic": stat, "p_value": p_value}

        # D'Agostino's K² Test
        elif test_name == "D'Agostino's K² Test":
            from scipy.stats import normaltest
            stat, p_value = normaltest(data)
            result = {"statistic": stat, "p_value": p_value}

        # Anderson-Darling Test
        elif test_name == "Anderson-Darling Test":
            from scipy.stats import anderson
            test_result = anderson(data)
            result = {
                "statistic": test_result.statistic,
                "critical_values": test_result.critical_values.tolist(),
                "significance_level": test_result.significance_level,
            }

        # Student's T-test
        elif test_name == "Student's T-test":
            from scipy.stats import ttest_ind
            group1, group2 = data["Group 1"], data["Group 2"]
            stat, p_value = ttest_ind(group1, group2)
            result = {"statistic": stat, "p_value": p_value}

        # Paired Student's T-test
        elif test_name == "Paired Student's T-test":
            from scipy.stats import ttest_rel
            before, after = data["Before"], data["After"]
            stat, p_value = ttest_rel(before, after)
            result = {"statistic": stat, "p_value": p_value}

        # Pearson Correlation
        elif test_name == "Pearson Correlation":
            from scipy.stats import pearsonr
            x, y = data["X"], data["Y"]
            coeff, p_value = pearsonr(x, y)
            result = {"correlation_coefficient": coeff, "p_value": p_value}

        # Spearman's Rank Correlation
        elif test_name == "Spearman's Rank Correlation":
            from scipy.stats import spearmanr
            x, y = data["X"], data["Y"]
            coeff, p_value = spearmanr(x, y)
            result = {"correlation_coefficient": coeff, "p_value": p_value}

        # Kendall's Rank Correlation
        elif test_name == "Kendall's Rank Correlation":
            from scipy.stats import kendalltau
            x, y = data["X"], data["Y"]
            coeff, p_value = kendalltau(x, y)
            result = {"correlation_coefficient": coeff, "p_value": p_value}

        # Chi-Squared Test
        elif test_name == "Chi-Squared Test":
            from scipy.stats import chi2_contingency
            contingency_table = data["Contingency Table"]
            stat, p_value, _, _ = chi2_contingency(contingency_table)
            result = {"statistic": stat, "p_value": p_value}

        # One-Way ANOVA
        elif test_name == "One-Way ANOVA":
            from scipy.stats import f_oneway
            # data is a dict of groups => run f_oneway
            groups = [arr for arr in data.values()]
            stat, p_value = f_oneway(*groups)
            result = {"statistic": stat, "p_value": p_value}

        # Two-Way ANOVA (placeholder)
        elif test_name == "Two-Way ANOVA":
            raise NotImplementedError("Two-Way ANOVA is not yet implemented.")

        # Repeated Measures ANOVA (placeholder)
        elif test_name == "Repeated Measures ANOVA":
            raise NotImplementedError("Repeated Measures ANOVA is not yet implemented.")

        # Mann-Whitney U Test
        elif test_name == "Mann-Whitney U Test":
            from scipy.stats import mannwhitneyu
            sample1, sample2 = data["Sample 1"], data["Sample 2"]
            stat, p_value = mannwhitneyu(sample1, sample2)
            result = {"statistic": stat, "p_value": p_value}

        # Wilcoxon Signed-Rank Test
        elif test_name == "Wilcoxon Signed-Rank Test":
            from scipy.stats import wilcoxon
            before, after = data["Before"], data["After"]
            stat, p_value = wilcoxon(before, after)
            result = {"statistic": stat, "p_value": p_value}

        # Kruskal-Wallis Test
        elif test_name == "Kruskal-Wallis Test":
            from scipy.stats import kruskal
            groups = [data[key] for key in data.keys()]
            stat, p_value = kruskal(*groups)
            result = {"statistic": stat, "p_value": p_value}

        # Friedman Test
        elif test_name == "Friedman Test":
            from scipy.stats import friedmanchisquare
            groups = [data[key] for key in data.keys()]
            # each key is presumably a subject
            # For the standard usage: friedmanchisquare(x1, x2, x3, ...)
            # each xN is a list of measurements across conditions.
            # If your data is the other way around, you might need to transpose.
            stat, p_value = friedmanchisquare(*groups)
            result = {"statistic": stat, "p_value": p_value}

        # Augmented Dickey-Fuller Test
        elif test_name == "Augmented Dickey-Fuller Test":
            from statsmodels.tsa.stattools import adfuller
            test_result = adfuller(data)
            result = {
                "adf_statistic": test_result[0],
                "p_value": test_result[1],
                "critical_values": test_result[4],
            }

        # KPSS Test
        elif test_name == "Kwiatkowski-Phillips-Schmidt-Shin (KPSS) Test":
            from statsmodels.tsa.stattools import kpss
            stat, p_value, _, crit_values = kpss(data, regression='c')
            result = {
                "kpss_statistic": stat,
                "p_value": p_value,
                "critical_values": crit_values,
            }

        # Linear Regression
        elif test_name == "Linear Regression":
            from sklearn.linear_model import LinearRegression
            predictors, response = data["Predictors"], data["Response"]
            model = LinearRegression()
            model.fit(predictors, response)
            result = {
                "coefficients": model.coef_.tolist(),
                "intercept": model.intercept_,
                "r_squared": model.score(predictors, response),
            }

        # Multiple Linear Regression
        elif test_name == "Multiple Linear Regression":
            from sklearn.linear_model import LinearRegression
            predictors, response = data["Predictors"], data["Response"]
            model = LinearRegression()
            model.fit(predictors, response)
            result = {
                "coefficients": model.coef_.tolist(),
                "intercept": model.intercept_,
                "r_squared": model.score(predictors, response),
            }

        # Logistic Regression
        elif test_name == "Logistic Regression":
            from sklearn.linear_model import LogisticRegression
            predictors, response = data["Predictors"], data["Response"]
            model = LogisticRegression()
            model.fit(predictors, response)
            result = {
                "coefficients": model.coef_.tolist(),
                "intercept": model.intercept_.tolist(),
            }

        # ANOVA (generic fallback if someone calls "ANOVA")
        elif test_name == "ANOVA":
            from scipy.stats import f_oneway
            groups = [data[key] for key in data.keys()]
            stat, p_value = f_oneway(*groups)
            result = {"statistic": stat, "p_value": p_value}

        # Kolmogorov-Smirnov Test
        elif test_name == "Kolmogorov-Smirnov Test":
            from scipy.stats import ks_2samp
            sample1, sample2 = data["Sample 1"], data["Sample 2"]
            stat, p_value = ks_2samp(sample1, sample2)
            result = {"statistic": stat, "p_value": p_value}

        else:
            raise NotImplementedError(f"Test '{test_name}' is not implemented!")

        print(f"DEBUG: Result for {test_name}: {result}")
        return result

    except Exception as e:
        print(f"DEBUG: Error in {test_name}: {e}")
        raise

def display_graph(selected_test, data):
    """
    Generate appropriate graphs based on the selected test and input data.
    """
    try:
        plt.figure(figsize=(10, 6))

        # Normality Tests
        if selected_test in ["Shapiro-Wilk Test", "D'Agostino's K² Test", "Anderson-Darling Test", "Kolmogorov-Smirnov Test"]:
            sns.histplot(data, kde=True, bins=10)
            plt.title("Histogram with KDE Plot")
            plt.xlabel("Values")
            plt.ylabel("Frequency")

        # Parametric Tests
        elif selected_test in ["Student's T-test", "Paired Student's T-test", "One-Way ANOVA", "Repeated Measures ANOVA"]:
            sns.boxplot(data=list(data.values()))
            plt.title("Boxplot of Groups")
            plt.xlabel("Groups")
            plt.ylabel("Values")

        # Non-Parametric Tests
        elif selected_test in ["Mann-Whitney U Test", "Wilcoxon Signed-Rank Test", "Kruskal-Wallis Test", "Friedman Test"]:
            sns.boxplot(data=list(data.values()))
            plt.title("Boxplot of Groups (Non-Parametric Test)")
            plt.xlabel("Groups")
            plt.ylabel("Values")

        # Correlation Tests
        elif selected_test in ["Pearson Correlation", "Spearman's Rank Correlation", "Kendall's Rank Correlation"]:
            sns.scatterplot(x=data["X"], y=data["Y"])
            plt.title("Scatter Plot")
            plt.xlabel("X")
            plt.ylabel("Y")

        # Chi-Squared Test
        elif selected_test == "Chi-Squared Test":
            contingency_table = pd.DataFrame(data["Contingency Table"])
            sns.heatmap(contingency_table, annot=True, cmap="coolwarm", fmt=".1f")
            plt.title("Contingency Table Heatmap")
            plt.xlabel("Categories")
            plt.ylabel("Categories")

        # Stationary Tests
        elif selected_test in ["Augmented Dickey-Fuller Test", "Kwiatkowski-Phillips-Schmidt-Shin (KPSS) Test"]:
            sns.lineplot(x=range(len(data)), y=data)
            plt.title("Time Series Plot")
            plt.xlabel("Time Steps")
            plt.ylabel("Values")

        # Regression Tests
        elif selected_test in ["Linear Regression", "Multiple Linear Regression"]:
            predictors = pd.DataFrame(data["Predictors"]).T
            response = pd.Series(data["Response"])
            if predictors.shape[1] == 1:  # Simple Linear Regression
                sns.scatterplot(x=predictors.iloc[:, 0], y=response)
                plt.plot(
                    predictors.iloc[:, 0],
                    LinearRegression().fit(predictors, response).predict(predictors),
                    color="red",
                )
                plt.title("Regression Line (Simple Linear Regression)")
                plt.xlabel("Predictor")
                plt.ylabel("Response")
            else:  # Multiple Linear Regression
                sns.heatmap(predictors.corr(), annot=True, cmap="coolwarm")
                plt.title("Predictors Correlation Heatmap")

        # Logistic Regression - Placeholder for visualizations
        elif selected_test == "Logistic Regression":
            plt.text(0.5, 0.5, "Logistic Regression Visualization Pending", ha="center", va="center", fontsize=12)
            plt.axis("off")

        # If no specific graph is available
        else:
            plt.text(0.5, 0.5, "No graphical representation available", ha="center", va="center", fontsize=12)
            plt.axis("off")

        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error creating graph: {e}")

print("Validating Predefined Datasets...\n")
for test_name, details in predefined_datasets.items():
    data = details["data"]
    expected_result = details["expected_result"]
    try:
        print(f"Running {test_name}...")
        actual_result = perform_test(test_name, data)
        print(f"Expected Result: {expected_result}")
        print(f"Actual Result: {actual_result}")
        print("---")
        # Compare results
        if isinstance(actual_result, dict) and isinstance(expected_result, dict):
            comparison_passed = all(
                abs(actual_result.get(key, 0) - expected_result.get(key, 0)) < 1e-6
                for key in expected_result
            )
        elif isinstance(actual_result, (float, int)) and isinstance(expected_result, (float, int)):
            comparison_passed = abs(actual_result - expected_result) < 1e-6
        else:
            comparison_passed = str(actual_result).strip().lower() in str(expected_result).strip().lower()

        if comparison_passed:
            print(f"✅ {test_name}: Result matches the expected output!")
        else:
            print(f"❌ {test_name}: Result does not match the expected output.")
    except Exception as e:
        print(f"Error in {test_name}: {e}")

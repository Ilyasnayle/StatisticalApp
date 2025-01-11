def get_test_info(test_name):
    info = {
        "Shapiro-Wilk Test": (
            "Shapiro-Wilk Test",
            "A test for normality of data. It checks whether a given data sample is drawn from a normally distributed population.",
            """
            **When to Use**:
            - To verify if a dataset meets the assumption of normality required for parametric tests (e.g., T-tests, ANOVA).
            - For small to medium-sized datasets (n < 2000).
            
            **When Not to Use**:
            - For very large datasets (n > 2000), as the test may become overly sensitive to small deviations from normality.
            - When the data contains significant outliers, which can affect the test's accuracy.

            **Examples**:
            - Checking if students' test scores follow a normal distribution before performing a T-test.
            - Validating the normality of sales data before using parametric regression models.
            """
        ),
        "D'Agostino's K² Test": (
            "D'Agostino's K² Test",
            "A normality test based on skewness and kurtosis.",
            """
            **When to Use**:
            - To assess normality in moderately sized datasets (n > 50).
            - As an alternative to the Shapiro-Wilk test when the dataset size increases.

            **When Not to Use**:
            - For very small datasets (n < 50), as the test may lack statistical power.
            - When the data distribution is heavily skewed or contains extreme outliers.

            **Examples**:
            - Evaluating the normality of customer age data in market segmentation studies.
            - Testing the normality of residuals in linear regression analysis.
            """
        ),
        "Anderson-Darling Test": (
            "Anderson-Darling Test",
            "A test for the goodness of fit to a specified distribution, often used to check for normality.",
            """
            **When to Use**:
            - To determine how well a dataset follows a normal distribution.
            - To validate assumptions of normality for parametric tests.

            **When Not to Use**:
            - For datasets with significant outliers.
            - When testing for distributions other than normal without modification.

            **Examples**:
            - Verifying the normality of manufacturing quality data.
            - Assessing the fit of rainfall data to a normal distribution.
            """
        ),
        "Spearman's Rank Correlation": (
            "Spearman's Rank Correlation",
            "A non-parametric measure of correlation between two continuous or ordinal variables.",
            """
            **When to Use**:
            - When the relationship between variables is monotonic but not necessarily linear.
            - For ordinal data or when one or both variables are not normally distributed.

            **When Not to Use**:
            - For datasets where the relationship between variables is non-monotonic.
            - When precise values, rather than ranks, are required to assess correlation.

            **Examples**:
            - Examining the relationship between employee rank and job satisfaction scores.
            - Assessing correlation between hours of study and exam ranks.
            """
        ),
        "Kendall's Rank Correlation": (
            "Kendall's Rank Correlation",
            "A non-parametric test to measure the strength of association between two ordinal or continuous variables.",
            """
            **When to Use**:
            - When dealing with ordinal data or small datasets.
            - To assess monotonic relationships that may not be linear.

            **When Not to Use**:
            - For large datasets, as it can be computationally intensive.
            - When precise correlation values are needed (Pearson's may be better).

            **Examples**:
            - Analyzing the correlation between customer satisfaction rank and loyalty score.
            - Examining the relationship between education rank and income rank.
            """
        ),
        "Chi-Squared Test": (
            "Chi-Squared Test",
            "Examines the association between categorical variables.",
            """
            **When to Use**:
            - To test independence between two categorical variables in a contingency table.
            - For large sample sizes (minimum expected frequency in each cell > 5).

            **When Not to Use**:
            - For small sample sizes; consider Fisher's Exact Test instead.
            - When the data is not in categorical format.

            **Examples**:
            - Testing if gender influences product preference in a survey.
            - Examining if education level is associated with job type.
            """
        ),
        "Augmented Dickey-Fuller Test": (
            "Augmented Dickey-Fuller Test",
            "A statistical test for stationarity in time series data.",
            """
            **When to Use**:
            - To determine if a time series is stationary (mean and variance are constant over time).
            - As a prerequisite for ARIMA or other time series forecasting models.

            **When Not to Use**:
            - For non-time series data or data with strong seasonal trends without prior differencing.
            - When the time series is too short (e.g., fewer than 20 observations).

            **Examples**:
            - Checking if monthly stock prices are stationary before applying ARIMA.
            - Determining whether temperature records over decades have a stable mean.
            """
        ),
        "Kwiatkowski-Phillips-Schmidt-Shin (KPSS) Test": (
            "Kwiatkowski-Phillips-Schmidt-Shin (KPSS) Test",
            "A test for stationarity in time series data, often used to complement the Augmented Dickey-Fuller Test.",
            """
            **When to Use**:
            - To validate stationarity assumptions for time series data.
            - As a complementary test alongside ADF for more robust conclusions.

            **When Not to Use**:
            - When the dataset contains missing values or is too short.
            - For data that has already been heavily differenced or transformed.

            **Examples**:
            - Validating the stationarity of economic indicators such as GDP growth.
            - Testing whether a time series of daily sales is suitable for seasonal decomposition.
            """
        ),
        "Student's T-test": (
            "Student's T-test",
            "Compares the means of two independent groups to see if they are statistically different.",
            """
            **When to Use**:
            - To compare the means of two independent samples.
            - When the data is continuous and normally distributed.

            **When Not to Use**:
            - For non-normal data (consider non-parametric alternatives like the Mann-Whitney U test).
            - When variances between groups are unequal without adjustment.

            **Examples**:
            - Comparing the test scores of students from two different schools.
            - Analyzing sales performance of two regions.
            """
        ),
        "Paired Student's T-test": (
            "Paired Student's T-test",
            "Compares the means of two related groups to determine if they differ significantly.",
            """
            **When to Use**:
            - To compare the means of related groups (e.g., before-and-after measurements).
            - For normally distributed data.

            **When Not to Use**:
            - For unrelated groups (use independent T-test instead).
            - When data is not normally distributed or contains outliers.

            **Examples**:
            - Comparing blood pressure before and after medication in the same patients.
            - Analyzing pre- and post-training test scores of employees.
            """
        ),
        "ANOVA": (
            "ANOVA (Analysis of Variance)",
            "Compares means across three or more groups to detect significant differences.",
            """
            **When to Use**:
            - When comparing means of three or more independent groups.
            - To determine if at least one group mean is significantly different.

            **When Not to Use**:
            - When there are only two groups (use T-test instead).
            - For datasets that violate the assumption of homogeneity of variances (use Welch’s ANOVA).

            **Examples**:
            - Comparing the effectiveness of three different training programs on employee performance.
            - Analyzing average sales across three regions.
            """
        ),
        "Two-Way Repeated Measures ANOVA": (
            "Two-Way Repeated Measures ANOVA",
            "Tests interaction effects between two factors in repeated measurements.",
            """
            **When to Use**:
            - To assess how two independent variables affect a dependent variable in a repeated-measures design.
            - For designs with two factors, such as treatment and time.

            **When Not to Use**:
            - When there are no repeated measurements or the design is purely between-subjects.
            - For datasets with incomplete data (e.g., missing observations).

            **Examples**:
            - Evaluating how different teaching methods and time intervals influence test performance.
            - Analyzing the effects of drug dosage and time on patient health metrics.
            """
        ),
        "Linear Regression": (
            "Linear Regression",
            "A method for modeling the relationship between a dependent variable and one or more independent variables.",
            """
            **When to Use**:
            - To predict a continuous dependent variable based on independent variables.
            - When the relationship between variables is linear, and residuals are normally distributed.

            **When Not to Use**:
            - When the relationship between variables is non-linear.
            - For datasets with high multicollinearity between predictors.

            **Examples**:
            - Predicting house prices based on size, location, and number of bedrooms.
            - Estimating sales revenue based on marketing spend.
            """
        ),"Kolmogorov-Smirnov Test": (
            "Kolmogorov-Smirnov Test",
            "A test to compare a sample's distribution with a reference distribution or compare two samples.",
            """
            **When to Use**:
            - To check if a sample follows a specific distribution.
            - To compare two empirical distributions.
            
            **When Not to Use**:
            - When the data has ties or is not continuous.
            
            **Examples**:
            - Verifying if income data follows a normal distribution.
            """
        ),
        "Mann-Whitney U Test": (
            "Mann-Whitney U Test",
            "A non-parametric test to compare medians of two independent groups.",
            """
            **When to Use**:
            - When comparing two groups without assuming normality.
            
            **When Not to Use**:
            - For paired data or more than two groups.
            
            **Examples**:
            - Comparing satisfaction scores between two customer groups.
            """
        ),
        "Wilcoxon Signed-Rank Test": (
            "Wilcoxon Signed-Rank Test",
            "A non-parametric test for paired data to assess differences in medians.",
            """
            **When to Use**:
            - When comparing two related samples or repeated measurements.
            
            **When Not to Use**:
            - For independent samples.
            
            **Examples**:
            - Comparing test scores before and after a training program.
            """
        ),
        "Kruskal-Wallis Test": (
            "Kruskal-Wallis Test",
            "A non-parametric alternative to one-way ANOVA for comparing medians of multiple groups.",
            """
            **When to Use**:
            - When comparing medians across three or more independent groups.
            
            **When Not to Use**:
            - When assumptions of normality are met (use ANOVA instead).
            
            **Examples**:
            - Comparing satisfaction scores across three store locations.
            """
        ),
        "Friedman Test": (
            "Friedman Test",
            "A non-parametric test for repeated measures across multiple groups.",
            """
            **When to Use**:
            - When comparing repeated measures in a non-parametric context.
            
            **When Not to Use**:
            - For independent samples.
            
            **Examples**:
            - Analyzing effects of different diets on weight loss over time.
            """
        ),
        "Logistic Regression": (
            "Logistic Regression",
            "A regression method to model binary or categorical outcomes.",
            """
            **When to Use**:
            - When predicting a binary outcome (e.g., success/failure).
            
            **When Not to Use**:
            - For continuous dependent variables.
            
            **Examples**:
            - Predicting whether a customer will make a purchase based on behavior data.
            """
        )
    }
    return info.get(test_name, ("", "", ""))

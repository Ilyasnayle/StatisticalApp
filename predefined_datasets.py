predefined_datasets = {
    "Shapiro-Wilk Test": {
        "data": [1.2, 1.8, 2.5, 2.3, 2.1],
        "expected_result": {
            "statistic": 0.943245,
            "p_value": 0.688962
        },
    },
    "D'Agostino's K² Test": {
        "data": [1.5, 1.7, 2.0, 1.9, 2.2, 2.5, 2.6, 2.8],  # Example with at least 8 samples
        "expected_result": {
            "statistic": 0.832345,  # Rounded to 6 decimal places
            "p_value": 0.659567    # Rounded to 6 decimal places
        },
    },
    "Anderson-Darling Test": {
        "data": [1.2, 1.5, 1.8, 2.0, 2.2],  # Keep the same input data
        "expected_result": {
            "statistic": 0.165202,  # Rounded to 6 decimal places
            "critical_values": [0.72, 0.82, 0.984, 1.148, 1.365],
            "significance_level": [15.0, 10.0, 5.0, 2.5, 1.0]
        },
    },
    "Student's T-test": {
        "data": {
            "Group 1": [1.2, 1.8, 2.5],  # Example data for Group 1
            "Group 2": [2.2, 2.8, 3.5],  # Example data for Group 2
        },
        "expected_result": {
            "statistic": -1.882367,  # Rounded to 6 decimal places
            "p_value": 0.132917      # Rounded to 6 decimal places
        },
    },
    "Paired Student's T-test": {
        "data": {
            "Before": [1.5, 2.0, 1.8, 2.2],  # Example data for 'Before'
            "After": [2.1, 2.3, 2.2, 2.8],   # Example data for 'After'
        },
        "expected_result": {
            "statistic": -6.333333,  # Rounded to 6 decimal places
            "p_value": 0.007960      # Rounded to 6 decimal places
        },
    },
    "ANOVA": {
        "data": {
            "Group 1": [1.2, 1.5, 1.8],  # Example data for Group 1
            "Group 2": [2.0, 2.3, 2.5],  # Example data for Group 2
            "Group 3": [3.0, 3.3, 3.5],  # Example data for Group 3
        },
        "expected_result": {
            "statistic": 32.600000,  # Rounded to 6 decimal places
            "p_value": 0.000598      # Rounded to 6 decimal places
        },
    },
    "Kruskal-Wallis Test": {
        "data": {
            "Group 1": [1.2, 1.5, 1.8],  # Example data for Group 1
            "Group 2": [2.0, 2.3, 2.5],  # Example data for Group 2
            "Group 3": [3.0, 3.3, 3.5],  # Example data for Group 3
        },
        "expected_result": {
            "statistic": 7.200000,  # Rounded to 6 decimal places
            "p_value": 0.027324     # Rounded to 6 decimal places
        },
    },
    "Pearson Correlation": {
        "data": {
            "X": [1, 2, 3, 4, 5],
            "Y": [2, 4, 6, 8, 10],
        },
        "expected_result": {
            "correlation_coefficient": 1.0,
            "p_value": 0.0
        },
    },
    "Spearman's Rank Correlation": {
        "data": {
            "X": [1, 2, 3, 4, 5],
            "Y": [5, 4, 3, 2, 1],
        },
        "expected_result": {
            "correlation_coefficient": -1.0,
            "p_value": 0.0
        },
    },
    "Kendall's Rank Correlation": {
        "data": {
            "X": [1, 2, 3],
            "Y": [3, 2, 1],
        },
        "expected_result": {
            "correlation_coefficient": -1.0,
            "p_value": 0.333333
        },
    },
    "Chi-Squared Test": {
        "data": {
            "Contingency Table": [[10, 20], [30, 40]],  # Example contingency table
        },
        "expected_result": {
            "statistic": 0.446429,  # Rounded to 6 decimal places
            "p_value": 0.504036     # Rounded to 6 decimal places
        },
    },
    "Augmented Dickey-Fuller Test": {
        "data": [1.2, 1.5, 1.8, 2.0, 2.5],  # Example time-series data
        "expected_result": {
            "adf_statistic": 0.683604,  # Rounded to 6 decimal places
            "p_value": 0.989505,        # Rounded to 6 decimal places
            "critical_values": {
                "1%": -7.355441,        # Rounded to 6 decimal places
                "5%": -4.474365,        # Rounded to 6 decimal places
                "10%": -3.126933        # Rounded to 6 decimal places
            }
        },
    },
    "Kwiatkowski-Phillips-Schmidt-Shin (KPSS) Test": {
        "data": [1.0, 1.1, 1.2, 1.3, 1.4],  # Example time-series data
        "expected_result": {
            "kpss_statistic": 0.371429,  # Rounded to 6 decimal places
            "p_value": 0.089470,         # Rounded to 6 decimal places
            "critical_values": {
                "10%": 0.347,
                "5%": 0.463,
                "2.5%": 0.574,
                "1%": 0.739
            }
        },
    },
    "Linear Regression": {
        "data": {
            "Predictors": [[1, 2], [2, 3], [3, 4]],  # Example predictor data
            "Response": [2, 3, 4],                  # Example response data
        },
        "expected_result": {
            "coefficients": [0.500000, 0.500000],  # Rounded to 6 decimal places
            "intercept": 0.500000,                # Rounded to 6 decimal places
            "r_squared": 1.000000                 # Rounded to 6 decimal places
        },
    },
        "Logistic Regression": {
            "data": {
                "Predictors": [[1], [2], [3]],  # Example predictor variables
                "Response": [0, 1, 1],         # Example response variables
            },
            "expected_result": {
                "coefficients": [[0.701610]],  # Rounded to 6 decimal places
                "intercept": [-0.655680]       # Rounded to 6 decimal places
            },
        },
    }


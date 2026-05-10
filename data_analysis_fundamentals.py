"""
Data Analysis Fundamentals Module
Author: Irem Victor Chinonso (princeville45)
Description: Production-quality module for data cleaning, descriptive statistics, and correlation analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats

class DataCleaner:
    """Handles missing values, outliers, type casting, and deduplication."""
    
    @staticmethod
    def clean(df):
        """Standard cleaning pipeline."""
        # Deduplication
        df = df.drop_duplicates()
        
        # Missing values (Numeric: median, Categorical: mode)
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
        
        return df

    @staticmethod
    def remove_outliers(df, column):
        """Removes outliers using the IQR method."""
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        return df[~((df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR)))]

class DescriptiveStats:
    """Generates a comprehensive descriptive statistics report."""
    
    @staticmethod
    def analyze(df):
        """Calculates mean, median, mode, std dev, variance, skewness, and kurtosis."""
        numeric_df = df.select_dtypes(include=[np.number])
        report = {}
        
        for col in numeric_df.columns:
            stats_dict = {
                'Mean': numeric_df[col].mean(),
                'Median': numeric_df[col].median(),
                'Std Dev': numeric_df[col].std(),
                'Variance': numeric_df[col].var(),
                'Skewness': numeric_df[col].skew(),
                'Kurtosis': numeric_df[col].kurtosis()
            }
            report[col] = stats_dict
            
        return report

class CorrelationAnalyzer:
    """Performs Pearson and Spearman correlation analysis with interpretation."""
    
    @staticmethod
    def analyze(df, col1, col2):
        """Calculates correlations and provides interpretation."""
        pearson_r, pearson_p = stats.pearsonr(df[col1], df[col2])
        spearman_r, spearman_p = stats.spearmanr(df[col1], df[col2])
        
        def interpret(r):
            if abs(r) > 0.7: return "Strong"
            if abs(r) > 0.4: return "Moderate"
            return "Weak"
            
        return {
            'Pearson': {'r': pearson_r, 'p': pearson_p, 'strength': interpret(pearson_r)},
            'Spearman': {'r': spearman_r, 'p': spearman_p, 'strength': interpret(spearman_r)}
        }

class ReportGenerator:
    """Generates clean plain-text reports from analysis output."""
    
    @staticmethod
    def generate_text_report(analysis_type, data):
        """Formats analysis data into a readable string."""
        report = f"--- {analysis_type.upper()} REPORT ---\n"
        
        if isinstance(data, dict):
            for key, values in data.items():
                report += f"\nENTITY: {key}\n"
                if isinstance(values, dict):
                    for sub_key, val in values.items():
                        report += f"  {sub_key}: {val:.4f}\n" if isinstance(val, (float, int)) else f"  {sub_key}: {val}\n"
        
        return report

if __name__ == "__main__":
    # Example usage
    data = {'A': [1, 2, 3, 4, 100], 'B': [5, 4, 3, 2, 1]}
    df = pd.DataFrame(data)
    
    # Cleaning
    clean_df = DataCleaner.remove_outliers(df, 'A')
    
    # Stats
    stats_out = DescriptiveStats.analyze(clean_df)
    print(ReportGenerator.generate_text_report("Descriptive Statistics", stats_out))
    
    # Correlation
    corr_out = CorrelationAnalyzer.analyze(clean_df, 'A', 'B')
    print(ReportGenerator.generate_text_report("Correlation Analysis", corr_out))

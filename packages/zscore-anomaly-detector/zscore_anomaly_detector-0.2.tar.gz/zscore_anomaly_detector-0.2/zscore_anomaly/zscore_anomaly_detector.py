import numpy as np
import pandas as pd

class ZScoreAnomalyDetector:
    def __init__(self, threshold=None):
        if threshold is None:
            self.threshold = 3  # Default threshold
        else:
            self.threshold = threshold
    
    def select_numeric_columns(self, data):
        numeric_data = data.select_dtypes(include=[np.number])
        return numeric_data

    def z_score(self, data):
        numeric_data = self.select_numeric_columns(data)
        return (numeric_data - numeric_data.mean()) / numeric_data.std()

    def detect_anomalies(self, data):
        z_scores = self.z_score(data)
        return (z_scores.abs() > self.threshold)

    def create_dataframe_with_anomalies(self, data):
        anomalies = self.detect_anomalies(data)
        anomaly_rows = anomalies.any(axis=1)
        data['Anomaly'] = anomaly_rows
        return data

    def style_dataframe(self, df):
        def highlight_anomalies(row):
            color = 'background-color: red' if row['Anomaly'] else ''
            return [color] * len(row)
        
        return df.style.apply(highlight_anomalies, axis=1)

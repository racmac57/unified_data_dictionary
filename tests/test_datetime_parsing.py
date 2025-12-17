# // 2025-12-17-19-30-00
# // __tests__/test_datetime_parsing.py
# // Author: R. A. Carucci
# // Purpose: Unit tests for datetime field parsing and validation

"""
Test Datetime Parsing

Tests datetime field parsing, coercion, and time sequence validation.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta


class TestDatetimeParsing:
    """Test suite for datetime parsing and validation"""
    
    def test_valid_datetime_format(self):
        """Test parsing of valid datetime strings"""
        
        df = pd.DataFrame({
            'TimeOfCall': ['2024-11-24 14:35:22', '2025-01-15 08:20:00']
        })
        
        df['TimeOfCall'] = pd.to_datetime(df['TimeOfCall'])
        
        assert df['TimeOfCall'].notna().all()
        assert df['TimeOfCall'].dtype == 'datetime64[ns]'
    
    def test_invalid_datetime_coercion(self):
        """Test that invalid datetime strings coerce to NaT"""
        
        df = pd.DataFrame({
            'TimeOfCall': ['2024-11-24 14:35:22', 'INVALID', '????']
        })
        
        df['TimeOfCall'] = pd.to_datetime(df['TimeOfCall'], errors='coerce')
        
        assert df['TimeOfCall'].isna().sum() == 2
    
    def test_time_sequence_valid(self):
        """Test valid time sequences"""
        
        base_time = datetime(2024, 11, 24, 14, 0, 0)
        
        df = pd.DataFrame({
            'TimeOfCall': [base_time],
            'TimeDispatched': [base_time + timedelta(minutes=2)],
            'TimeOut': [base_time + timedelta(minutes=7)],
            'TimeIn': [base_time + timedelta(minutes=30)]
        })
        
        # Check sequence
        assert (df['TimeDispatched'] >= df['TimeOfCall']).all()
        assert (df['TimeOut'] >= df['TimeDispatched']).all()
        assert (df['TimeIn'] >= df['TimeOut']).all()
    
    def test_time_sequence_invalid(self):
        """Test detection of invalid time sequences"""
        
        base_time = datetime(2024, 11, 24, 14, 0, 0)
        
        df = pd.DataFrame({
            'TimeOfCall': [base_time],
            'TimeDispatched': [base_time - timedelta(minutes=5)]  # Invalid: before call
        })
        
        invalid = df['TimeDispatched'] < df['TimeOfCall']
        
        assert invalid.sum() == 1, "Should detect sequence violation"
    
    def test_response_time_calculation(self):
        """Test response time calculation"""
        
        base_time = datetime(2024, 11, 24, 14, 0, 0)
        
        df = pd.DataFrame({
            'TimeOfCall': [base_time],
            'TimeDispatched': [base_time + timedelta(minutes=5)]
        })
        
        df['ResponseTimeMinutes'] = (df['TimeDispatched'] - df['TimeOfCall']).dt.total_seconds() / 60
        
        assert df['ResponseTimeMinutes'].iloc[0] == 5.0
    
    def test_on_scene_duration_calculation(self):
        """Test on-scene duration calculation"""
        
        base_time = datetime(2024, 11, 24, 14, 0, 0)
        
        df = pd.DataFrame({
            'TimeOut': [base_time],
            'TimeIn': [base_time + timedelta(minutes=30)]
        })
        
        df['OnSceneDuration'] = (df['TimeIn'] - df['TimeOut']).dt.total_seconds() / 60
        
        assert df['OnSceneDuration'].iloc[0] == 30.0
    
    def test_future_date_detection(self):
        """Test detection of future dates"""
        
        future_date = datetime.now() + timedelta(days=365)
        
        df = pd.DataFrame({
            'TimeOfCall': [future_date]
        })
        
        invalid = df['TimeOfCall'] > datetime.now()
        
        assert invalid.sum() == 1, "Should detect future dates"


if __name__ == "__main__":
    pytest.main([__file__, '-v'])

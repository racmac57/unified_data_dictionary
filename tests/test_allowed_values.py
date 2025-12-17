# // 2025-12-17-19-30-00
# // __tests__/test_allowed_values.py
# // Author: R. A. Carucci
# // Purpose: Unit tests for controlled vocabulary validation

"""
Test Allowed Values Validation

Tests that controlled vocabulary fields only contain permitted values.
"""

import pytest
import pandas as pd
import numpy as np


class TestAllowedValues:
    """Test suite for controlled vocabulary validation"""
    
    def test_how_reported_allowed_values(self):
        """Test HowReported field accepts only valid values"""
        
        allowed = ['9-1-1', 'Phone', 'Walk-in', 'Self-Initiated', 'Radio', 'Other']
        
        # Valid values
        df = pd.DataFrame({'HowReported': allowed})
        invalid = ~df['HowReported'].isin(allowed)
        
        assert invalid.sum() == 0, "All values should be valid"
    
    def test_how_reported_invalid_values(self):
        """Test HowReported field rejects invalid values"""
        
        allowed = ['9-1-1', 'Phone', 'Walk-in', 'Self-Initiated', 'Radio', 'Other']
        
        # Invalid values
        df = pd.DataFrame({'HowReported': ['INVALID', 'Email', '911']})
        invalid = ~df['HowReported'].isin(allowed)
        
        assert invalid.sum() == 3, "All test values should be invalid"
    
    def test_disposition_allowed_values(self):
        """Test Disposition field vocabulary"""
        
        allowed = ['Report Taken', 'Arrest Made', 'GOA', 'UTL', 'Unfounded', 'See Report']
        
        df = pd.DataFrame({'Disposition': allowed})
        invalid = ~df['Disposition'].isin(allowed)
        
        assert invalid.sum() == 0
    
    def test_pd_zone_allowed_values(self):
        """Test PDZone field vocabulary"""
        
        allowed = ['Z1', 'Z2', 'Z3', 'Z4', 'UNK']
        
        df = pd.DataFrame({'PDZone': allowed})
        invalid = ~df['PDZone'].isin(allowed)
        
        assert invalid.sum() == 0
    
    def test_pd_zone_case_sensitivity(self):
        """Test PDZone is case-sensitive"""
        
        allowed = ['Z1', 'Z2', 'Z3', 'Z4', 'UNK']
        
        # Lowercase should be invalid
        df = pd.DataFrame({'PDZone': ['z1', 'z2']})
        invalid = ~df['PDZone'].isin(allowed)
        
        assert invalid.sum() == 2, "Lowercase zones should be invalid"
    
    def test_response_type_allowed_values(self):
        """Test ResponseType field vocabulary"""
        
        allowed = ['Emergency', 'Priority', 'Routine', 'Not Specified']
        
        df = pd.DataFrame({'ResponseType': allowed})
        invalid = ~df['ResponseType'].isin(allowed)
        
        assert invalid.sum() == 0
    
    def test_null_values_handled(self):
        """Test that null values don't cause errors"""
        
        allowed = ['9-1-1', 'Phone', 'Walk-in']
        
        df = pd.DataFrame({'HowReported': ['9-1-1', None, 'Phone', np.nan]})
        invalid = ~df['HowReported'].isin(allowed)
        
        # NaN values should be flagged as invalid
        assert invalid.sum() == 2


if __name__ == "__main__":
    pytest.main([__file__, '-v'])

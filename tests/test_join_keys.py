# // 2025-12-17-19-30-00
# // __tests__/test_join_keys.py
# // Author: R. A. Carucci
# // Purpose: Unit tests for CAD/RMS join key validation

"""
Test Join Key Matching

Tests case number format validation and CAD/RMS join operations.
"""

import pytest
import pandas as pd


class TestJoinKeys:
    """Test suite for join key validation"""
    
    def test_case_number_format_valid(self):
        """Test valid case number formats"""
        
        df = pd.DataFrame({
            'ReportNumberNew': ['24-123456', '25-000001', '19-999999']
        })
        
        # Check format
        valid = df['ReportNumberNew'].str.match(r'^\d{2}-\d{6}$')
        
        assert valid.all(), "All case numbers should match format"
    
    def test_case_number_format_invalid(self):
        """Test detection of invalid case number formats"""
        
        df = pd.DataFrame({
            'ReportNumberNew': ['24-12345', '2024-123456', 'INVALID', '24-ABC123']
        })
        
        valid = df['ReportNumberNew'].str.match(r'^\d{2}-\d{6}$', na=False)
        
        assert (~valid).sum() == 4, "Should detect all invalid formats"
    
    def test_join_cad_rms_successful(self):
        """Test successful CAD/RMS join"""
        
        cad_df = pd.DataFrame({
            'ReportNumberNew': ['24-123456', '24-123457', '24-123458'],
            'Incident': ['ASSAULT', 'BURGLARY', 'THEFT']
        })
        
        rms_df = pd.DataFrame({
            'CaseNumber': ['24-123456', '24-123457'],
            'Location': ['123 MAIN ST', '456 ELM AVE']
        })
        
        merged = pd.merge(
            cad_df, rms_df,
            left_on='ReportNumberNew',
            right_on='CaseNumber',
            how='left'
        )
        
        assert len(merged) == 3
        assert merged['CaseNumber'].notna().sum() == 2
    
    def test_detect_orphaned_rms_records(self):
        """Test detection of RMS records without CAD match"""
        
        cad_df = pd.DataFrame({
            'ReportNumberNew': ['24-123456']
        })
        
        rms_df = pd.DataFrame({
            'CaseNumber': ['24-123456', '24-999999']  # 999999 is orphaned
        })
        
        orphaned = rms_df[~rms_df['CaseNumber'].isin(cad_df['ReportNumberNew'])]
        
        assert len(orphaned) == 1
        assert orphaned['CaseNumber'].iloc[0] == '24-999999'
    
    def test_case_number_uniqueness_cad(self):
        """Test that CAD case numbers are unique"""
        
        df = pd.DataFrame({
            'ReportNumberNew': ['24-123456', '24-123456', '24-123457']
        })
        
        assert not df['ReportNumberNew'].is_unique, "Should detect duplicates"
        
        duplicates = df[df['ReportNumberNew'].duplicated()]
        assert len(duplicates) == 1
    
    def test_case_number_uniqueness_rms(self):
        """Test that RMS case numbers are unique"""
        
        df = pd.DataFrame({
            'CaseNumber': ['24-123456', '24-123457', '24-123456']
        })
        
        assert not df['CaseNumber'].is_unique
        
        duplicates = df[df['CaseNumber'].duplicated()]
        assert len(duplicates) == 1
    
    def test_join_merge_rate_acceptable(self):
        """Test that merge rate meets threshold"""
        
        cad_df = pd.DataFrame({
            'ReportNumberNew': [f'24-{i:06d}' for i in range(1, 101)]
        })
        
        # RMS has 75% of CAD records
        rms_df = pd.DataFrame({
            'CaseNumber': [f'24-{i:06d}' for i in range(1, 76)]
        })
        
        merged = pd.merge(
            cad_df, rms_df,
            left_on='ReportNumberNew',
            right_on='CaseNumber',
            how='left'
        )
        
        merge_rate = merged['CaseNumber'].notna().sum() / len(merged)
        
        assert merge_rate >= 0.70, "Merge rate should be at least 70%"
    
    def test_case_number_whitespace_handling(self):
        """Test that whitespace in case numbers is handled"""
        
        cad_df = pd.DataFrame({
            'ReportNumberNew': [' 24-123456 ', '24-123457']
        })
        
        # Strip whitespace
        cad_df['ReportNumberNew'] = cad_df['ReportNumberNew'].str.strip()
        
        valid = cad_df['ReportNumberNew'].str.match(r'^\d{2}-\d{6}$')
        assert valid.all()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])

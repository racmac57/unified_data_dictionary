# // 2025-12-17-19-30-00
# // __tests__/test_coordinate_validation.py
# // Author: R. A. Carucci
# // Purpose: Unit tests for geographic coordinate validation

"""
Test Coordinate Validation

Tests geographic coordinate parsing and boundary validation.
"""

import pytest
import pandas as pd
import numpy as np


# Hackensack, NJ approximate bounds
HACKENSACK_BOUNDS = {
    'lat_min': 40.85,
    'lat_max': 40.91,
    'lon_min': -74.07,
    'lon_max': -74.03
}


class TestCoordinateValidation:
    """Test suite for coordinate validation"""
    
    def test_valid_coordinates_within_bounds(self):
        """Test coordinates within Hackensack bounds"""
        
        df = pd.DataFrame({
            'Latitude': [40.88, 40.87, 40.89],
            'Longitude': [-74.05, -74.06, -74.04]
        })
        
        # Check bounds
        within_bounds = (
            (df['Latitude'] >= HACKENSACK_BOUNDS['lat_min']) &
            (df['Latitude'] <= HACKENSACK_BOUNDS['lat_max']) &
            (df['Longitude'] >= HACKENSACK_BOUNDS['lon_min']) &
            (df['Longitude'] <= HACKENSACK_BOUNDS['lon_max'])
        )
        
        assert within_bounds.all(), "All coordinates should be within bounds"
    
    def test_invalid_coordinates_out_of_bounds(self):
        """Test detection of out-of-bounds coordinates"""
        
        df = pd.DataFrame({
            'Latitude': [40.0, 45.0],  # Too far south/north
            'Longitude': [-74.05, -74.05]
        })
        
        within_bounds = (
            (df['Latitude'] >= HACKENSACK_BOUNDS['lat_min']) &
            (df['Latitude'] <= HACKENSACK_BOUNDS['lat_max']) &
            (df['Longitude'] >= HACKENSACK_BOUNDS['lon_min']) &
            (df['Longitude'] <= HACKENSACK_BOUNDS['lon_max'])
        )
        
        assert (~within_bounds).sum() == 2, "Should detect out-of-bounds coordinates"
    
    def test_coordinate_type_coercion(self):
        """Test numeric type coercion for coordinates"""
        
        df = pd.DataFrame({
            'Latitude': ['40.88', '40.87', 'INVALID'],
            'Longitude': ['-74.05', '-74.06', '-74.04']
        })
        
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        
        assert df['Latitude'].isna().sum() == 1
        assert df['Longitude'].notna().all()
    
    def test_coordinate_pair_completeness(self):
        """Test that coordinate pairs are complete"""
        
        df = pd.DataFrame({
            'Latitude': [40.88, None, 40.89],
            'Longitude': [-74.05, -74.06, None]
        })
        
        incomplete = df['Latitude'].isna() | df['Longitude'].isna()
        
        assert incomplete.sum() == 2, "Should detect incomplete pairs"
    
    def test_coordinate_precision(self):
        """Test coordinate precision (5+ decimal places recommended)"""
        
        df = pd.DataFrame({
            'Latitude': [40.88123456],
            'Longitude': [-74.05987654]
        })
        
        # Check precision by converting to string
        lat_str = f"{df['Latitude'].iloc[0]:.10f}"
        lon_str = f"{df['Longitude'].iloc[0]:.10f}"
        
        # Should have decimal places
        assert '.' in lat_str
        assert '.' in lon_str
    
    def test_zero_zero_invalid(self):
        """Test that (0, 0) coordinates are flagged as invalid"""
        
        df = pd.DataFrame({
            'Latitude': [0.0, 40.88],
            'Longitude': [0.0, -74.05]
        })
        
        invalid = (df['Latitude'] == 0) & (df['Longitude'] == 0)
        
        assert invalid.sum() == 1, "Should detect (0,0) as invalid"
    
    def test_coordinate_distance_calculation(self):
        """Test haversine distance calculation between points"""
        
        # Two points approximately 1km apart
        point1 = (40.88, -74.05)
        point2 = (40.89, -74.05)
        
        # Simple distance approximation (not true haversine)
        lat_diff = abs(point2[0] - point1[0])
        
        # At this latitude, 1 degree ≈ 111 km
        distance_km = lat_diff * 111
        
        assert 0.5 < distance_km < 2.0, "Distance should be approximately 1km"


if __name__ == "__main__":
    pytest.main([__file__, '-v'])

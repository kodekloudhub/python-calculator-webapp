import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.calc import safe_divide


class TestSafeDivide:
    """Test cases for safe_divide function"""

    def test_normal_division_positive_numbers(self):
        """Test normal division with positive numbers"""
        assert safe_divide(10, 2) == 5
        assert safe_divide(15, 3) == 5
        assert safe_divide(100, 4) == 25

    def test_normal_division_negative_numbers(self):
        """Test normal division with negative numbers"""
        assert safe_divide(-10, 2) == -5
        assert safe_divide(10, -2) == -5
        assert safe_divide(-10, -2) == 5

    def test_division_by_zero_raises_error(self):
        """Test that division by zero raises ValueError"""
        with pytest.raises(ValueError, match="division by zero"):
            safe_divide(10, 0)

        with pytest.raises(ValueError, match="division by zero"):
            safe_divide(-5, 0)

        with pytest.raises(ValueError, match="division by zero"):
            safe_divide(0, 0)

    def test_float_division(self):
        """Test division with floating point numbers"""
        assert safe_divide(7.5, 2.5) == 3.0
        assert safe_divide(10.0, 3.0) == pytest.approx(3.333333, rel=1e-5)
        assert safe_divide(-7.5, 2.5) == -3.0
        assert safe_divide(7.5, -2.5) == -3.0

    def test_division_with_zero_dividend(self):
        """Test division when dividend is zero"""
        assert safe_divide(0, 5) == 0
        assert safe_divide(0, -5) == 0
        assert safe_divide(0, 2.5) == 0.0

    def test_division_by_one(self):
        """Test division by one"""
        assert safe_divide(5, 1) == 5
        assert safe_divide(-5, 1) == -5
        assert safe_divide(5.5, 1) == 5.5

    def test_small_numbers(self):
        """Test division with very small numbers"""
        assert safe_divide(0.1, 0.1) == 1.0
        assert safe_divide(0.001, 0.001) == 1.0
        assert safe_divide(1e-10, 1e-5) == pytest.approx(1e-5)

    def test_large_numbers(self):
        """Test division with large numbers"""
        assert safe_divide(1000000, 1000) == 1000
        assert safe_divide(1e12, 1e6) == 1e6
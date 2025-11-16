"""
Tests básicos para verificar que el entorno de testing funciona.
"""

import pytest


def test_pytest_works():
    """Test básico para verificar que pytest funciona."""
    assert True


def test_imports_work():
    """Test que las importaciones básicas funcionan."""
    import pandas as pd
    import numpy as np
    
    assert pd is not None
    assert np is not None

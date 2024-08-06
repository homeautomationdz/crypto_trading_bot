# tests/test_trendline_calculator.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pandas as pd
from trendline_calculator import calculate_trendlines, detect_breakdowns

def test_calculate_trendlines():
    data = pd.DataFrame({
        'high': [1, 2, 3, 4, 5],
        'low': [0, 1, 2, 3, 4],
    }, index=pd.date_range(start='2024-01-01', periods=5, freq='H'))

    trendline_peaks, trendline_troughs = calculate_trendlines(data)
    assert isinstance(trendline_peaks, pd.Series)
    assert isinstance(trendline_troughs, pd.Series)

def test_detect_breakdowns():
    data = pd.DataFrame({
        'close': [1, 2, 3, 4, 5],
    }, index=pd.date_range(start='2024-01-01', periods=5, freq='H'))

    trendline_peaks = pd.Series([3], index=[2], dtype='float64')
    trendline_troughs = pd.Series([2], index=[1], dtype='float64')

    breakout_indices, breakdown_indices, touching_indices = detect_breakdowns(data, trendline_peaks, trendline_troughs)
    assert len(breakout_indices) == 2
    assert len(breakdown_indices) == 1
    assert len(touching_indices) == 2

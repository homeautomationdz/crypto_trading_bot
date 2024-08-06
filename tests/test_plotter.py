# tests/test_plotter.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pandas as pd
from plotter import plot_trendlines

def test_plot_trendlines():
    data = pd.DataFrame({
        'close': [1, 2, 3, 4, 5],
    }, index=pd.date_range(start='2024-01-01', periods=5, freq='H'))

    trendline_peaks = pd.Series([3], index=[2], dtype='float64')
    trendline_troughs = pd.Series([2], index=[1], dtype='float64')

    image_buffer = plot_trendlines(
        data, trendline_peaks, trendline_troughs, [2], [1], [0, 2], 'BTCUSDT', '1h', 4, 1, 100, 50, 50, 10
    )
    assert isinstance(image_buffer, bytes)

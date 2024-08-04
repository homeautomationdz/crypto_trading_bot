import numpy as np
from scipy.signal import argrelextrema
import pandas as pd
import logging

def calculate_trendlines(data):
    window_size = 10
    valid_data = data.iloc[:-5].copy()  # Ignore the last few candles

    valid_data['timestamp'] = valid_data.index.astype(np.int64) // 10**9  # Convert to seconds

    valid_data['peaks'] = valid_data.iloc[argrelextrema(valid_data['high'].values, np.greater_equal, order=window_size)[0]]['high']
    valid_data['troughs'] = valid_data.iloc[argrelextrema(valid_data['low'].values, np.less_equal, order=window_size)[0]]['low']

    peaks = valid_data.dropna(subset=['peaks'])
    troughs = valid_data.dropna(subset=['troughs'])

    if len(peaks) < 2 or len(troughs) < 2:
        logging.warning("Not enough peaks or troughs to calculate trendlines.")
        return None, None

    x_peaks = peaks['timestamp'].values[-2:]  # Use the numeric timestamps
    y_peaks = peaks['peaks'].values[-2:]

    x_peaks = x_peaks.astype(float)
    y_peaks = y_peaks.astype(float)

    if np.isnan(x_peaks).any() or np.isnan(y_peaks).any():
        logging.warning(f"NaN values found in peaks: x_peaks={x_peaks}, y_peaks={y_peaks}")
        return None, None

    fit_peaks = np.polyfit(x_peaks, y_peaks, 1)
    trendline_peaks = np.polyval(fit_peaks, valid_data['timestamp'].values)

    x_troughs = troughs['timestamp'].values[-2:]
    y_troughs = troughs['troughs'].values[-2:]

    x_troughs = x_troughs.astype(float)
    y_troughs = y_troughs.astype(float)

    if np.isnan(x_troughs).any() or np.isnan(y_troughs).any():
        logging.warning(f"NaN values found in troughs: x_troughs={x_troughs}, y_troughs={y_troughs}")
        return None, None

    fit_troughs = np.polyfit(x_troughs, y_troughs, 1)
    trendline_troughs = np.polyval(fit_troughs, valid_data['timestamp'].values)

    return trendline_peaks, trendline_troughs

def detect_breakdowns(data, trendline_peaks, trendline_troughs):
    if trendline_peaks is None or trendline_troughs is None:
        return pd.Index([]), pd.Index([]), pd.Index([])

    trendline_peaks_full = np.full(data.shape[0], np.nan)
    trendline_troughs_full = np.full(data.shape[0], np.nan)

    trendline_peaks_full[-len(trendline_peaks):] = trendline_peaks
    trendline_troughs_full[-len(trendline_troughs):] = trendline_troughs

    trendline_peaks_full = pd.Series(trendline_peaks_full, index=data.index, dtype='float64')
    trendline_troughs_full = pd.Series(trendline_troughs_full, index=data.index, dtype='float64')

    data['close'] = data['close'].astype(float)

    breakout_indices = data[data['close'] > trendline_peaks_full].index
    breakdown_indices = data[data['close'] < trendline_troughs_full].index
    touching_indices = data[(data['close'] == trendline_peaks_full) | (data['close'] == trendline_troughs_full)].index
    return breakout_indices, breakdown_indices, touching_indices

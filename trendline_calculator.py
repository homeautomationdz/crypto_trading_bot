import numpy as np
from scipy.signal import argrelextrema

def calculate_trendlines(data, ignore_last=5):
    window_size = 10
    valid_data = data.iloc[:-ignore_last].copy()
    valid_data['peaks'] = valid_data.iloc[argrelextrema(valid_data['high'].values, np.greater_equal, order=window_size)[0]]['high']
    valid_data['troughs'] = valid_data.iloc[argrelextrema(valid_data['low'].values, np.less_equal, order=window_size)[0]]['low']

    peaks = valid_data.dropna(subset=['peaks'])
    troughs = valid_data.dropna(subset=['troughs'])

    if len(peaks) < 2 or len(troughs) < 2:
        return None, None

    x_peaks = peaks.index.values[-2:]
    y_peaks = peaks['peaks'].values[-2:]
    fit_peaks = np.polyfit(x_peaks, y_peaks, 1)
    trendline_peaks = np.polyval(fit_peaks, np.arange(len(data)))

    x_troughs = troughs.index.values[-2:]
    y_troughs = troughs['troughs'].values[-2:]
    fit_troughs = np.polyfit(x_troughs, y_troughs, 1)
    trendline_troughs = np.polyval(fit_troughs, np.arange(len(data)))

    return trendline_peaks, trendline_troughs

def detect_breakout_breakdown(data, trendline_peaks, trendline_troughs):
    breakout_indices = data[data['close'] > trendline_peaks].index
    breakdown_indices = data[data['close'] < trendline_troughs].index
    touching_indices = data[(data['close'] == trendline_peaks) | (data['close'] == trendline_troughs)].index
    return breakout_indices, breakdown_indices, touching_indices

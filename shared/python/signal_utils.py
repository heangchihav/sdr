"""
Signal processing utilities for SDR applications.
"""
import numpy as np
from typing import Tuple, List, Union

def normalize_signal(signal: np.ndarray) -> np.ndarray:
    """
    Normalize signal to have zero mean and unit variance.
    
    Args:
        signal: Input signal array
        
    Returns:
        Normalized signal
    """
    return (signal - np.mean(signal)) / np.std(signal)

def fft_shift(signal: np.ndarray, sample_rate: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Perform FFT shift to center the frequency spectrum.
    
    Args:
        signal: Input time-domain signal
        sample_rate: Sampling rate in Hz
        
    Returns:
        Tuple of (frequencies, fft_values)
    """
    n = len(signal)
    fft_vals = np.fft.fftshift(np.fft.fft(signal))
    freqs = np.fft.fftshift(np.fft.fftfreq(n, 1/sample_rate))
    return freqs, fft_vals

def apply_window(signal: np.ndarray, window_type: str = 'hann') -> np.ndarray:
    """
    Apply a window function to the signal.
    
    Args:
        signal: Input signal
        window_type: Type of window ('hann', 'hamming', 'blackman', 'flattop')
        
    Returns:
        Windowed signal
    """
    window_types = {
        'hann': np.hanning,
        'hamming': np.hamming,
        'blackman': np.blackman,
        'flattop': np.bartlett
    }
    
    if window_type not in window_types:
        raise ValueError(f"Window type must be one of {list(window_types.keys())}")
    
    window = window_types[window_type](len(signal))
    return signal * window

def db_scale(signal: np.ndarray) -> np.ndarray:
    """
    Convert signal to decibel scale.
    
    Args:
        signal: Input signal
        
    Returns:
        Signal in dB scale
    """
    return 20 * np.log10(np.abs(signal) + 1e-12)  # Add small value to avoid log(0)

def find_peaks(signal: np.ndarray, threshold: float = 0.5, min_distance: int = 10) -> List[int]:
    """
    Find peaks in a 1D signal.
    
    Args:
        signal: Input signal
        threshold: Minimum peak height (relative to max)
        min_distance: Minimum distance between peaks
        
    Returns:
        List of peak indices
    """
    from scipy.signal import find_peaks as scipy_find_peaks
    peaks, _ = scipy_find_peaks(
        signal, 
        height=threshold * np.max(signal),
        distance=min_distance
    )
    return peaks.tolist()

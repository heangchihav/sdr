/**
 * Signal processing utilities for SDR applications (JavaScript version).
 */

/**
 * Normalize signal to have zero mean and unit variance.
 * @param {Float32Array|number[]} signal - Input signal array
 * @returns {Float32Array} Normalized signal
 */
export function normalizeSignal(signal) {
  const mean = signal.reduce((a, b) => a + b, 0) / signal.length;
  const std = Math.sqrt(
    signal.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / signal.length
  );
  return new Float32Array(signal.map(x => (x - mean) / (std || 1)));
}

/**
 * Perform FFT shift to center the frequency spectrum.
 * @param {Float32Array|number[]} signal - Input time-domain signal
 * @param {number} sampleRate - Sampling rate in Hz
 * @returns {Object} Object containing frequencies and FFT values
 */
export function fftShift(signal, sampleRate) {
  const n = signal.length;
  const fft = new FFT(n);
  const out = new Float32Array(n * 2);
  
  // Create complex input (real/imaginary interleaved)
  const input = new Float32Array(n * 2);
  for (let i = 0; i < n; i++) {
    input[i * 2] = signal[i];
    input[i * 2 + 1] = 0; // Imaginary part
  }
  
  // Perform FFT
  fft.realTransform(out, input, false);
  
  // Calculate frequencies
  const freqs = new Float32Array(n);
  const fftValues = new Float32Array(n);
  
  for (let i = 0; i < n; i++) {
    const idx = i < n / 2 ? i + n / 2 : i - n / 2;
    freqs[idx] = (i - n / 2) * (sampleRate / n);
    // Calculate magnitude
    fftValues[idx] = Math.sqrt(
      Math.pow(out[i * 2], 2) + Math.pow(out[i * 2 + 1], 2)
    );
  }
  
  return { frequencies: freqs, fftValues };
}

/**
 * Apply a window function to the signal.
 * @param {Float32Array} signal - Input signal
 * @param {string} windowType - Type of window ('hann', 'hamming', 'blackman')
 * @returns {Float32Array} Windowed signal
 */
export function applyWindow(signal, windowType = 'hann') {
  const n = signal.length;
  const window = new Float32Array(n);
  
  switch (windowType.toLowerCase()) {
    case 'hann':
      for (let i = 0; i < n; i++) {
        window[i] = 0.5 * (1 - Math.cos((2 * Math.PI * i) / (n - 1)));
      }
      break;
      
    case 'hamming':
      for (let i = 0; i < n; i++) {
        window[i] = 0.54 - 0.46 * Math.cos((2 * Math.PI * i) / (n - 1));
      }
      break;
      
    case 'blackman':
      for (let i = 0; i < n; i++) {
        window[i] =
          0.42 -
          0.5 * Math.cos((2 * Math.PI * i) / (n - 1)) +
          0.08 * Math.cos((4 * Math.PI * i) / (n - 1));
      }
      break;
      
    default:
      throw new Error(
        `Unknown window type: ${windowType}. Use 'hann', 'hamming', or 'blackman'.`
      );
  }
  
  return signal.map((val, i) => val * window[i]);
}

/**
 * Convert signal to decibel scale.
 * @param {Float32Array|number[]} signal - Input signal
 * @returns {Float32Array} Signal in dB scale
 */
export function toDecibels(signal) {
  const minDb = -120; // Minimum dB value to avoid -Infinity
  return new Float32Array(
    signal.map(x => 20 * Math.log10(Math.max(Math.abs(x), Math.pow(10, minDb / 20))))
  );
}

/**
 * Find peaks in a 1D signal.
 * @param {Float32Array|number[]} signal - Input signal
 * @param {number} threshold - Minimum peak height (0-1, relative to max)
 * @param {number} minDistance - Minimum distance between peaks
 * @returns {number[]} Array of peak indices
 */
export function findPeaks(signal, threshold = 0.5, minDistance = 10) {
  const peaks = [];
  const maxVal = Math.max(...signal);
  const thresholdValue = threshold * maxVal;
  
  for (let i = 1; i < signal.length - 1; i++) {
    if (
      signal[i] > thresholdValue &&
      signal[i] > signal[i - 1] &&
      signal[i] > signal[i + 1]
    ) {
      // Check distance from previous peak
      if (peaks.length === 0 || i - peaks[peaks.length - 1] >= minDistance) {
        peaks.push(i);
      }
    }
  }
  
  return peaks;
}

// Note: You'll need to include a JavaScript FFT library like fft.js in your project
// and initialize it before using the fftShift function.

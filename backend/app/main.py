from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sources.sdr_source import SDRSource
from processing.filters import BandPassFilter
from analysis.spectrum import SpectrumAnalyzer
import asyncio, json
from config import SAMPLE_RATE, FREQ, AMPLITUDE, BAND_LOW, BAND_HIGH

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sdr = SDRSource(samp_rate=SAMPLE_RATE, freq=FREQ, amplitude=AMPLITUDE)
analyzer = SpectrumAnalyzer()
filter_block = BandPassFilter(lowcut=BAND_LOW, highcut=BAND_HIGH, fs=SAMPLE_RATE)

@app.websocket("/ws/signal")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        samples = sdr.run_capture()
        filtered = filter_block.filter(samples)
        freq, magnitude = analyzer.spectrum(filtered)
        payload = {"freq": freq[:1024].tolist(), "mag": magnitude[:1024].tolist()}
        await websocket.send_text(json.dumps(payload))
        await asyncio.sleep(0.1)

@app.get("/update_freq")
def update_freq(freq: float):
    sdr.update_params(freq=freq)
    return {"status": "ok", "freq": freq}

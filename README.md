sdr-dashboard-monorepo/
├─ backend/
│   ├─ app/
│   │   ├─ sources/             # SDR sources (GNU Radio, RTL-SDR, etc.)
│   │   │   └─ sdr_source.py
│   │   ├─ processing/          # DSP modules (filters, etc.)
│   │   │   └─ filters.py
│   │   ├─ analysis/            # Spectrum & waveform analysis
│   │   │   └─ spectrum.py
│   │   ├─ main.py              # FastAPI backend server
│   │   └─ config.py            # SDR default parameters
│   ├─ requirements.txt
│   └─ README.md
│
├─ frontend/
│   ├─ package.json
│   ├─ pages/
│   │   ├─ index.js             # Main dashboard page
│   │   └─ _app.js
│   ├─ components/
│   │   ├─ SignalDisplay.js
│   │   └─ Controls.js
│   ├─ public/
│   │   └─ favicon.ico
│   └─ styles/
│       └─ globals.css
│
├─ shared/                      # Optional shared utilities
│   ├─ js/                      # Shared JS helpers
│   └─ python/                  # Shared Python utils
│
├─ .gitignore
└─ README.md

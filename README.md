# Circuit Designer Pro
A professional circuit design tool built with Streamlit.

## Features
- Calculate Totem Pole PFC circuit components
- Modern, professional UI
- Real-time calculations
- Interactive parameter input
- Comprehensive design recommendations

## Installation
1. Clone this repository
2. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage
Run the application using:
```bash
streamlit run app.py
```

## Input Parameters
- Voltage Parameters (Min/Max Input/Output Voltages)
- Power Parameters (Max Output Power, Efficiency)
- Frequency Parameters (Switching Frequency, Line Frequency)

## Outputs
- Inductance (L)
- Capacitance (C)
- Maximum Ripple Current
- Design Recommendations for MOSFETs
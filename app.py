import streamlit as st
from utils.calculations import CircuitCalculator
from utils.validators import validate_input

def main():
    st.set_page_config(
        page_title="Circuit Designer Pro",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Professional header
    st.title("PFC Circuit Designer Pro")
    st.markdown("""
    <style>
        /* Modern theme with better visibility */
        .main {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
        }
        .stTitle {
            color: #ffffff !important;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 600;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            padding: 20px 0;
            text-align: center;
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.1);
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 15px;
        }
        .stNumberInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            padding: 15px !important;
        }
        /* Headers styling */
        h3 {
            color: #00d2ff !important;
            font-weight: 500;
            margin-top: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }
        /* Info boxes styling */
        .stAlert {
            background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%) !important;
            color: white !important;
            border: none !important;
            padding: 20px !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        /* Button styling */
        .stButton>button {
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
            color: white !important;
            border: none !important;
            padding: 15px 30px !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.2) !important;
        }
        /* Results text */
        .stMarkdown {
            color: #ffffff !important;
        }
        p {
            color: #ffffff !important;
        }
        /* Subheader styling */
        .stSubheader {
            color: #00d2ff !important;
            font-weight: 500;
            margin: 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }
        /* Error message styling */
        .stError {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff4b4b 100%) !important;
            color: white !important;
            border: none !important;
            padding: 20px !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        /* Labels styling */
        .stMarkdown label {
            color: #ffffff !important;
            font-weight: 500;
            margin-bottom: 8px;
        }
        /* Number input arrows styling */
        .stNumberInput div[data-baseweb="spinbutton"] button {
            background-color: rgba(255,255,255,0.1) !important;
            border: none !important;
            color: white !important;
        }
        /* Container styling */
        .element-container {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add a subtitle with design description
    st.markdown("""
        <p style='color: #00d2ff; text-align: center; font-size: 1.2em; margin-bottom: 30px;'>
            Professional Circuit Design Tool for Power Factor Correction
        </p>
    """, unsafe_allow_html=True)

    # Main content area
    st.subheader("Input Parameters")

    # Using columns for better organization
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Voltage Parameters")
        v_in_min = st.number_input("Min Input Voltage (V)", min_value=0.0, value=100.0)
        v_in_max = st.number_input("Max Input Voltage (V)", min_value=0.0, value=240.0)
        v_out_min = st.number_input("Min Output Voltage (V)", min_value=0.0, value=380.0)
        v_out_max = st.number_input("Max Output Voltage (V)", min_value=0.0, value=400.0)

    with col2:
        st.markdown("### Power Parameters")
        p_out_max = st.number_input("Max Output Power (W)", min_value=0.0, value=3000.0)
        efficiency = st.number_input("Efficiency (0-1)", min_value=0.0, max_value=1.0, value=0.98)
        v_ripple_max = st.number_input("Max Output Voltage Ripple (V)", min_value=0.0, value=20.0)

    with col3:
        st.markdown("### Frequency Parameters")
        switching_freq = st.number_input("Switching Frequency (Hz)", min_value=0.0, value=65000.0)
        line_freq_min = st.number_input("Min Line Frequency (Hz)", min_value=0.0, value=50.0)

    # Calculate button with professional styling
    if st.button("Calculate Component Values", key="calculate_btn"):
        # Input validation
        inputs = {
            "v_in_min": v_in_min,
            "v_in_max": v_in_max,
            "v_out_min": v_out_min,
            "v_out_max": v_out_max,
            "p_out_max": p_out_max,
            "efficiency": efficiency,
            "switching_freq": switching_freq,
            "line_freq_min": line_freq_min,
            "v_ripple_max": v_ripple_max
        }

        if validate_input(inputs):
            try:
                calculator = CircuitCalculator()
                results = calculator.calculate("Totem Pole PFC", inputs)
                
                # Display results in a professional format
                st.subheader("Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info("Required Components")
                    st.write(f"Inductance (L): {results['inductance']*1000:.2f} mH")
                    st.write(f"Capacitance (C): {results['capacitance']*1e6:.2f} μF")
                
                with col2:
                    st.info("Circuit Characteristics")
                    st.write(f"Maximum Ripple Current: {results['ripple_current']:.2f} A")
                    
                # Additional design notes
                st.markdown("### Design Notes")
                st.markdown("""
                - Select SiC MOSFETs with voltage rating > Max Output Voltage
                - Choose MOSFETs with lowest RDSon while considering cost and reliability
                - Ensure proper thermal management for the calculated current levels
                """)
            except Exception as e:
                st.error(f"Calculation error: {str(e)}")
        else:
            st.error("Please check your input values. All values must be positive.")

if __name__ == "__main__":
    main()
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
    st.title("Circuit Designer Pro")
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
    
    # Circuit type selection tabs
    tab1, tab2 = st.tabs(["Totem Pole PFC", "Synchronous Buck"])

    with tab1:
        st.markdown("""
            <p style='color: #00d2ff; text-align: center; font-size: 1.2em; margin-bottom: 30px;'>
                Power Factor Correction Circuit Design
            </p>
        """, unsafe_allow_html=True)
        
        st.subheader("PFC Input Parameters")
        
        # PFC Circuit parameters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Voltage Parameters")
            pfc_v_in_min = st.number_input("Min Input Voltage (V)", key="pfc_vin_min", min_value=0.0, value=100.0)
            pfc_v_in_max = st.number_input("Max Input Voltage (V)", key="pfc_vin_max", min_value=0.0, value=240.0)
            pfc_v_out_min = st.number_input("Min Output Voltage (V)", key="pfc_vout_min", min_value=0.0, value=380.0)
            pfc_v_out_max = st.number_input("Max Output Voltage (V)", key="pfc_vout_max", min_value=0.0, value=400.0)

        with col2:
            st.markdown("### Power Parameters")
            pfc_p_out_max = st.number_input("Max Output Power (W)", key="pfc_pout_max", min_value=0.0, value=3000.0)
            pfc_efficiency = st.number_input("Efficiency (0-1)", key="pfc_eff", min_value=0.0, max_value=1.0, value=0.98)
            pfc_v_ripple_max = st.number_input("Max Output Voltage Ripple (V)", key="pfc_vripple", min_value=0.0, value=20.0)

        with col3:
            st.markdown("### Frequency Parameters")
            pfc_switching_freq = st.number_input("Switching Frequency (Hz)", key="pfc_fs", min_value=0.0, value=65000.0)
            pfc_line_freq_min = st.number_input("Min Line Frequency (Hz)", key="pfc_fline", min_value=0.0, value=50.0)

        # PFC Calculate button
        if st.button("Calculate PFC Components", key="pfc_calc_btn"):
            pfc_inputs = {
                "v_in_min": pfc_v_in_min,
                "v_in_max": pfc_v_in_max,
                "v_out_min": pfc_v_out_min,
                "v_out_max": pfc_v_out_max,
                "p_out_max": pfc_p_out_max,
                "efficiency": pfc_efficiency,
                "switching_freq": pfc_switching_freq,
                "line_freq_min": pfc_line_freq_min,
                "v_ripple_max": pfc_v_ripple_max
            }

            if validate_input(pfc_inputs):
                try:
                    calculator = CircuitCalculator()
                    results = calculator.calculate("Totem Pole PFC", pfc_inputs)
                    
                    st.subheader("PFC Circuit Results")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info("Required Components")
                        st.write(f"Inductance (L): {results['inductance']*1000:.2f} mH")
                        st.write(f"Capacitance (C): {results['capacitance']*1e6:.2f} μF")
                    
                    with col2:
                        st.info("Circuit Characteristics")
                        st.write(f"Maximum Ripple Current: {results['ripple_current']:.2f} A")
                        
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

    with tab2:
        st.markdown("""
            <p style='color: #00d2ff; text-align: center; font-size: 1.2em; margin-bottom: 30px;'>
                Synchronous Buck Converter Design
            </p>
        """, unsafe_allow_html=True)
        
        st.subheader("Buck Converter Input Parameters")
        
        # Buck Circuit parameters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Voltage Parameters")
            buck_v_in_min = st.number_input("Min Input Voltage (V)", key="buck_vin_min", min_value=0.0, value=12.0)
            buck_v_in_max = st.number_input("Max Input Voltage (V)", key="buck_vin_max", min_value=0.0, value=24.0)
            buck_v_out_min = st.number_input("Min Output Voltage (V)", key="buck_vout_min", min_value=0.0, value=3.3)
            buck_v_out_max = st.number_input("Max Output Voltage (V)", key="buck_vout_max", min_value=0.0, value=5.0)
            buck_v_ripple_max = st.number_input("Output Voltage Ripple (V)", key="buck_vripple", min_value=0.0, value=0.05)
            buck_v_in_ripple = st.number_input("Input Voltage Ripple (V)", key="buck_vinripple", min_value=0.0, value=0.1)

        with col2:
            st.markdown("### Power & Current Parameters")
            buck_p_out_max = st.number_input("Max Output Power (W)", key="buck_pout_max", min_value=0.0, value=50.0)
            buck_efficiency = st.number_input("Efficiency (0-1)", key="buck_eff", min_value=0.0, max_value=1.0, value=0.95)
            buck_i_out_ripple = st.number_input("Inductor Current Ripple (A)", key="buck_iripple", min_value=0.0, value=0.5)

        with col3:
            st.markdown("### Transient Parameters")
            buck_switching_freq = st.number_input("Switching Frequency (Hz)", key="buck_fs", min_value=0.0, value=500000.0)
            buck_v_overshoot = st.number_input("Voltage Overshoot (V)", key="buck_vover", min_value=0.0, value=0.1)
            buck_v_undershoot = st.number_input("Voltage Undershoot (V)", key="buck_vunder", min_value=0.0, value=0.1)
            buck_i_loadstep = st.number_input("Load Step (A)", key="buck_istep", min_value=0.0, value=1.0)

        # Buck Calculate button
        if st.button("Calculate Buck Components", key="buck_calc_btn"):
            buck_inputs = {
                "v_in_min": buck_v_in_min,
                "v_in_max": buck_v_in_max,
                "v_out_min": buck_v_out_min,
                "v_out_max": buck_v_out_max,
                "p_out_max": buck_p_out_max,
                "efficiency": buck_efficiency,
                "switching_freq": buck_switching_freq,
                "v_ripple_max": buck_v_ripple_max,
                "v_in_ripple": buck_v_in_ripple,
                "i_out_ripple": buck_i_out_ripple,
                "v_overshoot": buck_v_overshoot,
                "v_undershoot": buck_v_undershoot,
                "i_loadstep": buck_i_loadstep
            }

            if validate_input(buck_inputs):
                try:
                    calculator = CircuitCalculator()
                    results = calculator.calculate("Synchronous Buck", buck_inputs)
                    
                    st.subheader("Buck Converter Results")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info("Required Components")
                        st.write(f"Inductance (L): {results['inductance']*1e6:.2f} μH")
                        st.write(f"Output Capacitance (Cout): {results['output_capacitance']*1e6:.2f} μF")
                        st.write(f"Input Capacitance (Cin): {results['input_capacitance']*1e6:.2f} μF")
                    
                    with col2:
                        st.info("Circuit Characteristics")
                        st.write(f"Maximum Duty Cycle: {results['duty_cycle_max']*100:.1f}%")
                        if results['output_cap_transient']:
                            st.write(f"Transient-based Cout: {results['output_cap_transient']*1e6:.2f} μF")
                        
                    st.markdown("### Design Notes")
                    st.markdown("""
                    - Select MOSFETs with voltage rating > Max Input Voltage
                    - Choose MOSFETs with lowest RDSon for efficiency
                    - For output capacitor, prefer ceramic capacitors for low ESR
                    - Consider thermal management for the calculated current levels
                    - Select inductors with saturation current > Peak inductor current
                    """)
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
            else:
                st.error("Please check your input values. All values must be positive.")

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

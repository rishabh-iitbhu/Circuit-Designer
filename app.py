import streamlit as st
from utils.calculations import CircuitCalculator
from utils.validators import validate_input
from utils.mosfet_selector import suggest_mosfets
from utils.inductor_selector import suggest_inductors
from utils.capacitor_selector import suggest_capacitors

def main():
    st.set_page_config(
        page_title="Circuit Designer",
        page_icon="⚡",
        layout="wide"
    )

    st.title("Circuit Designer")

    # Circuit type selection tabs
    tab1, tab2 = st.tabs(["PFC Circuit", "Buck Converter"])

    with tab1:
        st.subheader("PFC Circuit Parameters")
        
        # PFC Circuit parameters in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Voltage Parameters")
            v_in_min = st.number_input("Min Input Voltage (V)", key="pfc_vin_min", min_value=0.0, value=100.0)
            v_in_max = st.number_input("Max Input Voltage (V)", key="pfc_vin_max", min_value=0.0, value=240.0)
            v_out_min = st.number_input("Min Output Voltage (V)", key="pfc_vout_min", min_value=0.0, value=380.0)
            v_out_max = st.number_input("Max Output Voltage (V)", key="pfc_vout_max", min_value=0.0, value=400.0)

        with col2:
            st.markdown("### Power Parameters")
            p_out_max = st.number_input("Max Output Power (W)", key="pfc_pout_max", min_value=0.0, value=3000.0)
            efficiency = st.number_input("Efficiency (0-1)", key="pfc_eff", min_value=0.0, max_value=1.0, value=0.98)
            v_ripple_max = st.number_input("Max Output Voltage Ripple (V)", key="pfc_vripple", min_value=0.0, value=20.0)

        with col3:
            st.markdown("### Frequency Parameters")
            switching_freq = st.number_input("Switching Frequency (Hz)", key="pfc_fs", min_value=0.0, value=65000.0)
            line_freq_min = st.number_input("Min Line Frequency (Hz)", key="pfc_fline", min_value=0.0, value=50.0)

        if st.button("Calculate Component Values", key="pfc_calc_btn"):
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
                    
                    st.markdown("### Calculated Values")
                    st.write(f"Inductance = {results['inductance']*1000:.2f} mH")
                    st.write(f"Capacitance = {results['capacitance']*1e6:.2f} μF")
                    st.write(f"Ripple Current = {results['ripple_current']:.2f} A")
                    
                    # Component suggestions section
                    st.markdown("### Suggested Components")
                    
                    # MOSFET suggestions
                    with st.expander("🔌 Suggested MOSFETs"):
                        try:
                            mosfets = suggest_mosfets(v_in_max, results['ripple_current'])
                            if mosfets:
                                for idx, mosfet in enumerate(mosfets[:3]):
                                    with st.container():
                                        st.subheader(f"Option {idx + 1}: {mosfet['Part Name']}")
                                        st.write(f"Voltage Rating: {mosfet['Input Voltage']}V")
                                        st.write(f"Current Rating: {mosfet['Current Rating']}A")
                                        st.write(f"Technology: {mosfet['Technology']}")
                                        st.write(f"Package: {mosfet['Package Type']}")
                                        st.write(f"Brand: {mosfet['Brand']}")
                                        st.write(f"Price: ${mosfet['Price']}")
                                        st.write(f"[Purchase Link]({mosfet['Supplier Link']})")
                            else:
                                st.info("No suitable MOSFETs found for the calculated requirements.")
                        except Exception as e:
                            st.error(f"Error suggesting MOSFETs: {str(e)}")
                    
                    # Inductor suggestions
                    with st.expander("🛠️ Suggested Inductors"):
                        try:
                            inductors = suggest_inductors(results['inductance'], results['ripple_current'])
                            if inductors:
                                for idx, inductor in enumerate(inductors[:3]):
                                    with st.container():
                                        st.subheader(f"Option {idx + 1}: {inductor['Part Name']}")
                                        st.write(f"Inductance: {inductor['Inductance']*1e6:.2f} μH")
                                        st.write(f"Current Rating: {inductor['Current Rating']}A")
                                        st.write(f"DC Resistance: {inductor['DC Resistance']}")
                                        st.write(f"Efficiency: {inductor['Efficiency']}")
                                        st.write(f"Package: {inductor['Package Type']}")
                                        st.write(f"Brand: {inductor['Brand']}")
                                        st.write(f"Price: ${inductor['Price']}")
                                        st.write(f"[Purchase Link]({inductor['Supplier Link']})")
                            else:
                                st.info("No suitable inductors found for the calculated requirements.")
                        except Exception as e:
                            st.error(f"Error suggesting inductors: {str(e)}")
                    
                    # Capacitor suggestions
                    with st.expander("💾 Suggested Capacitors"):
                        try:
                            capacitors = suggest_capacitors(results['capacitance'], v_out_max)
                            if capacitors:
                                for idx, capacitor in enumerate(capacitors[:3]):
                                    with st.container():
                                        st.subheader(f"Option {idx + 1}: {capacitor['Part Name']}")
                                        st.write(f"Capacitance: {capacitor['Capacitance']*1e6:.2f} μF")
                                        st.write(f"Voltage Rating: {capacitor['Voltage Rating']}V")
                                        st.write(f"Type: {capacitor['Type']}")
                                        if capacitor['ESR'] != '-':
                                            st.write(f"ESR: {capacitor['ESR']}")
                                        st.write(f"Performance: {capacitor['Efficiency/Performance']}")
                                        st.write(f"Package: {capacitor['Package Type']}")
                                        st.write(f"Brand: {capacitor['Brand']}")
                                        st.write(f"Price: ${capacitor['Price']}")
                                        st.write(f"[Purchase Link]({capacitor['Supplier Link']})")
                            else:
                                st.info("No suitable capacitors found for the calculated requirements.")
                        except Exception as e:
                            st.error(f"Error suggesting capacitors: {str(e)}")
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
            else:
                st.error("Please check your input values. All values must be positive.")

    with tab2:
        st.subheader("Buck Converter Parameters")
        
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

        if st.button("Calculate Component Values", key="buck_calc_btn"):
            inputs = {
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

            if validate_input(inputs):
                try:
                    calculator = CircuitCalculator()
                    results = calculator.calculate("Synchronous Buck", inputs)
                    
                    st.markdown("### Calculated Values")
                    st.write(f"Inductance = {results['inductance']*1e6:.2f} μH")
                    st.write(f"Output Capacitance = {results['output_capacitance']*1e6:.2f} μF")
                    st.write(f"Input Capacitance = {results['input_capacitance']*1e6:.2f} μF")
                    st.write(f"Maximum Duty Cycle = {results['duty_cycle_max']*100:.1f}%")
                    
                    # MOSFET suggestions
                    st.markdown("### Suggested MOSFETs")
                    try:
                        # Calculate maximum current
                        max_current = buck_p_out_max / buck_v_out_min * (1 + buck_i_out_ripple)
                        st.info(f"Looking for MOSFETs with: Voltage ≥ {buck_v_in_max:.1f}V, Current ≥ {max_current:.1f}A")
                        mosfets = suggest_mosfets(buck_v_in_max, max_current)
                        if mosfets:
                            for idx, mosfet in enumerate(mosfets[:3]):  # Show top 3 suggestions
                                with st.expander(f"Option {idx + 1}: {mosfet['Part Name']}"):
                                    st.write(f"Voltage Rating: {mosfet['Input Voltage']}")
                                    st.write(f"Current Rating: {mosfet['Current Rating']}")
                                    st.write(f"Technology: {mosfet['Technology']}")
                                    st.write(f"Package: {mosfet['Package Type']}")
                                    st.write(f"Brand: {mosfet['Brand']}")
                                    st.write(f"Price: {mosfet['Price']}")
                                    st.write(f"[Purchase Link]({mosfet['Supplier Link']})")
                        else:
                            st.info("No suitable MOSFETs found for the calculated requirements.")
                    except Exception as e:
                        st.error(f"Error suggesting MOSFETs: {str(e)}")
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
            else:
                st.error("Please check your input values. All values must be positive.")

if __name__ == "__main__":
    main()
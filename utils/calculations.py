import math

class CircuitCalculator:
    def __init__(self):
        pass

    # PFC Circuit Calculations
    def calculate_ripple_current(self, p_out_max, v_in_max, efficiency):
        """
        Calculate the maximum ripple current for PFC
        I_(RIPPLE MAX) = (0.1 × √2 × P_(OUT MAX)) / (V_(IN MAX) × Eff)
        """
        return (0.1 * math.sqrt(2) * p_out_max) / (v_in_max * efficiency)

    def calculate_inductance(self, v_out_max, switching_freq, i_ripple_max):
        """
        Calculate the inductance for PFC
        L = V_(OUT MAX) / (12 × F_s × I_(RIPPLE MAX))
        """
        return v_out_max / (12 * switching_freq * i_ripple_max)

    def calculate_min_capacitance(self, p_out_max, line_freq_min, v_ripple_max, v_out):
        """
        Calculate the minimum capacitance for PFC
        C_(OUT MIN) = P_(OUT MAX) / (4 × π × f_(Line_min) × V_(RIPPLE MAX) × V_OUT)
        """
        return p_out_max / (4 * math.pi * line_freq_min * v_ripple_max * v_out)

    # Buck Converter Calculations
    def calculate_duty_cycle_max(self, v_out_max, v_in_min):
        """
        Calculate maximum duty cycle
        D_MAX = V_(OUT MAX) / V_(IN MIN)
        """
        return v_out_max / v_in_min

    def calculate_buck_inductance(self, v_in_max, v_out_min, d_max, f_s, i_out_ripple):
        """
        Calculate inductance for buck converter
        L = ((V_IN MAX - V_OUT MIN) × D_MAX) / (F_s × I_OUT RIPPLE)
        """
        return ((v_in_max - v_out_min) * d_max) / (f_s * i_out_ripple)

    def calculate_buck_output_cap_ripple(self, i_out_ripple, f_s, v_ripple_max):
        """
        Calculate output capacitance based on voltage ripple
        C_OUT MIN = I_OUT RIPPLE / (8 × F_s × V_RIPPLE MAX)
        """
        return i_out_ripple / (8 * f_s * v_ripple_max)

    def calculate_buck_output_cap_transient(self, l, i_loadstep, v_undershoot, v_in_max, v_out_min, d_max, v_overshoot, v_out_max):
        """
        Calculate output capacitance based on transient response
        """
        # For undershoot
        c_undershoot = (l * i_loadstep**2) / (2 * v_undershoot * (v_in_max - v_out_min) * d_max)
        # For overshoot
        c_overshoot = (l * i_loadstep**2) / (2 * v_overshoot * v_out_max)
        return max(c_undershoot, c_overshoot)

    def calculate_buck_input_cap(self, p_out_max, efficiency, v_in_min, d_max, f_s, v_in_ripple):
        """
        Calculate input capacitance
        I_IN = P_OUT MAX / (Eff × V_IN MIN)
        C_IN = (I_IN × D_MAX) / (F_s × V_IN RIPPLE)
        """
        i_in = p_out_max / (efficiency * v_in_min)
        return (i_in * d_max) / (f_s * v_in_ripple)

    def calculate_buck_circuit(self, inputs):
        """
        Calculate Synchronous Buck Converter circuit parameters
        """
        try:
            # Calculate duty cycle
            d_max = self.calculate_duty_cycle_max(
                inputs["v_out_max"],
                inputs["v_in_min"]
            )

            # Calculate inductance
            inductance = self.calculate_buck_inductance(
                inputs["v_in_max"],
                inputs["v_out_min"],
                d_max,
                inputs["switching_freq"],
                inputs["i_out_ripple"]
            )

            # Calculate output capacitance based on ripple
            c_out_ripple = self.calculate_buck_output_cap_ripple(
                inputs["i_out_ripple"],
                inputs["switching_freq"],
                inputs["v_ripple_max"]
            )

            # Calculate output capacitance based on transient if parameters provided
            if all(key in inputs for key in ["i_loadstep", "v_overshoot", "v_undershoot"]):
                c_out_transient = self.calculate_buck_output_cap_transient(
                    inductance,
                    inputs["i_loadstep"],
                    inputs["v_undershoot"],
                    inputs["v_in_max"],
                    inputs["v_out_min"],
                    d_max,
                    inputs["v_overshoot"],
                    inputs["v_out_max"]
                )
                c_out = max(c_out_ripple, c_out_transient)
            else:
                c_out = c_out_ripple

            # Calculate input capacitance
            c_in = self.calculate_buck_input_cap(
                inputs["p_out_max"],
                inputs["efficiency"],
                inputs["v_in_min"],
                d_max,
                inputs["switching_freq"],
                inputs["v_in_ripple"]
            )

            return {
                "duty_cycle_max": d_max,
                "inductance": inductance,
                "output_capacitance": c_out,
                "input_capacitance": c_in,
                "output_cap_ripple": c_out_ripple,
                "output_cap_transient": c_out_transient if 'c_out_transient' in locals() else None
            }
        except Exception as e:
            raise ValueError(f"Error in calculations: {str(e)}")

    def calculate_pfc_circuit(self, inputs):
        """
        Calculate Totem Pole PFC circuit parameters
        """
        try:
            i_ripple_max = self.calculate_ripple_current(
                inputs["p_out_max"],
                inputs["v_in_max"],
                inputs["efficiency"]
            )
            inductance = self.calculate_inductance(
                inputs["v_out_max"],
                inputs["switching_freq"],
                i_ripple_max
            )
            capacitance = self.calculate_min_capacitance(
                inputs["p_out_max"],
                inputs["line_freq_min"],
                inputs["v_ripple_max"],
                inputs["v_out_max"]
            )
            return {
                "inductance": inductance,
                "capacitance": capacitance,
                "ripple_current": i_ripple_max
            }
        except Exception as e:
            raise ValueError(f"Error in calculations: {str(e)}")

    def calculate(self, circuit_type, inputs):
        """
        Main calculation method that delegates to specific circuit calculators
        """
        if circuit_type == "Totem Pole PFC":
            return self.calculate_pfc_circuit(inputs)
        elif circuit_type == "Synchronous Buck":
            return self.calculate_buck_circuit(inputs)
        else:
            raise ValueError("Invalid circuit type")
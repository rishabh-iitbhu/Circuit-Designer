import math

class CircuitCalculator:
    def __init__(self):
        pass

    def calculate_ripple_current(self, p_out_max, v_in_max, efficiency):
        """
        Calculate the maximum ripple current
        I_(RIPPLE MAX) = (0.1 × √2 × P_(OUT MAX)) / (V_(IN MAX) × Eff)
        """
        return (0.1 * math.sqrt(2) * p_out_max) / (v_in_max * efficiency)

    def calculate_inductance(self, v_out_max, switching_freq, i_ripple_max):
        """
        Calculate the inductance
        L = V_(OUT MAX) / (12 × F_s × I_(RIPPLE MAX))
        """
        return v_out_max / (12 * switching_freq * i_ripple_max)

    def calculate_min_capacitance(self, p_out_max, line_freq_min, v_ripple_max, v_out):
        """
        Calculate the minimum capacitance
        C_(OUT MIN) = P_(OUT MAX) / (4 × π × f_(Line_min) × V_(RIPPLE MAX) × V_OUT)
        """
        return p_out_max / (4 * math.pi * line_freq_min * v_ripple_max * v_out)

    def calculate_pfc_circuit(self, inputs):
        """
        Calculate Totem Pole PFC circuit parameters
        """
        try:
            # Calculate maximum ripple current
            i_ripple_max = self.calculate_ripple_current(
                inputs["p_out_max"],
                inputs["v_in_max"],
                inputs["efficiency"]
            )

            # Calculate inductance
            inductance = self.calculate_inductance(
                inputs["v_out_max"],
                inputs["switching_freq"],
                i_ripple_max
            )

            # Calculate minimum capacitance
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
        else:
            raise ValueError("Invalid circuit type")
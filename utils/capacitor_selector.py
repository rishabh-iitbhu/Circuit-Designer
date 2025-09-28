import pandas as pd
import os

def load_capacitor_data():
    """Load capacitor data from CSV file."""
    file_path = os.path.join(os.path.dirname(__file__), 'Assets', 'Top_Capacitors_2025.csv')
    try:
        df = pd.read_csv(file_path)
        # Clean capacitance data (convert all to F)
        df['Capacitance'] = df['Capacitance'].apply(lambda x: 
            float(x.replace('mF', 'e-3').replace('µF', 'e-6').replace('nF', 'e-9').replace('F', ''))
        )
        # Clean voltage data
        df['Voltage Rating'] = df['Voltage Rating'].str.replace('V', '').astype(float)
        # Clean price data
        df['Price'] = df['Price'].str.replace('$', '').astype(float)
        return df
    except Exception as e:
        raise Exception(f"Error loading capacitor data: {str(e)}")

def suggest_capacitors(capacitance_requirement, voltage_requirement):
    """
    Suggest suitable capacitors based on capacitance and voltage requirements.
    
    Args:
        capacitance_requirement (float): Required capacitance in F
        voltage_requirement (float): Required voltage rating in V
    
    Returns:
        list: List of suitable capacitors with their details
    """
    try:
        capacitors_df = load_capacitor_data()
        
        # Add margins for requirements
        capacitance_with_margin = capacitance_requirement * 0.8  # Allow 20% lower for capacitance
        voltage_with_margin = abs(voltage_requirement) * 1.2  # Need 20% higher for voltage
        
        suitable_capacitors = capacitors_df[
            (capacitors_df['Capacitance'] >= capacitance_with_margin) &
            (capacitors_df['Voltage Rating'] >= voltage_with_margin)
        ]
        
        # Sort by price and efficiency/performance
        suitable_capacitors = suitable_capacitors.sort_values(
            by=['Price', 'Efficiency/Performance'],
            ascending=[True, False]
        )
        
        return suitable_capacitors.to_dict('records')
    except Exception as e:
        raise Exception(f"Error suggesting capacitors: {str(e)}")
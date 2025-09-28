import pandas as pd
import os

def load_mosfet_data():
    """Load MOSFET data from CSV file."""
    file_path = os.path.join(os.path.dirname(__file__), 'Assets', 'Top_MOSFETs_2025.csv')
    try:
        # Read CSV with comma delimiter
        df = pd.read_csv(file_path)
        
        # Clean voltage data - remove 'V' and convert to float
        df['Input Voltage'] = df['Input Voltage'].str.replace('V', '').astype(float)
        
        # Clean current data - remove 'A' and handle 'unknown' values
        df['Current Rating'] = df['Current Rating'].apply(lambda x: 0 if x == 'unknown' else float(x.replace('A', '')))
        
        # Clean price data - remove '$' and convert to float
        df['Price'] = df['Price'].str.replace('$', '').astype(float)
        
        return df
    except Exception as e:
        raise Exception(f"Error loading MOSFET data: {str(e)}")

def suggest_mosfets(voltage_requirement, current_requirement):
    """
    Suggest suitable MOSFETs based on voltage and current requirements.
    
    Args:
        voltage_requirement (float): Required voltage rating in V
        current_requirement (float): Required current rating in A
    
    Returns:
        list: List of suitable MOSFETs with their details
    """
    try:
        mosfets_df = load_mosfet_data()
        
        # Filter MOSFETs based on requirements
        # Add 20% margin for voltage and current ratings
        voltage_with_margin = abs(voltage_requirement) * 1.2  # Use absolute value for voltage
        current_with_margin = abs(current_requirement) * 1.2  # Use absolute value for current
        
        suitable_mosfets = mosfets_df[
            (mosfets_df['Input Voltage'] >= voltage_with_margin) &
            (mosfets_df['Current Rating'] >= current_with_margin)
        ]
        
        # Sort by price and efficiency
        suitable_mosfets = suitable_mosfets.sort_values(
            by=['Price', 'Efficiency'],
            ascending=[True, False]
        )
        
        return suitable_mosfets.to_dict('records')
    except Exception as e:
        raise Exception(f"Error suggesting MOSFETs: {str(e)}")
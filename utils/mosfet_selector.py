import pandas as pd
import os

def load_mosfet_data():
    """Load MOSFET data from CSV file."""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Assets', 'optivolt_mosfet_dataset.csv')
    try:
        # Read CSV with comma delimiter
        df = pd.read_csv(file_path)
        
        # Create consistent column names
        df = df.rename(columns={
            'MOSFET Name': 'Part Name',
            'Vds (V)': 'Input Voltage',
            'Continuous Id (A)': 'Current Rating',
            'Package': 'Package Type'
        })
        
        # Convert voltage and current to float
        df['Input Voltage'] = pd.to_numeric(df['Input Voltage'], errors='coerce')
        df['Current Rating'] = pd.to_numeric(df['Current Rating'], errors='coerce')
        
        # Add standard columns if missing
        if 'Price' not in df.columns:
            df['Price'] = 0.0
        if 'Efficiency/Performance' not in df.columns:
            df['Efficiency/Performance'] = df['Efficiency Range'].fillna('N/A')
        if 'Supplier Link' not in df.columns:
            df['Supplier Link'] = df['Datasheet URL']
        
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
        
        # Sort by price and efficiency range
        # Convert efficiency range to numeric value (take the average of the range)
        suitable_mosfets['Efficiency_Value'] = suitable_mosfets['Efficiency Range'].str.extract('(\d+).*?(\d+)').astype(float).mean(axis=1)
        
        # Sort by price and efficiency value
        suitable_mosfets = suitable_mosfets.sort_values(
            by=['Price', 'Efficiency_Value'],
            ascending=[True, False]
        )
        
        return suitable_mosfets.to_dict('records')
    except Exception as e:
        raise Exception(f"Error suggesting MOSFETs: {str(e)}")
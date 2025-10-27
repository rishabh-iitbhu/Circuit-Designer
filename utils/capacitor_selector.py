import pandas as pd
import os

def load_capacitor_data():
    """Load capacitor data from CSV file."""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Assets', 'powercrux_output_cap_dataset_starter.csv')
    try:
        df = pd.read_csv(file_path)
        
        # Clean and convert capacitance data to float
        # Handle any ranges like '8.2–1500' by taking the lower value
        df['Capacitance'] = df['Capacitance_uF'].astype(str).apply(
            lambda x: float(x.split('–')[0]) if '–' in x else float(x)
        )
        
        # Convert capacitance from µF to F
        df['Capacitance'] = df['Capacitance'] * 1e-6
        
        # Handle voltage data - use original Voltage_V column
        df['Voltage Rating'] = pd.to_numeric(df['Voltage_V'], errors='coerce')
        
        # Clean ESR data - extract numeric value from string patterns
        def clean_esr(esr_str):
            if pd.isna(esr_str):
                return None
            esr_str = str(esr_str)
            if 'low' in esr_str.lower():
                return 1.0  # Assume low ESR is good
            if '~' in esr_str:
                # Extract first number from patterns like "~12-20"
                nums = [float(s) for s in esr_str.replace('~','').split('-')[0].split() if s.replace('.','',1).isdigit()]
                return nums[0] if nums else None
            if 'series' in esr_str.lower():
                return None
            try:
                return float(esr_str.split()[0])
            except:
                return None
                
        df['ESR'] = df['ESR_mOhm'].apply(clean_esr)
        
        # Create performance metric from Type and Dielectric
        df['Performance'] = df.apply(
            lambda row: f"{row['Type']} ({row['Dielectric']})" if pd.notna(row['Dielectric']) else row['Type'],
            axis=1
        )
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
        
        # Filter capacitors meeting requirements
        suitable_capacitors = capacitors_df[
            (capacitors_df['Capacitance'] >= capacitance_with_margin) &
            (capacitors_df['Voltage Rating'] >= voltage_with_margin)
        ].copy()  # Make a copy to avoid SettingWithCopyWarning
        
        if len(suitable_capacitors) == 0:
            return []
            
        # Calculate how close each capacitor is to the required value
        suitable_capacitors['CapacitanceMatch'] = abs(
            (suitable_capacitors['Capacitance'] - capacitance_requirement) / capacitance_requirement
        )
        
        # Sort by capacitance match (closest to requirement) and ESR (lower is better)
        suitable_capacitors = suitable_capacitors.sort_values(
            by=['CapacitanceMatch', 'ESR'],
            ascending=[True, True],
            na_position='last'
        )
        
        return suitable_capacitors.to_dict('records')
    except Exception as e:
        raise Exception(f"Error suggesting capacitors: {str(e)}")
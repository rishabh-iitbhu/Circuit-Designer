import pandas as pd
import os

def load_inductor_data():
    """Load inductor data from CSV file."""
    file_path = os.path.join(os.path.dirname(__file__), 'Assets', 'Top_Inductors_2025.csv')
    try:
        df = pd.read_csv(file_path)
        # Clean inductance data (convert all to H)
        df['Inductance'] = df['Inductance'].apply(lambda x: 
            float(x.replace('mH', 'e-3').replace('µH', 'e-6').replace('H', ''))
        )
        # Clean current data
        df['Current Rating'] = df['Current Rating'].str.replace('A', '').astype(float)
        # Clean price data
        df['Price'] = df['Price'].str.replace('$', '').astype(float)
        return df
    except Exception as e:
        raise Exception(f"Error loading inductor data: {str(e)}")

def suggest_inductors(inductance_requirement, current_requirement):
    """
    Suggest suitable inductors based on inductance and current requirements.
    
    Args:
        inductance_requirement (float): Required inductance in H
        current_requirement (float): Required current rating in A
    
    Returns:
        list: List of suitable inductors with their details
    """
    try:
        inductors_df = load_inductor_data()
        
        # Add 20% margin for inductance and current ratings
        inductance_with_margin = inductance_requirement * 0.8  # Allow 20% lower for inductance
        current_with_margin = abs(current_requirement) * 1.2
        
        suitable_inductors = inductors_df[
            (inductors_df['Inductance'] >= inductance_with_margin) &
            (inductors_df['Current Rating'] >= current_with_margin)
        ]
        
        # Sort by price and efficiency
        suitable_inductors = suitable_inductors.sort_values(
            by=['Price', 'Efficiency'],
            ascending=[True, False]
        )
        
        return suitable_inductors.to_dict('records')
    except Exception as e:
        raise Exception(f"Error suggesting inductors: {str(e)}")
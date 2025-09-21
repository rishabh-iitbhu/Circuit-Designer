def validate_input(inputs):
    """
    Validate input parameters for circuit calculations
    
    Args:
        inputs (dict): Dictionary containing input parameters
        
    Returns:
        bool: True if all inputs are valid, False otherwise
    """
    try:
        # Check if all values are positive
        for value in inputs.values():
            if value <= 0:
                return False
        return True
    except Exception:
        return False
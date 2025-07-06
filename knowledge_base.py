"""
This module contains the knowledge base for the Concrete Strength Predictor.
It includes rules and constraints based on domain expertise for concrete engineering.
"""

def check_inputs(input_values):
    """
    Checks the input values against a set of rules.

    Args:
        input_values (dict): A dictionary of input feature values.

    Returns:
        list: A list of warning messages. Returns an empty list if all checks pass.
    """
    warnings = []
    
    # Rule 1: Critical components must not be zero.
    zero_fields = []
    if input_values.get('cement') == 0:
        zero_fields.append("Cement")
    if input_values.get('water') == 0:
        zero_fields.append("Water")
    if input_values.get('age') == 0:
        zero_fields.append("Age")

    if zero_fields:
        warnings.append(f"The following fields must not be zero for a valid prediction: {', '.join(zero_fields)}.")
        return warnings # Return early if critical fields are zero

    # Rule 2: Water-Cement Ratio
    w_c_ratio = input_values.get('water') / input_values.get('cement')
    if not 0.4 <= w_c_ratio <= 0.6:
        warnings.append(f"Warning: The water-cement ratio ({w_c_ratio:.2f}) is outside the typical range of 0.4 to 0.6.")

    # Rule 3: Aggregate Proportions (assuming standard concrete)
    total_aggregates = input_values.get('coarseagg') + input_values.get('fineagg')
    if total_aggregates > 0:
        coarse_agg_ratio = input_values.get('coarseagg') / total_aggregates
        if not 0.5 <= coarse_agg_ratio <= 0.7:
            warnings.append(f"Warning: The coarse aggregate to total aggregate ratio ({coarse_agg_ratio:.2f}) is outside the typical range of 0.5 to 0.7.")

    # Rule 4: Superplasticizer Dosage (typical range)
    if input_values.get('superplasticizer') > 20:
        warnings.append("Warning: The superplasticizer dosage is higher than the typical maximum of 20 kg/m³.")

    return warnings

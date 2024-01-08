"""Parser module to parse gear config.json."""

from typing import Tuple
from flywheel_gear_toolkit import GearToolkitContext

def parse_config(
    gear_context: GearToolkitContext, 
) -> Tuple[dict, dict, dict]: # Add dict for each set of outputs
    """Parse the config and other options from the context, both gear and app options.

    Returns:
        input_image
    """

    input_image = gear_context.get_input_path("nifti-input")

    # gear_inputs, 
    return input_image
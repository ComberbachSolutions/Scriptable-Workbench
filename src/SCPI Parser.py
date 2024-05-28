import re

def parse_scpi(command: str) -> dict:
    """
    Parses a generic SCPI command into a dictionary.

    Args:
        command (str): The SCPI command as a string.

    Returns:
        dict: Parsed command as a dictionary with 'command', 'parameters', and optional 'subsystem'.
    """
    # Regular expression for matching SCPI command
    pattern = r'(?P<command>[A-Za-z]+):?(?P<subsystem>[A-Za-z]*)\s*(?P<parameters>.*)'

    match = re.match(pattern, command)
    if not match:
        raise ValueError(f"Invalid SCPI command: {command}")

    # Extract the groups from the matched pattern
    command_dict = match.groupdict()

    # Split parameters by commas or spaces
    if command_dict['parameters']:
        parameters = re.split(r'[, ]+', command_dict['parameters'].strip())
        command_dict['parameters'] = parameters
    else:
        command_dict['parameters'] = []

    # Remove empty strings from the dictionary
    command_dict = {k: v for k, v in command_dict.items() if v}

    return command_dict

# Example usage
scpi_command = "SENS:VOLT:DC:RANG [<range|MINimum|MAXimum|AUTOmatic>]"
parsed = parse_scpi(scpi_command)
print(parsed)

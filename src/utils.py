# src/utils.py
"""
Utility functions for working with LFSRs.
"""


def calculate_maximum_period(size):
    """
    Calculate the maximum period of an LFSR based on its size.
    
    For a maximum-length sequence, the period is 2^n - 1.
    
    Parameters:
        size (int): The size of the LFSR in bits.
    
    Returns:
        int: The maximum possible period.
    """
    return (1 << size) - 1


def is_maximum_length(lfsr, max_checks=None):
    """
    Check if an LFSR generates a maximum-length sequence.
    
    Parameters:
        lfsr: An LFSR instance with next_bit() and reset() methods.
        max_checks (int, optional): Maximum number of iterations to check.
                                   If None, checks 2^n iterations.
    
    Returns:
        bool: True if the LFSR generates a maximum-length sequence.
    """
    # Store the initial state to restore it later
    if hasattr(lfsr, 'get_state'):
        initial_state = lfsr.get_state()
    
    # Determine the expected period
    expected_period = calculate_maximum_period(lfsr.size)
    
    # If max_checks is not specified, use 2 * expected_period
    if max_checks is None:
        max_checks = 2 * expected_period
    
    # Track the sequence of states
    seen_states = set()
    current_period = 0
    
    # Generate bits and track states
    for _ in range(max_checks):
        # Get the current state as an integer for easy comparison
        state_int = lfsr.state
        
        # If we've seen this state before, we've found a cycle
        if state_int in seen_states:
            break
        
        seen_states.add(state_int)
        lfsr.next_bit()
        current_period += 1
    
    # Restore the initial state if possible
    if hasattr(lfsr, 'reset') and hasattr(lfsr, 'get_state'):
        if hasattr(initial_state, 'state'):
            lfsr.reset(int(initial_state, 2))
    
    # Check if the period matches the expected maximum
    return current_period == expected_period


def generate_sequence(lfsr, length):
    """
    Generate a sequence of bits from an LFSR.
    
    Parameters:
        lfsr: An LFSR instance with next_bit() method.
        length (int): Number of bits to generate.
    
    Returns:
        list: A list of generated bits.
    """
    return [lfsr.next_bit() for _ in range(length)]


def bits_to_bytes(bits):
    """
    Convert a list of bits to bytes.
    
    Parameters:
        bits (list): List of bit values (0 or 1).
    
    Returns:
        bytes: The bits packed into bytes.
    """
    # Ensure we have a multiple of 8 bits
    padded_bits = bits + [0] * ((8 - len(bits) % 8) % 8)
    
    # Pack bits into bytes
    result_bytes = bytearray()
    for i in range(0, len(padded_bits), 8):
        byte_bits = padded_bits[i:i+8]
        byte_value = 0
        for j, bit in enumerate(byte_bits):
            byte_value |= (bit & 1) << (7 - j)
        result_bytes.append(byte_value)
    
    return bytes(result_bytes)
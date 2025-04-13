# src/basic_lfsr.py
"""
Basic LFSR Implementation

A simple 4-bit Linear Feedback Shift Register with hardcoded polynomial x⁴ + x + 1.
"""


class BasicLFSR:
    """
    A basic 4-bit Linear Feedback Shift Register implementation
    with hardcoded polynomial x⁴ + x + 1 (taps at positions 3 and 0).
    
    This implementation is mainly for educational purposes and serves
    as a simple example of an LFSR with fixed parameters.
    """
    
    def __init__(self):
        """
        Initialize the LFSR with the default seed 0110 (binary) = 6 (decimal).
        """
        self.state = 0b0110
        self.size = 4  # 4-bit LFSR
    
    def get_state(self):
        """
        Return the current state as a binary string.
        
        Returns:
            str: Binary representation of the current state.
        """
        return format(self.state, f'0{self.size}b')
    
    def next_bit(self):
        """
        Calculate next bit, update state, and return the output bit.
        Based on polynomial x⁴ + x + 1 (taps at positions 3 and 0).
        
        Returns:
            int: The output bit (0 or 1).
        """
        # Extract the rightmost bit (output bit)
        output_bit = self.state & 1
        
        # Calculate feedback: XOR the bits at tap positions
        bit_3 = (self.state >> 3) & 1  # 4th bit (position 3)
        bit_0 = self.state & 1         # 1st bit (position 0)
        feedback = bit_3 ^ bit_0       # XOR operation
        
        # Shift right by 1 and place feedback at the leftmost position
        self.state = (self.state >> 1) | (feedback << (self.size - 1))
        
        return output_bit
    
    def __str__(self):
        """
        Human-readable representation.
        
        Returns:
            str: String representation of the LFSR.
        """
        return f"BasicLFSR(state={self.get_state()})"
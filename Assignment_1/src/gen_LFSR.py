# src/general_lfsr.py
"""
General LFSR Implementation

A configurable Linear Feedback Shift Register implementation
supporting arbitrary size, tap positions, and seed values.
"""


class GeneralLFSR:
    """
    A general-purpose Linear Feedback Shift Register implementation
    supporting arbitrary size, tap positions, and seed values.
    
    This implementation allows for experimentation with different LFSR
    configurations and can be used for various applications from random
    number generation to cryptographic operations.
    """
    
    def __init__(self, size=4, taps=None, seed=0b0110):
        """
        Initialize a general-purpose LFSR.
        
        Parameters:
            size (int): Bit length of the LFSR.
            taps (list): List of bit positions (0-indexed) to use for feedback.
                         If None, uses [size-1, 0] as default.
            seed (int): Initial state as an integer.
        
        Raises:
            ValueError: If seed is too large for the given size or if taps
                        include positions outside the valid range.
        """
        self.size = size
        self.max_value = (1 << size) - 1  # Maximum value based on size (all 1s)
        
        # Ensure seed is valid for the given size
        if seed > self.max_value:
            raise ValueError(f"Seed value too large for {size}-bit LFSR")
        self.state = seed
        
        # Default taps for a common LFSR polynomial (x^n + x + 1)
        self.taps = taps if taps else [size-1, 0]
        
        # Validate that all taps are within range
        if any(tap >= self.size or tap < 0 for tap in self.taps):
            raise ValueError(f"Taps must be between 0 and {self.size-1}")
    
    def get_state(self):
        """
        Return the current state as a binary string.
        
        Returns:
            str: Binary representation of the current state.
        """
        return format(self.state, f'0{self.size}b')
    
    def set_taps(self, new_taps):
        """
        Change the feedback taps.
        
        Parameters:
            new_taps (list): New list of tap positions.
        
        Returns:
            list: The updated taps list.
            
        Raises:
            ValueError: If any tap position is out of range.
        """
        # Validate that all taps are within range
        if any(tap >= self.size or tap < 0 for tap in new_taps):
            raise ValueError(f"Taps must be between 0 and {self.size-1}")
        self.taps = new_taps
        return self.taps
    
    def reset(self, new_seed=None):
        """
        Reset the LFSR to the initial seed or a new seed.
        
        Parameters:
            new_seed (int, optional): New seed value. If None, keeps current state.
        
        Returns:
            int: The current state after reset.
            
        Raises:
            ValueError: If the new seed is too large for the LFSR size.
        """
        if new_seed is not None:
            if new_seed > self.max_value:
                raise ValueError(f"Seed value too large for {self.size}-bit LFSR")
            self.state = new_seed
        return self.state
    
    def next_bit(self):
        """
        Calculate next bit, update state, and return the output bit.
        Uses dynamic feedback calculation based on tap positions.
        
        Returns:
            int: The output bit (0 or 1).
        """
        # Extract the rightmost bit (output bit)
        output_bit = self.state & 1
        
        # Calculate feedback by XORing bits at all tap positions
        feedback = 0
        for tap in self.taps:
            feedback ^= (self.state >> tap) & 1
        
        # Shift right by 1 and place feedback at the leftmost position
        self.state = (self.state >> 1) | (feedback << (self.size - 1))
        
        return output_bit
    
    def __str__(self):
        """
        Human-readable representation of LFSR state.
        
        Returns:
            str: String representation of the LFSR.
        """
        return f"LFSR(size={self.size}, taps={self.taps}, state={self.get_state()})"


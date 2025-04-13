# tests/test_basic_lfsr.py
"""
Unit tests for the BasicLFSR implementation.
"""
import unittest
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.basic_lfsr import BasicLFSR


class TestBasicLFSR(unittest.TestCase):
    """Test cases for the BasicLFSR class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lfsr = BasicLFSR()
    
    def test_initial_state(self):
        """Test that the initial state is 0110."""
        self.assertEqual(self.lfsr.get_state(), "0110")
    
    def test_next_bit_sequence(self):
        """Test that the LFSR generates the expected sequence of bits."""
        # Expected sequence for first 5 iterations with seed 0110
        expected_bits = [0, 1, 1, 0, 0]
        
        # Generate bits and compare
        for expected in expected_bits:
            bit = self.lfsr.next_bit()
            self.assertEqual(bit, expected)
    
    def test_state_transitions(self):
        """Test that the state transitions correctly."""
        # Expected states after each iteration
        expected_states = ["0011", "1001", "1100", "0110"]
        
        for expected_state in expected_states:
            self.lfsr.next_bit()
            self.assertEqual(self.lfsr.get_state(), expected_state)
    
    def test_full_period(self):
        """Test that the LFSR completes a full period of 2^4-1 = 15 states."""
        # Store the initial state
        initial_state = self.lfsr.state
        
        # We should see 15 unique states (excluding all zeros)
        seen_states = set()
        
        # Generate bits until we see a repeat or exceed maximum
        max_iterations = 20  # More than the expected period
        
        for _ in range(max_iterations):
            state = self.lfsr.state
            
            # If we've seen this state before, we've found a cycle
            if state in seen_states:
                break
                
            seen_states.add(state)
            self.lfsr.next_bit()
        
        # Check that we saw exactly 15 unique states
        self.assertEqual(len(seen_states), 15)
        
        # Check that we eventually return to the initial state
        found_initial = False
        for _ in range(15):  # One full period
            if self.lfsr.state == initial_state:
                found_initial = True
                break
            self.lfsr.next_bit()
            
        self.assertTrue(found_initial)


if __name__ == '__main__':
    unittest.main()
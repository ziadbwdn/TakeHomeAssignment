# tests/test_general_lfsr.py
"""
Unit tests for the GeneralLFSR implementation.
"""
import unittest
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.general_lfsr import GeneralLFSR


class TestGeneralLFSR(unittest.TestCase):
    """Test cases for the GeneralLFSR class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a default 4-bit LFSR
        self.lfsr = GeneralLFSR()
    
    def test_initialization(self):
        """Test initialization with various parameters."""
        # Test default initialization
        lfsr = GeneralLFSR()
        self.assertEqual(lfsr.size, 4)
        self.assertEqual(lfsr.taps, [3, 0])
        self.assertEqual(lfsr.state, 0b0110)
        
        # Test custom initialization
        lfsr = GeneralLFSR(size=8, taps=[7, 3, 2, 1], seed=0b10101010)
        self.assertEqual(lfsr.size, 8)
        self.assertEqual(lfsr.taps, [7, 3, 2, 1])
        self.assertEqual(lfsr.state, 0b10101010)
        
        # Test invalid seed
        with self.assertRaises(ValueError):
            GeneralLFSR(size=4, seed=0b11111)
            
        # Test invalid taps
        with self.assertRaises(ValueError):
            GeneralLFSR(size=4, taps=[4, 0])
    
    def test_set_taps(self):
        """Test setting new tap positions."""
        # Set valid taps
        self.lfsr.set_taps([2, 1])
        self.assertEqual(self.lfsr.taps, [2, 1])
        
        # Try setting invalid taps
        with self.assertRaises(ValueError):
            self.lfsr.set_taps([4, 0])
            
        with self.assertRaises(ValueError):
            self.lfsr.set_taps([-1, 0])
    
    def test_reset(self):
        """Test resetting the LFSR state."""
        # Advance the LFSR a few steps
        for _ in range(3):
            self.lfsr.next_bit()
            
        # Reset to default seed
        self.lfsr.reset()
        self.assertEqual(self.lfsr.state, 0b0110)
        
        # Reset to custom seed
        self.lfsr.reset(0b1001)
        self.assertEqual(self.lfsr.state, 0b1001)
        
        # Try resetting with invalid seed
        with self.assertRaises(ValueError):
            self.lfsr.reset(0b10000)
    
    def test_next_bit(self):
        """Test generating next bits with custom taps."""
        # Initialize with custom taps [2, 1] on a 4-bit LFSR
        lfsr = GeneralLFSR(size=4, taps=[2, 1], seed=0b1111)
        
        # Expected bits for first few iterations
        expected_bits = [1, 1, 1, 0, 1, 0, 0]
        
        # Generate and check bits
        generated_bits = [lfsr.next_bit() for _ in range(len(expected_bits))]
        self.assertEqual(generated_bits, expected_bits)
    
    def test_multiple_taps(self):
        """Test LFSR with multiple tap positions."""
        # Create 8-bit LFSR with 4 taps
        lfsr = GeneralLFSR(size=8, taps=[7, 5, 3, 0], seed=0b10101010)
        
        # Generate some bits and ensure they're 0 or 1
        for _ in range(20):
            bit = lfsr.next_bit()
            self.assertIn(bit, [0, 1])


if __name__ == '__main__':
    unittest.main()
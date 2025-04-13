# examples/basic_example.py
"""
Basic example demonstrating the use of BasicLFSR.
"""
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.basic_lfsr import BasicLFSR


def main():
    """Demonstrate basic LFSR functionality."""
    print("Basic LFSR Example")
    print("-----------------")
    
    # Create a basic 4-bit LFSR
    lfsr = BasicLFSR()
    print(f"Initial state: {lfsr.get_state()}")
    
    # Generate and print first 20 bits
    print("\nGenerating sequence:")
    for i in range(20):
        bit = lfsr.next_bit()
        print(f"Bit {i+1}: {bit} (State: {lfsr.get_state()})")
    
    print("\nNote that after 15 steps, the sequence will start to repeat.")


if __name__ == "__main__":
    main()
# examples/general_example.py
"""
Example demonstrating the use of GeneralLFSR with various configurations.
"""
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.general_lfsr import GeneralLFSR
from src.utils import generate_sequence, calculate_maximum_period


def demonstrate_different_sizes():
    """Demonstrate LFSRs of different sizes."""
    print("LFSR Size Comparison")
    print("-------------------")
    
    sizes = [4, 8, 16]
    
    for size in sizes:
        lfsr = GeneralLFSR(size=size, taps=[size-1, 0], seed=1)
        max_period = calculate_maximum_period(size)
        
        print(f"\n{size}-bit LFSR:")
        print(f"  Maximum period: {max_period} bits")
        
        # Generate first 10 bits
        sequence = generate_sequence(lfsr, 10)
        print(f"  First 10 bits: {sequence}")


def demonstrate_different_taps():
    """Demonstrate LFSRs with different tap configurations."""
    print("\nLFSR Tap Configuration Comparison")
    print("--------------------------------")
    
    # Common primitive polynomials for 8-bit LFSR
    tap_configs = [
        [7, 0],            # x^8 + x + 1
        [7, 6, 5, 3],      # x^8 + x^7 + x^6 + x^4 + 1
        [7, 6, 4, 2]       # x^8 + x^7 + x^5 + x^3 + 1
    ]
    
    for i, taps in enumerate(tap_configs):
        lfsr = GeneralLFSR(size=8, taps=taps, seed=1)
        
        # Generate 20 bits
        sequence = generate_sequence(lfsr, 20)
        
        print(f"\nConfiguration {i+1} (taps={taps}):")
        print(f"  Sequence: {sequence}")
        
        # Split sequence into 4-bit chunks for readability
        hex_representation = []
        for j in range(0, len(sequence), 4):
            chunk = sequence[j:j+4]
            if len(chunk) == 4:
                hex_value = chunk[0]*8 + chunk[1]*4 + chunk[2]*2 + chunk[3]
                hex_representation.append(hex(hex_value)[2:])
        
        print(f"  Hex (4-bit chunks): {''.join(hex_representation)}")


def demonstrate_state_manipulation():
    """Demonstrate state manipulation in the GeneralLFSR."""
    print("\nLFSR State Manipulation")
    print("----------------------")
    
    lfsr = GeneralLFSR(size=8, taps=[7, 5, 3, 0], seed=0b10101010)
    
    print(f"Initial state: {lfsr.get_state()}")
    
    # Generate 5 bits
    print("\nGenerating 5 bits:")
    for i in range(5):
        bit = lfsr.next_bit()
        print(f"  Bit {i+1}: {bit} (State: {lfsr.get_state()})")
    
    # Change taps
    print("\nChanging taps to [7, 0]")
    lfsr.set_taps([7, 0])
    
    # Generate 5 more bits
    print("\nGenerating 5 more bits with new taps:")
    for i in range(5):
        bit = lfsr.next_bit()
        print(f"  Bit {i+1}: {bit} (State: {lfsr.get_state()})")
    
    # Reset to new seed
    print("\nResetting to seed 0b11001100")
    lfsr.reset(0b11001100)
    
    # Generate 5 more bits
    print("\nGenerating 5 bits with new seed:")
    for i in range(5):
        bit = lfsr.next_bit()
        print(f"  Bit {i+1}: {bit} (State: {lfsr.get_state()})")


def main():
    """Run all demonstrations."""
    demonstrate_different_sizes()
    demonstrate_different_taps()
    demonstrate_state_manipulation()


if __name__ == "__main__":
    main()

# examples/cryptographic_usage.py
"""
Example demonstrating a simple cryptographic application of LFSRs.
"""
import sys
from pathlib import Path
import time

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.general_lfsr import GeneralLFSR
from src.utils import bits_to_bytes


class SimpleStreamCipher:
    """
    A simple stream cipher using an LFSR as a pseudorandom generator.
    
    WARNING: This is for educational purposes only and should NOT be used
    for actual encryption, as simple LFSRs are not cryptographically secure.
    """
    
    def __init__(self, key, size=16):
        """
        Initialize the cipher with a key.
        
        Parameters:
            key (int): The key to use for the cipher (used as seed).
            size (int): The size of the LFSR in bits.
        """
        # Create LFSR with key as seed
        # Using a common primitive polynomial for the given size
        if size == 8:
            taps = [7, 5, 3, 0]  # x^8 + x^6 + x^4 + x + 1
        elif size == 16:
            taps = [15, 14, 12, 3]  # x^16 + x^15 + x^13 + x^4 + 1
        elif size == 32:
            taps = [31, 30, 28, 1]  # x^32 + x^31 + x^29 + x^2 + 1
        else:
            # Default to x^n + x + 1
            taps = [size-1, 0]
            
        self.lfsr = GeneralLFSR(size=size, taps=taps, seed=key)
    
    def generate_keystream(self, length):
        """
        Generate a keystream of the specified length.
        
        Parameters:
            length (int): The number of bits to generate.
            
        Returns:
            list: A list of bits.
        """
        return [self.lfsr.next_bit() for _ in range(length)]
    
    def encrypt(self, plaintext):
        """
        Encrypt a string using the LFSR-based stream cipher.
        
        Parameters:
            plaintext (str): The text to encrypt.
            
        Returns:
            bytes: The encrypted data.
        """
        # Convert plaintext to bytes
        plaintext_bytes = plaintext.encode('utf-8')
        
        # Generate keystream of sufficient length (8 bits per byte)
        keystream = self.generate_keystream(len(plaintext_bytes) * 8)
        
        # Convert keystream to bytes
        keystream_bytes = bits_to_bytes(keystream)
        
        # XOR plaintext with keystream
        ciphertext = bytes(p ^ k for p, k in zip(plaintext_bytes, keystream_bytes))
        
        return ciphertext
    
    def decrypt(self, cipherte):
        '''
        '''
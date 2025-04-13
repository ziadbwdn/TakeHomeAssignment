# Assignment 1: LFSR Theory and Implementation

## What is an LFSR?

A Linear Feedback Shift Register (LFSR) is a shift register whose input bit is a linear function (typically XOR) of its previous state. LFSRs are commonly used for generating pseudorandom binary sequences.

## Basic Structure

An LFSR consists of:
1. A shift register of n bits
2. Feedback taps (positions within the register)
3. A feedback function (typically XOR) that combines the values at tap positions

## Feedback Polynomial

The configuration of an LFSR is often described using a polynomial, known as the feedback polynomial or characteristic polynomial. For example:
- A 4-bit LFSR with polynomial x⁴ + x + 1 has taps at positions 3 and 0
- An 8-bit LFSR with polynomial x⁸ + x⁴ + x³ + x² + 1 has taps at positions 7, 3, 2, and 1

## Maximum Length Sequences

To achieve the maximum possible sequence length (2^n - 1), the feedback polynomial must be primitive. Not all polynomials are primitive, and selecting appropriate tap positions is crucial for cryptographic applications.

## Applications

LFSRs have numerous applications:
- Stream cipher key generation
- Pseudorandom number generation
- Built-in self-test for integrated circuits
- Error detection and correction (CRC)
- Digital signal processing

## Security Considerations

Basic LFSRs are not cryptographically secure on their own because:
- Given 2n consecutive bits of output, the entire state can be determined
- The period is limited to 2^n - 1
- The sequence is linearly predictable

For cryptographic applications, LFSRs are typically combined with non-linear components or other techniques to increase security.

----
# Assignment 2:  Django Warehouse System

# Overview
This documentation provides a comprehensive guide to the Django Warehouse System, a REST API designed to simulate a stock management system for a distribution center. The application allows tracking of inventory items, recording purchase and sale transactions, and generating audit reports that track changes in stock levels over time.
System Architecture
The system is built using Django and Django REST Framework (DRF) with a modular approach consisting of four primary modules:

# Items Module: Manages inventory items in the warehouse
- Purchases Module: Handles stock replenishment through purchase transactions
- Sells Module: Manages the reduction of stock through sales transactions
- Reports Module: Generates historical reports of stock changes over time

Each module follows Django's app structure pattern with models, serializers, views, and URL configurations.

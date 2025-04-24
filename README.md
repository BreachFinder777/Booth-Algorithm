# Booth's Multiplication Algorithm Implementation

This repository contains a Python implementation of Booth's multiplication algorithm, a technique for multiplying binary numbers in two's complement notation.

## Overview

Booth's algorithm is an efficient method for binary multiplication that handles both positive and negative numbers in two's complement form. It reduces the number of additions needed by grouping consecutive 1s in the multiplier.

## How Booth's Algorithm Works

Booth's algorithm examines pairs of bits in the multiplier (including an appended 0 bit) and performs operations based on these bit pairs:

- When transitioning from 0 to 1 (01): Add the multiplicand to the accumulator
- When transitioning from 1 to 0 (10): Subtract the multiplicand from the accumulator
- When bits are the same (00 or 11): No operation

After each operation, the accumulator and multiplier are arithmetically right-shifted.

## Implementation Details

The Python implementation:

1. Converts input numbers to binary two's complement representation
2. Processes the bits according to Booth's algorithm
3. Displays step-by-step operations and the final result
4. Includes explanations of each step

## Example Calculation: 15 × (-3)

Let's trace through how our algorithm multiplies 15 by -3:

### Initial Values
- Multiplicand (M): 15 = 00001111 in binary
- Multiplier: -3 = 11111101 in two's complement
- -M = 11110001 (negative of multiplicand)

### Step-by-Step Process

The algorithm initializes:
- Accumulator (A): 00000000
- Multiplier (Q): 11111101
- Extra bit (Q₋₁): 0

For each bit position:
1. Examine Q₀Q₋₁ to determine the operation (add M, subtract M, or no operation)
2. Perform the operation on the accumulator
3. Right shift [A, Q, Q₋₁]
4. Repeat for each bit

As we process through the bits:
- When Q₀Q₋₁ = 01, we add M to A
- When Q₀Q₋₁ = 10, we subtract M (add -M) to A
- When Q₀Q₋₁ = 00 or 11, we do nothing

### Final Result

After 8 iterations (for 8-bit numbers), the result is in the combined A and Q registers. For 15 × (-3), we get:
- Result in binary: 1111111111010011
- Result in decimal: -45

## Understanding Negative Results

When the result is negative, we can calculate its value by taking the two's complement:
1. Invert all bits
2. Add 1
3. Calculate the decimal value
4. Apply the negative sign

## Python Code Example

```python
def booths_algorithm(multiplicand, multiplier, bit_size=8):
    # Convert to binary and handle negative numbers
    if multiplicand < 0:
        multiplicand_bin = bin((1 << bit_size) + multiplicand)[2:].zfill(bit_size)
    else:
        multiplicand_bin = bin(multiplicand)[2:].zfill(bit_size)
    
    if multiplier < 0:
        multiplier_bin = bin((1 << bit_size) + multiplier)[2:].zfill(bit_size)
    else:
        multiplier_bin = bin(multiplier)[2:].zfill(bit_size)
    
    # 2's complement for negative M
    neg_multiplicand = ""
    if multiplicand >= 0:
        # Find 2's complement if M is positive
        inverted = ''.join('1' if bit == '0' else '0' for bit in multiplicand_bin)
        neg_multiplicand = bin(int(inverted, 2) + 1)[2:].zfill(bit_size)
    else:
        # If M is already negative, its positive value is its 2's complement
        inverted = ''.join('1' if bit == '0' else '0' for bit in multiplicand_bin)
        neg_multiplicand = bin(int(inverted, 2) + 1)[2:].zfill(bit_size)
    
    # Initialize registers
    A = "0" * bit_size  # Accumulator
    Q = multiplier_bin  # Multiplier
    Q_minus_1 = "0"     # Extra bit
    
    # Execute algorithm steps...
    # (See full implementation in code file)
    
    # Combine A and Q for result
    result_bin = A + Q
    result = int(result_bin, 2)
    
    # Handle negative result
    if result_bin[0] == '1':
        result = result - (1 << (2 * bit_size))
    
    return result
```

## Usage

To use the implementation:

```python
# Calculate 15 × (-3)
result = booths_algorithm(15, -3, 8)
print(f"15 × (-3) = {result}")  # Output: -45
```

## Applications

Booth's algorithm is used in:
- Computer arithmetic units
- Digital signal processing
- Hardware multiplier implementations
- Low-power multiplication circuits

## Advantages

- Efficiently handles both positive and negative numbers
- Optimizes multiplication by reducing the number of additions
- Can skip over consecutive 1s in the multiplier
- Utilizes standard two's complement representation

## References

- Computer Organization and Design by Patterson and Hennessy
- Digital Computer Arithmetic by Ercegovac and Lang
- Computer Arithmetic Algorithms by Israel Koren

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
    
    # Initialize
    A = "0" * bit_size  # Accumulator
    Q = multiplier_bin  # Multiplier
    Q_minus_1 = "0"     # Extra bit
    
    # Print initial values
    print(f"Multiplying {multiplicand} ({multiplicand_bin}) by {multiplier} ({multiplier_bin})")
    print(f"M = {multiplicand_bin} (multiplicand)")
    print(f"-M = {neg_multiplicand} (negative multiplicand)")
    print("\nBooth's Algorithm Steps:")
    print("-" * 80)
    print(f"{'Step':^5} | {'Operation':^15} | {'A':^{bit_size}} | {'Q':^{bit_size}} | {'Q_-1':^3} | {'Explanation'}")
    print("-" * 80)
    print(f"{'Init':^5} | {'':^15} | {A:^{bit_size}} | {Q:^{bit_size}} | {Q_minus_1:^3} | Initial values")
    
    # Execute Booth's algorithm for bit_size steps
    for i in range(bit_size):
        explanation = ""
        operation = ""
        
        # Check last two bits
        if Q[-1] + Q_minus_1 == "10":
            # Subtract M from A
            operation = "Subtract M"
            explanation = "Q[-1]Q_-1 = 10, subtract M"
            A = bin((int(A, 2) + int(neg_multiplicand, 2)) % (1 << bit_size))[2:].zfill(bit_size)
        elif Q[-1] + Q_minus_1 == "01":
            # Add M to A
            operation = "Add M"
            explanation = "Q[-1]Q_-1 = 01, add M"
            A = bin((int(A, 2) + int(multiplicand_bin, 2)) % (1 << bit_size))[2:].zfill(bit_size)
        else:
            operation = "No operation"
            explanation = f"Q[-1]Q_-1 = {Q[-1]}{Q_minus_1}, no operation"
        
        # Right shift
        next_Q_minus_1 = Q[-1]
        next_Q = A[-1] + Q[:-1]
        next_A = A[0] + A[:-1]  # Arithmetic shift right (preserve sign bit)
        
        A, Q, Q_minus_1 = next_A, next_Q, next_Q_minus_1
        
        print(f"{i+1:^5} | {operation:^15} | {A:^{bit_size}} | {Q:^{bit_size}} | {Q_minus_1:^3} | {explanation}")
        print(f"{'':^5} | {'Shift right':^15} | {A:^{bit_size}} | {Q:^{bit_size}} | {Q_minus_1:^3} | Arithmetic right shift")
    
    # Combine A and Q for result
    result_bin = A + Q
    result = int(result_bin, 2)
    
    # Handle negative result
    if result_bin[0] == '1':
        # If the result is negative, convert from 2's complement
        result = result - (1 << (2 * bit_size))
    
    print("-" * 80)
    print(f"\nResult in binary: {result_bin}")
    print(f"Result in decimal: {result}")
    
    # Calculate using 2's complement
    if result_bin[0] == '1':
        print("\nCalculating the negative value:")
        print(f"2's complement = {result_bin}")
        inverted = ''.join('1' if bit == '0' else '0' for bit in result_bin)
        print(f"Invert bits   = {inverted}")
        two_comp = bin(int(inverted, 2) + 1)[2:].zfill(2*bit_size)
        print(f"Add 1         = {two_comp}")
        
        # Calculate the value
        calculation = []
        value = 0
        for i, bit in enumerate(reversed(two_comp)):
            if bit == '1':
                value += 2**i
                calculation.append(f"2^{i} = {2**i}")
        
        print(f"Value = {' + '.join(calculation)} = {value}")
        print(f"Therefore, result = -{value} = {result}")
    
    return result
# Keep a note if you want to multiply like 20 and -3 you have to set the no of bits to 8
# Test with the example from the image: 15 × (-3)
"""here i have set the bit to 5 for less no of calculation steps
#change the bits according to your need"""
booths_algorithm(15, -3, 5)

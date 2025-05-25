def booths_algorithm(multiplicand, multiplier):
    """
    Implements Booth's algorithm for signed binary multiplication.

    Args:
        multiplicand (int): The number to be multiplied (M).
        multiplier (int): The number by which to multiply (Q).
    """

    # --- 1. Determine the optimal bit_size for representation ---
    # We need enough bits to represent both the multiplicand and multiplier
    # in 2's complement form, including a sign bit.
    # For a number 'x', the minimum bits for 2's complement is generally:
    #   - If x = 0: 1 bit (0)
    #   - If x > 0: x.bit_length() + 1 (e.g., 1 (01), 3 (011))
    #   - If x < 0: abs(x).bit_length() + 1 (e.g., -1 (11), -3 (101))
    
    # Calculate required bits for multiplicand
    if multiplicand == 0:
        min_bits_multiplicand = 1
    elif multiplicand > 0:
        min_bits_multiplicand = multiplicand.bit_length() + 1
    else: # multiplicand < 0
        min_bits_multiplicand = abs(multiplicand).bit_length() + 1

    # Calculate required bits for multiplier
    if multiplier == 0:
        min_bits_multiplier = 1
    elif multiplier > 0:
        min_bits_multiplier = multiplier.bit_length() + 1
    else: # multiplier < 0
        min_bits_multiplier = abs(multiplier).bit_length() + 1

    # The chosen bit_size must accommodate the largest number
    bit_size = max(min_bits_multiplicand, min_bits_multiplier)
    
    # Ensure a minimum bit_size (e.g., 4) for better visualization of binary strings
    bit_size = max(bit_size, 4)

    # --- 2. Convert numbers to their 2's complement binary representation ---
    # For a negative number `n`, its 2's complement in `k` bits is `(1 << k) + n`.
    # For a non-negative number `n`, it's simply `n`.
    
    multiplicand_bin = bin((1 << bit_size) + multiplicand)[2:].zfill(bit_size) \
                       if multiplicand < 0 else bin(multiplicand)[2:].zfill(bit_size)
    
    multiplier_bin = bin((1 << bit_size) + multiplier)[2:].zfill(bit_size) \
                     if multiplier < 0 else bin(multiplier)[2:].zfill(bit_size)
    
    # Calculate -M (negative multiplicand) in 2's complement binary form
    # This is the 2's complement representation of `-multiplicand`.
    neg_multiplicand_val = -multiplicand
    neg_multiplicand_bin = bin((1 << bit_size) + neg_multiplicand_val)[2:].zfill(bit_size) \
                           if neg_multiplicand_val < 0 else bin(neg_multiplicand_val)[2:].zfill(bit_size)

    # --- 3. Initialize Registers ---
    A = "0" * bit_size  # Accumulator, initially all zeros
    Q = multiplier_bin  # Multiplier register
    Q_minus_1 = "0"     # Extra bit (Q_-1), initially zero
    
    # --- 4. Print Initial State and Table Header ---
    print(f"\n--- Booth's Algorithm for Signed Multiplication ---")
    print(f"Multiplying {multiplicand} by {multiplier} using {bit_size} bits.")
    print(f"M (Multiplicand)          = {multiplicand} (binary: {multiplicand_bin})")
    print(f"Q (Multiplier)            = {multiplier} (binary: {multiplier_bin})")
    print(f"-M (Negative Multiplicand) = {-multiplicand} (binary: {neg_multiplicand_bin})")
    
    print("\n--- Booth's Algorithm Steps ---")
    # Dynamic width for separator line
    header_width = 5 + 15 + bit_size + bit_size + 6 + 13 + 10 # Sum of column widths + pipes
    print("-" * header_width)
    print(f"{'Step':^5} | {'Operation':^15} | {'A':^{bit_size}} | {'Q':^{bit_size}} | {'Q_-1':^6} | {'Explanation'}")
    print("-" * header_width)
    print(f"{'Init':^5} | {'':^15} | {A:^{bit_size}} | {Q:^{bit_size}} | {Q_minus_1:^6} | Initial values")
    
    # --- 5. Execute Booth's Algorithm for bit_size Steps ---
    for i in range(bit_size):
        explanation = ""
        operation = ""
        
        q_lsb = Q[-1] # Least Significant Bit (LSB) of Q
        
        # Check the combination of Q_LSB and Q_minus_1
        if q_lsb == "1" and Q_minus_1 == "0": # Case "10": Subtract M from A
            operation = "Subtract M"
            explanation = "Q_LSB Q_-1 = 10 (End of a block of 1s)"
            # Perform A = A - M (effectively A + (-M) in 2's complement arithmetic)
            A_val = int(A, 2)
            neg_multiplicand_val_int = int(neg_multiplicand_bin, 2)
            # Modulo arithmetic handles potential overflow in 2's complement addition
            A = bin((A_val + neg_multiplicand_val_int) % (1 << bit_size))[2:].zfill(bit_size)
            
        elif q_lsb == "0" and Q_minus_1 == "1": # Case "01": Add M to A
            operation = "Add M"
            explanation = "Q_LSB Q_-1 = 01 (End of a block of 0s)"
            # Perform A = A + M
            A_val = int(A, 2)
            multiplicand_val_int = int(multiplicand_bin, 2)
            A = bin((A_val + multiplicand_val_int) % (1 << bit_size))[2:].zfill(bit_size)
        else: # Cases "00" or "11": No arithmetic operation
            operation = "No operation"
            explanation = f"Q_LSB Q_-1 = {q_lsb}{Q_minus_1} (No transition)"
        
        # Print state BEFORE shift
        print(f"{i+1:^5} | {operation:^15} | {A:^{bit_size}} | {Q:^{bit_size}} | {Q_minus_1:^6} | {explanation}")

        # Arithmetic Right Shift: A, Q, and Q_minus_1
        # The sign bit of A (A[0]) is preserved during the shift into A.
        # The LSB of A (A[-1]) shifts into the MSB of Q.
        # The LSB of Q (Q[-1]) shifts into Q_minus_1.
        
        next_Q_minus_1 = Q[-1]       # Q_minus_1 takes value of Q's old LSB
        next_Q = A[-1] + Q[:-1]      # Q shifts right, its MSB takes A's old LSB
        next_A = A[0] + A[:-1]       # A shifts right, its MSB (sign bit) is duplicated
        
        # Update registers for the next iteration
        A, Q, Q_minus_1 = next_A, next_Q, next_Q_minus_1
        
        # Print state AFTER shift
        print(f"{'':^5} | {'Shift right':^15} | {A:^{bit_size}} | {Q:^{bit_size}} | {Q_minus_1:^6} | Arithmetic right shift")
    
    # --- 6. Combine A and Q for the final result ---
    result_bin = A + Q
    
    # --- 7. Convert the 2*bit_size result from 2's complement to decimal ---
    # The combined result (A+Q) is a 2*bit_size 2's complement number.
    # If its Most Significant Bit (MSB, which is result_bin[0]) is '1', it's negative.
    
    # First, convert the binary string to an unsigned integer
    final_decimal_result = int(result_bin, 2)
    
    # If the MSB is '1', convert from 2's complement to its true negative value
    if result_bin[0] == '1':
        # Subtract 2^(total_bits) from the unsigned value
        final_decimal_result = final_decimal_result - (1 << (2 * bit_size))
    
    print("-" * header_width)
    print(f"\nFinal Result (A+Q) in binary ({2*bit_size} bits): {result_bin}")
    print(f"Final Result in decimal: {final_decimal_result}")
    
    # --- 8. Show detailed 2's Complement to Decimal Conversion for Negative Results ---
    if result_bin[0] == '1':
        print("\n--- Detailed 2's Complement to Decimal Conversion ---")
        print(f"Binary 2's complement: {result_bin}")
        
        # Step 1: Invert all bits
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in result_bin)
        print(f"1. Invert bits:        {inverted_bits}")
        
        # Step 2: Add 1 to the inverted result
        inverted_int = int(inverted_bits, 2)
        plus_one_int = inverted_int + 1
        two_comp_pos_val_bin = bin(plus_one_int)[2:].zfill(2*bit_size)
        print(f"2. Add 1:              {two_comp_pos_val_bin}")
        
        # Step 3: Convert this positive binary to decimal
        positive_value = int(two_comp_pos_val_bin, 2)
        print(f"3. Convert to decimal: {positive_value}")
        print(f"Therefore, the decimal value is -{positive_value}.")
    
    return final_decimal_result

# --- Get user input ---
print("This program implements Booth's Algorithm for Signed Binary Multiplication.")
print("It automatically determines the number of bits required for calculation.")

try:
    m_input = int(input("\nEnter the Multiplicand (M): "))
    q_input = int(input("Enter the Multiplier (Q): "))
except ValueError:
    print("\nInvalid input. Please enter integer numbers only.")
    exit()

# --- Run the algorithm with user inputs ---
booths_algorithm(m_input, q_input)

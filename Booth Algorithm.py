def booths_algorithm(multiplicand, multiplier):
    def twos_complement_to_int(bin_str):
        bits = len(bin_str)
        val = int(bin_str, 2)
        if bin_str[0] == '1':
            val -= (1 << bits)
        return val

    def int_to_twos_complement(val, bits):
        if val < 0:
            val = (1 << bits) + val
        return bin(val % (1 << bits))[2:].zfill(bits)

    # Step 1: Determine bit size
    min_bits_m = abs(multiplicand).bit_length() + 1
    min_bits_q = abs(multiplier).bit_length() + 1
    bit_size = max(min_bits_m, min_bits_q, 4)

    # Step 2: Get 2's complement binary strings
    multiplicand_bin = int_to_twos_complement(multiplicand, bit_size)
    multiplier_bin = int_to_twos_complement(multiplier, bit_size)
    neg_multiplicand_bin = int_to_twos_complement(-multiplicand, bit_size)

    # Step 3: Initialize registers
    A = '0' * bit_size
    Q = multiplier_bin
    Q_minus_1 = '0'

    print(f"\n--- Booth's Algorithm for Signed Multiplication ---")
    print(f"Multiplying {multiplicand} by {multiplier} using {bit_size} bits.")
    print(f"M (Multiplicand)          = {multiplicand} (binary: {multiplicand_bin})")
    print(f"Q (Multiplier)            = {multiplier} (binary: {multiplier_bin})")
    print(f"-M (Negative Multiplicand) = {-multiplicand} (binary: {neg_multiplicand_bin})")

    print("\n--- Booth's Algorithm Steps ---")
    action_col_width = 28
    comment_col_width = 50

    col_widths_list = [5, action_col_width, bit_size, bit_size, 6, comment_col_width]
    header_width = sum(col_widths_list) + (len(col_widths_list) - 1) * 3

    print("-" * header_width)
    print(f"{'Step':^5} | {'Action':^{action_col_width}} | {'A':^{bit_size}} | {'Q':^{bit_size}} | {'Q_-1':^6} | {'Comment':^{comment_col_width}}")
    print("-" * header_width)
    print(f"{'Init':^5} | {'Initialize Registers':^{action_col_width}} | {A:^{bit_size}} | {Q:^{bit_size}} | {Q_minus_1:^6} | {'Initial values':^{comment_col_width}}")

    # Step 4: Run the algorithm
    for i in range(bit_size):
        print("-" * header_width)
        step_label_str = f"{i+1}" # Label for the current step number
        
        q_lsb = Q[-1]
        # Store A, Q, Q-1 values at the beginning of the iteration, before any modifications for this step
        A_bin_before_op = A
        A_val_before_op = twos_complement_to_int(A_bin_before_op)
        Q_before_shift = Q
        Q_minus_1_before_shift = Q_minus_1

        A_after_arithmetic_op = A # Initialize with current A, will be updated if arithmetic op occurs

        # Line 1: Show state leading to decision (uses A_bin_before_op, Q_before_shift, Q_minus_1_before_shift)
        if q_lsb == '1' and Q_minus_1_before_shift == '0': # Case: 10 (A = A - M)
            decision_action = "Examine Q_LSB, Q_-1"
            decision_comment = f"Q_LSB,Q_-1 = 10. Action: A = A - M"
            print(f"{step_label_str:^5} | {decision_action:^{action_col_width}} | {A_bin_before_op:^{bit_size}} | {Q_before_shift:^{bit_size}} | {Q_minus_1_before_shift:^6} | {decision_comment:^{comment_col_width}}")
            step_label_str = "" 

            # Perform A = A - M
            A_val_after_op = A_val_before_op + twos_complement_to_int(neg_multiplicand_bin)
            A_after_arithmetic_op = int_to_twos_complement(A_val_after_op, bit_size)
            
            # Line 2: Show result of A operation (shows A_after_arithmetic_op, Q_before_shift, Q_minus_1_before_shift)
            op_action = "A <- A - M"
            op_comment = f"Execute: A = {A_bin_before_op} + ({neg_multiplicand_bin}) = {A_after_arithmetic_op}"
            print(f"{step_label_str:^5} | {op_action:^{action_col_width}} | {A_after_arithmetic_op:^{bit_size}} | {Q_before_shift:^{bit_size}} | {Q_minus_1_before_shift:^6} | {op_comment:^{comment_col_width}}")

        elif q_lsb == '0' and Q_minus_1_before_shift == '1': # Case: 01 (A = A + M)
            decision_action = "Examine Q_LSB, Q_-1"
            decision_comment = f"Q_LSB,Q_-1 = 01. Action: A = A + M"
            print(f"{step_label_str:^5} | {decision_action:^{action_col_width}} | {A_bin_before_op:^{bit_size}} | {Q_before_shift:^{bit_size}} | {Q_minus_1_before_shift:^6} | {decision_comment:^{comment_col_width}}")
            step_label_str = ""

            # Perform A = A + M
            A_val_after_op = A_val_before_op + twos_complement_to_int(multiplicand_bin)
            A_after_arithmetic_op = int_to_twos_complement(A_val_after_op, bit_size)

            # Line 2: Show result of A operation (shows A_after_arithmetic_op, Q_before_shift, Q_minus_1_before_shift)
            op_action = "A <- A + M"
            op_comment = f"Execute: A = {A_bin_before_op} + {multiplicand_bin} = {A_after_arithmetic_op}"
            print(f"{step_label_str:^5} | {op_action:^{action_col_width}} | {A_after_arithmetic_op:^{bit_size}} | {Q_before_shift:^{bit_size}} | {Q_minus_1_before_shift:^6} | {op_comment:^{comment_col_width}}")
        
        else: # Cases: 00 or 11 (No arithmetic op on A)
            decision_action = "Examine Q_LSB, Q_-1"
            decision_comment = f"Q_LSB,Q_-1 = {q_lsb}{Q_minus_1_before_shift}. No arithmetic op on A."
            print(f"{step_label_str:^5} | {decision_action:^{action_col_width}} | {A_bin_before_op:^{bit_size}} | {Q_before_shift:^{bit_size}} | {Q_minus_1_before_shift:^6} | {decision_comment:^{comment_col_width}}")
            step_label_str = ""
            # A_after_arithmetic_op remains A_bin_before_op as no operation was performed on it.
            # No separate "Line 2" for A operation needed here.

        # Line 3: Arithmetic right shift
        # A for the shift is A_after_arithmetic_op (which is A_bin_before_op if no arithmetic op occurred)
        # Q for the shift is Q_before_shift
        # Q-1 for the shift is Q_minus_1_before_shift
        combined = A_after_arithmetic_op + Q_before_shift + Q_minus_1_before_shift 
        shifted = combined[0] + combined[:-1] 
        
        A = shifted[:bit_size]
        Q = shifted[bit_size:2*bit_size]
        Q_minus_1 = shifted[-1]

        shift_action = "Shift Right (ASR)"
        shift_comment = "Arithmetic Right Shift A, Q; Q_LSB to Q_-1"
        # If no arithmetic operation was performed, step_label_str will be empty (correct)
        # If an arithmetic op was performed, step_label_str will be empty (correct)
        # If it was the "Examine" line for a no-op case, step_label_str will be empty for the shift line (correct)
        print(f"{step_label_str:^5} | {shift_action:^{action_col_width}} | {A:^{bit_size}} | {Q:^{bit_size}} | {Q_minus_1:^6} | {shift_comment:^{comment_col_width}}")

    # Step 5: Final result
    result_bin = A + Q
    result_val = twos_complement_to_int(result_bin)

    print("-" * header_width)
    print(f"\nFinal Result (AQ) in binary ({2*bit_size} bits): {result_bin}")
    print(f"Final Result in decimal: {result_val}")

    if result_val < 0 :
        print("\n--- Detailed 2's Complement to Decimal Conversion for Result ---")
        inverted_bits = ''.join('1' if b == '0' else '0' for b in result_bin)
        print(f"1. Invert bits of {result_bin}: {inverted_bits}")
        inverted_int = int(inverted_bits, 2)
        plus_one_int = inverted_int + 1
        two_comp_pos_val_bin = bin(plus_one_int % (1 << (2*bit_size)))[2:].zfill(2*bit_size)
        print(f"2. Add 1:              {two_comp_pos_val_bin} (This is the positive magnitude)")
        print(f"3. Convert magnitude to decimal: {plus_one_int}")
        print(f"Therefore, the decimal value is -{plus_one_int}.")
    elif result_val > 0 :
        direct_decimal = int(result_bin, 2)
        print(f"\n--- Positive Binary to Decimal Conversion for Result ---")
        print(f"Binary {result_bin} directly converts to decimal {direct_decimal}.")
    else: 
        print(f"\n--- Result is Zero ---")
        print(f"Binary {result_bin} converts to decimal 0.")

    return result_val


# Get user input
print("This program implements Booth's Algorithm for Signed Binary Multiplication.")
print("It automatically determines the number of bits required for calculation.")

try:
    m_input = int(input("\nEnter the Multiplicand (M): "))
    q_input = int(input("Enter the Multiplier (Q): "))
except ValueError:
    print("\nInvalid input. Please enter integer numbers only.")
    exit()

# Run the algorithm
booths_algorithm(m_input, q_input)

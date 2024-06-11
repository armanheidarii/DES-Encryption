from pkg.constants import *


class DES:
    # Hexadecimal to binary conversion
    def hex2bin(s):
        bin = ""
        for i in range(len(s)):
            bin = bin + mp_hex2bin[s[i]]
        return bin

    # Binary to hexadecimal conversion
    def bin2hex(s):
        hex = ""
        for i in range(0, len(s), 4):
            ch = ""
            ch = ch + s[i]
            ch = ch + s[i + 1]
            ch = ch + s[i + 2]
            ch = ch + s[i + 3]
            hex = hex + mp_bin2hex[ch]

        return hex

    # Binary to decimal conversion
    def bin2dec(binary):

        binary1 = binary
        decimal, i, n = 0, 0, 0
        while binary != 0:
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary // 10
            i += 1
        return decimal

    # Decimal to binary conversion
    def dec2bin(num):
        res = bin(num).replace("0b", "")
        if len(res) % 4 != 0:
            div = len(res) / 4
            div = int(div)
            counter = (4 * (div + 1)) - len(res)
            for i in range(0, counter):
                res = "0" + res
        return res

    # Permute function to rearrange the bits
    def permute(k, arr, n):
        permutation = ""
        for i in range(0, n):
            permutation = permutation + k[arr[i] - 1]
        return permutation

    # Shifting the bits towards left by nth shifts
    def shift_left(k, nth_shifts):
        s = ""
        for i in range(nth_shifts):
            for j in range(1, len(k)):
                s = s + k[j]
            s = s + k[0]
            k = s
            s = ""
        return k

    # Calculating xow of two strings of binary number a and b
    def xor(a, b):
        ans = ""
        for i in range(len(a)):
            if a[i] == b[i]:
                ans = ans + "0"
            else:
                ans = ans + "1"
        return ans

    # Get first 64 bit of last_name
    def get_16_hex(last_name):
        return "".join([hex(ord(c))[2:].zfill(2) for c in last_name])[:16].zfill(16)

    def keygen(key):
        # Key generation
        # --hex to binary
        key = DES.hex2bin(key)

        # getting 56 bit key from 64 bit using the parity bits
        key = DES.permute(key, keyp, 56)

        # Splitting
        left = key[0:28]  # rkb for RoundKeys in binary
        right = key[28:56]  # rk for RoundKeys in hexadecimal

        rkb = []
        rk = []
        for i in range(0, 16):
            # Shifting the bits by nth shifts by checking from shift table
            left = DES.shift_left(left, shift_table[i])
            right = DES.shift_left(right, shift_table[i])

            # Combination of left and right string
            combine_str = left + right

            # Compression of key from 56 to 48 bits
            round_key = DES.permute(combine_str, key_comp, 48)

            rkb.append(round_key)
            rk.append(DES.bin2hex(round_key))

        return rkb, rk

    def encrypt_block(pt, rkb, rk, log=False):
        # Initial Permutation
        pt = DES.permute(pt, initial_perm, 64)

        if log:
            print("After initial permutation", DES.bin2hex(pt))

        # Splitting
        left = pt[0:32]
        right = pt[32:64]

        if log:
            print(f"Left {left}")
            print(f"Right {right}")

        for i in range(0, 16):
            # Expansion D-box: Expanding the 32 bits data into 48 bits
            right_expanded = DES.permute(right, exp_d, 48)

            if log:
                print(f"Expanding the 32 bits data into 48 bits {right_expanded}")

            # XOR RoundKey[i] and right_expanded
            xor_x = DES.xor(right_expanded, rkb[i])

            if log:
                print(f"XOR RoundKey[i] and right expanded is {xor_x}")

            # S-boxex: substituting the value from s-box table by calculating row and column
            sbox_str = ""
            for j in range(0, 8):
                row = DES.bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
                col = DES.bin2dec(
                    int(
                        xor_x[j * 6 + 1]
                        + xor_x[j * 6 + 2]
                        + xor_x[j * 6 + 3]
                        + xor_x[j * 6 + 4]
                    )
                )
                val = sbox[j][row][col]

                if log:
                    print(f"Value of sbox {j} in row {row} and column {col} is {val}")

                sbox_str = sbox_str + DES.dec2bin(val)

            # Straight D-box: After substituting rearranging the bits
            sbox_str = DES.permute(sbox_str, per, 32)

            if log:
                print(f"After substituting rearranging the bits {sbox_str}")

            # XOR left and sbox_str
            result = DES.xor(left, sbox_str)
            left = result

            # Swapper
            if i != 15:
                left, right = right, left

            if log:
                print(
                    "Round ",
                    i + 1,
                    " ",
                    DES.bin2hex(left),
                    " ",
                    DES.bin2hex(right),
                    " ",
                    rk[i],
                    "\n",
                )

        # Combination
        combine = left + right

        # Final permutation: final rearranging of bits to get cipher text
        cipher_text = DES.permute(combine, final_perm, 64)

        return cipher_text

    # Class entry point
    def encrypt(pt, key, log=False):
        pt = DES.hex2bin(pt)
        rkb, rk = DES.keygen(key)

        return DES.encrypt_block(pt, rkb, rk, log=log)

    def decrypt(ct, key, log=False):
        ct = DES.hex2bin(ct)
        rkb, rk = DES.keygen(key)

        return DES.encrypt_block(ct, rkb[::-1], rk[::-1], log=log)

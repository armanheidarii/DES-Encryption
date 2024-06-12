# DES Encryption

## Contents

- [Introduction](#introduction)
- [Usage](#usage)

## Introduction
DES (Data Encryption Standard) is a symmetric-key cryptographic algorithm that was once the most widely used method for securing digital communications. It was developed by IBM and adopted as a federal standard in the United States in 1977.

The DES algorithm works as follows:

1. **Key Generation*: The algorithm takes a 56-bit key as input, which is used to encrypt and decrypt data.
2. **Initial Permutation**: The 64-bit plaintext input is first subjected to an initial permutation, which rearranges the bits according to a predefined pattern.
3. **Feistel Structure**: The permuted input is then divided into two 32-bit halves, which undergo 16 rounds of a Feistel network structure. In each round, the following steps are performed:
+ The right half is expanded from 32 bits to 48 bits.
+ The expanded right half is XORed with a 48-bit subkey derived from the main key.
+ The result is passed through a series of S-boxes, which substitute the 48-bit input into a 32-bit output.
+ The output of the S-boxes is permuted according to a fixed P-box.
+ The result is XORed with the left half, and the left and right halves are swapped for the next round.
4. Final Permutation: After the 16 rounds, the left and right halves are recombined, and a final permutation is applied to produce the 64-bit ciphertext.

The DES algorithm is considered insecure by modern standards due to its small key size, which can be brute-forced by powerful computers. As a result, it has been largely replaced by newer and more secure algorithms, such as AES (Advanced Encryption Standard).

However, DES remains an important historical algorithm and is still used in some legacy systems and applications. Understanding its inner workings is essential for comprehending the development of modern cryptographic techniques.

## Usage
```bash
python main.py
```

# Adaptive Arithmetic & Lempel–Ziv Coding Toolkit

This repository implements and compares two fundamental lossless data compression techniques:

- **Adaptive Arithmetic Coding**
- **Lempel–Ziv (LZ78-style) Coding**

It also includes:
- Efficiency evaluation utilities
- A **PyQt5 graphical interface** for interactive encoding/decoding
- Supporting binary/utility functions

---

## Project Structure

```

.
├── arithmetic.py        # Adaptive arithmetic encoder/decoder
├── lempel_ziv.py        # Lempel–Ziv encoder/decoder
├── utils.py             # Binary, matching, and helper utilities
├── gui.py               # PyQt5 GUI application
└── README.md

````

---

## Features

### Adaptive Arithmetic Coding
- Fully **adaptive** probability model (no prior statistics required)
- High-precision arithmetic using `decimal.Decimal`
- Binary fraction labeling
- Encoder, decoder, and compression efficiency computation

### Lempel–Ziv Coding
- Dictionary-based parsing (LZ78 variant)
- Dynamic bit-width packing of dictionary indices
- Binary stream packing/unpacking
- Full reconstruction of original sequence

### GUI Application
- Interactive encoding and decoding
- Algorithm selection (Arithmetic / LZ)
- Alphabet inference or manual entry
- Compression efficiency display
- Logging and error handling

---

## Requirements

- Python 3.9+
- PyQt5

Install dependencies:
```bash
pip install PyQt5
````

---

## Usage

### 1. Adaptive Arithmetic Coding (CLI)

```python
from arithmetic import adaptive_arithmetic_encode, adaptive_arithmetic_decode

sequence = "abbca"
encoded = adaptive_arithmetic_encode(sequence)

alphabet = sorted(set(sequence))
decoded = adaptive_arithmetic_decode(encoded, alphabet, len(sequence))
```

### Compression Efficiency

```python
from arithmetic import calculate_adaptive_efficiency

eff = calculate_adaptive_efficiency(sequence, alphabet)
```

---

### 2. Lempel–Ziv Coding (CLI)

```python
from lempel_ziv import lz_encode, lz_decode

sequence = "abbca"
alphabet = sorted(set(sequence))

encoded = lz_encode(sequence, alphabet)
decoded = lz_decode(encoded, alphabet)
```

### Compression Efficiency

```python
from lempel_ziv import calculate_lz_efficiency

eff = calculate_lz_efficiency(sequence, alphabet)
```

---

## Graphical Interface

Run the GUI:

```bash
python gui.py
```

### GUI Capabilities

* Encode sequences using either algorithm
* Decode binary streams
* Automatically infer alphabet from previous encoding
* Manual alphabet override
* Display compression efficiency
* Supports arbitrary text input (case-insensitive)

---

## Test Sequences

The following sequences are included for benchmarking:

* `S1 = "ABBCA"`
* `S2 = "ABCABACBABCCACBAABBCCABAABB"`
* `S3 = Full English sentence (case-insensitive)`

---

## Notes & Assumptions

* Alphabet is derived from symbols present in the sequence unless specified
* Adaptive arithmetic decoding **requires the original sequence length**
* All arithmetic coding operations use **1000-digit precision**
* Efficiency is measured relative to fixed-length encoding:

  ```
  original_bits = n × ceil(log2(|alphabet|))
  ```

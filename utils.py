from typing import List, Optional, Tuple
import math


def float_decimal_to_binary(decimal: int, length: int) -> str:
    """
    Similar to how I do it by hand, avoids internal `bin()` magic
    """
    ret = ""
    for _ in range(length):
        sig = int(2*decimal)
        ret = ret + str(sig)
        decimal = 2*decimal-sig
    return ret


def binary_to_float_decimal(binary: str) -> float:
    dec = 0.0
    factor = 0.5
    for bit in binary:
        dec += int(bit) * factor
        factor /= 2
    return dec


def integer_decimal_to_binary(value: int) -> int:
    if value == 0:
        return "0"
    ret = ""
    while value > 0:
        ret = str(value % 2) + ret
        value //= 2
    return ret


def binary_to_integer_decimal(binary: str) -> int:
    dec = 0
    length = len(binary)
    for i, bit in enumerate(binary):
        dec += int(bit) * (2 ** (length - i - 1))
    return dec


def calculate_distribution(sequence: str) -> dict:
    # A bit redundant but does the work
    symbols = sorted(list(set(sequence)))
    probabilities = [sequence.count(sigma)/len(sequence) for sigma in symbols]
    return dict(zip(symbols, probabilities))


def window_match(sequence: str,
                 wordbook: List[str]) -> Optional[Tuple[str, int]]:
    # This is not a generic function, only works for Lempel-Ziv use case
    matches = [s for s in wordbook if sequence.startswith(s)]
    word = max(matches, key=len) if matches else sequence[0]
    index = wordbook.index(word) if matches else 1
    return word, index


def symbol_to_binary(symbol: str, length: int, index: int) -> str:
    """Convert a symbol to its binary representation.

    :symbol: The symbol to convert.
    :length: The length of the binary representation.
    :index: The index of the symbol in the symbol list.
    :returns: The binary representation of the symbol as a string.

    """
    binary = bin(index)[2:].zfill(length)
    return binary


def calculate_efficiency(probabilities: List[float],
                         average_length: float) -> float:
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    efficiency = entropy / average_length if average_length > 0 else 0
    return efficiency


if __name__ == "__main__":
    print(calculate_distribution("ABCABACBABCCACBAABBCCABAABB"))

from typing import Dict, List, Tuple
from decimal import Decimal, getcontext
import math

getcontext().prec = 1000


def decimal_to_binary_fraction(f: Decimal, length: int) -> str:
    s = ''
    for _ in range(length):
        f *= Decimal('2')
        if f >= Decimal('1'):
            s += '1'
            f -= Decimal('1')
        else:
            s += '0'
    return s


def binary_to_decimal_fraction(code: str) -> Decimal:
    f = Decimal('0')
    p = Decimal('1') / Decimal('2')
    for bit in code:
        if bit == '1':
            f += p
        p /= Decimal('2')
    return f


def construct_line(symbols: List[str], probabilities: List[Decimal], prev: Decimal = Decimal('0'), inter: Decimal = Decimal('1')) -> Dict[str, Tuple[Decimal, Decimal]]:
    line = {}
    for i, sigma in enumerate(symbols):
        next_ = prev + probabilities[i] * inter
        line[sigma] = (prev, next_)
        prev = next_
    return line


def adaptive_arithmetic_encode(sequence: str) -> str:
    symbols: List[str] = sorted(list(set(sequence)))
    counts: Dict[str, Decimal] = {sigma: Decimal('1') for sigma in symbols}
    total: Decimal = Decimal(len(symbols))
    line: Dict[str, Tuple[Decimal, Decimal]] = construct_line(
        symbols,
        [counts[sigma] / total for sigma in symbols]
    )
    prev: Decimal = Decimal('0')
    inter: Decimal = Decimal('1')
    for char in sequence:
        prev, nxt = line[char]
        inter = nxt - prev
        counts[char] += Decimal('1')
        total += Decimal('1')
        probabilities = [counts[sigma] / total for sigma in symbols]
        line = construct_line(symbols, probabilities, prev=prev, inter=inter)
    label: Decimal = prev + inter / Decimal('2')
    ln2 = Decimal('2').ln()
    minus_log2 = - (inter.ln() / ln2)
    length: int = math.ceil(float(minus_log2)) + 1
    encoded: str = decimal_to_binary_fraction(label, length)
    return encoded


def adaptive_arithmetic_decode(code: str, alphabet: List[str],
                               length: int) -> str:
    counts: Dict[str, Decimal] = {sigma: Decimal('1') for sigma in alphabet}
    total: Decimal = Decimal(len(alphabet))
    line: Dict[str, Tuple[Decimal, Decimal]] = construct_line(
        alphabet,
        [counts[sigma] / total for sigma in alphabet]
    )
    label: Decimal = binary_to_decimal_fraction(code)
    prev: Decimal = Decimal('0')
    inter: Decimal = Decimal('1')
    decoded: str = ""
    for _ in range(length):
        for sigma in alphabet:
            next_ = line[sigma][1]
            if prev <= label < next_:
                decoded += sigma
                prev, next_ = line[sigma]
                inter = next_ - prev
                counts[sigma] += Decimal('1')
                total += Decimal('1')
                probabilities = [counts[s] / total for s in alphabet]
                line = construct_line(alphabet, probabilities,
                                      prev=prev, inter=inter)
                break
    return decoded


def calculate_adaptive_efficiency(sequence: str, alphabet: list) -> float:
    encoded = adaptive_arithmetic_encode(sequence)
    coded_length = len(encoded)
    original_length = len(sequence) * math.ceil(math.log2(len(alphabet)))
    efficiency =  coded_length / original_length
    return efficiency


if __name__ == "__main__":
    # • The sequence S1 = [A B B C A].
    # • The sequence S2 = [A B C A B A C B A B C C A C B A A B B C C A B A A B
    # B].
    # • The sequence, S3, of characters in the sentence: ” I’m the master’s
    # nightmarish, gorgonian
    # hatemonger, his moth-eaten gonorrhoea, smothering mightiest heroism,
    # thrashing egomania’s (or, to me, ignorant mismanagement’s) strong-arm
    # mishmash or staggering high treason”.
    # Assume the letters are case insensitive.
    # Assume that the alphabet is composed of the symbols in the sequence only.
    sequences = {
        "S1": "ABBCA",
        "S2": "ABCABACBABCCACBAABBCCABAABB",
        "S3": "I'm the master's nightmarish, gorgonian hatemonger, his moth-eaten gonorrhoea, smothering mightiest heroism, thrashing ego-mania's (or, to me, ignorant mismanagement's) strong-arm mishmash or staggering high treason".lower()
    }

    for name, seq in sequences.items():
        print(f"Processing adaptive {name}")
        alphabet = sorted(list(set(seq)))
        adaptive_encoded = adaptive_arithmetic_encode(seq)
        print(f"Adaptive Encoded {name}: {adaptive_encoded}")
        # adaptive_decoded = adaptive_arithmetic_decode(
        #     adaptive_encoded, alphabet, len(seq))
        # print(f"Adaptive Decoded {name}: {adaptive_decoded}")
        # assert adaptive_decoded == seq, "Adaptive decoded sequence does not match original!"
        efficiency = calculate_adaptive_efficiency(seq, alphabet)
        print(f"Adaptive Efficiency for {name}: {efficiency:.4f}\n")

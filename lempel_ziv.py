from math import ceil, log2
from typing import Dict, List, Tuple
from utils import window_match, symbol_to_binary, integer_decimal_to_binary, binary_to_integer_decimal, \
    calculate_efficiency

import logging

# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


def lz_thesaurus(sequence: str) -> List[Tuple[int, str]]:
    # Using terminology from the english literature cause it makes more sense
    # this way as i don't know the formal name of the lists we create
    wordbook: List[str] = [""]
    thesaurus: List[Tuple[int, str]] = []
    i: int = 0

    while i < len(sequence):
        synonym, index = window_match(sequence[i:], wordbook)
        window = len(synonym)
        word = sequence[i + window:i + window + 1]
        if word == '':
            # Only one symbol left, send it as is
            thesaurus.append((0, sequence[i:]))
            logging.debug(f"[THESAURUS] Matched last symbol: '{sequence[i:]}' at index 0")
            break
        reference = sequence[i:i + window + 1]
        logging.debug(f"[THESAURUS] Matched synonym: '{synonym}' at index {index}, next word: '{word}'")
        thesaurus.append((index, word))
        wordbook.append(reference)
        i += window + 1
    logging.info(f"[THESAURUS] Final thesaurus:{thesaurus}")
    return thesaurus


def lz_pack_thesaurus(dictionary: List[Tuple[int, str]],
                      alphabet: list) -> str:
    index_bits = ceil(log2(len(alphabet)))

    alphabet_map: Dict[str, str] = {
        sigma: symbol_to_binary(sigma, index_bits, i)
        for i, sigma in enumerate(alphabet)
    }
    logging.debug(f"[PACK] Alphabet map: {alphabet_map}")

    xy_pairs = [
        (integer_decimal_to_binary(index), alphabet_map[symbol])
        for index, symbol in dictionary
    ]
    logging.debug(f"[PACK] XY pairs: {xy_pairs}")

    # for a = 2^(index_bits)
    a = 2 ** (index_bits)
    logging.debug(f"[PACK] Value of a: {a}")

    xy_mapped = [
        a * binary_to_integer_decimal(index_bin) +
        binary_to_integer_decimal(symbol_bin)
        for index_bin, symbol_bin in xy_pairs
    ]
    logging.debug(f"[PACK] XY mapped values: {xy_mapped}")

    # FIX: The max value is determined by the maximum possible dictionary index at that step
    # AND the maximum possible symbol value.
    # Max value = (Current Dictionary Size) * a + (Max Symbol Value)
    max_xy_mapped = [a * i + (a - 1) for i in range(len(xy_mapped))]

    logging.debug(f"[PACK] Max XY mapped values: {max_xy_mapped}")

    no_of_bits = [ceil(log2(val + 1)) for val in max_xy_mapped]
    logging.debug(f"[PACK] Number of bits for each pair: {no_of_bits}")

    binary_encoded = [
        integer_decimal_to_binary(xy).zfill(bits)
        for xy, bits in zip(xy_mapped, no_of_bits)
    ]
    logging.info(f"Binary encoded segments: {binary_encoded}")

    return "".join(binary_encoded)


def lz_unpack_thesaurus(encoded: str, alphabet: list) -> List[Tuple[int, str]]:
    index_bits = ceil(log2(len(alphabet)))
    a = 2 ** (index_bits)

    dictionary: List[Tuple[int, str]] = []
    i = 0

    logging.debug(f"Starting UNPACK | encoded length = {len(encoded)} bits")
    logging.debug(f"Alphabet: {alphabet} | index_bits={index_bits} | a={a}")

    while i < len(encoded):
        # FIX: Calculate bits required based on current dictionary size
        # This matches the logic in lz_pack_thesaurus
        max_val = a * len(dictionary) + (a - 1)
        bits = ceil(log2(max_val + 1))

        segment = encoded[i:i + bits]

        # Guard against incomplete segments (optional safety)
        if len(segment) < bits:
            logging.warning("Reached end of stream with incomplete segment.")
            break

        xy_mapped = binary_to_integer_decimal(segment)

        index = xy_mapped // a
        symbol_index = xy_mapped % a

        if symbol_index >= len(alphabet):
            logging.debug(f"Symbol index {symbol_index} outside alphabet at offset {i}")
            raise ValueError(
                "Corrupted encoded data: symbol index out of range.")

        symbol = alphabet[symbol_index]

        logging.debug(
            f"[UNPACK] offset={i} bits={bits} seg='{segment}' xy_val={xy_mapped} "
            f"-> index={index}, symbol='{symbol}' (symbol_index={symbol_index})"
        )

        dictionary.append((index, symbol))
        i += bits

    logging.debug(f"Final unpacked dictionary: {dictionary}")
    return dictionary


def lz_reconstruct_sequence(dictionary: List[Tuple[int, str]]) -> str:
    wordbook: List[str] = [""]
    sequence: str = ""

    logging.debug(f"Starting RECONSTRUCT with dictionary: {dictionary}")

    for step, (index, symbol) in enumerate(dictionary):
        reference = wordbook[index] + symbol
        sequence += reference
        wordbook.append(reference)

        logging.debug(
            f"[RECONSTRUCT] step={step} index={index} symbol='{symbol}' "
            f"reference='{reference}'"
        )

    logging.debug(f"[RECONSTRUCT] Final reconstructed sequence: '{sequence}'")
    return sequence


def lz_encode(sequence: str, alphabet: list) -> str:
    dictionary = lz_thesaurus(sequence)
    encoded = lz_pack_thesaurus(dictionary, alphabet)
    return encoded


def lz_decode(encoded: str, alphabet: list) -> str:
    dictionary = lz_unpack_thesaurus(encoded, alphabet)
    sequence = lz_reconstruct_sequence(dictionary)
    return sequence


def calculate_lz_efficiency(sequence: str, alphabet: list) -> float:
    encoded = lz_encode(sequence, alphabet)
    coded_length = len(encoded)
    original_length = len(sequence) * ceil(log2(len(alphabet)))
    logging.debug(f"Coded length: {coded_length} bits")
    logging.debug(f"Original length: {original_length} bits")
    efficiency = coded_length / original_length
    return efficiency


if __name__ == "__main__":
    # Test sequences
    sequences = {
        "S1": "ABBCA",
        "S2": "ABCABACBABCCACBAABBCCABAABB",
        "S3": "I'm the master's nightmarish, gorgonian hatemonger, his moth-eaten gonorrhoea, smothering mightiest heroism, thrashing ego-mania's (or, to me, ignorant mismanagement's) strong-arm mishmash or staggering high treason".lower()
    }

    for name, seq in sequences.items():
        print(f"Processing Lempel-Ziv {name}")
        alphabet = sorted(list(set(seq)))
        # print(f"Processing {name} with alphabet: {alphabet}")
        encoded = lz_encode(seq, alphabet)
        print(f"Lempel-Ziv Encoded {name}: {encoded}")
        # decoded = lz_decode(encoded, alphabet)
        # print(f"Decoded {name}: {decoded}")
        # assert decoded == seq, "Decoded sequence does not match original!"
        efficiency = calculate_lz_efficiency(seq, alphabet)
        print(f"Lempel-Ziv Efficiency for {name}: {efficiency:.4f}\n")

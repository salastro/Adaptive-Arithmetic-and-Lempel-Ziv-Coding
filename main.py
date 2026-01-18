import sys
from typing import List
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout,
    QGroupBox, QMessageBox, QFormLayout, QGridLayout
)
from PyQt5.QtCore import Qt

from arithmetic import (
    adaptive_arithmetic_encode,
    adaptive_arithmetic_decode,
    calculate_adaptive_efficiency
)
from lempel_ziv import (
    lz_encode,
    lz_decode,
    calculate_lz_efficiency
)


class CoderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adaptive Arithmetic / Lempel-Ziv Coder")
        self.resize(900, 600)

        self.last_sequence: str = ""
        self.last_alphabet: List[str] = []

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        enc_group = QGroupBox("Encode")
        enc_layout = QGridLayout()
        enc_group.setLayout(enc_layout)

        enc_layout.addWidget(QLabel("Sequence to encode"), 0, 0)
        self.seq_input = QLineEdit()
        self.seq_input.setPlaceholderText(
            "Enter sequence, e.g. ABBCA or full sentence")
        enc_layout.addWidget(self.seq_input, 0, 1)

        enc_layout.addWidget(
            QLabel("Alphabet (optional, comma-separated)"), 1, 0)
        self.alphabet_input = QLineEdit()
        self.alphabet_input.setPlaceholderText(
            "e.g. A,B,C or leave blank to use last encoded sequence alphabet")
        enc_layout.addWidget(self.alphabet_input, 1, 1)

        enc_layout.addWidget(QLabel("Choose algorithm"), 2, 0)
        algo_box = QWidget()
        algo_layout = QHBoxLayout()
        algo_box.setLayout(algo_layout)
        self.radio_arith = QRadioButton("Adaptive Arithmetic")
        self.radio_lz = QRadioButton("Lempel-Ziv")
        self.radio_arith.setChecked(True)
        algo_layout.addWidget(self.radio_arith)
        algo_layout.addWidget(self.radio_lz)
        enc_layout.addWidget(algo_box, 2, 1)

        self.encode_btn = QPushButton("Encode")
        self.encode_btn.clicked.connect(self.do_encode)
        enc_layout.addWidget(self.encode_btn, 3, 1)

        enc_layout.addWidget(QLabel("Binary output"), 4, 0)
        self.encoded_output = QTextEdit()
        self.encoded_output.setReadOnly(True)
        enc_layout.addWidget(self.encoded_output, 4, 1)

        enc_layout.addWidget(QLabel("Efficiency"), 5, 0)
        self.eff_label = QLabel("-")
        enc_layout.addWidget(self.eff_label, 5, 1)

        layout.addWidget(enc_group)

        dec_group = QGroupBox("Decode")
        dec_layout = QGridLayout()
        dec_group.setLayout(dec_layout)

        dec_layout.addWidget(QLabel("Binary to decode"), 0, 0)
        self.binary_input = QLineEdit()
        self.binary_input.setPlaceholderText(
            "Paste binary string produced by encoder")
        dec_layout.addWidget(self.binary_input, 0, 1)

        dec_layout.addWidget(
            QLabel("Alphabet (optional, comma-separated)"), 1, 0)
        self.alphabet_input = QLineEdit()
        self.alphabet_input.setPlaceholderText(
            "e.g. A,B,C or leave blank to use last encoded sequence alphabet")
        dec_layout.addWidget(self.alphabet_input, 1, 1)

        dec_layout.addWidget(QLabel("Decoded length (optional)"), 2, 0)
        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText(
            "Number of symbols expected (for arithmetic decoding)")
        dec_layout.addWidget(self.length_input, 2, 1)

        self.decode_btn = QPushButton("Decode")
        self.decode_btn.clicked.connect(self.do_decode)
        dec_layout.addWidget(self.decode_btn, 3, 1)

        dec_layout.addWidget(QLabel("Decoded output"), 4, 0)
        self.decoded_output = QTextEdit()
        self.decoded_output.setReadOnly(True)
        dec_layout.addWidget(self.decoded_output, 4, 1)

        layout.addWidget(dec_group)

        status_group = QGroupBox("Status / Log")
        status_layout = QVBoxLayout()
        status_group.setLayout(status_layout)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        status_layout.addWidget(self.log_area)
        layout.addWidget(status_group)

        footer = QWidget()
        foot_layout = QHBoxLayout()
        footer.setLayout(foot_layout)
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        foot_layout.addWidget(self.clear_btn)
        foot_layout.addStretch()
        layout.addWidget(footer)

        self.log("Ready. Choose algorithm, enter sequence, and press Encode.")

    def log(self, msg: str):
        self.log_area.append(msg)

    def clear_all(self):
        self.seq_input.clear()
        self.encoded_output.clear()
        self.eff_label.setText("-")
        self.binary_input.clear()
        self.decoded_output.clear()
        self.alphabet_input.clear()
        self.length_input.clear()
        self.log("Cleared all fields.")

    def do_encode(self):
        seq = self.seq_input.text().lower()
        if not seq:
            QMessageBox.warning(self, "Input required",
                                "Please enter a sequence to encode.")
            return

        try:
            if self.radio_arith.isChecked():
                self.log(
                    f"Encoding using Adaptive Arithmetic: sequence length {len(seq)}")
                encoded = adaptive_arithmetic_encode(seq)
                eff = calculate_adaptive_efficiency(
                    seq, sorted(list(set(seq))))
            else:
                self.log(
                    f"Encoding using Lempel-Ziv: sequence length {len(seq)}")
                encoded = lz_encode(seq, sorted(list(set(seq))))
                eff = calculate_lz_efficiency(seq, sorted(list(set(seq))))

            self.encoded_output.setPlainText(encoded)
            if eff is None:
                self.eff_label.setText("-")
            else:
                try:
                    eff_f = float(eff)
                    self.eff_label.setText(f"{eff_f:.4f}")
                except Exception:
                    self.eff_label.setText(str(eff))

            self.last_sequence = seq
            self.last_alphabet = sorted(list(set(seq)))
            self.log(f"Encoding complete. Output bits: {
                     len(encoded)}. Alphabet: {self.last_alphabet}")
        except Exception as e:
            self.log(f"Error during encoding: {e}")
            QMessageBox.critical(self, "Encoding error",
                                 f"An error occurred: {e}")

    def parse_alphabet_field(self) -> List[str]:
        txt = self.alphabet_input.text().strip()
        if txt:
            if "," in txt:
                parts = [p.strip() for p in txt.split(",") if p.strip() != ""]
                return parts
            else:
                return list(txt)
        if self.last_alphabet:
            return self.last_alphabet
        return []

    def do_decode(self):
        code = self.binary_input.text().strip()
        if not code:
            QMessageBox.warning(self, "Input required",
                                "Please paste the binary string to decode.")
            return

        try:
            alphabet = self.parse_alphabet_field()
            if not alphabet:
                QMessageBox.warning(
                    self, "Alphabet required", "Please provide an alphabet (comma-separated) or encode a sequence first so the alphabet can be inferred.")
                return

            if self.radio_arith.isChecked():
                length_text = self.length_input.text().strip()
                if length_text:
                    try:
                        expected_len = int(length_text)
                        if expected_len <= 0:
                            raise ValueError()
                    except ValueError:
                        QMessageBox.warning(
                            self, "Bad length", "Decoded length must be a positive integer.")
                        return
                else:
                    if self.last_sequence:
                        expected_len = len(self.last_sequence)
                        self.log(f"No length provided. Using last encoded sequence length {
                                 expected_len}.")
                    else:
                        QMessageBox.warning(
                            self, "Length required", "Adaptive arithmetic decoding requires the number of symbols to decode. Provide it in 'Decoded length' or encode a sequence first.")
                        return

                self.log(f"Decoding (Arithmetic) with alphabet {
                         alphabet} and expected length {expected_len}")
                decoded = adaptive_arithmetic_decode(
                    code, alphabet, expected_len)
                self.decoded_output.setPlainText(decoded)
                self.log("Adaptive arithmetic decoding complete.")
            else:
                self.log(f"Decoding (LZ) with alphabet {alphabet}")
                decoded = lz_decode(code, alphabet)
                self.decoded_output.setPlainText(decoded)
                self.log("Lempel-Ziv decoding complete.")

        except Exception as e:
            self.log(f"Error during decoding: {e}")
            QMessageBox.critical(self, "Decoding error",
                                 f"An error occurred: {e}")


def main():
    app = QApplication(sys.argv)
    win = CoderGUI()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

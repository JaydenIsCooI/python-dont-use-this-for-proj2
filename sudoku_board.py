from typing import Tuple
import clingo


class Sudoku:
    def __init__(self, sudoku: dict[Tuple[int, int], int]):
        self.sudoku = sudoku

    def __str__(self) -> str:
        rows = []

        for i in range(1, 10):
            parts = []

            for j in range(1, 10):
                parts.append(str(self.sudoku[(i, j)]))

                if j in (3, 6):
                    parts.append("")

            rows.append(" ".join(parts))

            if i in (3, 6):
                rows.append("")

        return "\n".join(rows)

    @classmethod
    def from_str(cls, s: str) -> "Sudoku":
        sudoku = {}
        row = 0

        for line in s.splitlines():
            line = line.strip()
            if not line:
                continue

            row += 1
            values = line.split()

            for col, value in enumerate(values, start=1):
                if value != "-":
                    sudoku[(row, col)] = int(value)

        return cls(sudoku)

    @classmethod
    def from_model(cls, model: clingo.solving.Model) -> "Sudoku":
        sudoku = {}
        for symbol in model.symbols(shown=True):
            if symbol.name == "sudoku" and len(symbol.arguments) == 3:
                i = symbol.arguments[0].number
                j = symbol.arguments[1].number
                v = symbol.arguments[2].number
                sudoku[(i, j)] = v
        return cls(sudoku)

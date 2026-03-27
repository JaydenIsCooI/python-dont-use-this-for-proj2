import clingo
from clingo.application import Application, clingo_main
from sudoku_board import Sudoku

SUDOKU_PROGRAM = """
cell(1..9).
num(1..9).
grid(1..9).

1 { sudoku(X,Y,N) : num(N) } 1 :- cell(X), cell(Y).

:- sudoku(X,Y,N), sudoku(X,Y2,N), Y < Y2.
:- sudoku(X,Y,N), sudoku(X2,Y,N), X < X2.

subgrid(X,Y,G) :- cell(X), cell(Y), G = 1 + ((X-1)/3)*3 + (Y-1)/3.
:- grid(G), num(N), 2 <= #count { X,Y : sudoku(X,Y,N), subgrid(X,Y,G) }.

:- initial(X,Y,N), not sudoku(X,Y,N).

#show sudoku/3.
"""


class Context:
    def __init__(self, board: Sudoku):
        self.board = board

    def initial(self) -> list[clingo.symbol.Symbol]:
        facts = []
        for (i, j), v in sorted(self.board.sudoku.items()):
            facts.append(
                clingo.Function(
                    "",
                    [clingo.Number(i), clingo.Number(j), clingo.Number(v)],
                    True
                )
            )
        return facts


class ClingoApp(Application):
    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        print(str(sudoku))

    def main(self, ctl, files):
        ctl.add("base", [], SUDOKU_PROGRAM)
        ctl.load("sudoku_py.lp")

        if not files:
            return

        with open(files[0], "r") as f:
            board = Sudoku.from_str(f.read())

        context = Context(board)
        ctl.ground([("base", [])], context=context)
        ctl.solve()


if __name__ == "__main__":
    clingo_main(ClingoApp())
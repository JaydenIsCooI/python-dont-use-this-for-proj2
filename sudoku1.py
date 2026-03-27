import sys
import clingo
from clingo.application import Application, clingo_main

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

class ClingoApp(Application):
    def print_model(self, model, printer):
        symbols = sorted(model.symbols(shown=True))
        print(" ".join(str(s) for s in symbols))
        sys.stdout.flush()

    def main(self, ctl, files):
        try:
            ctl.add("base", [], SUDOKU_PROGRAM)

            for f in files:
                ctl.load(f)

            if not files:
                ctl.load("-")

            ctl.ground([("base", [])])
        except RuntimeError as error:
            print("*** ERROR: (clingo):", error)
            sys.stdout.flush()
            return

        ctl.solve()

if __name__ == "__main__":
    clingo_main(ClingoApp())
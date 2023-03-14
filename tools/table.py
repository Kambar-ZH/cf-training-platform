
from texttable import Texttable

def build(rows) -> str:
    t = Texttable()
    t.add_rows(rows)
    return t.draw()
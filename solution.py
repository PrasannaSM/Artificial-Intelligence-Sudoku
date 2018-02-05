from utils import *
assignments = []

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

cols1 = cols[::-1]
left_diagonal = [[rows[i]+cols[i] for i in range(len(rows))]]
right_diagonal = [[rows[i]+cols1[i] for i in range (len(rows))]]
unitlist = unitlist+left_diagonal+right_diagonal
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
def naked_twins(values):
    for unit in unitlist:
        twins = []
        vals = []
        for box in unit:
            b1 = box
            for box1 in unit:
                b2 = box1
                if b1 != b2 and values[b1] == values[b2] and len(values[b1]) == 2:
                    twins.append(b1)
                    twins.append(b2)
                    vals.append(values[b1])
        boxes = []
        if len(twins) > 1:
            for unit in unitlist:
                if twins[0] in unit and twins[1] in unit:
                    boxes = unit
        if len(boxes) > 0:
            for box in boxes:
                if box not in twins:
                    if vals[0][0] in values[box]:
                        values[box] = values[box].replace(vals[0][0], '')
                    if vals[0][1] in values[box]:
                        values[box] = values[box].replace(vals[0][1], '')
    return values
def eliminate(values):
    for key in values.keys():
        if len(values[key])==1:
            digit = values[key]
            for peer in peers[key]:
                values = assign_value(values, peer, values[peer].replace(digit,''))
    return values
def only_choice(values):
    for ul in unitlist:
        for digit in '123456789':
            d_pos = []
            for box in ul:
                if digit in values[box]:
                    d_pos.append(box)
            if len(d_pos) == 1:
                values = assign_value(values, d_pos[0], digit)
    return values
def reduce_puzzle(values):
    flag = False
    while not flag:
        c1 = 0
        c2 = 0
        for key in values.keys():
            if len(values[key]) == 1:
                c1 = c1+1
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        print (values)
        for key in values.keys():
            if len(values[key]) == 1: 
                c2 = c2+1
        flag = c1 == c2
        if len([key for key in values.keys() if len(values[key]) == 0]): 
            return False
    return values
def search(values):
    values = reduce_puzzle(values)    
    if values is False:
        return False
    if all(len(values[b]) == 1 for b in boxes): 
        return values
    n,b = min((len(values[b]), b) for b in boxes if len(values[b]) > 1)
    for val in values[b]:
        values1 = values.copy()
        values1[b] = val
        res = search(values1)
        if res:
            return res
def solve(grid):
    values = grid2values(grid)
    values = search(values)
    return values
if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)
    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
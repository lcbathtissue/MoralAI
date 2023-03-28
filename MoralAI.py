GRID_SIZE = 100  # 1 m = 100 cm (square grid)

grid = [['_' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def set_cell(x, y, value):
    grid[y-1][x-1] = value

def grid_to_str():
    result = ''
    # header = "                      1                   2                   3                   4                   5                   6                   7                   8                   9                   10\n"
    header = "   "
    for i in range(1, 11):
        header += f"{i:20}"
    header += "\n"
    result += header
    # add rows
    for i, row in enumerate(grid):
        row_str = ' '.join(row)
        # pad row number with whitespace
        row_num_str = str(i+1)
        if i+1 < 10:
            row_num_str = ' ' + row_num_str
        if i == 99:
            result += f'{row_num_str} {row_str} {row_num_str}\n'
        else:
            result += f'{row_num_str}  {row_str} {row_num_str}\n'
    result += header
    return result



print(grid_to_str())

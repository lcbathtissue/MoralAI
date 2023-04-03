import math, random

def observation_matrix(grid, radius, center_x, center_y):

    # define the observable space around the agent, 
    # 'X' out of range, 'A' is agent at centre, '0' is reachable cell in radius 
    center = radius  
    matrix = [[0.0 for x in range(2*radius+1)] for y in range(2*radius+1)]

    for i in range(2*radius+1):
        # perform distance calculations 
        for j in range(2*radius+1):
            dist = math.sqrt((i-center)**2 + (j-center)**2) 
            matrix[i][j] = round(dist, 2) 

    for i in range(len(matrix)):
        # exclude any cells out of radius threshold
        for j in range(len(matrix[0])):
            if matrix[i][j] > radius:
                matrix[i][j] = 'X'
            else:
                matrix[i][j] = '0'

    center_row = len(matrix) // 2
    center_col = len(matrix[0]) // 2
    matrix[center_row][center_col] = 'A'

    # translate the observable space into relative 
    # coordinates based off agent position
    coords = []
    num_rows, num_cols = len(matrix), len(matrix[0])
    offset_x, offset_y = center_x - (num_rows // 2), center_y - (num_cols // 2)
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            if matrix[i][j] == '0':
                row.append([j + offset_y, i + offset_x])
            elif matrix[i][j] == 'A' or matrix[i][j] == 'X':
                row.append(matrix[i][j])
        coords.append(row)

    # using the matrix of relative coordinates and the values
    # in the grid parameter, replace observable cells with
    # the values found in grid, excluding cells outside of
    # the border of the grid which also will become 'X'
    num_rows, num_cols = len(grid), len(grid[0])
    values_matrix = [['X' for j in range(len(coords[0]))] for i in range(len(coords))]
    for i in range(len(coords)):
        for j in range(len(coords[0])):
            if coords[i][j] == 'A' or coords[i][j] == 'X':
                values_matrix[i][j] = coords[i][j]
            else:
                x, y = coords[i][j]
                if x < 0 or x >= num_cols or y < 0 or y >= num_rows:
                    values_matrix[i][j] = 'X'
                else:
                    values_matrix[i][j] = grid[y][x]
    return values_matrix

radius = 10
grid = [[random.randint(0, 9) for j in range(100)] for i in range(100)]  # test grid
search_matrix = observation_matrix(grid, 10, 0, 0)
print(f"radius={radius}, search_size={(2*radius+1)}")
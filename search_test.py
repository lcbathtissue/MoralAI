import numpy as np

def dfs(agent_pos, path, matrix):
    # Check if goal is captured
    if matrix[agent_pos] == 1:
        return path
    
    # Check each direction and move if possible
    for drow, dcol in [(1,0),(-1,0),(0,1),(0,-1)]:
        new_row, new_col = agent_pos[0]+drow, agent_pos[1]+dcol
        if (0 <= new_row < 100) and (0 <= new_col < 100) and (matrix[new_row, new_col] != -1):
            new_path = path + [(new_row, new_col)]
            new_matrix = np.copy(matrix)  # Use numpy.copy() instead of matrix.copy()
            new_matrix[agent_pos] = -1
            new_matrix[new_row, new_col] = 2
            solution = dfs((new_row, new_col), new_path, new_matrix)
            if solution:
                return solution

    # If no solution is found
    return None

# Initialize the matrix with agent and goal randomly placed
matrix = np.zeros((100,100))-1
agent_pos = (np.random.randint(45, 55), np.random.randint(45, 55))  # Adjust the range of random positions
goal_pos = (np.random.randint(45, 55), np.random.randint(45, 55))
matrix[agent_pos] = 2
matrix[goal_pos] = 1

# Find a solution using DFS
solution = dfs(agent_pos, [agent_pos], matrix)

# Print the solution
if solution:
    print("Solution found:", solution)
else:
    print("No solution found.")

import os

def show_moves(grids_list):
    grids_list = [
        [[1, 2, 2], [3, 4, 2], [3, 4, 2]], 
        [[5, 6, 2], [7, 8, 2], [3, 4, 2]], 
        [[9, 10, 2], [11, 12, 2], [3, 4, 2]]
    ]

    for i, array in enumerate(grids_list):
        if i > 0:
            input("\nPress Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in array:
            print(" ".join(str(elem) for elem in row))

show_moves(None)
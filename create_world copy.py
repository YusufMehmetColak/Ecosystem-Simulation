import classes 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
import numpy as np
import random



    
KATSAYI = 10

def initilazie_world(row_number,col_numbers):
    cells = []
    type_choices = [0,1] #1 for ground 0 for water
    for row in range(row_number):
        rows = []
        for column in range(col_numbers):
            # Determine if the current cell is on the border of the grid
            is_border_cell = (row == 0 or column == 0 or
                              row == row_number - 1 or column == col_numbers - 1)

            # Choose the probability distribution based on the cell's location
            probabilities = [1, 0] if is_border_cell else [0.2, 0.8]

            # Select a cell type based on the defined probabilities
            cell_type = np.random.choice(type_choices, p=probabilities)

            if cell_type == 0: #if nothing in the cell make it ground
                rows.append(classes.Cell(None ,None, None, TYPE=0))
            else:
                animal = np.random.choice([2,3,4])
                if animal == 2:
                    rows.append(classes.Cell(VEGETOP= np.random.randint(0,100),
                                             ERBAST = None,
                                             CARVIZ = [np.random.randint(10,15*KATSAYI), np.random.choice([1, 0]), 0, np.random.randint(10,30*KATSAYI)],
                                             TYPE= 1)) #carviz = [energy, socialability, age, lifetime]
                if animal == 4:
                    rows.append(classes.Cell(VEGETOP=np.random.randint(0,50),
                                             ERBAST=[np.random.randint(10, 20*KATSAYI), np.random.choice([1, 0]), 0, np.random.randint(10,30*KATSAYI)],
                                             CARVIZ=[np.random.randint(10*KATSAYI, 15*KATSAYI), np.random.choice([1, 0]), 0,
                                                     np.random.randint(1, 30*KATSAYI)],
                                             TYPE=1))  # carviz = [energy, socialability, age, lifetime]

                if animal == 3:
                    rows.append(classes.Cell(VEGETOP= np.random.randint(0, 75),
                                             ERBAST=[np.random.randint(10, 20*KATSAYI), np.random.choice([1, 0]), 0, np.random.randint(10,30*KATSAYI)], #0 = age
                                             CARVIZ=None,
                                             TYPE = 1))
        cells.append(rows)


    return cells

    

def shuffle_type_1_cells(cells):
    type_1_cells = []

    # Gather all type 1 cells
    for row in cells:
        for cell in row:
            if cell.Type == 1:
                type_1_cells.append(cell)

    # Shuffle the type 1 cells
    random.shuffle(type_1_cells)

    # Redistribute the shuffled type 1 cells back into the grid
    index = 0
    for row in range(len(cells)):
        for column in range(len(cells[row])):
            if cells[row][column].Type == 1:
                cells[row][column] = type_1_cells[index]
                index += 1

    return cells

# Initialize the world
cells = initilazie_world(25, 25)
cells = shuffle_type_1_cells(cells)






def uptade_world(days,cells):  # Fixed typo here, should be 'update_world'
    for i in range(days):
        for row in cells:
            for cell in row:
                cell.grow_vegetop()
                cell.grow_carviz()
                cell.grow_erbast()
                cell.eat()
                cell.fight()







import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def check_adjacent_for_erbast(cells, row, col):
    # Check the cell to the left if it exists
    if col > 0:
        if cells[row][col - 1].ERBAST:
            return True
    # If not found, check the cell above if it exists
    if row > 0:
        if cells[row - 1][col].ERBAST:
            return True
    # If not found, check the cell to the right if it exists
    if col < len(cells[0]) - 1:
        if cells[row][col + 1].ERBAST:
            return True
    # If not found, check the cell below if it exists
    if row < len(cells) - 1:
        if cells[row + 1][col].ERBAST:
            return True
    return False
def check_adjacent_vegetop(cells, row, col, threshold):
    # Check the cell to the left if it exists and is not None
    if col > 0:
        if cells[row][col - 1].VEGETOP is not None and cells[row][col - 1].VEGETOP > threshold:
            return True
    # If not found, check the cell above if it exists and is not None
    if row > 0:
        if cells[row - 1][col].VEGETOP is not None and cells[row - 1][col].VEGETOP > threshold:
            return True
    # If not found, check the cell to the right if it exists and is not None
    if col < len(cells[0]) - 1:
        if cells[row][col + 1].VEGETOP is not None and cells[row][col + 1].VEGETOP > threshold:
            return True
    # If not found, check the cell below if it exists and is not None
    if row < len(cells) - 1:
        if cells[row + 1][col].VEGETOP is not None and cells[row + 1][col].VEGETOP > threshold:
            return True
    return False

def main_plot(cells):
   
    if cells is None:
        raise ValueError("Error: cells is None in main_plot.")
    grid = []
    vegetop_grid = []
    creature_grid = []
    dead_erbast = 0
    dead_carviz = 0
    carviz_counter = 0
    erbast_counter = 0
    dead_erbast_list = []
    dead_carviz_list = []
    row_counter = 0
    erbast_coordinates = []
    carviz_coordinates = []
    creature_positions = []

    # Initialize creature_grid with zeros
    for row in cells:
        creature_row = []
        for cell in row:
            creature_row.append(0)
        creature_grid.append(creature_row)

    for row in cells:
        rows = []
        vegetop_row = []
        row_counter += 1
        cell_counter = 0

        for cell in row:
            if cell.Type == 0:
                rows.append(cell.Type)
                vegetop_row.append(1)
                creature_grid[row_counter - 1][cell_counter] = -1  # Water

            elif cell.ERBAST:
                rows.append(cell.ERBAST[0])
                vegetop_row.append(cell.VEGETOP)
                creature_grid[row_counter - 1][cell_counter] = cell.ERBAST[0] + 250  # Offset for erbast

                erbast_coordinates.append([cell.ERBAST, row_counter, cell_counter + 1])
                creature_positions.append([row_counter - 1, cell_counter])  # Store positions for later swap
                no_adjacent_vegetop = not check_adjacent_vegetop(cells, row_counter - 1, cell_counter, 20)

                if len(erbast_coordinates) > 1 and cell.VEGETOP < 20 and no_adjacent_vegetop and cell.ERBAST[0] > 0:
                    for i in range(1, len(erbast_coordinates)):
                        current_erbast = erbast_coordinates[i][0]
                        before_erbast = erbast_coordinates[i - 1][0]

                        # Print statements to show the swap process
                        #print(f'Before swap: current_erbast = {current_erbast}, before_erbast = {before_erbast}')
                        if current_erbast[0] > 0 and before_erbast[0] > 0: # Ensure current creature energy is greater than 0
            # Check for herd conditions
                            counter_erbast_herd = 1
                            if current_erbast[1] == 1 and before_erbast[1] == 1:
                                counter_erbast_herd += 1
                # Merge erbast values
                                #print(f'Before herd swap: erbast_herd = {current_erbast}, before_erbast = {before_erbast}')

                                erbast_herd = [
                                (current_erbast[0] + before_erbast[0]) , #enerjilerinin toplami
                                    1, #socialability ayni kaliyor
                                (current_erbast[2] + before_erbast[2]) // 2, # yaslarinin ortalamasi
                                max(current_erbast[3], before_erbast[3]) # lifetime larindan da buyuk olanini al
                                        ]

                                # Update the coordinates
                                current_erbast = erbast_herd
                                before_erbast = [0, 0, 0, 0]
                                erbast_coordinates[i][0] = current_erbast
                                erbast_coordinates[i - 1][0] = before_erbast
                                
                                x1, y1 = creature_positions[i]
                                x2, y2 = creature_positions[i - 1]
                                creature_grid[x1][y1] = (current_erbast[0] +100) / counter_erbast_herd
                                creature_grid[x2][y2] = before_erbast[0] + 100
                                #print(f'after herd swap: erbast_herd = {current_erbast}, before_erbast = {before_erbast}')
                        # Swapping the values
                            temporary_erbast = current_erbast
                            current_erbast = before_erbast
                            before_erbast = temporary_erbast

                        # Update the coordinates
                            erbast_coordinates[i][0] = current_erbast
                            erbast_coordinates[i - 1][0] = before_erbast

                        # Swap positions in the creature_positions list
                            temp_pos = creature_positions[i]
                            creature_positions[i] = creature_positions[i - 1]
                            creature_positions[i - 1] = temp_pos

                        # Update the creature_grid for visualizing movement
                        x1, y1 = creature_positions[i]
                        x2, y2 = creature_positions[i - 1]
                        if current_erbast[0] > 0 and before_erbast[0] > 0:
                            current_erbast[0] = current_erbast[0] - 1
                            before_erbast[0] = before_erbast[0] - 1
                        creature_grid[x1][y1] = current_erbast[0] + 250
                        creature_grid[x2][y2] = before_erbast[0] + 250
                        

                        #print(f'After swap: current_erbast = {current_erbast}, before_erbast = {before_erbast}')

                if cell.ERBAST[0] <= 0:
                    dead_erbast += 1
                    dead_erbast_list.append(dead_erbast)
                else:
                    erbast_counter += 1

            elif cell.CARVIZ:
                rows.append(cell.CARVIZ[0])
                vegetop_row.append(cell.VEGETOP)
                creature_grid[row_counter - 1][cell_counter] = cell.CARVIZ[0] + 100  # Offset for carviz

                carviz_coordinates.append([cell.CARVIZ, row_counter, cell_counter + 1])
                creature_positions.append([row_counter - 1, cell_counter])  # Store positions for later swap

                # Check if there are no erbasts in the adjacent cells
                no_erbasts = not check_adjacent_for_erbast(cells, row_counter - 1, cell_counter)

                if len(carviz_coordinates) > 1 and no_erbasts and cell.CARVIZ[0] > 0:
                    for i in range(1, len(carviz_coordinates)):
                        current_carviz = carviz_coordinates[i][0]
                        before_carviz = carviz_coordinates[i - 1][0]
                        if current_carviz[0] > 0 and before_carviz[0] > 0: # Ensure current creature energy is greater than 0
            # Check for herd conditions
                            carviz_herd_counter = 1
                            if current_carviz[1] == 1 and before_carviz[1] == 1:
                                carviz_herd_counter += 1
                                #print(f'before herd swap: herd_carviz = {current_carviz}, before_carviz = {before_carviz}')

                # Merge erbast values
                                carviz_pride = [
                                (current_carviz[0] + before_carviz[0]) , #enerjilerinin toplami
                                    1, #socialability ayni kaliyor
                                (current_carviz[2] + before_carviz[2]) // 2, # yaslarinin ortalamasi
                                max(current_carviz[3], before_carviz[3]) # lifetime larindan da buyuk olanini al
                                        ]

                                # Update the coordinates
                                current_carviz = carviz_pride
                                before_carviz= [0, 0, 0, 0]
                                carviz_coordinates[i][0] = current_carviz
                                carviz_coordinates[i - 1][0] = before_carviz
                                x1, y1 = creature_positions[i]
                                x2, y2 = creature_positions[i - 1]
                                creature_grid[x1][y1] = (current_carviz[0] +100 )/ carviz_herd_counter
                                creature_grid[x2][y2] = before_carviz[0] + 100
                                #print(f'after herd swap: herd_carviz = {current_carviz}, before_carviz = {before_carviz}')


                                
                        # Print statements to show the swap process
                        #print(f'Before swap: current_carviz = {current_carviz}, before_carviz = {before_carviz}')

                        # Swapping the values
                        temporary_carviz = current_carviz
                        current_carviz = before_carviz
                        before_carviz = temporary_carviz

                        # Update the coordinates
                        carviz_coordinates[i][0] = current_carviz
                        carviz_coordinates[i - 1][0] = before_carviz

                        # Swap positions in the creature_positions list
                        temp_pos = creature_positions[i]
                        creature_positions[i] = creature_positions[i - 1]
                        creature_positions[i - 1] = temp_pos
                        if current_carviz[0] > 0 and before_carviz[0] > 0:
                            current_carviz[0] = current_carviz[0] - 1
                            before_carviz[0] = before_carviz[0] - 1
                        # Update the creature_grid for visualizing movement
                        x1, y1 = creature_positions[i]
                        x2, y2 = creature_positions[i - 1]
                        creature_grid[x1][y1] = current_carviz[0] + 100
                        creature_grid[x2][y2] = before_carviz[0] + 100

                        #print(f'After swap: current_carviz = {current_carviz}, before_carviz = {before_carviz}')

                if cell.CARVIZ[0] <= 0:
                    dead_carviz += 1
                    dead_carviz_list.append(dead_carviz)
                else:
                    carviz_counter += 1
            else:
                vegetop_row.append(cell.VEGETOP)
                creature_grid[row_counter - 1][cell_counter] = 20  # Ground

            cell_counter += 1

            #print(f'row and cell {row_counter},{cell_counter}')

        grid.append(rows)
        vegetop_grid.append(vegetop_row)

    print(f'dead erbast :{dead_erbast}, dead carviz {dead_carviz}, carviz counter{carviz_counter}, erbast counter {erbast_counter}')
    print(f'energy level grid :{grid}')
    print(f'vegetob density grid:{vegetop_grid}')
    print(f'creature place grid:{creature_grid}')

    # Define custom colormaps
    colors = [
        (0, 'blue'),        # Water
        (0.1, 'black'),    # Ground
        (0.2, 'yellow'),   # Start of Carviz range
        (0.6, 'orange'),
        (0.8, 'lightgreen'),      # End of Carviz range
        (1.0, 'darkgreen') # End of Erbast range
    ]

    cmap = LinearSegmentedColormap.from_list('creature_colors', colors, N=301)

    # Adjusting for 3 subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    # First Graph - Creature Energy Levels
    energy_im = axs[0, 0].imshow(grid, cmap='hot')
    fig.colorbar(energy_im, ax=axs[0, 0], fraction=0.046, pad=0.04)
    axs[0, 0].set_title('Creature Energy Levels')
    # Second Graph - VEGETOP Density
    dens_veg_im = axs[0, 1].imshow(vegetop_grid, cmap='Greens')
    fig.colorbar(dens_veg_im, ax=axs[0, 1], fraction=0.046, pad=0.04)
    axs[0, 1].set_title('VEGETOP Density in Each Cell')
    # Third Graph - Number of Dead and Alive Creatures
    categories = ['ERBAST', 'CARVIZ']
    alive_counts = [erbast_counter, carviz_counter]
    dead_counts = [dead_erbast, dead_carviz]
    index = range(len(categories))
    bar_width = 0.35

    bars_alive = axs[1, 0].bar(index, alive_counts, bar_width, label='Alive', color='green')
    bars_dead = axs[1, 0].bar([p + bar_width for p in index], dead_counts, bar_width, label='Dead', color='red')

    axs[1, 0].set_title('Counts of Alive and Dead Creatures')
    axs[1, 0].set_xticks([p + bar_width / 2 for p in index])
    axs[1, 0].set_xticklabels(categories)
    axs[1, 0].legend()
    # Fourth Graph - Placement of the creatures
    creature_im = axs[1, 1].imshow(creature_grid, cmap=cmap, vmin=-1, vmax=300)
    cbar = fig.colorbar(creature_im, ax=axs[1, 1], fraction=0.046, pad=0.04)
   
    axs[1, 1].set_title('Creature Locations')
    cbar.set_ticks([-1, 20, 100, 250])  # Set ticks at the values used for water, ground, carviz, and erbast
    cbar.set_ticklabels(['Water', 'Ground', 'Carviz (0-100)', 'Erbast (100-300)'])  # Define custom labels
    plt.tight_layout()
    plt.suptitle('Platinus')
    manager = plt.get_current_fig_manager()
    manager.resize(2100, 1200)  # Piksel cinsinden boyut (genişlik, yükseklik)
    plt.show()
    return creature_grid


                



def animation(cells):
    plt.ion()  # Turn on interactive mode
    day_counter = 0
    for i in range(25):  # Animation duration in days
        uptade_world(i, cells)
        creature_grid = main_plot(cells)
        plt.pause(0.60)
        day_counter += 1
        print(f'DAY_{day_counter}')
    

    plt.ioff()  # Turn off interactive mode
    
    plt.show()  # Show the final plot
    plt.close()  # Close the plot window


print(cells)
animation(cells)
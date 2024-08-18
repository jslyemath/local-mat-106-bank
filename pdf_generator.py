import csv


def get_named_value(filename, name, direction):
    # Open and read the CSV file
    with open(filename, mode='r') as file:
        csv_reader = list(csv.reader(file))  # Convert to list for easier access to adjacent cells

        # Map direction to row and column index offsets
        direction_map = {
            'above': (-1, 0), 'up': (-1, 0),
            'below': (1, 0), 'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

        # Get the row and column offsets from the direction_map
        row_offset, col_offset = direction_map.get(direction.lower(), (0, 0))

        # Loop through each row by index
        for i, row in enumerate(csv_reader):
            # Look for the 'name' string in the row
            for j, cell in enumerate(row):
                if cell == name:
                    # Calculate the target row and column based on direction
                    target_row = i + row_offset
                    target_col = j + col_offset

                    # Check if the target cell is within bounds
                    if 0 <= target_row < len(csv_reader) and 0 <= target_col < len(csv_reader[target_row]):
                        return csv_reader[target_row][target_col]
                    else:
                        return None  # If out of bounds, return None

    return None  # Return None if 'name' not found in the CSV file


filename = 'test.csv'
name = 'W6:'
direction = 'below'
value = get_named_value(filename, name, direction)
print(f'{name} value: {value}')

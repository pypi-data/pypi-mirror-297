## Table Creation Example

The `Table` class allows you to create and print structured tables with headers and rows.

### Example:

```python
from beautiprint import Table

# Define table headers
table = Table(headers=["Name", "Age", "City"])

# Add rows to the table
table.add_row(["Alice", "30", "New York"])
table.add_row(["Bob", "25", "Los Angeles"])

# Access specific data
print(table.get_row(1))  # Outputs: ['Bob', '25', 'Los Angeles']
print(table.get_column("City"))  # Outputs: ['New York', 'Los Angeles']

# Print the table
table.print()
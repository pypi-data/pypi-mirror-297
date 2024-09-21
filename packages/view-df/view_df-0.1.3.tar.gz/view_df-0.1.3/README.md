# DataFrame Viewer

A Python module to display large pandas DataFrames with auto-adjusted column widths in a web browser.

## Overview

This module lets you visualize pandas DataFrames in a more readable format by rendering them as HTML tables in your default web browser. It includes basic styling to ensure that column widths are auto-adjusted, making it easier to view large DataFrames without saving them to disk.

## Features

- **Auto-Adjusted Column Widths**: Improves readability by adjusting column widths dynamically.
- **Hightlight Selected Cells**: Row and Column of any selected cell is highlighted for better visuals.
- **HTML Rendering**: Displays DataFrames in a formatted HTML table.
- **No Disk Writes**: Uses temporary files automatically deleted after use.

## Installation

1. **Install directly**:
    ```bash
    pip install view_df
    ```
### or
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/TheKola/dataframe-viewer.git
   ```
2. **Navigate to the Project Directory**:
    ```bash
    cd dataframe-viewer
    ```
3. **Copy the file `view_df.py` to your project folder**
## Usage

1. Import the Module:
    ```bash
    from view_df import view_df
2. Create a DataFrame and view it:
    ```bash
    import pandas as pd
    from view_df import view_df

    # Example DataFrame
    data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Occupation': ['Engineer', 'Doctor', 'Artist'],
    'Location': ['New York', 'Los Angeles', 'Chicago']
    }
    df = pd.DataFrame(data)

    # View the DataFrame in a web browser
    view_df(df)

## Output
   <p align="center">
  <img src="example_output.png" width="100%" title="hover text">
</p>

## Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more details.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

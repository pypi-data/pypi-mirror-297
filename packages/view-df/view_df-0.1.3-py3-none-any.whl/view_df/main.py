import pandas as pd
import webbrowser
import tempfile

def view_df(df: pd.DataFrame):
    """
    Converts the given DataFrame to an HTML file with auto-adjusted column widths,
    highlights rows and columns on click, and opens it in the default web browser.
    
    Parameters:
    df (pd.DataFrame): The pandas DataFrame to display.
    """
    # Define custom CSS and JavaScript for highlighting
    css = """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 8px;
        text-align: left;
        white-space: nowrap;
        position: relative;
    }
    th {
        background-color: #f2f2f2;
        position: relative;
    }
    .highlight-row {
        background-color: #d3d3d3; /* Light gray for row highlight */
    }
    .highlight-column {
        background-color: #d3d3d3; /* Light gray for column highlight */
    }
    </style>
    <script>
    var lastClickedRow = null;
    var lastClickedCol = null;

    function highlight(rowIdx, colIdx) {
        var rows = document.querySelectorAll('tr');
        var cols = document.querySelectorAll('td');
        
        rows.forEach(function(row) {
            row.classList.remove('highlight-row');
        });
        
        cols.forEach(function(col) {
            col.classList.remove('highlight-column');
        });

        document.querySelectorAll('tr')[rowIdx].classList.add('highlight-row');
        document.querySelectorAll('td:nth-child(' + (colIdx + 1) + ')').forEach(function(cell) {
            cell.classList.add('highlight-column');
        });
        
        lastClickedRow = rowIdx;
        lastClickedCol = colIdx;
    }
    
    function removeHighlight() {
        if (lastClickedRow !== null && lastClickedCol !== null) {
            var rows = document.querySelectorAll('tr');
            var cols = document.querySelectorAll('td');
            
            rows.forEach(function(row) {
                row.classList.remove('highlight-row');
            });
            
            cols.forEach(function(col) {
                col.classList.remove('highlight-column');
            });

            document.querySelectorAll('tr')[lastClickedRow].classList.add('highlight-row');
            document.querySelectorAll('td:nth-child(' + (lastClickedCol + 1) + ')').forEach(function(cell) {
                cell.classList.add('highlight-column');
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        var cells = document.querySelectorAll('td');
        
        cells.forEach(function(cell) {
            cell.addEventListener('click', function() {
                var rowIdx = cell.parentElement.rowIndex;
                var colIdx = cell.cellIndex;
                highlight(rowIdx, colIdx);
            });
        });

        document.addEventListener('click', function(event) {
            if (!event.target.closest('td')) {
                removeHighlight();
            }
        });
    });
    </script>
    """
    
    # Convert DataFrame to HTML
    html = df.to_html(classes='dataframe', escape=False, index=False)
    
    # Combine CSS, JavaScript, and HTML
    html_with_css_js = css + html
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as temp_file:
        # Write the HTML with CSS and JavaScript to the temporary file
        temp_file.write(html_with_css_js)
        temp_file.flush()  # Ensure all data is written
        
        # Open the HTML file in the default web browser
        webbrowser.open('file://' + temp_file.name)

# Example usage
if __name__ == "__main__":
    data = {'Name': ['Alice', 'Bob', 'Charlie'],
            'Occupation': ['Engineer', 'Doctor', 'Artist'],
            'Location': ['New York', 'Los Angeles', 'Chicago']}
    df = pd.DataFrame(data)
    view_df(df)

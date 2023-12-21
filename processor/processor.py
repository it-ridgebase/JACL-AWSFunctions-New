import pandas as pd

def process_excel(file_path):
    
    # Read the Excel file
    df = pd.read_excel(file_path)

    return df

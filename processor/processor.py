import pandas as pd

def process_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Rename columns to match Airtable column names

    employee = {
        "LiQ - Payroll Number",
        "LiQ - First Name✏️",
        "LiQ - Last Name✏️",
        "LiQ - Date Of Birth✏️",
        "LiQ - Address Line 1✏️",
        "LiQ - Address Line 2✏️",
        "LiQ - Address Town✏️",
        "LiQ - Province✏️",
        "LiQ - Address Post Code✏️",
        "LiQ - Home Phone✏️",
        "LiQ - Cell Phone✏️",
        "LiQ - Email✏️",
        "LiQ - Hired Date",
        "LiQ - Position",
        "LiQ - Subway Id",
        "LiQ - Salaried Employee",
        "LiQ - Separation date",
        "LiQ - Emergency 1 - Name✏️",
        "LiQ - Emergency 1 - Relationship✏️",
        "LiQ - Emergency 1 - Home Phone Number✏️",
        "LiQ - Emergency 1 - Mobile Phone Number✏️",
        "LiQ - Emergency 2 - Name✏️",
        "LiQ - Emergency 2 - Relationship✏️",
        "LiQ - Emergency 2 - Home Phone Number✏️",
        "LiQ - Emergency 2 - Mobile Phone Number✏️",
        # "POS Security Permissions",
        "LiQ - Standard Rate",
        "LiQ - Standard Rate - Start Date",
        "LiQ - Standard Rate - End Date",
        "LiQ - Allocated Store",
        "LiQ - Clerk ID",
        "LiQ - Main Store - Start Date",
        "LiQ - Main Store End Date"
    }
    column_mapping = {
        'Payroll Number*': 'LiQ - Payroll Number',
        'Title': 'LiQ - Title',  # Assuming you have a corresponding field in Airtable
        'First Name*': 'LiQ - First Name✏️',
        'Initials': 'LiQ - Initials',  # Assuming you have a corresponding field in Airtable
        'Last Name*': 'LiQ - Last Name✏️',
        'Known As': 'LiQ - Known As',  # Assuming you have a corresponding field in Airtable
        'Date Of Birth*': 'LiQ - Date Of Birth✏️',
        'Address Line 1': 'LiQ - Address Line 1✏️',
        'Address Line 2': 'LiQ - Address Line 2✏️',
        'Address Town': 'LiQ - Address Town✏️',
        'State': 'LiQ - Province✏️',
        'Address Post Code': 'LiQ - Address Post Code✏️',
        'Home Phone': 'LiQ - Home Phone✏️',
        'Cell Phone': 'LiQ - Cell Phone✏️',
        'Email': 'LiQ - Email✏️',
        'Start Date': 'LiQ - Hired Date',
        'Position*': 'LiQ - Position',
        'PRO Qualified': 'LiQ - PRO Qualified',  # Assuming you have a corresponding field in Airtable
        'Subway Id': 'LiQ - Subway Id',
        'Salaried Employee': 'LiQ - Salaried Employee',
        'End Current Employment Period': 'LiQ - Separation date',
        # Add other mappings as needed
    }
    df.rename(columns=column_mapping, inplace=True)

    # Convert date columns to ISO format and handle nulls
    date_columns = ['LiQ - Date Of Birth✏️', 'LiQ - Hired Date', 'LiQ - Separation date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S')

    # Replace NaN with appropriate defaults or empty strings
    df.fillna('', inplace=True)

    # Additional transformations
    # For example, converting 'Salaried Employee' to a boolean string
    if 'LiQ - Salaried Employee' in df.columns:
        df['LiQ - Salaried Employee'] = df['LiQ - Salaried Employee'].apply(lambda x: 'True' if x else 'False')

    # Additional transformations for other fields can be added here
    # ...

    return df

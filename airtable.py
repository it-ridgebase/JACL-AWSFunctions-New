from airtable import Airtable 

# Uploads data to an Airtable table
def upload_to_airtable(api_key, base_id, table_name, data):

    # Initialize an Airtable object. This object is used to interact with a specific Airtable table.
    # 'base_id' is the ID of the Airtable base, 'table_name' is the name of the table within the base,
    # and 'api_key' is the API key for accessing Airtable
    airtable = Airtable(base_id, table_name, api_key)


    # Iterate over each record in the data. The data is expected to be a pandas DataFrame,
    # and 'to_dict('records')' converts it into a list of dictionaries where each dictionary
    # represents a row in the DataFrame
    for record in data.to_dict('records'):

        # Insert each record into the Airtable table. The 'insert' method adds a new row to the table
        # with the data from the record dictionary
        airtable.insert(record)

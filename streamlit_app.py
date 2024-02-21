import streamlit as st
import pandas as pd

def transform_data(df):
    df1 = df.copy()

    column_mapping = {
        'Day Name': 'Day',
        'Campaign Name': 'Campaign Name',
        'Brand Name': 'Brand Name',
        'Media Type': 'Medium Type',
        'Media Platform': 'Vendor Name',
        'Program': 'Program',
        'Time From': 'Time',
        'No. Of Insertions': 'Qty',
        'Spot Start Date': 'Year/ Month',
        'NTC (LCY)': 'NTC (LCY)',
        'Supplier Name': 'Supplier',
        'Client Billing Currency': 'Suppl.Curr.',
        'Location': 'Location',
        'Market': 'Market',
        'Campaign End Date': 'Month End Date',
        'Description': 'Description'
    }

    df1 = df1.rename(columns=lambda x: column_mapping.get(x.strip(), x))

    empty_columns = [
        'Booking Date', 'Campaign No.', 'Insertion No.', 'Customer Name', 'Position',
        'Duration', 'Medium Unit', 'Spot Status', 'Spot Kind', 'Gross (LCY)', 'NTM (LCY)',
        'NTC - NTM (LCY)', 'Customer VAT (LCY)', 'Vendor VAT (AED)', 'BO No.',
        'Old BO-No. (void spots)', 'Suppl.Net', 'Suppl.VAT', 'Adv.Paid?', 'MI No.',
        'MI Date', 'MI Curr.', 'MI Net', 'MI VAT', 'MI Status', 'Adv.Billed?', 'Customer LPO',
        'Extern.Doc.No.', 'Material', 'Edititon', 'Site', 'Master Medium', 'Product',
        'Group Customer', 'Group Supplier', 'Division', 'Customer No.', 'Group Cust No.',
        'Cust. Posting Group', 'User ID', 'Placement Instructions', 'Rate Per Unit(BCY)',
        'Vendor 1st?', 'Practice'
    ]

    df_new = pd.concat([df1, pd.DataFrame(columns=empty_columns)], axis=1)

    desired_order = [
        'Booking Date', 'Day', 'Campaign No.', 'Insertion No.', 'Campaign Name',
        'Customer Name', 'Brand Name', 'Medium Type', 'Vendor Name', 'Position',
        'Program', 'Time', 'Duration', 'Medium Unit', 'Spot Status', 'Qty',
        'Spot Kind', 'Year/ Month', 'Gross (LCY)', 'NTM (LCY)', 'NTC (LCY)',
        'NTC - NTM (LCY)', 'Customer VAT (LCY)', 'Vendor VAT (AED)', 'BO No.',
        'Old BO-No. (void spots)', 'Supplier', 'Suppl.Curr.', 'Suppl.Net',
        'Suppl.VAT', 'Adv.Paid?', 'MI No.', 'MI Date', 'MI Curr.', 'MI Net',
        'MI VAT', 'MI Status', 'Adv.Billed?', 'Customer LPO', 'Extern.Doc.No.',
        'Material', 'Edititon', 'Site', 'Location', 'Master Medium', 'Product', 'Group Customer',
        'Group Supplier', 'Division', 'Market', 'Customer No.', 'Group Cust No.',
        'Cust. Posting Group', 'User ID', 'Placement Instructions',
        'Rate Per Unit(BCY)', 'Month End Date', 'Vendor 1st?', 'Practice',
        'Description'
    ]

    df_new = df_new[desired_order]

    df_new['Year/ Month'] = pd.to_datetime(df_new['Year/ Month'], format='%d-%m-%Y').dt.strftime('%d/%m/%Y')
    df_new['Month End Date'] = pd.to_datetime(df_new['Month End Date'], format='%d-%m-%Y').dt.strftime('%d/%m/%Y')

    day_mapping = {
        'Monday': 'Mon',
        'Tuesday': 'Tue',
        'Wednesday': 'Wed',
        'Thursday': 'Thu',
        'Friday': 'Fri',
        'Saturday': 'Sat',
        'Sunday': 'Sun'
        # Add mappings for other days if needed
    }

    # Apply the mapping to the 'Day' column
    df_new['Day'] = df_new['Day'].map(day_mapping)

    df_new['Year/ Month'] = pd.to_datetime(df_new['Year/ Month'], format='%d/%m/%Y')
    df_new['Time'] = df_new['Time'].str.slice(0, 5)
    df_new['Year/ Month'] = df_new['Year/ Month'].dt.strftime('%Y/%m (%b)')

    return df_new

def main():
    st.title("Data Transformation App")

    # Upload file
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

    if uploaded_file:
        # Read data from uploaded file
        df = pd.read_excel(uploaded_file, skiprows=7)

        st.write("### Original Data:")
        st.write(df)

        st.write("### Transformed Data:")
        transformed_df = transform_data(df)
        st.write(transformed_df)

        st.markdown("### Download Transformed Data")
        
        # Create a link for downloading the transformed data
        transformed_data_link = get_transformed_data_link(transformed_df)
        
        # Display download link
        st.markdown(transformed_data_link, unsafe_allow_html=True)

def get_transformed_data_link(df):
    # Save the transformed data to a temporary file
    temp_file_path = "/tmp/transformed_data.xlsx"
    df.to_excel(temp_file_path, index=False, engine='xlsxwriter')
    
    # Generate a download link
    download_link = f'<a href="/download?file_path={temp_file_path}" download="transformed_data.xlsx">Click here to download the transformed data</a>'
    
    return download_link

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import pyperclip
import os

from supabase_py import create_client,Client



# Set initial scale for very small screens
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=0.5">', unsafe_allow_html=True)

# Display the PNG image in the top left corner of the Streamlit sidebar with custom dimensions
# Display the PNG image in the top left corner of the Streamlit sidebar with custom dimensions
image_path = r"C:\Users\User\Desktop\Career-Exploration-main\graphics\VS-logo.png"
st.sidebar.image(image_path, width=150)

logo_path = r"C:\Users\User\Downloads\pngtree-vector-assignment-icon-png-image_4254076.jpg"
st.sidebar.image(logo_path, width=90)

# Predefined dictionary of user names and access codes known only to administrators
user_access_codes = {
    "Shalini": "abc123",
    "Titli": "def456",
    "Deepika": "ghi789",
    # Add more user names and access codes as needed
}

# Prompt the user to enter their access code
entered_code = st.sidebar.text_input("Enter Your Access Code *:", type="password")
# Check if either of the boxes is not selected
if not entered_code:
    st.error("Please fill in all the compulsory fields marked with * before proceeding.")
    st.stop()

# Filter the user names based on the entered access code
filtered_user_names = [user_name for user_name, access_code in user_access_codes.items() if entered_code == access_code]

# If a user name is found for the entered access code, display the select box for that user
selected_user_name = st.sidebar.selectbox('Select Your User Name:', filtered_user_names)

selected_Cohort = st.sidebar.selectbox("Select an option", ["Incubator_1","Incubator_2","Incubator_3"])

# Display the selected option
st.write("Selected Option:", selected_Cohort)

# Read all assignment files and store them in a dictionary
import os
import pandas as pd
import streamlit as st
import pyperclip

# Function to read all CSV files from a folder and store them in a dictionary
def read_assignment_files(folder_path):
    file_mapping = {}
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        file_mapping[file_name] = pd.read_csv(file_path)
    
    return file_mapping

# Function to get the dataset for a selected assignment file
def get_dataset(selected_assignment_file):
    return file_mapping[selected_assignment_file]

# Define the folder path for CSV files
folder_path = r"C:\Users\User\OneDrive\VS GUI\GUI\venv\stemcheck files"

# Read all assignment files from the folder
file_mapping = read_assignment_files(folder_path)

# Streamlit app interface
# Create the Streamlit app interface
st.title('STEMCHECK - STEM Assignment Checker Kit')

# Select the assignment file from the available files
selected_assignment_file = st.sidebar.selectbox('Select an assignment file', list(file_mapping.keys()))
if selected_assignment_file is not None:
    #st.write(f"Displaying data for file: {selected_assignment_file}")
    selected_dataset = get_dataset(selected_assignment_file)
    #st.write(selected_dataset)


# Read the category dataset and extract unique categories
import requests
import pandas as pd
from io import BytesIO

# URL pointing to the CSV file
file_url = 'https://bvvaailuzioczysisnoc.supabase.co/storage/v1/object/sign/Stemcheck/Comments_sheet.csv?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJTdGVtY2hlY2svQ29tbWVudHNfc2hlZXQuY3N2IiwiaWF0IjoxNzE3NjYwMzQ1LCJleHAiOjE3NDkxOTYzNDV9.gUNII7Hhc3yqRNJKJ780GVlfvOTEAi9fhxIh9AWbGV0&t=2024-06-06T07%3A52%3A24.268Z'

# Make a GET request to the URL to retrieve the CSV file
try:
    response = requests.get(file_url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Read the content of the response as a pandas DataFrame, specifying the appropriate encoding
    category_dataset = pd.read_csv(BytesIO(response.content), encoding='latin1')  # You can try 'latin1' encoding as an alternative
    # Proceed with processing the data in the dataframe 'df'
except requests.exceptions.RequestException as e:
    print("An error occurred while accessing the CSV file:", e)
except Exception as e:
    print("An error occurred while reading the CSV file:", e)


#category_dataset = pd.read_csv("C:/Users/User/Downloads/Comments sheet.csv", encoding='latin1')
unique_categories = category_dataset['Category '].unique()
unique_status = category_dataset['Accepted /Rejected'].unique()

data = get_dataset(selected_assignment_file)


# Create a dropdown to select the file status
file_statuses = data['status'].unique()
selected_status = st.sidebar.selectbox('Select File Status', file_statuses)


# Filter the data based on the selected status from the selected assignment file
filtered_data = get_dataset(selected_assignment_file)
filtered_data = filtered_data[filtered_data['status'] == selected_status]

# Create a dropdown to select the email ID
if 'user/email' in filtered_data.columns:
    email_list = filtered_data['user/email'].str.split('-').str[1].tolist()  # Extract email IDs after the hyphen
    
    # Placeholder to store the list of processed email IDs

    if "processed_emails" not in st.session_state:
        st.session_state.processed_emails = []  # Initialize the variable
    
    # Filter out the processed email IDs
    email_list = [email for email in email_list if email not in st.session_state.processed_emails]
    
    selected_email = st.selectbox('Select Email ID:', email_list)

    # Filter data based on selected email
    filtered_email_data = filtered_data[filtered_data['user/email'] == 'vigyanshaalainternational1617-' + selected_email]

    # Add a copy button to copy the email address to the clipboard
    if selected_email:
        copy_email_button_text = "Copy Email Address"
        if st.button(copy_email_button_text):
            pyperclip.copy(selected_email)  # Copy the email address to the clipboard
            st.write("Email address copied to clipboard")  # Inform the user that the email address has been copied

    if not filtered_email_data.empty:
        latest_submission_email = None
        latest_submission_col = None
        latest_submission_no = None

    # Get the latest filled column without NA or blank for the file name format 'data/{i}/fileName'
    for col in filtered_email_data.columns[::-1]:  # Iterate in reverse to get the last filled column
        if 'fileName' in col:
            latest_submission_email = filtered_email_data[col].dropna().iloc[-1] if not filtered_email_data[col].dropna().empty else None
            if latest_submission_email:
                latest_submission_col = col
                break

    file_name = latest_submission_col
    split_file_name = file_name.split('/')
    if len(split_file_name) > 2:
        result = split_file_name[1]  # Extract the part between the slashes
        latest_submission_no = result
    else:
        print("Invalid format")

    if latest_submission_email is not None:
        st.markdown(f"File name: {latest_submission_email}")
    else:
        st.sidebar.text("No valid file name found")

    if latest_submission_no is not None:
        st.markdown(f"Submission Number: {latest_submission_no}")

    if not filtered_email_data.empty:
        latest_messages = []
        # Get the latest message for the filtered email ID
        for col in filtered_email_data.columns:
            if 'message' in col:
                latest_message_column = filtered_email_data[col].dropna()
                if not latest_message_column.empty:
                    latest_message = latest_message_column.iloc[-1]
                    latest_messages.append(latest_message)

        if latest_messages:
            latest_email_message = latest_messages[-1]
            write_text = f"Comment: **{latest_email_message}**"
            st.sidebar.write(write_text)
        else:
            st.write('No message found for the selected email')
    else:
        st.write('No data found for the selected email')


# Display the select boxes with asterisk for compulsory selection
selected_category = st.sidebar.selectbox('Select category*', unique_categories, key='category_select')
selected_category_status = st.sidebar.radio('Select comments category status*', unique_status, key='category_status_radio')

# Check if either of the boxes is not selected
if not selected_category or not selected_category_status:
    st.error("Please fill in all the compulsory fields marked with * before proceeding.")
    st.stop()



# Filter the comments based on acceptance or rejection
if 'Accepted /Rejected' in category_dataset.columns and 'Comment' in category_dataset.columns:
    selected_category_accepted = category_dataset[(category_dataset['Category '] == selected_category) & (category_dataset['Accepted /Rejected'] == selected_category_status)]['Comment'].tolist()
    
    if selected_category_accepted:
        # Create a multiselect to choose from the available comments
        selected_comments_accepted = st.multiselect('Select Comments:*', selected_category_accepted)
        
        # Check if either of the boxes is not selected
        if not selected_comments_accepted:
            st.error("Please fill in all the compulsory fields marked with * before proceeding.")
            st.stop()

        if selected_comments_accepted:
            selected_comments_text_accepted = '\n'.join(selected_comments_accepted)
            comment_area_accepted = st.text_area('Selected Comments:', value=selected_comments_text_accepted, height=120)

        # Text area to allow the user to provide a custom comment
        custom_comment = st.text_area('Add Custom Comment:', height=60)
        
        # Concatenate the selected comments with the custom comment
        all_comments = selected_comments_accepted + [custom_comment] if custom_comment else selected_comments_accepted

        if all_comments:
            selected_comments_text_accepted = '\n'.join(all_comments)

# Create a text box to enter marks for the selected email ID and assignment file
if selected_email and selected_assignment_file:
    marks_key = f"marks_{selected_email}_{selected_assignment_file}"
    marks = st.text_input("Enter Marks:*", key=marks_key)
    # Check if either of the boxes is not selected
    if not marks:
        st.error("Please fill in all the compulsory fields marked with * before proceeding.")
        st.stop()
    if marks:
        st.write(f"Marks entered: {marks}")


# Add an empty line to visually separate the elements
st.write("")

unique_key = latest_submission_email + " " + f"_Email {selected_email}"+" "+f"_Sub No:{latest_submission_no}"

# Define a function to create a DataFrame with the provided data
def create_feedback_dataframe(unique_key,selected_user_name,selected_assignment_file, selected_status, latest_submission_email, latest_submission_no, selected_email, latest_messages, selected_comments_accepted,marks,selected_Cohort):
    data = {
        'Email_ID': [selected_email],
        'Assignment_File': [selected_assignment_file],
        'File_Status': [selected_status],
        'PDF_Name': [latest_submission_email],
        'Submission_Number': [latest_submission_no],
        'Message_Displayed': [latest_messages],
        #'Category Status': [selected_category_status],
        'Marks': [marks],
        'Comments': [", ".join(selected_comments_accepted) if selected_comments_accepted else None],
        'User_Name': [selected_user_name],
        'key': [unique_key],
        'Cohort':[selected_Cohort]
    }
    feedback_df = pd.DataFrame(data)
    return feedback_df


url: str = 'https://bvvaailuzioczysisnoc.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ2dmFhaWx1emlvY3p5c2lzbm9jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc1OTEwNTMsImV4cCI6MjAzMzE2NzA1M30.kDC8CsjhjB_XkVo9OM3EchNMWk5ytyc-s629I0-qr1k'
supabase: Client = create_client(url, key)


# Function to save feedback data to Supabase
def save_feedback_to_supabase(feedback_data, table_name):
    response = supabase.table(table_name).insert(feedback_data).execute()
    return response


# Function to read data from Supabase table
def read_data_from_supabase(table_name):
    response = supabase.table(table_name).select().execute()
    if response.get('error'):
        print(f"Error fetching data from '{table_name}': {response['error']}")
        return None
    return response.get('data')

# Create a button to copy the comment for the email ID, save feedback data, and extract email IDs
if selected_comments_accepted:
    combined_button_text = "Copy Comment, Save Feedback Data, and Extract Email IDs"
    if st.button(combined_button_text):
        # Copy the comment to the clipboard
        pyperclip.copy(selected_comments_text_accepted)
        
        # Create a DataFrame with the feedback data
        feedback_df = create_feedback_dataframe(unique_key, selected_user_name, selected_assignment_file, selected_status, latest_submission_email, latest_submission_no, selected_email, latest_messages, selected_comments_accepted, marks,selected_Cohort)
        
        # Convert DataFrame to dictionary records
        records = feedback_df.to_dict(orient='records')
        
        table_name = "TableF"
        
        # Save feedback data to Supabase
        response = save_feedback_to_supabase(records, table_name)

        
        for record in records:
            record_id = record.get('key')
            
            # Perform insertion or update based on record existence
            existing_record = supabase.table(table_name).select().eq('key', record_id).execute()
            
            if existing_record.get('error'):
                print(f"Error fetching existing record for key '{record_id}': {existing_record['error']}")
            else:
                if existing_record.get('data'):
                    # Update the existing record
                    response = supabase.table(table_name).update(record).eq('key', record_id).execute()
                    print(f"Updated Record with key {record_id}: {response}")
                else:
                    # Insert a new record
                    response = supabase.table(table_name).insert(record).execute()
                    print(f"Inserted New Record with key {record_id}: {response}")


        # Inform the user about the actions taken
        st.write("Comment copied to clipboard, Feedback data saved to Feedback.xlsx")
        

        # Fetch and display data from Supabase table 'TableF'
        supabase_table_name = 'TableF'
        supabase_url = 'https://bvvaailuzioczysisnoc.supabase.co'
        supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ2dmFhaWx1emlvY3p5c2lzbm9jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc1OTEwNTMsImV4cCI6MjAzMzE2NzA1M30.kDC8CsjhjB_XkVo9OM3EchNMWk5ytyc-s629I0-qr1k'

        response = requests.get(f'{supabase_url}/rest/v1/{supabase_table_name}', headers={'apikey': supabase_key})

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            print(df)  # Display the fetched data
        else:
            print(f"Failed to fetch data from '{supabase_table_name}': {response.text}")

        
        if filtered_user_names:
    # Group the DataFrame by 'Cohort' and 'User_Name' columns and count the number of occurrences
            cohort_user_counts = df.groupby(['Cohort', 'User_Name']).size().reset_index(name='User_Count')

        # Filter the cohort_user_counts DataFrame based on the selected_user_name
            selected_user_cohort_count = cohort_user_counts[cohort_user_counts['User_Name'] == selected_user_name]
            selected_user_cohort_count = cohort_user_counts[(cohort_user_counts['User_Name'] == selected_user_name) & (cohort_user_counts['Cohort'] == selected_Cohort)]

            if not selected_user_cohort_count.empty:
                st.write(f"Total Assignments corrected by {selected_user_name} in {selected_Cohort}: {selected_user_cohort_count['User_Count'].values[0]}")
            else:
                st.write(f"No assignments found for {selected_user_name} in {selected_Cohort}.")
        else:
            st.write("No user found for the entered access code. Please enter a valid code.")

            

        
# Add the processed email to the session state to remove it from the dropdown
        st.session_state.processed_emails.append(selected_email)




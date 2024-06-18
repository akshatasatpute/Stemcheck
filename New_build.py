#Has code with the Submissions number updated.
import streamlit as st

# Set initial scale for very small screens
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=0.5">', unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import pyperclip  # Import the pyperclip module for clipboard operations
import os

# Display the PNG image in the top left corner of the Streamlit sidebar with custom dimensions
image_path = r"C:\Users\User\Desktop\Career-Exploration-main\graphics\VS-logo.png"
st.sidebar.image(image_path, width=150)

logo_path = r"C:\Users\User\Downloads\pngtree-vector-assignment-icon-png-image_4254076.jpg"
st.sidebar.image(logo_path, width=90)

# Update the user name list with Shalini, Titli, and Deepika
#user_names = ['Shalini', 'Titli', 'Deepika']
# Predefined dictionary of user names and access codes known only to administrators
user_access_codes = {
    "Shalini": "abc123",
    "Titli": "def456",
    "Deepika": "ghi789",
    # Add more user names and access codes as needed
}

# Prompt the user to enter their access code
entered_code = st.sidebar.text_input("Enter Your Access Code:", type="password")

# Filter the user names based on the entered access code
filtered_user_names = [user_name for user_name, access_code in user_access_codes.items() if entered_code == access_code]

# If a user name is found for the entered access code, display the select box for that user

selected_user_name = st.sidebar.selectbox('Select Your User Name:', filtered_user_names)



# Read all assignment files and store them in a dictionary
file_mapping = {
    'CAP Classwork.csv': pd.read_csv(r"C:\Users\User\Downloads\Assignment_Assignment_CAP Classwork (13).csv"),
    'CV_ Resume.csv': pd.read_csv(r"C:\Users\User\Downloads\Assignment_Assignment_CV_ Resume (16).csv"),
    'Full CAP - GoalA+B.csv': pd.read_csv(r"C:\Users\User\Downloads\Assignment_Assignment_Full CAP - GoalA+B (13).csv"),
    'Long term dreams and short term goals.csv': pd.read_csv(r"C:\Users\User\Downloads\Assignment_Assignment_Long term dreams and short term goals (31).csv"),
    'Preparing for PG_Masters.csv': pd.read_csv(r"C:\Users\User\Downloads\Assignment_Assignment_Preparing for PG_Masters (33).csv")
}

# Read the category dataset and extract unique categories
category_dataset = pd.read_csv("C:/Users/User/Downloads/Comments sheet.csv", encoding='latin1')  # Replace 'path_to_category_dataset.csv' with the actual path
unique_categories = category_dataset['Category '].unique()
unique_status=category_dataset['Accepted /Rejected'].unique()

# Define function to get dataset based on selected assignment file
def get_dataset(selected_assignment_file):
    return file_mapping[selected_assignment_file]

data = get_dataset('CAP Classwork.csv')  # Initialize the data with one of the assignment files

# Create the Streamlit app interface
st.title('STEMCHECK - STEM Assignment Checker Kit')

# Create a dropdown to select the assignment file
selected_assignment_file = st.sidebar.selectbox('Select Assignment File', list(file_mapping.keys()))

# Create a dropdown to select the file status
file_statuses = data['status'].unique()
selected_status = st.sidebar.selectbox('Select File Status', file_statuses)

# Filter the data based on the selected status from the selected assignment file
filtered_data = get_dataset(selected_assignment_file)
filtered_data = filtered_data[filtered_data['status'] == selected_status]


# Create a dropdown to select the email ID
if 'user/email' in filtered_data.columns:
    email_list = filtered_data['user/email'].str.split('-').str[1].tolist()  # Extract email IDs after the hyphen
    selected_email = st.selectbox('Select Email ID:', email_list)
    # Filter data based on selected email
    filtered_email_data = filtered_data[filtered_data['user/email'] == 'vigyanshaalainternational1617-'+selected_email]

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

    #if latest_submission_email is not None:
        # Display the latest file name in the Streamlit sidebar
        #st.sidebar.markdown(f"File name: {latest_submission_email} (from column: {latest_submission_col})")
        #st.markdown(f"File name: {latest_submission_email}")
        #st.markdown(f"Submission No:{latest_submission_col}")
    file_name = latest_submission_col
    split_file_name = file_name.split('/')
    if len(split_file_name) > 2:
        result = split_file_name[1]  # Extract the part between the slashes
        latest_submission_no=result
    else:
        print("Invalid format")
    
    if latest_submission_email is not None:
        #st.markdown(f"File name: {latest_submission_email} (Submission No: {latest_submission_col})")
        #st.markdown(f"File name: {latest_submission_email} (Submission No: {result})")
        st.markdown(f"File name: {latest_submission_email}")
    else:
        st.sidebar.text("No valid file name found")


    if latest_submission_no is not None:
        st.markdown(f"Submission Number:{latest_submission_no}")

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

    

# Create a dropdown to select the categories
selected_category = st.sidebar.selectbox('Select category', unique_categories)
selected_category_status=st.sidebar.radio('Select category status',unique_status)

# Filter the comments based on acceptance or rejection
if 'Accepted /Rejected' in category_dataset.columns and 'Comment' in category_dataset.columns:
    selected_category_accepted = category_dataset[(category_dataset['Category '] == selected_category) & (category_dataset['Accepted /Rejected'] ==selected_category_status)]['Comment'].tolist()
    
    if selected_category_accepted:
        # Create a multiselect to choose from the available comments
        selected_comments_accepted = st.multiselect('Select Comments:', selected_category_accepted)

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
    marks = st.text_input("Enter Marks:", key=marks_key)

    if marks:
        st.write(f"Marks entered: {marks}")



# Add an empty line to visually separate the elements
st.write("")

unique_key=latest_submission_email+ " " +f",Submssion no {latest_submission_no}"
# Define a function to create a DataFrame with the provided data
def create_feedback_dataframe(selected_assignment_file,selected_status ,latest_submission_email,latest_submission_no, selected_email, latest_messages, selected_category_status,selected_comments_accepted,marks,unique_key):
    data = {
        'User Name' : [selected_user_name],
        'Assignment File': [selected_assignment_file],
        'File Status': [selected_status],
        'PDF Name': [latest_submission_email],
        'Submission Number':[latest_submission_no],
        'Email ID': [selected_email],
        'Message Displayed': [latest_messages],
        'Category Status': [selected_category_status],
        'Comments': [", ".join(selected_comments_accepted) if selected_comments_accepted else None],
        'Marks':[marks],
        'key':[unique_key]
    }
    feedback_df = pd.DataFrame(data)
    return feedback_df

# Create an empty list to store the feedback data
all_feedback_data = []


import os

# Create a button to copy the comment for the email ID and save feedback data
if selected_comments_accepted:
    copy_button_text_accepted = "Copy Comment & Save Feedback Data"
    if st.button(copy_button_text_accepted):
        # Copy the comment to the clipboard
        pyperclip.copy(selected_comments_text_accepted)
        
        
        # Create a DataFrame with the feedback data
        feedback_df = create_feedback_dataframe(selected_assignment_file,selected_status ,latest_submission_email,latest_submission_no,selected_email, latest_messages, selected_category_status,selected_comments_accepted,marks,unique_key)
        
        # Check if the Excel file already exists
        if os.path.isfile(r"C:\Users\User\Downloads\Feedback.xlsx"):
            # Read the existing Excel file
            existing_data = pd.read_excel(r"C:\Users\User\Downloads\Feedback.xlsx")
            
            # Append the new feedback data below the existing data
            updated_data = pd.concat([existing_data, feedback_df], ignore_index=True)
            
            # Write the updated data to the Excel file
            updated_data.to_excel(r"C:\Users\User\Downloads\Feedback.xlsx", index=False)
        else:
            # If the Excel file does not exist, create a new file and write the feedback data
            feedback_df.to_excel(r"C:\Users\User\Downloads\Feedback.xlsx", index=False)

        st.write("Comment copied to clipboard and Feedback data saved to Feedback.xlsx")  # Inform the user about the actions taken


Feedback_file= pd.read_excel(r"C:\Users\User\Downloads\Feedback.xlsx")


# If a user name is found for the entered access code, display the select box for that user
if filtered_user_names:

    # Display the count for the selected user name
    selected_user_count = Feedback_file[Feedback_file['User Name'] == selected_user_name].shape[0]
    st.write(f"The count for {selected_user_name} is: {selected_user_count}")
else:
    st.write("No user found for the entered access code. Please enter a valid code.")



# Create the user interface in Streamlit
st.write('Click the button below to extract email IDs with unique keys.')

# Function to extract email IDs with unique keys and save to Excel
def extract_and_save_email_ids():
    try:
        # Read the feedback file into a dataframe
        feedback_data = Feedback_file

        # Group the data by unique values in the key column without aggregating the email IDs
        grouped_data = feedback_data.groupby(['key', 'Email ID']).size().reset_index().drop(0, axis=1)

        # Create a new dataframe with the email IDs and associated unique values in the key column
        new_dataframe = pd.DataFrame({
            'key': grouped_data['key'],
            'email_ids': grouped_data['Email ID']
        })

        # Write the data with email IDs having multiple unique key values to a new Excel sheet
        new_dataframe.to_excel(r"C:\Users\User\Downloads\unique_email_ids_unique_keys.xlsx", index=False)
        st.write('Email IDs with unique values in the unique key column have been saved to unique_email_ids_unique_keys.xlsx')
    except FileNotFoundError:
        st.write("The feedback_file.csv does not exist. Please check the file path.")
    except KeyError:
        st.write("The 'Unique key' column does not exist in the dataset. Please check the column name.")

# Check if the button is clicked
if st.button('Extract Email IDs'):
    extract_and_save_email_ids()  # Call the function to extract and save email IDs


merged_data = email_list
unique_email_data = pd.read_excel(r"C:\Users\User\Downloads\unique_email_ids_unique_keys.xlsx")

# Check if the 'email_ids' column exists in the unique email data
if 'email_ids' in unique_email_data.columns:
    # Convert the merged_data list to a DataFrame
    merged_data_df = pd.DataFrame({'email_ids': merged_data})

    # Filter out emails that are not present in the unique email data
    filtered_emails = merged_data_df[~merged_data_df['email_ids'].isin(unique_email_data['email_ids'])]
    filtered_emails = filtered_emails['email_ids'].unique()

    # Create a select box with the filtered unique email IDs
    selected_email = st.selectbox('Select Email ID:', filtered_emails)
else:
    st.error("The 'email_ids' column does not exist in the unique email data.")


import pandas as pd
import numpy as np

file_path = "namelist.csv"  # Use the CSV file path

try:            
    df = pd.read_csv(file_path)
    print("CSV file loaded successfully.")
except Exception as e:
    print(f"Error loading CSV file: {e}")
    df = pd.DataFrame()

if not df.empty:
    # Strip spaces from column names to avoid KeyError
    df.columns = df.columns.str.strip()

    # Define the six subjects
    subjects = [
        "LINUX",
        "PYTHON",
        "MACHINE LEARNING",
        "JAVA",
        "DATABASE",
    ]

    # Expand the dataset so each student has all six subjects
    expanded_data = []
    for _, row in df.iterrows():
        sl_no = row["Sl. No."]
        name = row["Name"]  # Accessing after stripping spaces
        mail = row["MAIL"]

        for course_id, course in enumerate(subjects, start=101):  # Assign Course ID 101-106
            mark = np.random.randint(30, 100)  # Generate random marks

            # Assign attempt based on marks
            if mark >= 85:
                attempt_id = 1
            elif mark >= 75:
                attempt_id = 2
            elif mark >= 50:
                attempt_id = 3
            else:
                attempt_id = 4

            expanded_data.append({
                "Sl. No.": sl_no,
                "Name": name,
                "MAIL": mail,
                "Course Name": course,
                "Course ID": course_id,
                "Attempt ID": attempt_id,
                "Mark": mark
            })

    expanded_df = pd.DataFrame(expanded_data)

    # Assign grades based on marks
    def assign_grade(mark):
        if mark >= 85:
            return "A"
        elif mark >= 70:
            return "B"
        elif mark >= 50:
            return "C"
        else:
            return "D"

    expanded_df["Grade"] = expanded_df["Mark"].apply(assign_grade)

    # Save the processed dataset
    expanded_df.to_csv("synthetic_data.csv", index=False)
    print("Processed dataset created and saved as 'synthetic_data.csv'")
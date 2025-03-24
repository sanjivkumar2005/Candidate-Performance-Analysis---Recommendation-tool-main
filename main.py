import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Features", page_icon="🚀", layout="wide")

# Sidebar - Feature selection
st.sidebar.title("🚀 Features")
selected_feature = st.sidebar.radio("Select a Feature", [
    "📤 Upload Data",
    "📋 Read Performance Report",
    "💪 Highlight Strengths & Weaknesses",
    "📚 Recommend To-Do Courses",
    "🤝 Pair Poor Performers",
    "📊 Class Performance Dashboard",
    "🔍 Course-Specific Analysis",
    "📤 Export Reports"
])

# Initialize session state
if "df" not in st.session_state:
    st.session_state.df = None

# Function to categorize performance
def categorize_performance(grade):
    if grade in ["A", "B"]:
        return "Good"
    elif grade in ["D", "F"]:
        return "Poor"
    else:
        return "Neutral"

# Function to get course recommendations
def get_Course_Recommendation(course_name):
    recommendations = {
        "LINUX": ["Linux Command Line Basics (Udemy, Coursera)", "Advanced Linux Shell Scripting (Coursera)"],
        "PYTHON": ["Python for Beginners (Udemy, Codecademy)", "Deep Learning with Python (Coursera)"],
        "MACHINE LEARNING": ["Machine Learning by Andrew Ng (Coursera)", "Deep Learning Specialization (Coursera)"],
        "JAVA": ["Java Programming for Beginners (Udemy, Coursera)", "Advanced Java (Coursera)"],
        "DATABASE": ["SQL for Data Science (Coursera, DataCamp)", "The Complete SQL Bootcamp (Udemy)"]
    }
    return recommendations.get(course_name, ["No recommendations available"])

# Main content - Show details based on selected feature
st.title(selected_feature)

if "Upload Data" in selected_feature:
    st.subheader("📤 Upload your data file")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)  # Store in session state
        st.success("File uploaded successfully!")
    
    # Always show dataset if uploaded before
    if st.session_state.df is not None:
        st.write("📊 **Uploaded Dataset Preview:**")
        st.write(st.session_state.df.head())  # Show only the first few rows
    else:
        st.warning("Please upload a dataset.")

elif "Class Performance Dashboard" in selected_feature:
    st.subheader("📊 Class Performance Overview")

    if st.session_state.df is not None:
        if "Grade" in st.session_state.df.columns:
            grade_counts = st.session_state.df["Grade"].value_counts()
            fig, ax = plt.subplots()
            grade_counts.plot(kind="bar", ax=ax, color="skyblue")
            ax.set_title("Grade Distribution")
            ax.set_xlabel("Grades")
            ax.set_ylabel("Number of Students")
            st.pyplot(fig)
        else:
            st.warning("Grade column not found in the dataset!")
    else:
        st.warning("Please upload data first!")

elif "Highlight Strengths & Weaknesses" in selected_feature:
    st.subheader("💪 Identifying Strengths & Weaknesses")

    if st.session_state.df is not None:
        # Ensure required columns exist
        if "Name" in st.session_state.df.columns and "Grade" in st.session_state.df.columns and "Course Name" in st.session_state.df.columns:
            
            # Identify top and weak students
            top_students = st.session_state.df[st.session_state.df["Grade"] == "A"]
            weak_students = st.session_state.df[st.session_state.df["Grade"].isin(["D", "F"])]

            st.write("🏆 **Top Performers:**")
            st.write(top_students[["Name", "Grade"]])

            st.write("⚠️ **Students Needing Improvement:**")
            st.write(weak_students[["Name", "Grade"]])

            # Select a student to analyze
            student_name = st.selectbox("Select a Student to Analyze:", st.session_state.df["Name"].unique())

            # Filter data for the selected student
            student_data = st.session_state.df[st.session_state.df["Name"] == student_name]

            # Identify strong and weak subjects
            strong_subjects = student_data[student_data["Grade"].isin(["A", "B"])]["Course Name"].tolist()
            weak_subjects = student_data[student_data["Grade"].isin(["D", "F"])]["Course Name"].tolist()

            st.write(f"📈 **Strong Subjects for {student_name}:**", strong_subjects if strong_subjects else "None")
            st.write(f"📉 **Weak Subjects for {student_name}:**", weak_subjects if weak_subjects else "None")

        else:
            st.warning("Required columns (Name, Grade, Course Name) not found in the dataset!")

    else:
        st.warning("Please upload data first!")

elif "Course-Specific Analysis" in selected_feature:
    st.subheader("🔍 Course-Specific Performance")

    if st.session_state.df is not None:
        if "Course Name" in st.session_state.df.columns and "Grade" in st.session_state.df.columns:
            selected_course = st.selectbox("Select a Course", st.session_state.df["Course Name"].unique())
            course_data = st.session_state.df[st.session_state.df["Course Name"] == selected_course]
            st.write(course_data)
            
            grade_counts = course_data["Grade"].value_counts()
            fig, ax = plt.subplots()
            grade_counts.plot(kind="bar", ax=ax, color="green")
            ax.set_title(f"Performance in {selected_course}")
            ax.set_xlabel("Grades")
            ax.set_ylabel("Number of Students")
            st.pyplot(fig)
        else:
            st.warning("Required columns (Course Name, Grade) not found in the dataset!")
    else:
        st.warning("Please upload data first!")


elif "Read Performance Report" in selected_feature:
    st.subheader("📋 Viewing Performance Report")
    if st.session_state.df is not None:
        st.write(st.session_state.df.describe())
    else:
        st.warning("Please upload data first!")

elif "Pair Poor Performers" in selected_feature:
    st.subheader("🤝 Pairing Students for Improvement")

    if st.session_state.df is not None:
        if "Name" in st.session_state.df.columns and "Grade" in st.session_state.df.columns:
            st.session_state.df["Performance"] = st.session_state.df["Grade"].apply(categorize_performance)
            
            performance_summary = st.session_state.df.groupby("Name")["Performance"].value_counts().unstack(fill_value=0)
            performance_summary["Category"] = performance_summary.apply(
                lambda row: "Good" if row.get("Good", 0) > row.get("Poor", 0) else (
                    "Poor" if row.get("Poor", 0) > row.get("Good", 0) else "Neutral"
                ),
                axis=1
            )
            
            good_performers = performance_summary[performance_summary["Category"] == "Good"].reset_index()
            poor_performers = performance_summary[performance_summary["Category"] == "Poor"].reset_index()
            
            num_pairs = min(len(good_performers), len(poor_performers))
            pairs = [{"Poor Performer": poor_performers.iloc[i]["Name"], 
                      "Good Performer": good_performers.iloc[i]["Name"]} for i in range(num_pairs)]
            
            pairs_df = pd.DataFrame(pairs)
            st.write("📌 **Student Pairs for Collaboration:**")
            st.write(pairs_df)
        else:
            st.warning("Required columns (Name, Grade) not found in the dataset!")
    else:
        st.warning("Please upload data first!")

elif "Recommend To-Do Courses" in selected_feature:
    st.subheader("📚 Personalized Course Recommendations")
    
    if st.session_state.df is not None:
        if "Name" in st.session_state.df.columns and "Course Name" in st.session_state.df.columns and "Performance" in st.session_state.df.columns:
            st.session_state.df.loc[st.session_state.df["Performance"] == "Poor", "Course Recommendation"] = \
                st.session_state.df.loc[st.session_state.df["Performance"] == "Poor", "Course Name"].apply(get_Course_Recommendation)
            
            st.write(st.session_state.df[st.session_state.df["Performance"] == "Poor"][["Name", "Course Name", "Course Recommendation"]])
        else:
            st.warning("Required columns (Name, Course Name, Performance) not found in the dataset!")
    else:
        st.warning("Please upload data first!")

elif "Export Reports" in selected_feature:
    st.subheader("📤 Export Performance Reports")

    if st.session_state.df is not None:
        # Dropdown to select export type
        export_option = st.radio("Select Export Type:", ["Export All Students", "Export Individual Student"])

        if export_option == "Export Individual Student":
            # Select student name
            student_name = st.selectbox("Select a Student", st.session_state.df["Name"].unique())
            student_data = st.session_state.df[st.session_state.df["Name"] == student_name]

            # Save individual report
            student_filename = f"{student_name}_report.csv"
            student_data.to_csv(student_filename, index=False)
            
            with open(student_filename, "rb") as file:
                st.download_button(f"Download {student_name}'s Report", file, file_name=student_filename, mime="text/csv")

        else:
            # Export full dataset
            full_report_filename = "All_Students_Report.csv"
            st.session_state.df.to_csv(full_report_filename, index=False)
            
            with open(full_report_filename, "rb") as file:
                st.download_button("Download Full Report", file, file_name=full_report_filename, mime="text/csv")

    else:
        st.warning("Please upload data first!")



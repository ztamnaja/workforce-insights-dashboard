import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load data from CSV files
worker_data = pd.read_csv('./data/worker.csv')
bonus_data = pd.read_csv('./data/bonus.csv')
title_data = pd.read_csv('./data/title.csv')

# Data preprocessing
# Merge dataframes to get a comprehensive dataset for analysis
merged_data = pd.merge(worker_data, bonus_data, how="left", left_on="WORKER_ID", right_on="WORKER_REF_ID")
merged_data = pd.merge(merged_data, title_data, how="left", left_on="WORKER_ID", right_on="WORKER_REF_ID")
merged_data['BONUS_DATE'] = pd.to_datetime(merged_data['BONUS_DATE'])
merged_data['JOINING_DATE'] = pd.to_datetime(merged_data['JOINING_DATE'])

print(merged_data.columns)
# Set up Streamlit page configuration
st.set_page_config(page_title="Workforce Dashboard", layout="centered")

# Adding custom HTML to center the page
st.markdown("""
    <style>
        .reportview-container {
            display: flex;
            justify-content: center;
        }
        .main {
            width: 80%;
        }
    </style>
""", unsafe_allow_html=True)

st.title("[DEMO] Workforce Dashboard")

# Tabs for different sections of the dashboard
tab1, tab2, tab3, tab4 = st.tabs(["Key Metrics", "Salary Breakdown", "Bonus Allocation", "Title & Salary Comparison"])

# 1. Key Metrics and KPIs - Tab 1
with tab1:
    st.subheader("Key Metrics and KPIs")
    
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        total_salary = worker_data['SALARY'].sum()
        st.metric(label="Total Salary Expense", value=f"${total_salary:,.2f}")

    with col2:
        avg_salary = worker_data['SALARY'].mean()
        st.metric(label="Average Salary", value=f"${avg_salary:,.2f}")

    with col3:
        highest_salary = worker_data['SALARY'].max()
        st.metric(label="Highest Salary", value=f"${highest_salary:,.2f}")

    with col4:
        num_departments = worker_data['DEPARTMENT'].nunique()
        st.metric(label="Unique Departments", value=f"{num_departments}")
    with col5:
        num_workers = worker_data['WORKER_ID'].nunique()
        st.metric(label="Number of Workers", value=f"{num_workers:,}")
    with col6:
        lowest_salary = worker_data['SALARY'].min()
        st.metric(label="Lowest Salary", value=f"${lowest_salary:,.2f}")

    # Employee Performance (Salary vs Bonus) - Scatter Plot
    fig, ax = plt.subplots()
    sns.scatterplot(data=merged_data, x="SALARY", y="BONUS_AMOUNT", hue="WORKER_TITLE", ax=ax)
    st.pyplot(fig)
    
    # Salary vs Bonus Comparison - Trend Line
    merged_data['DATE'] = pd.to_datetime(merged_data['BONUS_DATE']).dt.to_period('M')
    salary_bonus_time_series = merged_data.groupby('DATE')[['SALARY', 'BONUS_AMOUNT']].sum()
    fig, ax = plt.subplots()
    salary_bonus_time_series.plot(ax=ax)
    st.pyplot(fig)

# 2. Salary Breakdown by Department/Title - Tab 2
with tab2:
    st.subheader("Salary Breakdown Analysis")

    # Salary Summary Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        total_salary = worker_data['SALARY'].sum()
        st.metric(label="Total Salary Expense", value=f"${total_salary:,.2f}")

    with col2:
        avg_salary = worker_data['SALARY'].mean()
        st.metric(label="Average Salary", value=f"${avg_salary:,.2f}")

    with col3:
        highest_salary = worker_data['SALARY'].max()
        st.metric(label="Highest Salary", value=f"${highest_salary:,.2f}")

    # Salary Distribution by Department or Title
    department_title_filter = st.selectbox("Select Distribution Type", options=["Department", "Title", "All"])

    if department_title_filter == "Department":
        department_data = merged_data.groupby('DEPARTMENT')['SALARY'].mean().sort_values(ascending=False)
        st.bar_chart(department_data, use_container_width=True)
        st.write("### Department-wise Average Salary")
        st.dataframe(department_data.reset_index().rename(columns={'DEPARTMENT': 'Department', 'SALARY': 'Average Salary'}))

    elif department_title_filter == "Title":
        title_data = merged_data.groupby('WORKER_TITLE')['SALARY'].mean().sort_values(ascending=False)
        st.bar_chart(title_data, use_container_width=True)
        st.write("### Title-wise Average Salary")
        st.dataframe(title_data.reset_index().rename(columns={'WORKER_TITLE': 'Title', 'SALARY': 'Average Salary'}))

    else:
        all_salary_data = merged_data.groupby(['DEPARTMENT', 'WORKER_TITLE'])['SALARY'].mean().unstack().fillna(0)
        st.write("### Combined Salary Breakdown by Department and Title")
        fig = px.imshow(all_salary_data, title="Salary Breakdown Heatmap", labels=dict(x="Title", y="Department", color="Salary"))
        st.plotly_chart(fig)

    # Salary Trends Over Time
    st.subheader("Salary Trends Over Time")
    salary_trends = merged_data.groupby(merged_data['JOINING_DATE'].dt.to_period('M'))['SALARY'].mean().reset_index()
    salary_trends['JOINING_DATE'] = salary_trends['JOINING_DATE'].dt.to_timestamp()

    fig_trend = px.line(salary_trends, x='JOINING_DATE', y='SALARY', title="Average Salary Over Time", markers=True)
    fig_trend.update_layout(xaxis_title="Date", yaxis_title="Average Salary")
    st.plotly_chart(fig_trend)

    # Top 5 Departments and Titles with Highest Salaries
    st.subheader("Top 5 Departments and Titles with Highest Salaries")

    top_departments = merged_data.groupby('DEPARTMENT')['SALARY'].mean().nlargest(5).reset_index()
    top_titles = merged_data.groupby('WORKER_TITLE')['SALARY'].mean().nlargest(5).reset_index()

    col4, col5 = st.columns(2)

    with col4:
        st.write("### Top 5 Departments by Average Salary")
        fig_top_dept = px.bar(top_departments, x='SALARY', y='DEPARTMENT', orientation='h', title="Top Departments by Average Salary", text='SALARY')
        fig_top_dept.update_layout(xaxis_title="Average Salary", yaxis_title="Department")
        st.plotly_chart(fig_top_dept)

    with col5:
        st.write("### Top 5 Titles by Average Salary")
        fig_top_titles = px.bar(top_titles, x='SALARY', y='WORKER_TITLE', orientation='h', title="Top Titles by Average Salary", text='SALARY')
        fig_top_titles.update_layout(xaxis_title="Average Salary", yaxis_title="Title")
        st.plotly_chart(fig_top_titles)


# 3. Bonus Allocation - Tab 3
with tab3:
    st.subheader("Bonus Distribution Analysis")

    # Bonus Summary Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        total_bonus = bonus_data['BONUS_AMOUNT'].sum()
        st.metric(label="Total Bonus Amount", value=f"${total_bonus:,.2f}")

    with col2:
        avg_bonus_per_worker = bonus_data.groupby('WORKER_REF_ID')['BONUS_AMOUNT'].sum().mean()
        st.metric(label="Average Bonus per Worker", value=f"${avg_bonus_per_worker:,.2f}")

    with col3:
        bonus_count = bonus_data['BONUS_AMOUNT'].count()
        st.metric(label="Total Bonus Transactions", value=f"{bonus_count:,}")

    # Dropdown for selecting "Title" or "Department"
    distribution_filter = st.selectbox("Select Distribution Type", options=["By Title", "By Department"])

    # Bonus Distribution by Title and Department - Pie Chart using Plotly
    bonus_by_title_and_dept = merged_data.groupby(['WORKER_TITLE', 'DEPARTMENT'])['BONUS_AMOUNT'].sum().reset_index()

    if distribution_filter == "By Title":
        fig_title = px.pie(bonus_by_title_and_dept, names='WORKER_TITLE', values='BONUS_AMOUNT', title='Bonus Distribution by Title')
        st.plotly_chart(fig_title)
    elif distribution_filter == "By Department":
        fig_dept = px.pie(bonus_by_title_and_dept, names='DEPARTMENT', values='BONUS_AMOUNT', title='Bonus Distribution by Department')
        st.plotly_chart(fig_dept)

    # Bonus Trends Over Time
    st.subheader("Bonus Trends Over Time")
    bonus_data['BONUS_DATE'] = pd.to_datetime(bonus_data['BONUS_DATE'])
    bonus_trends = bonus_data.groupby(bonus_data['BONUS_DATE'].dt.to_period('M'))['BONUS_AMOUNT'].sum().reset_index()
    bonus_trends['BONUS_DATE'] = bonus_trends['BONUS_DATE'].dt.to_timestamp()

    fig_trend = px.line(bonus_trends, x='BONUS_DATE', y='BONUS_AMOUNT', title="Bonus Amount Over Time", markers=True)
    fig_trend.update_layout(xaxis_title="Date", yaxis_title="Bonus Amount")
    st.plotly_chart(fig_trend)

    # Top 5 Titles and Departments with Highest Bonuses
    st.subheader("Top 5 Titles and Departments with Highest Bonuses")

    top_titles = bonus_by_title_and_dept.groupby('WORKER_TITLE')['BONUS_AMOUNT'].sum().nlargest(5).reset_index()
    top_departments = bonus_by_title_and_dept.groupby('DEPARTMENT')['BONUS_AMOUNT'].sum().nlargest(5).reset_index()

    col4, col5 = st.columns(2)

    with col4:
        st.write("### Top 5 Titles by Bonus")
        fig_top_titles = px.bar(top_titles, x='BONUS_AMOUNT', y='WORKER_TITLE', orientation='h', title="Top Titles by Bonus", text='BONUS_AMOUNT')
        fig_top_titles.update_layout(xaxis_title="Bonus Amount", yaxis_title="Title")
        st.plotly_chart(fig_top_titles)

    with col5:
        st.write("### Top 5 Departments by Bonus")
        fig_top_departments = px.bar(top_departments, x='BONUS_AMOUNT', y='DEPARTMENT', orientation='h', title="Top Departments by Bonus", text='BONUS_AMOUNT')
        fig_top_departments.update_layout(xaxis_title="Bonus Amount", yaxis_title="Department")
        st.plotly_chart(fig_top_departments)


with tab4:
    st.subheader("Insights")

    # Summary Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        unique_titles = merged_data['WORKER_TITLE'].nunique()
        st.metric(label="Unique Titles", value=f"{unique_titles}")

    with col2:
        highest_avg_salary_title = merged_data.groupby('WORKER_TITLE')['SALARY'].mean().idxmax()
        highest_avg_salary = merged_data.groupby('WORKER_TITLE')['SALARY'].mean().max()
        st.metric(label="Highest Avg Salary by Title", value=f"{highest_avg_salary_title} (${highest_avg_salary:,.2f})")

    with col3:
        lowest_avg_salary_title = merged_data.groupby('WORKER_TITLE')['SALARY'].mean().idxmin()
        lowest_avg_salary = merged_data.groupby('WORKER_TITLE')['SALARY'].mean().min()
        st.metric(label="Lowest Avg Salary by Title", value=f"{lowest_avg_salary_title} (${lowest_avg_salary:,.2f})")

    # Distribution of Salaries by Title - Box Plot
    st.write("### Distribution of Salaries by Title")
    fig_salary_dist = px.box(
        merged_data,
        x='WORKER_TITLE',
        y='SALARY',
        title='Salary Distribution by Title',
        labels={'WORKER_TITLE': 'Title', 'SALARY': 'Salary'},
        points="all"
    )
    fig_salary_dist.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig_salary_dist)

    # Titles with Salary & Bonus Insights
    st.write("### Salary and Bonus Comparison by Title")
    salary_bonus_by_title = merged_data.groupby('WORKER_TITLE')[['SALARY', 'BONUS_AMOUNT']].mean().reset_index()
    fig_salary_bonus = px.scatter(
        salary_bonus_by_title,
        x='SALARY',
        y='BONUS_AMOUNT',
        text='WORKER_TITLE',
        title='Salary vs Bonus by Title',
        labels={'SALARY': 'Average Salary', 'BONUS_AMOUNT': 'Average Bonus'},
        size='SALARY',
        color='BONUS_AMOUNT',
    )
    fig_salary_bonus.update_traces(textposition='top center')
    st.plotly_chart(fig_salary_bonus)

    

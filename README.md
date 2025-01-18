# Workforce Insights Dashboard

[![Streamlit App](https://img.shields.io/badge/Streamlit-Launch%20App-green)](https://workforce-insights-dashboard-bmqmxapmepknsgmmsgpivx.streamlit.app/)

## Project for Interview Demo

This project was created as part of the interview process. The primary goal of this project is to showcase my skills in data engineering, in part of building data dashboard.

## Overview

The **Workforce Insights Dashboard** is an interactive analytics tool designed to provide HR teams and executives with actionable insights into employee compensation, bonus distributions, and organizational performance metrics. Built with Python and Streamlit, this dashboard offers an easy-to-use interface for analyzing key workforce data.

---

## Features

### **1. Key Metrics and KPIs**
   - Visualize total salary expenses, average salaries, and workforce demographics.
   - Insights into highest and lowest salaries, number of unique departments, and total workforce size.

### **2. Salary Breakdown**
   - Analyze salary distribution by department or job title.
   - Compare average salaries across departments and titles in an intuitive bar chart.
   - Filter for specific views based on your needs.

### **3. Bonus Allocation**
   - Interactive insights into bonus distribution:
     - **By Title**: Analyze how bonuses are allocated across different job titles.
     - **By Department**: Understand bonus trends within departments.
   - Explore trends and identify gaps in bonus distribution.

### **4. Title & Salary Comparison**
   - Insights into how titles relate to salary distribution.
   - Highlight top-performing roles and departments in terms of average salary and compensation.
   - Drill down to view data specific to titles or departments.

---

## Installation (For Local Deployment)

To run the dashboard locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/workforce-insights-dashboard.git
   cd workforce-insights-dashboard
   
2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt

3. Run the Streamlit app:

    ```bash
    streamlit run app.py
Open your browser and navigate to: http://localhost:8501

### Technology Stack
- Python
- pandas for data manipulation
- plotly and seaborn for visualizations
- Streamlit: Interactive web app framework
- Data: CSV files containing workforce and compensation data
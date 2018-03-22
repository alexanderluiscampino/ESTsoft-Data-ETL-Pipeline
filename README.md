# ESTsoft-Data-Statistics-by-Period
Using Python to create an ETL pipeline for all the Data created daily through the several Webtools available

## Problem
- Data used is not centralized or readily accessible. Weekly wrangling efforts take too much time to gather all the data needed to perform the market analysis and produce insightful recommendations
## Goal
- This project has as a goal to wrangle all the data from the several webtools where it is stored at the moment in a single database 
- Use this database in a web server application to visualize all the data on a  daily, weekly, monthly basis
- Automate creating of data analysis reports

## ETL Pipeline
### Extract
- Use of Python requetss module to extract the data from the several webtools avaialble.

### Transform
- Use of Python library Pandas to transform all the data in a useful form

### Load
- Load the transformed data into CSV file and SQL database so it can be used by an web server application. 

## Web Application Development

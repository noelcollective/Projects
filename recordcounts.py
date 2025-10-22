# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 14:41:47 2021

@author: Noel_R
"""
#The Current Population Survey (CPS), a monthly survey of
#about 60,000 households that the Census Bureau conducts
#for BLS, provides a comprehensive body of information on the
#employment and unemployment experience of the nation’s
#population, classified by age, gender, race, ethnicity, education,
#and a variety of other characteristics. The CPS is the source of data
#on the national unemployment rate; employment by occupation;
# Intro: Working on enhancements to the Manager Validation of CPS Data. This is an
# activity within the Unemployment producion cycle, which examines and verifies the
# data received from Census as it goes through recoding and other slight data 
# mining and manipulation. Since there are security limitations, I cannot
# use the actual Census data, but there may possibily be a way to access
# the data through the platform I use for Python in the future. The data I use
# only has slight variable name and coding differences, so this is a good proxy 
# I am retrieving data that can been extracted through SAS, and will
# being it into Python so that I can work on it. 

#To work with Python, I first have to bring in packages or tools outside of 
# the base packages that Python has built in:
#Change type of python version to 3.11.9 if it doesnt work

#Run install of libraries individually

#  pip install pandas --upgrade 
#  pip install streamlit --upgrade
#  pip install plotly
#  pip install bokeh
#  pip install --upgrade nbformat
#  pip install ipykernel
#  pip install scipy
#  pip install seaborn
#  pip install --upgrade pip
#  pip install venv

#Import different packages
import pandas as pd
import numpy as np
import seaborn as sb
import streamlit as st
import plotly.express as px
import plotly as plt
#import matplotlib.pyplot as plt
#import matplotlib.style as style
#from plotly.subplots import make_subplots
#import plotly.graph_objects as go
import altair as alt
#import plotly.figure_factory as ff


#Establish file location  (fill this out)
file_path = '/mount/src/Projects/'

cps_file = "cpsjan24.csv"

data = pd.read_csv(file_path+cps_file).rename(columns=str.lower)

#Defining what months will be used (fill this out)
current   = 'jan24'
currntmo  = 1
currntyr  = 2024
prevmnth  = 'dec23'
prevmomo  = 12
prevmoyr  = 2023
prevyear  = 'jan23'
prevyrmo  = 1
prevyryr  = 2023         

datavar_list = ["hrhhid2", "hrmonth", "hryear4", "hefaminc", "hwhhwgt", "prunedur",
                "pwcmpwgt", "peio1icd", "prwkstat", "prdthsp", "prpthrs", "peio1cow", "prdasian", 
                "prabsrea", "peeduca", "prsjmj", "perrp", "hrmis", "pepar1typ", "pepar2typ",
                "prtage", "pesex", "ptdtrace", "pepar1", "pepar2", "pemlr"]

#Truncate data to only columns neeeded, located in datavar_list
data1 = data[datavar_list]    

# check first 5 obs and look at descipton o
data1.head()
data1.describe()

count_current = len(data1[(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))])
count_prevmo = len(data1[(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))])
count_prevyr = len(data1[(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))])

st.set_page_config(layout="wide")
st.title('CPS Data Validation Dashboard')
st.subheader('Record counts of the current period compared to previous month and previous year')
st.write("The Current Population Survey, a monthly survey of about 60,000 households that the Census Bureau conducts for BLS, provides a comprehensive body of information on the employment and unemployment experience of the nation’s population, classified by age, gender, race, ethnicity, education, and a variety of other characteristics. The CPS is the source of data for the national unemployment rate and employment by occupation. Click the buttons to the left for frequency counts of a variable")
col1, col2, col3 = st.columns(3)
with col1:
  st.write(f":blue[Number of records in current period {count_current}]")
with col2:
  st.write(f":green[Number of records in previous month: {count_prevmo}]")
with col3:
  st.write(f":red[Number of records in previous year: {count_prevyr}]")

st.divider()

#Create tabes for different parts
choice = st.sidebar.radio(
label = 'Choose CPS variable to analyze',
options = ("prwkstat: FT/ PT Work Status", "peio1cow: Class of Worker", "prdthsp: Detailed Hispanic", "prpthrs: At Work 1-34 Hours", "prdasian: Detailed Asian", 
"prabsrea: Not at work/ Pay Status", "peeduca: Education Level", "prsjmj: Single/ Multi Jobholder", "perrp: Relation to Reference", "pemlr: Labor Force Recode"
"pepar1typ: Type of 1st Parent", "pepar2typ: Type of 2nd Parent", "pesex: Sex", "ptdtrace: Race", "prtage: Age")  
)


# Title: FULL/PART-TIME WORK STATUS------------------------------------------------------------------------------
#Dictionary - FULL/PART-TIME WORK STATUS------------------------------------------------------------------------------
prwkstat_label = {-1: 'N/A', 1: 'NOT IN LABOR FORCE', 2: 'FT HOURS (35+), USUALLY FT', 
                  3: 'PT FOR ECONOMIC REASONS, USUALLY FT', 4: 'PT FOR NON-ECONOMIC REASONS, USUALLY FT', 
                  5: 'NOT AT WORK, USUALLY FT', 6: 'PT HRS, USUALLY PT FOR ECONOMIC REASONS', 
                  7: 'PT HRS, USUALLY PT FOR NON-ECONOMIC REASONS', 
                  8: 'FT HOURS, USUALLY PT FOR ECONOMIC REASONS', 
                  9: 'FT HOURS, USUALLY PT FOR NON-ECONOMIC', 10: 'NOT AT WORK, USUALLY PART-TIME', 
                  11: 'UNEMPLOYED FT', 12: 'UNEMPLOYED PT'}
prwkstat_labels = pd.Series(prwkstat_label).to_frame('label')

#Filtering dataframe for data of current month, prev month, and prev year
prwkstat_current  = data1["prwkstat"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
prwkstat_current["type"] = "current"
prwkstat_prevmnth = data1["prwkstat"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
prwkstat_prevmnth["type"] = "prevmnth"
prwkstat_prevyear = data1["prwkstat"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
prwkstat_prevyear["type"] = "prevyear"
#Creating  a dataframe with different values; axis 1 makes it into multiple columns, axis=0 stacks all the columns on top of each
prwkstat= pd.concat([prwkstat_current, prwkstat_prevmnth, prwkstat_prevyear]).reset_index()

#Creating  a dataframe with different values; axis 1 makes it into multiple columns
prwkstat1_current  = data1["prwkstat"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
prwkstat1_prevmnth = data1["prwkstat"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
prwkstat1_prevyear = data1["prwkstat"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
prwkstat1 = pd.concat([prwkstat_labels, prwkstat1_current, prwkstat1_prevmnth, prwkstat1_prevyear], axis=1).reset_index()

####def a function that can loop through all of these variables....
if choice == "prwkstat: FT/ PT Work Status":
# # Display the dataframe
   st.write("# prwkstat: FT/ PT Work Status")
   st.dataframe(prwkstat1)
   #Validation check compared to Previous Month
   for i in prwkstat_current.index:
    prwkstat_prevmnth_val = abs((0.70*(data1["prwkstat"][(data1["prwkstat"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["prwkstat"][(data1["prwkstat"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prwkstat"][(data1["prwkstat"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
    if prwkstat_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prwkstat = ' + str(i))
   #Validation check compared to Previous Year
   for i in prwkstat_current.index:
    prwkstat_prevyear_val = abs((0.70*(data1["prwkstat"][(data1["prwkstat"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["prwkstat"][(data1["prwkstat"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prwkstat"][(data1["prwkstat"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
    if prwkstat_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous year for prwkstat = ' + str(i))

   st.divider()
  # st.pyplot(g)
   st.bar_chart(data=prwkstat1, x_label="prwkstat codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])
# For testing sb.barplot(x="index", y="current", data=prwkstat1)
# plt.savefig(file_path + "my_seaborn_plot.jpg")
# plt.show()

elif choice == "peio1cow: Class of Worker":
 ## peio1cow: INDIVIDUAL CLASS OF WORKER CODE-------------------------------------------------------------------------
 peio1cow_label = {-1: 'N/A', 1: 'GOVERNMENT - FEDERAL', 2: 'GOVERNMENT - STATE', 
     3: ' GOVERNMENT - LOCAL', 4: ' PRIVATE, FOR PROFIT', 5: ' PRIVATE, NONPROFIT', 
     6: ' SELF-EMPLOYED, INCORPORATED', 7: ' SELF-EMPLOYED, UNINCORPORATED', 
     8: ' WITHOUT PAY'}
 peio1cow_labels = pd.Series(peio1cow_label).to_frame('label')
 #Filtering dataframe for data of current month, prev month, and prev year into one column, axis=0 stacks all the columns on top of each
 peio1cow_current  = data1["peio1cow"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
 peio1cow_current["type"] = "current"
 peio1cow_prevmnth = data1["peio1cow"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
 peio1cow_prevmnth["type"] = "prevmnth"
 peio1cow_prevyear = data1["peio1cow"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
 peio1cow_prevyear["type"] = "prevyear"
 peio1cow= pd.concat([peio1cow_current, peio1cow_prevmnth, peio1cow_prevyear]).reset_index()
 #Creating  a dataframe with different values; axis 1 makes it into multiple columns
 peio1cow1_current  = data1["peio1cow"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
 peio1cow1_prevmnth = data1["peio1cow"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
 peio1cow1_prevyear = data1["peio1cow"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
 peio1cow1 = pd.concat([peio1cow_labels, peio1cow1_current, peio1cow1_prevmnth, peio1cow1_prevyear], axis=1).reset_index()
 # Display the dataframe
 st.write("# peio1cow: Class of Worker")
 st.dataframe(peio1cow1)
  #Validation check compared to Previous Month
 for i in peio1cow_current.index:
   peio1cow_prevmnth_val = abs((0.70*(data1["peio1cow"][(data1["peio1cow"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["peio1cow"][(data1["peio1cow"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["peio1cow"][(data1["peio1cow"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if peio1cow_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for peio1cow = ' + str(i))
   #Validation check compared to Previous Year
 for i in peio1cow_current.index:
   peio1cow_prevyear_val = abs((0.70*(data1["peio1cow"][(data1["peio1cow"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["peio1cow"][(data1["peio1cow"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["peio1cow"][(data1["peio1cow"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if peio1cow_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for peio1cow = ' + str(i))

 st.divider()
 st.bar_chart(data=peio1cow1, x_label="peio1cow codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])

# #DETAILED HISPANIC RECODE---------------------------------------------------------------------
elif choice == "prdthsp: Detailed Hispanic":
 prdthsp_label = {-1: 'NOT LISTED', 1: 'Mexican', 2: 'Puerto Rican', 
     3: 'Cuban', 4: 'Dominican', 5: 'Salvadoran', 
     6: 'Central American', 7: 'South American', 8: 'Other Spanish'}
 prdthsp_labels = pd.Series(prdthsp_label).to_frame('label')

 #Filtering dataframe for data of current month, prev month, and prev year into one column, axis=0 stacks all the columns on top of each
 prdthsp_current  = data1["prdthsp"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
 prdthsp_current["type"] = "current"
 prdthsp_prevmnth = data1["prdthsp"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
 prdthsp_prevmnth["type"] = "prevmnth"
 prdthsp_prevyear = data1["prdthsp"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
 prdthsp_prevyear["type"] = "prevyear"
 prdthsp= pd.concat([prdthsp_current, prdthsp_prevmnth, prdthsp_prevyear]).reset_index()
 #Creating  a dataframe with different values; axis 1 makes it into multiple columns
 prdthsp1_current  = data1["prdthsp"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
 prdthsp1_prevmnth = data1["prdthsp"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
 prdthsp1_prevyear = data1["prdthsp"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
 prdthsp1 = pd.concat([prdthsp_labels, prdthsp1_current, prdthsp1_prevmnth, prdthsp1_prevyear], axis=1).reset_index()
 prdthsp2 = prdthsp1[(prdthsp1["index"]!=-1)]
 
 # Display the dataframe
 st.write("# prdthsp: Detailed Hispanic")
 st.dataframe(prdthsp1)
  #Validation check compared to Previous Month
 for i in prdthsp_current.index:
   prdthsp_prevmnth_val = abs((0.70*(data1["prdthsp"][(data1["prdthsp"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["prdthsp"][(data1["prdthsp"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prdthsp"][(data1["prdthsp"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prdthsp_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prdthsp = ' + str(i))
   #Validation check compared to Previous Year
 for i in prdthsp_current.index:
   prdthsp_prevyear_val = abs((0.70*(data1["prdthsp"][(data1["prdthsp"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["prdthsp"][(data1["prdthsp"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prdthsp"][(data1["prdthsp"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prdthsp_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prdthsp = ' + str(i))

 st.divider()
 st.bar_chart(data=prdthsp1, x_label="prdthsp codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])
 fig1 = px.pie(prdthsp2, values='current', names='label', title="Hispanic Breakout for Current Month")
 fig2 = px.pie(prdthsp2, values='prevmo', names='label', title="Hispanic Breakout for Previous Month")
 fig3 = px.pie(prdthsp2, values='prevyr', names='label', title="Hispanic Breakout for Previous Year")
 col1, col2, col3 = st.columns(3)
 with col1:
  st.plotly_chart(fig1)
 with col2:
  st.plotly_chart(fig2)
 with col3:
  st.plotly_chart(fig3)
 

elif choice == "prpthrs: At Work 1-34 Hours":
 prpthrs_label = {-1: 'N/A', 0: 'FT, PT Non-Econ Reasons', 1: 'FT, PT 1-4 Hrs', 2: 'FT, PT 5-14 Hrs', 
     3: 'FT, PT 15-29 Hrs', 4: 'FT, PT 30-34 Hrs', 5: 'PT Econ Reasons, PT 1-4 Hrs', 
     6: 'PT Econ Reasons', 7: 'PT Econ Reasons, PT 15-29 Hrs', 8: 'PT Econ Reasons, PT 30-34 Hrs',
     9: 'PT Non-Econ Reasons, PT 1-4 Hrs', 10: 'PT Non-Econ Reasons, PT 5-14 Hrs', 
     11: 'PT Non-Econ Reasons, PT 15-29 Hrs', 12: 'PT Non-Econ Reasons PT 30-34 Hrs'}
 prpthrs_labels = pd.Series(prpthrs_label).to_frame('label')
 
 #Filtering dataframe for data of current month, prev month, and prev year into one column, axis=0 stacks all the columns on top of each
 prpthrs_current  = data1["prpthrs"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
 prpthrs_current["type"] = "current"
 prpthrs_prevmnth = data1["prpthrs"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
 prpthrs_prevmnth["type"] = "prevmnth"
 prpthrs_prevyear = data1["prpthrs"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
 prpthrs_prevyear["type"] = "prevyear"
 prpthrs= pd.concat([prpthrs_current, prpthrs_prevmnth, prpthrs_prevyear]).reset_index()
 
 #Creating  a dataframe with different values; axis 1 makes it into multiple columns
 prpthrs1_current  = data1["prpthrs"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
 prpthrs1_prevmnth = data1["prpthrs"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
 prpthrs1_prevyear = data1["prpthrs"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
 prpthrs1 = pd.concat([prpthrs_labels, prpthrs1_current, prpthrs1_prevmnth, prpthrs1_prevyear], axis=1).reset_index()
 prpthrs2 = prpthrs1[(prpthrs1["index"]!=-1)]
 
 #Display the dataframe
 st.write("# prpthrs: At work 1-34 Hours")
 st.dataframe(prpthrs1)
  #Validation check compared to Previous Month
 for i in prpthrs_current.index:
   prpthrs_prevmnth_val = abs((0.70*(data1["prpthrs"][(data1["prpthrs"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["prpthrs"][(data1["prpthrs"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prpthrs"][(data1["prpthrs"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prpthrs_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prpthrs = ' + str(i))
   #Validation check compared to Previous Year
 for i in prpthrs_current.index:
   prpthrs_prevyear_val = abs((0.70*(data1["prpthrs"][(data1["prpthrs"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["prpthrs"][(data1["prpthrs"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prpthrs"][(data1["prpthrs"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prpthrs_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prpthrs = ' + str(i))

 st.divider()
 st.bar_chart(data=prpthrs2, x_label="prpthrs codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])
 fig1 = px.pie(prpthrs2, values='current', names='label', title="34 hours Breakout for Current Month")
 fig2 = px.pie(prpthrs2, values='prevmo', names='label', title="34 hours Breakout for Previous Month")
 fig3 = px.pie(prpthrs2, values='prevyr', names='label', title="34 hours Breakout for Previous Year")
 col1, col2, col3 = st.columns(3)
 with col1:
  st.plotly_chart(fig1)
 with col2:
  st.plotly_chart(fig2)
 with col3:
  st.plotly_chart(fig3)

# DETAILED ASIAN RECODE------------------------------------------------------------------------
elif choice == "prdasian: Detailed Asian":
 prdasian_label = {-1: 'N/A', 1: 'Asian Indian', 2: 'Chinese', 3: 'Filipino', 4: 'Japanese', 5: 'Korean', 6: 'Vietnamese', 7: 'Other'}
 prdasian_labels = pd.Series(prdasian_label).to_frame('label')

 #Filtering dataframe for data of current month, prev month, and prev year into one column, axis=0 stacks all the columns on top of each
 prdasian_current  = data1["prdasian"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
 prdasian_current["type"] = "current"
 prdasian_prevmnth = data1["prdasian"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
 prdasian_prevmnth["type"] = "prevmnth"
 prdasian_prevyear = data1["prdasian"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
 prdasian_prevyear["type"] = "prevyear"
 prdasian= pd.concat([prdasian_current, prdasian_prevmnth, prdasian_prevyear]).reset_index()
 #Creating  a dataframe with different values; axis 1 makes it into multiple columns
 prdasian1_current  = data1["prdasian"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
 prdasian1_prevmnth = data1["prdasian"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
 prdasian1_prevyear = data1["prdasian"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
 prdasian1 = pd.concat([prdasian_labels, prdasian1_current, prdasian1_prevmnth, prdasian1_prevyear], axis=1).reset_index()
 prdasian2 = prdasian1[(prdasian1["index"]!=-1)]
  #Display the dataframe
 st.write("# prdasian: Detailed Asian")
 st.dataframe(prdasian1)
  #Validation check compared to Previous Month
 for i in prdasian_current.index:
   prdasian_prevmnth_val = abs((0.70*(data1["prdasian"][(data1["prdasian"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["prdasian"][(data1["prdasian"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prdasian"][(data1["prdasian"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prdasian_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prdasian = ' + str(i))
   #Validation check compared to Previous Year
 for i in prdasian_current.index:
   prdasian_prevyear_val = abs((0.70*(data1["prdasian"][(data1["prdasian"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["prdasian"][(data1["prdasian"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prdasian"][(data1["prdasian"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prdasian_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prdasian = ' + str(i))

   st.divider()
   st.bar_chart(data=prdasian1, x_label="prdasian codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])
   fig1 = px.pie(prdasian2, values='current', names='label', title="Asian Breakout for Current Month")
   fig2 = px.pie(prdasian2, values='prevmo', names='label', title="Asian Breakout for Previous Month")
   fig3 = px.pie(prdasian2, values='prevyr', names='label', title="Asian Breakout for Previous Year")
 col1, col2, col3 = st.columns(3)
 with col1:
   st.plotly_chart(fig1)
 with col2:
   st.plotly_chart(fig2)
 with col3:
   st.plotly_chart(fig3)

# #PRABSREA REASON NOT AT WORK AND PAY STATUS-------------------------------------------------
elif choice == "prabsrea: Not at work/ Pay Status":
 prabsrea_label = {1 : 'FT paid-vacation', 2 : 'FT paid-own illness', 3 : 'FT paid child care problems', 4 : 'FT paid-other family/personal oblig.', 
5 : 'FT paid-maternity/paternity leave', 6 : 'FT paid-labor dispute', 7 : 'FT paid-weather affected job', 8 : 'FT paid-school/training', 
9 : 'FT paid-civic/military duty', 10: 'FT paid-other', 11: 'FT unpaid-vacation', 12: 'FT unpaid-own illness', 13: 'FT unpaid-child care problems', 
14: 'FT unpaid-other fam/personal obligation', 15: 'FT unpaid-maternity/paternity leave', 16: 'FT unpaid-labor dispute', 17: 'FT unpaid-weather affected job', 
18: 'FT unpaid-school/training', 19: 'FT unpaid-civic/military duty', 20: 'FT unpaid-other', 21: 'PT paid-vacation', 22: 'PT paid-own illness', 
23: 'PT paid-child care problems', 24: 'PT paid-other family/personal oblig.', 25: 'PT paid-maternity/paternity leave', 26: 'PT paid-labor dispute', 
27: 'PT paid-weather affected job', 28: 'PT paid-school/training', 29: 'PT paid-civic/military duty', 30: 'PT paid-other', 31: 'PT unpaid-vacation', 
32: 'PT unpaid-own illness', 33: 'PT unpaid-child care problems', 34: 'PT unpaid-other fam/personal obligation', 35: 'PT unpaid-maternity/paternity leave', 
36: 'PT unpaid-labor dispute', 37: 'PT unpaid-weather affected job', 38: 'PT unpaid-school/training', 39: 'PT unpaid-civic/military duty', 40: 'PT unpaid-other' 
}
 prabsrea_labels = pd.Series(prabsrea_label).to_frame('label')

 #Filtering dataframe for data of current month, prev month, and prev year into one column, axis=0 stacks all the columns on top of each
 prabsrea_current  = data1["prabsrea"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
 prabsrea_current["type"] = "current"
 prabsrea_prevmnth = data1["prabsrea"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
 prabsrea_prevmnth["type"] = "prevmnth"
 prabsrea_prevyear = data1["prabsrea"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
 prabsrea_prevyear["type"] = "prevyear"
 prabsrea= pd.concat([prabsrea_current, prabsrea_prevmnth, prabsrea_prevyear]).reset_index()
 #Creating  a dataframe with different values; axis 1 makes it into multiple columns
 prabsrea1_current  = data1["prabsrea"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
 prabsrea1_prevmnth = data1["prabsrea"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
 prabsrea1_prevyear = data1["prabsrea"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
 prabsrea1 = pd.concat([prabsrea_labels, prabsrea1_current, prabsrea1_prevmnth, prabsrea1_prevyear], axis=1).reset_index()
  #Display the dataframe
 st.write("# prabsrea: Not at work/ Pay Status")
 st.dataframe(prabsrea1)
  #Validation check compared to Previous Month
 for i in prabsrea_current.index:
   prabsrea_prevmnth_val = abs((0.70*(data1["prabsrea"][(data1["prabsrea"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["prabsrea"][(data1["prabsrea"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prabsrea"][(data1["prabsrea"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prabsrea_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prabsrea = ' + str(i))
   #Validation check compared to Previous Year
 for i in prabsrea_current.index:
   prabsrea_prevyear_val = abs((0.70*(data1["prabsrea"][(data1["prabsrea"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["prabsrea"][(data1["prabsrea"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prabsrea"][(data1["prabsrea"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prabsrea_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prabsrea = ' + str(i))

   st.divider()
   st.bar_chart(data=prabsrea1, x_label="prabsrea codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])


# #PEEDUCA HIGHEST LEVEL OF SCHOOL COMPLETED OR DEGREE RECEIVED-----------------------------------------------------------

elif choice == "peeduca: Education Level":
 peeduca_label = {31: 'LESS THAN 1ST GRADE', 32: ' 1ST, 2ND, 3RD OR 4TH GRADE', 33: ' 5TH OR 6TH GRADE', 34: '7TH OR 8TH GRADE', 35: ' 9TH GRADE', 
                 36: '10TH GRADE', 37: '11TH GRADE', 38: '12TH GRADE NO DIPLOMA', 39: 'HIGH SCHOOL GRAD-DIPLOMA OR EQUIV (GED)', 
                 40: 'SOME COLLEGE BUT NO DEGREE', 41: 'ASSOCIATE DEGREE-OCCUPATIONAL/VOCATIONAL', 42: ' ASSOCIATE DEGREE-ACADEMIC PROGRAM', 
                 43: 'BACHELORS DEGREE (EX: BA, AB, BS)', 44: ' MASTERS DEGREE (EX: MA, MS, MEng, MEd, MSW)', 45: ' PROFESSIONAL SCHOOL DEG (EX: MD, DDS, DVM)', 
                 46: ' DOCTORATE DEGREE (EX: PhD, EdD)'} 
 peeduca_labels = pd.Series(peeduca_label).to_frame('label')

 #Filtering dataframe for data of current month, prev month, and prev year into one column, axis=0 stacks all the columns on top of each
 peeduca_current  = data1["peeduca"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
 peeduca_current["type"] = "current"
 peeduca_prevmnth = data1["peeduca"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
 peeduca_prevmnth["type"] = "prevmnth"
 peeduca_prevyear = data1["peeduca"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
 peeduca_prevyear["type"] = "prevyear"
 peeduca= pd.concat([peeduca_current, peeduca_prevmnth, peeduca_prevyear]).reset_index()
 #Creating  a dataframe with different values; axis 1 makes it into multiple columns
 peeduca1_current  = data1["peeduca"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
 peeduca1_prevmnth = data1["peeduca"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
 peeduca1_prevyear = data1["peeduca"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
 peeduca1 = pd.concat([peeduca_labels, peeduca1_current, peeduca1_prevmnth, peeduca1_prevyear], axis=1).reset_index()
 peeduca2 = peeduca1[(peeduca1["index"]!=-1)]
  #Display the dataframe
 st.write("# peeduca: Education Level")
 st.dataframe(peeduca1)
  #Validation check compared to Previous Month
 for i in peeduca_current.index:
   peeduca_prevmnth_val = abs((0.70*(data1["peeduca"][(data1["peeduca"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["peeduca"][(data1["peeduca"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["peeduca"][(data1["peeduca"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if peeduca_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for peeduca = ' + str(i))
   #Validation check compared to Previous Year
 for i in peeduca_current.index:
   peeduca_prevyear_val = abs((0.70*(data1["peeduca"][(data1["peeduca"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["peeduca"][(data1["peeduca"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["peeduca"][(data1["peeduca"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if peeduca_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for peeduca = ' + str(i))

   st.divider()
   st.bar_chart(data=peeduca1, x_label="peeduca codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])
   fig1 = px.pie(peeduca2, values='current', names='label', title="Education Level Breakout for Current Month")
   fig2 = px.pie(peeduca2, values='prevmo', names='label', title="Education Level Breakout for Previous Month")
   fig3 = px.pie(peeduca2, values='prevyr', names='label', title="Education Level Breakout for Previous Year")
 col1, col2, col3 = st.columns(3)
 with col1:
   st.plotly_chart(fig1)
 with col2:
   st.plotly_chart(fig2)
 with col3:
   st.plotly_chart(fig3)


# #PRSJMJ SINGLE/MULTIPLE JOBHOLDER RECODE------------------------------------------------------------------------------------
# PRSJMJ_label = ['-1 N/A', '1 SINGLE JOBHOLDER', '2 MULTIPLE JOBHOLDER']
elif choice == "prsjmj: Single/ Multi Jobholder":
 prsjmj_label = {-1: 'N/A', 1: 'SINGLE JOBHOLDER', 2: 'MULTIPLE JOBHOLDER'} 
 prsjmj_labels = pd.Series(prsjmj_label).to_frame('label')

 #Filtering dataframe for data of current month, prev month, and prev year into one column, axis=0 stacks all the columns on top of each
 prsjmj_current  = data1["prsjmj"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
 prsjmj_current["type"] = "current"
 prsjmj_prevmnth = data1["prsjmj"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
 prsjmj_prevmnth["type"] = "prevmnth"
 prsjmj_prevyear = data1["prsjmj"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
 prsjmj_prevyear["type"] = "prevyear"
 prsjmj= pd.concat([prsjmj_current, prsjmj_prevmnth, prsjmj_prevyear]).reset_index()
 #Creating  a dataframe with different values; axis 1 makes it into multiple columns
 prsjmj1_current  = data1["prsjmj"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
 prsjmj1_prevmnth = data1["prsjmj"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
 prsjmj1_prevyear = data1["prsjmj"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
 prsjmj1 = pd.concat([prsjmj_labels, prsjmj1_current, prsjmj1_prevmnth, prsjmj1_prevyear], axis=1).reset_index()
 prsjmj2 = prsjmj1[(prsjmj1["index"]!=-1)]
  #Display the dataframe
 st.write("# prsjmj: Single/ Multi Jobholder")
 st.dataframe(prsjmj1)
  #Validation check compared to Previous Month
 for i in prsjmj_current.index:
   prsjmj_prevmnth_val = abs((0.70*(data1["prsjmj"][(data1["prsjmj"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["prsjmj"][(data1["prsjmj"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prsjmj"][(data1["prsjmj"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prsjmj_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prsjmj = ' + str(i))
   #Validation check compared to Previous Year
 for i in prsjmj_current.index:
   prsjmj_prevyear_val = abs((0.70*(data1["prsjmj"][(data1["prsjmj"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["prsjmj"][(data1["prsjmj"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["prsjmj"][(data1["prsjmj"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if prsjmj_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for prsjmj = ' + str(i))

   st.divider()
   st.bar_chart(data=prsjmj1, x_label="prsjmj codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])
   fig1 = px.pie(prsjmj2, values='current', names='label', title="Jobholder Breakout for Current Month")
   fig2 = px.pie(prsjmj2, values='prevmo', names='label', title="Jobholder Breakout for Previous Month")
   fig3 = px.pie(prsjmj2, values='prevyr', names='label', title="Jobholder Breakout for Previous Year")
 col1, col2, col3 = st.columns(3)
 with col1:
   st.plotly_chart(fig1)
 with col2:
   st.plotly_chart(fig2)
 with col3:
   st.plotly_chart(fig3)
                        

# #PERRP RELATIONSHIP TO REFERENCE PERSON--------------------------------------------------                
elif choice == "perrp: Relation to Reference":
 perrp_label = {40: 'REFERENCE PERSON W/RELS.', 41: 'REFERENCE PERSON W/O RELS.', 42: 'OPPOSITE SEX SPOUSE', 
43: 'OPPOSITE SEX PARTNER WITH RELATIVES', 44: 'OPPOSITE SEC PARTNER WITHOUT RELATIVES', 
45: 'SAME SEX SPOUSE', 46: 'SAME SEX PARTNER WITH RELATIVES', 47: 'SAME SEX PARTNER WITHOUT RELATIVES', 
48: 'CHILD', 49: 'GRANDCHILD', 50: 'PARENT', 51: 'BROTHER/SISTER', 52: 'OTHER REL. OR REF. PERSON', 
53: 'FOSTER CHILD', 54: 'HOUSEMATE/ROOMMATE W/RELS.', 55: ' HOUSEMATE/ROOMMATEW/O RELS.', 
56: 'ROOMER/BOARDER W/RELS.', 57: 'ROOMER/BOARDER W/OUT RELS.', 58: 'NONRELATIVE OF REFERENCE PERSON W/RELS.', 
59: 'NONRELATIVE OF REFERENCE PERSON W/OUT RELS.'} 
 perrp_labels = pd.Series(perrp_label).to_frame('label')

 #Filtering dataframe for data of current month, prev month, and prev year into one column, axis=0 stacks all the columns on top of each
 perrp_current  = data1["perrp"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
 perrp_current["type"] = "current"
 perrp_prevmnth = data1["perrp"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
 perrp_prevmnth["type"] = "prevmnth"
 perrp_prevyear = data1["perrp"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
 perrp_prevyear["type"] = "prevyear"
 perrp= pd.concat([perrp_current, perrp_prevmnth, perrp_prevyear]).reset_index()
 #Creating  a dataframe with different values; axis 1 makes it into multiple columns
 perrp1_current  = data1["perrp"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
 perrp1_prevmnth = data1["perrp"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
 perrp1_prevyear = data1["perrp"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
 perrp1 = pd.concat([perrp_labels, perrp1_current, perrp1_prevmnth, perrp1_prevyear], axis=1).reset_index()
 perrp2 = perrp1[(perrp1["index"]!=-1)]
  #Display the dataframe
 st.write("# perrp: Relation to Reference")
 st.dataframe(perrp1)
  #Validation check compared to Previous Month
 for i in perrp_current.index:
   perrp_prevmnth_val = abs((0.70*(data1["perrp"][(data1["perrp"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["perrp"][(data1["perrp"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["perrp"][(data1["perrp"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if perrp_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for perrp = ' + str(i))
   #Validation check compared to Previous Year
 for i in perrp_current.index:
   perrp_prevyear_val = abs((0.70*(data1["perrp"][(data1["perrp"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["perrp"][(data1["perrp"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["perrp"][(data1["perrp"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if perrp_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for perrp = ' + str(i))

   st.divider()
   st.bar_chart(data=perrp1, x_label="perrp codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])
   fig1 = px.pie(perrp2, values='current', names='label', title="Relation Reference Breakout for Current Month")
   fig2 = px.pie(perrp2, values='prevmo', names='label', title="Relation Reference Breakout for Previous Month")
   fig3 = px.pie(perrp2, values='prevyr', names='label', title="Relation Reference Breakout for Previous Year")
 col1, col2, col3 = st.columns(3)
 with col1:
   st.plotly_chart(fig1)
 with col2:
   st.plotly_chart(fig2)
 with col3:
   st.plotly_chart(fig3)

   plotly_chart(fig3)

# #PEPAR1TYP: TYPE OF SECOND PARENT-------------------------------------------------------------
# PEPAR1TYP_label = ['-1 NO PEPAR1 PRESENT', '01 BIOLOGICAL', '02 STEP','03 ADOPTED']

# w=4
# bar1 = np.arange(len(PEPAR1TYP_label))
# bar2 = [i+w for i in bar1]
# bar3 = [i+w for i in bar2]

# #Filtering dataframe for data of current month, prev month, and prev year
# PEPAR1TYP_current  = data1["PEPAR1TYP"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().sort_index()
# PEPAR1TYP_prevmnth = data1["PEPAR1TYP"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().sort_index()
# PEPAR1TYP_prevyear = data1["PEPAR1TYP"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().sort_index()

# #Validation check compared to Previous Month
# for i in PEPAR1TYP_current.index:
#     PEPAR1TYP_prevmnth_val = (.85*(data1["PEPAR1TYP"][(data1["PEPAR1TYP"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum())) <= (data1["PEPAR1TYP"][(data1["PEPAR1TYP"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PEPAR1TYP"][(data1["PEPAR1TYP"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum()))              
#     if PEPAR1TYP_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous month for PEPAR1TYP = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous month for PEPAR1TYP = ' + str(i))

# #Validation check compared to Previous Year
# for i in PEPAR1TYP_current.index:
#     PEPAR1TYP_prevyear_val = (.85*(data1["PEPAR1TYP"][(data1["PEPAR1TYP"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum())) <= (data1["PEPAR1TYP"][(data1["PEPAR1TYP"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PEPAR1TYP"][(data1["PEPAR1TYP"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum()))              
#     if PEPAR1TYP_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous year for PEPAR1TYP = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous year for PEPAR1TYP = ' + str(i))
# a = ['-1 NO PEPAR1 PRESENT', '01 BIOLOGICAL', '02 STEP', '03 ADOPTED', '-1 NO PEPAR1 PRESENT', '01 BIOLOGICAL', '02 STEP', '03 ADOPTED', '-1 NO PEPAR1 PRESENT', '01 BIOLOGICAL', '02 STEP', '03 ADOPTED']
# b = np.arange(len(a))
# #Visual graphs
# plt.rcParams['font.size'] = '8'
# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["figure.titlesize"] = '25'
# style.use('dark_background')
# plt.suptitle("PEPAR1TYP: TYPE OF SECOND PARENT")
# plt.bar(bar1, PEPAR1TYP_current, 0.75, color = 'red', label="Current")
# plt.bar(bar2, PEPAR1TYP_prevmnth, 0.75, color = 'blue', label="Prev Month")
# plt.bar(bar3, PEPAR1TYP_prevyear, 0.75, color = 'green', label="Prev Year")
# plt.legend(loc="upper left", ncol=3)
# plt.xticks(b, a, rotation=-80)
# plt.show()  


# #PEPAR2TYP: TYPE OF FIRST PARENT-----------------------------------------------------------
# PEPAR2TYP_label = ['-1 NO PEPAR1 PRESENT', '01 BIOLOGICAL', '02 STEP','03 ADOPTED']
# w=4
# bar1 = np.arange(len(PEPAR2TYP_label))
# bar2 = [i+w for i in bar1]
# bar3 = [i+w for i in bar2]

# #Filtering dataframe for data of current month, prev month, and prev year
# PEPAR2TYP_current  = data1["PEPAR2TYP"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().sort_index()
# PEPAR2TYP_prevmnth = data1["PEPAR2TYP"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().sort_index()
# PEPAR2TYP_prevyear = data1["PEPAR2TYP"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().sort_index()

# #Validation check compared to Previous Month
# for i in PEPAR2TYP_current.index:
#     PEPAR2TYP_prevmnth_val = (.85*(data1["PEPAR2TYP"][(data1["PEPAR2TYP"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum())) <= (data1["PEPAR2TYP"][(data1["PEPAR2TYP"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PEPAR2TYP"][(data1["PEPAR2TYP"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum()))              
#     if PEPAR2TYP_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous month for PEPAR2TYP = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous month for PEPAR2TYP = ' + str(i))

# #Validation check compared to Previous Year
# for i in PEPAR2TYP_current.index:
#     PEPAR2TYP_prevyear_val = (.85*(data1["PEPAR2TYP"][(data1["PEPAR2TYP"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum())) <= (data1["PEPAR2TYP"][(data1["PEPAR2TYP"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PEPAR2TYP"][(data1["PEPAR2TYP"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum()))              
#     if PEPAR2TYP_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous year for PEPAR2TYP = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous year for PEPAR2TYP = ' + str(i))
# a = ['-1 NO PEPAR1 PRESENT', '01 BIOLOGICAL', '02 STEP', '03 ADOPTED', '-1 NO PEPAR1 PRESENT', '01 BIOLOGICAL', '02 STEP', '03 ADOPTED', '-1 NO PEPAR1 PRESENT', '01 BIOLOGICAL', '02 STEP', '03 ADOPTED']
# b = np.arange(len(a))
# #Visual graphs
# plt.rcParams['font.size'] = '8'
# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["figure.titlesize"] = '25'
# style.use('dark_background')
# plt.suptitle("PEPAR2TYP: TYPE OF FIRST PARENT")
# plt.bar(bar1, PEPAR2TYP_current, 0.75, color = 'red', label="Current")
# plt.bar(bar2, PEPAR2TYP_prevmnth, 0.75, color = 'blue', label="Prev Month")
# plt.bar(bar3, PEPAR2TYP_prevyear, 0.75, color = 'green', label="Prev Year")
# plt.legend(loc="upper left", ncol=3)
# plt.xticks(b, a, rotation=-80)
# plt.show()  
               
              
            
# #PEMLR MONTHLY LABOR FORCE RECODE 
elif choice == "pemlr: Labor Force Recode":
 pemlr_label = {1: 'EMPLOYED-AT WORK', 2: 'EMPLOYED-ABSENT', 3: 'UNEMPLOYED-ON LAYOFF', 4: 'UNEMPLOYED-LOOKING', 
                5: 'NOT IN LABOR FORCE-RETIRED', 6: 'NOT IN LABOR FORCE-DISABLED', 7: 'NOT IN LABOR FORCE-OTHER'} 
 pemlr_labels = pd.Series(perrp_label).to_frame('label')

 #Filtering dataframe for data of current month, prev month, and prev year into one column, axis=0 stacks all the columns on top of each
 pemlr_current  = data1["pemlr"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('count').sort_index()
 pemlr_current["type"] = "current"
 pemlr_prevmnth = data1["pemlr"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('count').sort_index()
 pemlr_prevmnth["type"] = "prevmnth"
 pemlr_prevyear = data1["pemlr"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('count').sort_index()
 pemlr_prevyear["type"] = "prevyear"
 pemlr= pd.concat([pemlr_current, pemlr_prevmnth, pemlr_prevyear]).reset_index()
 #Creating  a dataframe with different values; axis 1 makes it into multiple columns
 pemlr1_current  = data1["pemlr"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().to_frame('current').sort_index()
 pemlr1_prevmnth = data1["pemlr"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().to_frame('prevmo').sort_index()
 pemlr1_prevyear = data1["pemlr"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().to_frame('prevyr').sort_index()
 pemlr1 = pd.concat([pemlr_labels, pemlr1_current, pemlr1_prevmnth, pemlr1_prevyear], axis=1).reset_index()
 pemlr2 = pemlr1[(pemlr1["index"]!=-1)]
  #Display the dataframe
 st.write("# pemlr: Labor Force Recode")
 st.dataframe(pemlr1)
  #Validation check compared to Previous Month
 for i in pemlr_current.index:
   pemlr_prevmnth_val = abs((0.70*(data1["pemlr"][(data1["pemlr"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count()))) <= abs(data1["pemlr"][(data1["pemlr"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["pemlr"][(data1["pemlr"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if pemlr_prevmnth_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for pemlr = ' + str(i))
   #Validation check compared to Previous Year
 for i in pemlr_current.index:
   pemlr_prevyear_val = abs((0.70*(data1["pemlr"][(data1["pemlr"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].count()))) <= abs(data1["pemlr"][(data1["pemlr"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].count()) <= abs((1.30*(data1["pemlr"][(data1["pemlr"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].count())))              
   if pemlr_prevyear_val == False:
      st.write('Value NOT within 30% data validation threshhold of previous month for pemlr = ' + str(i))

   st.divider()
   st.bar_chart(data=pemlr1, x_label="pemlr codes", x="index", y_label="No. of records by Month", y=["current", "prevmo", "prevyr"], stack=False, color=["#0000FF", "#00FF00", "#FF0000"])
   fig1 = px.pie(pemlr2, values='current', names='label', title="Labor Force Recode for Current Month")
   fig2 = px.pie(pemlr2, values='prevmo', names='label', title="Labor Force Recode for Previous Month")
   fig3 = px.pie(pemlr2, values='prevyr', names='label', title="Labor Force Recode for Previous Year")
 col1, col2, col3 = st.columns(3)
 with col1:
   st.plotly_chart(fig1)
 with col2:
   st.plotly_chart(fig2)
 with col3:
   st.plotly_chart(fig3)
# #Filtering dataframe for data of current month, prev month, and prev year
# PEMLR_current  = data1["PEMLR"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().sort_index()
# PEMLR_prevmnth = data1["PEMLR"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().sort_index()
# PEMLR_prevyear = data1["PEMLR"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().sort_index()

# #Validation check compared to Previous Month
# for i in PEMLR_current.index:
#     PEMLR_prevmnth_val = (.85*(data1["PEMLR"][(data1["PEMLR"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum())) <= (data1["PEMLR"][(data1["PEMLR"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PEMLR"][(data1["PEMLR"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum()))              
#     if PEMLR_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous month for PEMLR = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous month for PEMLR = ' + str(i))

# #Validation check compared to Previous Year
# for i in PEMLR_current.index:
#     PEMLR_prevyear_val = (.85*(data1["PEMLR"][(data1["PEMLR"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum())) <= (data1["PEMLR"][(data1["PEMLR"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PEMLR"][(data1["PEMLR"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum()))              
#     if PEMLR_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous year for PEMLR = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous year for PEMLR = ' + str(i))

# #Visual graphs
# plt.rcParams['font.size'] = '30'
# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["axes.labelweight"] = "bold"
# plt.rcParams["figure.titlesize"] = '50'
# style.use('dark_background')
# fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(40,20))
# plt.suptitle("PEMLR: MONTHLY LABOR FORCE RECODE")
# ax1.barh(PEMLR_label, PEMLR_current, color = 'red')
# ax1.set_title("Current")
# ax2.barh(PEMLR_label, PEMLR_prevmnth, color = 'blue')
# ax2.set_title("Prev Month")
# ax2.get_yaxis().set_visible(False)
# ax3.barh(PEMLR_label, PEMLR_prevyear, color = 'green')
# ax3.set_title("Prev Year")
# ax3.get_yaxis().set_visible(False)
# plt.show()     
                    

# #PESEX--------------------------------------------------------------------------------------
# PESEX_label = ['1 MALE', '2 FEMALE']
# w=2
# bar1 = np.arange(len(PESEX_label))
# bar2 = [i+w for i in bar1]
# bar3 = [i+w for i in bar2]

# #Filtering dataframe for data of current month, prev month, and prev year
# PESEX_current  = data1["PESEX"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().sort_index()
# PESEX_prevmnth = data1["PESEX"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().sort_index()
# PESEX_prevyear = data1["PESEX"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().sort_index()

# #Validation check compared to Previous Month
# for i in PESEX_current.index:
#     PESEX_prevmnth_val = (.85*(data1["PESEX"][(data1["PESEX"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum())) <= (data1["PESEX"][(data1["PESEX"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PESEX"][(data1["PESEX"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum()))              
#     if PESEX_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous month for PESEX = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous month for PESEX = ' + str(i))

# #Validation check compared to Previous Year
# for i in PESEX_current.index:
#     PESEX_prevyear_val = (.85*(data1["PESEX"][(data1["PESEX"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum())) <= (data1["PESEX"][(data1["PESEX"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PESEX"][(data1["PESEX"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum()))              
#     if PESEX_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous year for PESEX = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous year for PESEX = ' + str(i))

# #Visual graphs
# a = ['1 MALE', '2 FEMALE', '1 MALE', '2 FEMALE', '1 MALE', '2 FEMALE']
# b = np.arange(len(a))
# plt.rcParams['font.size'] = '8'
# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["figure.titlesize"] = '25'
# style.use('dark_background')
# plt.suptitle("PESEX: SEX")
# plt.bar(bar1, PESEX_current, 0.75, color = 'red', label="Current")
# plt.bar(bar2, PESEX_prevmnth, 0.75, color = 'blue', label="Prev Month")
# plt.bar(bar3, PESEX_prevyear, 0.75, color = 'green', label="Prev Year")
# plt.legend(loc="upper left", ncol=3)
# plt.xticks(b, a, rotation=-80)
# plt.show()  


# #PTDTRACE:RACE--------------------------------------------------------------------------------
# PTDTRACE_label = ['01 W Only', '02 B Only', '03 AI, AN Only', '04 A Only', '05 HP Only', '06 W-B',
#                   '07 W-AI', '08 W-A', '09 W-HP', '10 B-AI', '11 B-A', '12 B-HP', '13 AI-A', 
#                   '14 AI-HP', '15 A-HP', '16 W-B-AI', '17 W-B-A', '18 W-B-HP', '19 W-AI-A', 
#                   '20 W-AI-HP', '21 W-A-HP', '22 B-AI-A', '23 W-B-AI-A', '24 W-AI-A-HP', 
#                   '25 Other 3', '26 Other 4,5']

# #Filtering dataset for data of current month, prev month, and prev year
# PTDTRACE_current  = data1["PTDTRACE"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].value_counts().sort_index()
# PTDTRACE_prevmnth = data1["PTDTRACE"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].value_counts().sort_index()
# PTDTRACE_prevyear = data1["PTDTRACE"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].value_counts().sort_index()

# #Validation check compared to Previous Month
# for i in PTDTRACE_current.index:
#     PTDTRACE_prevmnth_val = (.85*(data1["PTDTRACE"][(data1["PTDTRACE"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum())) <= (data1["PTDTRACE"][(data1["PTDTRACE"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PTDTRACE"][(data1["PTDTRACE"]==i) & (data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))].sum()))              
#     if PTDTRACE_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous month for PTDTRACE = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous month for PTDTRACE = ' + str(i))

# #Validation check compared to Previous Year
# for i in PTDTRACE_current.index:
#     PTDTRACE_prevyear_val = (.85*(data1["PTDTRACE"][(data1["PTDTRACE"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum())) <= (data1["PTDTRACE"][(data1["PTDTRACE"]==i) & (data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))].sum()) <= (1.15*(data1["PTDTRACE"][(data1["PTDTRACE"]==i) & (data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))].sum()))              
#     if PTDTRACE_prevmnth_val == True:
#         print('\033[3;32;40m Value within 15% data validation threshhold of previous year for PTDTRACE = ' + str(i))
#     else: print ('\033[3;31;40m Value NOT within 15% data validation threshhold of previous year for PTDTRACE = ' + str(i))

# #Visual graphs
# plt.rcParams['font.size'] = '30'
# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["axes.labelweight"] = "bold"
# plt.rcParams["figure.titlesize"] = '50'
# style.use('dark_background')
# fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(40,20))
# plt.suptitle("PTDTRACE: RACE")
# ax1.barh(PTDTRACE_current.index, PTDTRACE_current, color = 'red')
# ax1.set_title("Current")
# ax2.barh(PTDTRACE_prevmnth.index, PTDTRACE_prevmnth, color = 'blue')
# ax2.set_title("Prev Month")
# ax2.get_yaxis().set_visible(False)
# ax3.barh(PTDTRACE_prevyear.index, PTDTRACE_prevyear, color = 'green')
# ax3.set_title("Prev Year")
# ax3.get_yaxis().set_visible(False)
# plt.show()


# #PERSONS AGE: Age Distribution------------------------------------------------------
# PRTAGE_current  = data1["PRTAGE"][(data1["hrmonth"]==(currntmo)) & (data1["hryear4"]==(currntyr))]
# PRTAGE_prevmnth = data1["PRTAGE"][(data1["hrmonth"]==(prevmomo)) & (data1["hryear4"]==(prevmoyr))]
# PRTAGE_prevyear = data1["PRTAGE"][(data1["hrmonth"]==(prevyrmo)) & (data1["hryear4"]==(prevyryr))]
# style.use('dark_background')
# plt.rcParams['font.size'] = '10'
# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["figure.titlesize"] = '30'
# plt.suptitle("PRTAGE: Age Distribution")
# plt.legend('upper center')
# sb.distplot(PRTAGE_current, hist=False, rug=True, label='Current', color='r',)
# sb.distplot(PRTAGE_prevmnth, hist=False, rug=True, label='Prev Month', color='b', kde_kws={'linestyle':'--'})
# sb.distplot(PRTAGE_prevyear, hist=False, rug=True, label='Prev Year', color='g', kde_kws={'linestyle':':'})
# plt.show()
#group_labels = ['Current', 'PrevMo', 'PrevYr']
# Create distplot with custom bin_size
#fig = ff.create_barplot(
#        hist_data, group_labels, bin_size=[.1, .25, .5])
# Plot!
#st.plotly_chart(fig)



#alt.layer(barchart1, barchart2, barchart3).resolve_scale(y='independent')
#st.bar_chart() st.area_chart() st.line_chart st.map() for a map but you need longitude and latititude st.scatter_chart
#import altair as alt
#st.altair_chart(altair_chart, use_container_width=True)
#where altair_chart = (
#alt.Chart(data)
#.mark_circle()
#.encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"],)
#)
# import graphvix import pydeck as pdk
#import plotly.figure_factory as ff
#dis_fig = ff.create_distplot(data, labels, bin_size)
#st.plotly_chart(dis_fig, use_container_width=True)
    


# # Title for sub
#st.subheader('Count of each variable by period')



# # Sidebar
# st.sidebar.header('Analysis By Work Status')
# selected_prwkstat = st.sidebar.multiselect('Select Work Status', data1['prwkstat'].unique())

# # Display filtered data
# st.subheader('Filtered Data')
# st.write(prwkstat)

# fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(40,20))
# plt.suptitle("prwkstat: FULL/PART-TIME WORK STATUS CODE")
# ax1.barh(prwkstat["prwkstat"], prwkstat_current, color = 'red')
# ax1.set_title("Current")
# ax2.barh(prwkstat["prwkstat"], prwkstat_prevmnth, color = 'blue')
# ax2.set_title("Prev Month")
# ax2.get_yaxis().set_visible(False)
# ax3.barh(prwkstat["prwkstat"], prwkstat_prevyear, color = 'green')
# ax3.set_title("Prev Year")
# ax3.get_yaxis().set_visible(False)
# plt.show()


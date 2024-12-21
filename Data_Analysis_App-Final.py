#!/usr/bin/env python
# coding: utf-8

# In[8]:


######## Importing Libraries ########

import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import table 

import json, os

import tkinter as Tk
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile 
from tkinter.filedialog import asksaveasfilename
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


######## DECLARING GLOBAL VARIABLES ########

# Changes to true once file clean has been done at least once
file_cleaned = False


######## Tkinker WINDOW ########

# creating instance of Tk class
window = tk.Tk()
window.title("Data Analysis App")

# Not allowing window to resize
window.resizable(False, False)  

# Positioning window at the center of the screen and adjusting window's height and width
app_width = 600
app_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width/2) - (app_width/2)
y = (screen_height/2) - (app_height/2)
window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')


######## STYLING ########

# Assigned Style to labels and buttons
style_label = ttk.Style()
style_label.configure("Yell.TLabel", foreground="#4D4D4D", font=("Times", 15), padding=3)
style_button = ttk.Style()
style_button.configure("Yell.TButton", foreground="#030303", background = "#C1CDCD", font=("Times", 12), 
                       relief="flat", padding=6)


######## TABS ########

# Adding "Clean Data" and "Generate Visual" Tabs to window 
notebook = ttk.Notebook(window)
# Putting tabs to the window
notebook.pack(fill='both', expand=True)
# Creating tabs and adjusting their width and height
clean_data_tab = ttk.Frame(notebook, width = app_width, height = app_height)
generate_visual_tab = ttk.Frame(notebook, width = app_width, height = app_height)
# Adding tabs to notebook
notebook.add(clean_data_tab, text="Clean Data")
notebook.add(generate_visual_tab, text="Generate Visual")


######## STATUS ########

status_text = StringVar(window)
status_text.set("[GUIDE] Please click the browse button(s) to load your file(s).")
status_bar = Label(window, textvariable=status_text, bd=1, relief=tk.SUNKEN, font=('Helvetica', 12, 'normal'))
status_bar.configure(foreground='green')
status_bar.pack(side=BOTTOM, fill=X)
status_bar.config(background='#F9F9F9', relief = RAISED, height = 2)


######## HEADERS ########

merge_headers = ['EID', 'NGR', 'Site Height', 'Aerial height(m)', 'Power(kW)', 'Date', 'Site', 'Frequency', 'Block', 'Serv Label1 ', 'Serv Label2 ', 'Serv Label3 ','Serv Label4 ', 'Serv Label10 ']
summary_headers = ["Mean", "Median", "Mode"]


############ DEFINING FUNCTIONS ############


######## SHOW STATUS ########
 
def status_guide1():
    status_bar.configure(foreground='green')
    status_text.set("[GUIDE] Antenna file uploaded. Now please upload Params file!")    
    
def status_guide2():
    status_bar.configure(foreground='green')
    status_text.set("[GUIDE] All files uploaded. Now please click on Clean & Backup to get it clean!")        
    
def status_cleaning():
    status_bar.configure(foreground='yellow4')
    status_text.set("[STATUS] ...Cleaning loaded files")

def status_cleaned_backup():
    status_bar.configure(foreground='green')
    status_text.set("[SUCCESS] Files are clean & backup. Now please click on save as to save your file!")
    print("All files are clean and backup. Now please click on save as to save your file!")

def status_saved():
    status_bar.configure(foreground='green')
    status_text.set("[SUCCESS] You have exported your new data files. Now please go to next tab!")
    print("You have exported your new data files. Now please go to next tab!")

def error_files():
    status_bar.configure(foreground='red')
    status_text.set('[ERROR] There is some problem with your file(s). Please check before taking this action!')
    print("There is some problem with your files. Please check before taking this action!")

def status_json():
    status_bar.configure(foreground='green')
    status_text.set(' [STATUS] Your JSON file is loaded. Now please select visual!')   
    print("... Your JSON file is loaded. Now please select visual!")
    
def status_invalid():
    status_bar.configure(foreground='red')
    status_text.set('[ERROR] Please first clean your files before you click on save as!')
    print("Please first clean your files before you click on save as!")

def error_location():
    status_bar.configure(foreground='red')
    status_text.set('[ERROR] Please load a valid data file location by clicking browse.')
    print("Please load a valid data file location by clicking browse.")

def building_graphs():
    status_bar.configure(foreground='yellow4')
    status_text.set('[STATUS] ...Building your graphs! Check output.')
    print(" ...Building your graphs! Check output.")
    
def status_graph_built():
    status_bar.configure(foreground='green')
    status_text.set('[SUCCESS] You have built your graphs!')
    print("You have built your graphs")

def status_graph_export():
    status_bar.configure(foreground='green')
    status_text.set('[SUCCESS] Your graphs have been exported into the same folder!')
    print("Your graphs have been exported into the same folder!")
    
    
######## SAVE AS ########    

def save_as():
    global df_cleaned
    data = df_cleaned
    
    try:
        # Checking if file has been cleaned and if the fields contain text
        if (file_cleaned == True ) and (len(input_antenna.get()) != 0) and (len(input_params.get()) != 0):
            global savefile
            savefile = asksaveasfilename(filetypes=(("JSON", "*.json"),
                                                ("All files", "*.*") )) 

            data.to_json(savefile, index=True)   
            status_saved()

        elif (file_cleaned == False) or (len(input_antenna.get()) != 0) or (len(input_params.get()) != 0):
            status_invalid()
        
        else:
            error_files()
        
      
    except NameError:
        error_files()
        print("Failed to save your file\n'%s'" % savefile, "Please check you uploaded the Antenna and Params files correctly.")
    except FileNotFoundError:
        error_files()
        print("Sorry, no such file or directory found. Please try again.")
    except ValueError:
        error_files()
        print("Dataframe index should be unique. Check your dataframe.")
    

######## Backup JSON FILE ########

def back_up(file):

    global status_bar, new_json_name, file_name

    file_name = "Cleaned_data"

    try:
        # New json name
        new_json_name = file_name + ".json"
        file.to_json(new_json_name, index=True)
        
        # Update input field with file upload url
        input_filename.delete(0, tk.END)
        var_filename.set(new_json_name)
    
    except NameError:
        error_files() 


######## EXIT ########        

# Exit Button
def exit():
    if messagebox.askokcancel("Data Analysis App", "Wants to save your changes to the app? Click okay to exit."):
        window.destroy()


######## BROWSING FILES ########

# Browse inventory file to upload function
def open_file1():
    
    global antenna_df, status_bar
    
    try:
        # browse file, open only CSV
        file = filedialog.askopenfile(filetypes =[('CSV', '*.csv')])
        
        # Fill in missing value with NaN
        missing_values = ['NONE', 'none' 'None', "N/A", "n/a", "NA","na", "Na", 
                      "NaN", "NAN", "nan", "NULL", "Null", "null", r"^\s*$", "", " "]
        
        antenna_df = pd.read_csv(file.name, na_values = missing_values)
        file_name = "Antenna_df"
        df_name = file_name + ".csv"
        
        # Update input field with file upload url
        input_antenna.delete(0, tk.END)
        var_antenna.set(df_name)

        status_guide1()
        
    except AttributeError:
        status_bar.configure(foreground='red')
        status_text.set('[ERROR] Attribute not found')
        print("Attribute not found")
    except FileNotFoundError:
        status_bar.configure(foreground='red')
        status_text.set('[ERROR] Please open a valid file')
        print("Please open a valid file")

   
# Browse violation file to upload function
def open_file2():
    global params_df

    try:
        # browse file, open only CSV
        file = filedialog.askopenfile(filetypes =[('CSV', '*.csv')])
        
        # Fill in missing value with NaN
        missing_values = ['NONE', 'none' 'None', "N/A", "n/a", "NA","na", "Na", 
                      "NaN", "NAN", "nan", "NULL", "Null", "null", r"^\s*$", "", " "]
        
        params_df = pd.read_csv(file.name, encoding='latin-1', na_values = missing_values)   
        file_name = "Params_df"
        df_name = file_name + ".csv"

        # Update input field with file upload url
        input_params.delete(0, tk.END)
        var_params.set(df_name)
        
        status_guide2()

    except AttributeError:
        status_bar.configure(foreground='red')
        status_text.set('[ERROR] Attribute not found')
        print("Attribute not found")
    except FileNotFoundError:
        status_bar.configure(foreground='red')
        status_text.set('[ERROR] Please open a valid file')
        print("Please open a valid file")

        
def open_file3(): 
    global json_file
    try:
         # browse file, open only CSV
        file = filedialog.askopenfile(filetypes =[('JSON', '*.json')])
        
        # change json file to dataframe 
        json_file = pd.read_json(file)
        json_file['Date'] = json_file['Date'].apply(pd.to_datetime, format='%d/%m/%Y')
        input_text = file.name
        df_name = input_text + ".json"

        # Update input field with file upload url
        input_prepared.delete(0, tk.END)
        var_prepared.set(df_name)
        
        status_json()

    except AttributeError or ValueError:
        error_location()
        print("Please open a valid data file location")



######## CLEANING DATA ########

def cleaning(data1, data2):
    
    # Dropping irrelevant columns
    global merged_df, file_cleaned
    
    data1.drop(['Longitude/Latitude','Dir Max ERP','0','10','20','30','40','50','60','70','80','90','100','110','120','130','140','150','160','170','180','190','200','210','220','230','240','250','260','270','280','290','300','310','320','330','340','350','Lat','Long'], axis=1, inplace=True)
    data2.drop(['Ensemble', 'Licence', 'Ensemble Area','Transmitter Area','TII Main Id (Hex)','TII Sub Id (Hex)','SId 1 (Hex)', 'LSN 1 (Hex)','SId 2 (Hex)', 'LSN 2 (Hex)','SId 3 (Hex)', 'LSN 3 (Hex)','SId 4 (Hex)','LSN 4 (Hex)','SId 5 (Hex)', 'LSN 5 (Hex)','SId 6 (Hex)', 'LSN 6 (Hex)','SId 7 (Hex)', 'LSN 7 (Hex)','SId 8 (Hex)','LSN 8 (Hex)','SId 9 (Hex)', 'LSN 9 (Hex)','SId 11 (Hex)','LSN 11 (Hex)','Serv Label5 ', 'Serv Label6 ', 'Serv Label7 ', 'Serv Label8 ','Serv Label9 ', 'Serv Label12 ','SId 12 (Hex)','LSN 12 (Hex)','Serv Label13 ','SId 13 (Hex)','LSN 13 (Hex)','Serv Label14 ','SId 14 (Hex)','LSN 14 (Hex)','Serv Label15 ','SId 15 (Hex)','LSN 15 (Hex)','Serv Label16 ','SId 16 (Hex)','LSN 16 (Hex)','Serv Label17 ','SId 17 (Hex)','LSN 17 (Hex)','Serv Label18 ','SId 18 (Hex)','LSN 18 (Hex)','Serv Label19 ','SId 19 (Hex)','LSN 19 (Hex)','Serv Label20 ','SId 20 (Hex)','LSN 20 (Hex)','Serv Label21 ','SId 21 (Hex)','LSN 21 (Hex)','Serv Label22 ','SId 22 (Hex)','LSN 22 (Hex)','Serv Label23 ','SId 23 (Hex)','LSN 23 (Hex)','Serv Label24 ','SId 24 (Hex)','LSN 24 (Hex)','Serv Label25 ','SId 25 (Hex)','LSN 25 (Hex)','Serv Label26 ','SId 26 (Hex)','LSN 26 (Hex)','Serv Label27 ','SId 27 (Hex)','LSN 27 (Hex)','Serv Label28 ','SId 28 (Hex)','LSN 28 (Hex)','Serv Label29 ','SId 29 (Hex)','LSN 29 (Hex)','Serv Label30 ','SId 30 (Hex)','LSN 30 (Hex)','Serv Label31 ','SId 31 (Hex)','LSN 31 (Hex)','Serv Label32 ','SId 32 (Hex)','LSN 32 (Hex)','Data Serv Label1','Data SId 1 (Hex)','Data Serv Label2','Data SId 2 (Hex)','Data Serv Label3','Data SId 3 (Hex)','Data Serv Label4','Data SId 4 (Hex)','Data Serv Label5','Data SId 5 (Hex)','Data Serv Label6','Data SId 6 (Hex)','Data Serv Label7','Data SId 7 (Hex)','Data Serv Label8','Data SId 8 (Hex)','Data Serv Label9','Data SId 9 (Hex)','Data Serv Label10','Data SId 10 (Hex)','SId 10 (Hex)','LSN 10 (Hex)','Serv Label11 ', 'Data Serv Label11', 'Data SId 11 (Hex)', 'Data Serv Label12','Data SId 12 (Hex)', 'Data Serv Label13', 'Data SId 13 (Hex)','Data Serv Label14', 'Data SId 14 (Hex)', 'Data Serv Label15','Data SId 15 (Hex)'], axis=1, inplace=True)
    print("... Dropping irrelevant columns")
    
    # Excluding following NGR: NZ02553847, SE213515, NT05399374 and NT25265908 
    if 'NGR' in data1:
        data1 = data1.loc[(antenna_df['NGR']!='NZ02553847') & (data1['NGR']!='SE213515') & (data1['NGR']!='NT05399374') & (data1['NGR']!='NT25265908')]
        #data1.reset_index(inplace=True)
    if 'id' in data1:
        data1.index = data1.id
        #data1.drop(['id', 'index'], axis=1, inplace=True)
        data1 = data1.drop(['id'], axis=1)
    if 'id' in data2:
        data2.index = params_df.id
        data2.drop(['id'], axis=1, inplace=True)
    print("... Excluding NGR")
    
    
    # Merging datasets
    merged_df = pd.merge(data1, data2, left_index = True, right_index = True, how = 'inner')
    print("...Merging both datasets")
    
    
    # Filling missing values:
    for column in merged_df:
        # Checking if we have missing values in our dataset
        if pd.isnull(merged_df[column]).any(axis = 0):
            # If we have null values, fill them with the value that appears the most
            merged_df[column].fillna(merged_df[column].agg(lambda x: pd.Series.mode(x)[0]))
    print("... Filling missing values")

        
    # Checking duplicates
    # Checking for duplicate rows
    dup = merged_df[merged_df.duplicated()]
    print("... Checking for Duplicates")
    if(len(dup.values) == 0):
        print("Your data has no duplicates")
    else:
        print("... Dropping duplicates")
        merged_df.drop_duplicates(inplace = True)
        print("Your data has now been cleaned!")

        
    # Extracting EID
    # Extracting DAB Multiplex Blocks: C18A, C18F and C188
    if 'EID' in merged_df:
        merged_df = merged_df.loc[(merged_df["EID"] == 'C18A') | (merged_df["EID"] == 'C18F') | (merged_df["EID"] == 'C188')]
        # Making EID our new index:
        merged_df.index = merged_df.EID
        merged_df = merged_df.drop(['EID'], axis=1)
        merged_df.reset_index(inplace=True)
    print("... Extracting EID")

    
    # New header
    if ('In-Use Ae Ht' in merged_df) & ('In-Use ERP Total' in merged_df) :
        merged_df.rename(columns={'In-Use Ae Ht': 'Aerial height(m)', 'In-Use ERP Total': 'Power(kW)'}, inplace=True)
        merged_df = merged_df.rename(columns={'Freq.': 'Frequency'})
    print("... Renaming Headers")
    
    
    # Cleaning power column
    if 'Power(kW)' in merged_df:
        merged_df['Power(kW)'] = merged_df['Power(kW)'].str.replace(',', '')
        merged_df['Power(kW)'] = merged_df['Power(kW)'].astype(float)
    print("... Cleaning Power")
    print("... CLEANING 100% COMPLETE")
    
    file_cleaned = True

    print(merged_df.head(5))

    return merged_df


######## CLEAN FUNCTION FOR BUTTON COMMAND ########
 
def clean_files():
    
    global df_cleaned

    status_cleaning()

    # Cleaning Datasets

    try: 
            
        # Only clean if ALL files are present 
        if (len(input_params.get()) != 0) and (len(input_antenna.get()) != 0):
            
            global df_cleaned
            
            # Clean and created subset of inventory
            clean = cleaning(antenna_df, params_df)
            df_cleaned = pd.DataFrame(clean, columns = merge_headers)
            
            back_up(df_cleaned)
            
            status_cleaned_backup()
            
        else:
            # If 1 or both files are not present
            error_files()

    except NameError:
        print("There is an issue with one or more of your file uploads, please check them then try again.")


######## SUMMARY ########

# ---- Site Height Summary: MEAN, MEDIAN, MODE  ----
def summary_sh():

    global json_file
    df = json_file
    
    # Site height column summary
    if "Site Height" in df:
        sh_group = df.loc[(df['Site Height'] > 75)]
        sh_group = sh_group[['Power(kW)']].groupby(sh_group.index)
        sh_mean = sh_group.mean()
        sh_mode = sh_group.agg(lambda x: pd.Series.mode(x)[0])
        sh_median = sh_group.median()
    
    merged_sh = pd.merge(pd.merge(sh_mean, sh_median, left_index = True, right_index = True), sh_mode, left_index = True, right_index = True)
    merged_sh = merged_sh.rename(columns={'Power(kW)_x': 'Mean', 'Power(kW)_y': 'Median', 'Power(kW)': 'Mode'})

    
    print("... Merging summary datasets for Site Height")

    print("---- Site Height Summary ----", end=2*"\n")
    print(merged_sh)
    return merged_sh
    
    
# ---- Date Summary: MEAN, MEDIAN, MODE  ----
def summary_date():
    
    global json_file
    df = json_file
    
    # Date column summary
    if "Date" in df:
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        date_group = df.loc[(df["Date"].dt.year > 2001)]
        date_group = date_group[['Power(kW)']].groupby(date_group.index)
        date_mean = date_group.mean()
        date_mode = date_group.agg(lambda x: pd.Series.mode(x)[0])
        date_median = date_group.median()

    merged_date = pd.merge(pd.merge(date_mean, date_median, left_index = True, right_index = True), date_mode, left_index = True, right_index = True)
    merged_date = merged_date.rename(columns={'Power(kW)_x': 'Mean', 'Power(kW)_y': 'Median', 'Power(kW)': 'Mode'})
    
    
    print("... Merging summary datasets for Date")
        
    print("---- Date Summary ----", end=2*"\n") 
    print(merged_date)
    return merged_date


######## PLOTTING GRAPHS ########

# ---- Creating subplot for graphs  ----
def creating_graphs():
    global graphs, axes
    graphs, axes = plt.subplots(4, 2, constrained_layout = True)
    graphs.set_figwidth(15) 
    graphs.set_figheight(20)
    return graphs, axes


# ----- Preparing data to display information from the three DAB multiplexes ----- 

def prepare_1st_visual_data():
    
    global json_file
    # Getting prepared data
    data = json_file.copy(deep=True)
    
    data.index = data.EID
    data.drop("EID", axis=1, inplace=True)
    
    visual_site = data[['Site']]
    visual_block = data[['Block']]
    visual_sl1 = data[['Serv Label1 ']]
    visual_sl2 = data[['Serv Label2 ']]
    visual_sl3 = data[['Serv Label3 ']]
    visual_sl4 = data[['Serv Label4 ']]
    visual_sl10 = data[['Serv Label10 ']]
    visual_freq = data[['Frequency']]
    
    # Applyling group by to compute sum for DAB multiplex block (EID)
    visual_freq.reset_index(inplace=True)
    visual_freq  = visual_freq.groupby('EID')[['Frequency']].sum()
    group_freq = visual_freq.copy()
    group_freq.reset_index(inplace=True)

    
    # Applying cross tab to compute group frequencies
    cross_site = pd.crosstab(index=visual_site['Site'],
                            columns=visual_site.index)

    cross_block = pd.crosstab(index=visual_block['Block'],
                            columns=visual_block.index)

    cross_sl1 = pd.crosstab(index=visual_sl1['Serv Label1 '],
                            columns=visual_sl1.index)

    cross_sl2 = pd.crosstab(index=visual_sl2['Serv Label2 '],
                            columns=visual_sl2.index)

    cross_sl3 = pd.crosstab(index=visual_sl3['Serv Label3 '],
                            columns=visual_sl3.index)

    cross_sl4 = pd.crosstab(index=visual_sl4['Serv Label4 '],
                            columns=visual_sl4.index)

    cross_sl10 = pd.crosstab(index=visual_sl10['Serv Label10 '],
                            columns=visual_sl10.index)
    
    return group_freq, cross_site, cross_block, cross_sl1, cross_sl2, cross_sl3, cross_sl4, cross_sl10   
    
    
    
    
    
# ----- Plotting  graphs to display information from the three DAB multiplexes ----- 

def plotting_multiplex_info():
    
    # Creating graphs
    global graphs, axes
    graphs, axes = plt.subplots(4, 2, constrained_layout = True)
    graphs.set_figwidth(15) 
    graphs.set_figheight(20)
    
    # Plotting graphs for prepared data
    group_freq, cross_site, cross_block, cross_sl1, cross_sl2, cross_sl3, cross_sl4, cross_sl10 = prepare_1st_visual_data()
    

    # Plotting BAR GRAPH: Site
    plot_site = cross_site.plot(kind='bar', 
                        stacked=True,
                        ax=axes[0,0],
                        colormap='Set3', 
                        legend=False)


    # Plotting BAR GRAPH: Block
    plot_block = cross_block.plot(kind='bar', 
                        stacked=True,
                        ax=axes[0,1],
                        colormap='Set3',
                        legend=False)


    # Plotting BAR GRAPH: Serv Label1
    plot_sl1 = cross_sl1.plot(kind='bar', 
                        stacked=True,
                        ax=axes[1,0],
                        colormap='Set3',
                        legend=False)


    #Plotting BAR GRAPH: Serv Label2
    plot_sl2 = cross_sl2.plot(kind='bar', 
                        stacked=True,
                        ax=axes[1,1],
                        colormap='Set3',
                        legend=False)



    #Plotting BAR GRAPH: Serv Label3
    plot_sl3 = cross_sl3.plot(kind='bar', 
                   stacked=True,
                   ax=axes[2,0],
                   colormap='Set3',
                   legend=False)


    #Plotting BAR GRAPH: Serv Label4
    plot_sl4 = cross_sl4.plot(kind='bar', 
                        stacked=True,
                        ax=axes[2,1],
                        colormap='Set3',
                        legend=False)


    #Plotting BAR GRAPH: Serv Label10
    plot_sl10 = cross_sl10.plot(kind='bar', 
                                stacked=True,
                                ax=axes[3,0],
                                colormap='Set3',
                                legend=False)


    #Plotting BAR GRAPH: Freq
    colors = {"C18A": '#8dd3c7', "C18F": '#b3de69', "C188": '#ffed6f'}
    plot_freq = group_freq.plot.bar(x= "EID",
                                    y= "Frequency",
                                    color=[colors[i] for i in group_freq["EID"]],
                                    stacked=True,
                                    ax=axes[3,1],
                                    legend=False
                                   )


    # Labels to use in the legend for each line
    labels = ["C18A", "C18F", "C188"]
    handles = [plot_site, plot_block, plot_sl1, plot_sl2, plot_sl3, plot_sl4, plot_sl10, plot_freq]
    # Setting a main legend for all the subplots
    graphs.legend(handles=handles ,labels=labels, loc="upper left")

    
    # Setting a main title for all the subplots
    graphs.suptitle('Displaying Information for three DAB multiplexes', fontsize=20)
    # Adjusting the sub-plots
    
    plt.show()  
    
    
    

    
# ----- Preparing data to see if there is any significant correlation between variables -----

def prepare_2nd_visual_data():
    
    global json_file
    # Getting prepared data
    data = json_file.copy(deep=True)
    
    data.index = data.EID
    data.drop("EID", axis=1, inplace=True)
    
    # Extracting relevant columns 
    visual_corr = data.drop(['NGR', 'Site Height', 'Aerial height(m)', 'Power(kW)', 'Date', 'Site'], axis=1)
    
    
    # Transform the prepared data to dummy variables, one-hot encoded:
    DataMatrix = pd.get_dummies(visual_corr)

    return DataMatrix
    

# ----- Plotting graphs to see if there is any significant correlation between variables -----
def plotting_correlation():
    global svm
    # Getting prepared data
    DataMatrix = prepare_2nd_visual_data()
    
    # Plotting correlation heatmap for prepared data:
    plt.figure(figsize=(15,12))
    graphs, axes = plt.subplots(figsize = (16,8))
    graphs.suptitle('Significant Correlation Between Variables', fontsize=20)
    svm = sns.heatmap(DataMatrix.corr('pearson'), cmap='coolwarm', center=0, annot=True, cbar=False)
    
    plt.show()
    
    
    
######## Plotting  graphs ########

def generate_graphs():  

    try:
        if (len(input_prepared.get()) == 0):
            error_files()
        else:
            building_graphs()
            graph_selection()
            plt.show()
            status_graph_built()

    except AttributeError or ValueError:
        error_location()
        print("Please open a valid data file location")


######## GRAPHS FUNCTION FOR BUTTON COMMAND ########

def graph_selection():
    
    graphs, axes = creating_graphs() 
    
    # Clear graph 
    graphs.clear()
    
    # Draw graphs
    if var_graph.get() == 1:
        # Summary for ‘In-Use ERP Total’ where ‘Site Height’ is more than 75
        summary_sh()
    
    elif var_graph.get() == 2:
        # Summary for ‘In-Use ERP Total’ where ‘Date’ is  2001 onwards
        summary_date()
    
    elif var_graph.get() == 3:
        # DAB multiplexes information
        plotting_multiplex_info()
    
    elif var_graph.get() == 4:
        # Significant correlation 
        plotting_correlation()
    
    else:
        status_text.set('You have not selected any graph. Please pick one.')    


######## EXPORTING GRAPH TO PNG FILE ########

def export_summary_df(df):
    try:
        graphs, axes = plt.subplots() 
        table(axes, df, loc='center')  # Create a table, where df is your dataframe
        axes.xaxis.set_visible(False)  # hide the x axis
        axes.yaxis.set_visible(False)  # hide the y axis
        # Giving title to plots
        if var_graph.get() == 1:
            graphs.suptitle('Displaying Site Height Summary', fontsize=15)
        elif var_graph.get() == 2:
            graphs.suptitle('Displaying Date Summary', fontsize=15)
        graphs.savefig('df_graph.png')
        
    except NameError:
        error_location()
    

# Exporting graphs as PNG files
def export_graphs():
    global var_graph, svm
    try: 
        graph_selection()
        if var_graph.get() == 1:
            df = summary_sh()
            export_summary_df(df)
            status_graph_export()
        
        elif var_graph.get() == 2:
            df = summary_date()
            export_summary_df(df)
            status_graph_export()
        
        elif (var_graph.get() == 3):    
            # Export as image
            plt.figure(figsize=(30,30))
            plt.gcf().set_size_inches(30, 30)
            plt.tight_layout()
            graphs.savefig('graphs.png', dpi=400)
            status_graph_export() 
        
        elif (var_graph.get() == 4):    
            # Export as image
            plt.figure(figsize=(50,50))
            figure = svm.get_figure()    
            figure.savefig('graphs.png', dpi=400)
            status_graph_export()
    
    except NameError:
        error_location()


######## CLEAN DATA TAB ########

# Adding text label
ttk.Label(clean_data_tab, text="Antenna File", style="STD.Label").grid(row= 1, column=0, padx=10, pady=10, sticky=W)
ttk.Label(clean_data_tab, text="Params File", style="STD.Label").grid(row= 2, column=0, padx=10, pady=10, sticky=W)
ttk.Label(clean_data_tab, text="Backup File Name", style="STD.Label").grid(row=4, column=0, padx=10, pady=25, sticky=W)
ttk.Label(clean_data_tab, text="Please upload csv files for cleaning", style='STD.Label').grid(row=0, column=0, columnspan=3, padx=10, pady=30)

# Adding input fields to clean_data_tab
var_antenna = StringVar()
var_params = StringVar()
var_filename = StringVar()
input_antenna = ttk.Entry(clean_data_tab, textvariable=var_antenna, state=DISABLED)
input_params = ttk.Entry(clean_data_tab, textvariable=var_params, state=DISABLED)
input_filename = ttk.Entry(clean_data_tab, textvariable=var_filename, state=DISABLED)

# Position of input fields
input_antenna.grid(row=1, column=1, padx=5, pady=0)
input_params.grid(row=2, column=1, padx=5, pady=0)
input_filename.grid(row=4, column=1, padx=0, pady=0)

# File Browse Buttons
btn_browse1 = ttk.Button(clean_data_tab, text="Browse", command = lambda:open_file1())
btn_browse2 = ttk.Button(clean_data_tab, text="Browse", command = lambda:open_file2())
# Browse button layout  
btn_browse1.grid(row=1, column=2, sticky=E)
btn_browse2.grid(row=2, column=2, sticky=E)

# Adding Buttons to clean data tab
btn_save = ttk.Button(clean_data_tab, text="Save As", command= lambda:save_as())
btn_clean = ttk.Button(clean_data_tab, text="Clean & Backup", command= lambda:clean_files())
btn_exit = ttk.Button(clean_data_tab, text="Exit", command=exit)
# Action button layout
btn_clean.grid(row=4, column=2, columnspan=2, sticky=W)
btn_save.grid(row=5, column=1, sticky=W, pady=20)
btn_exit.grid(row=5, column=2, sticky=W)


######## GENERATE VISUAL TAB ########

ttk.Label(generate_visual_tab, text="Upload your cleaned data file to produce graphs for analysis", style='STD.Label').grid(row=0, column=0, columnspan=3, padx=10, pady=20)

# Upload data file 
ttk.Label(generate_visual_tab, text="Output File", style='STD.Label').grid(row=1, column=0, padx=10, pady=10, sticky=W)

# Adding input fields to generate_visual_tab
var_prepared = StringVar()
input_prepared = ttk.Entry(generate_visual_tab, textvariable=var_prepared, state=DISABLED)
# Position of input fields
input_prepared.grid(row=1, column=1, sticky=W)

# Browse button 
btn_graph_browse = ttk.Button(generate_visual_tab, text="Browse", command = lambda:open_file3())
btn_graph_browse.grid(row=1, column=2, sticky=W)

# Select graphs 
ttk.Label(generate_visual_tab, text="Select the visualisations you would like to generate", style="STD.Label").grid(row= 2, column=0, padx=10, pady=10, sticky=W, columnspan=3)


######## Radio buttons ########

var_graph = tk.IntVar()

# Summary where ‘Site Height’ more than 75
radio_sum_sh=Radiobutton(generate_visual_tab,text="Summary filtered by SiteHeight", variable=var_graph, value=1, background='#ececec')
radio_sum_sh.grid(row=3,column=0, sticky=W,columnspan=3,  padx=5, pady=5)

# Summary where ‘Date’ from 2001 onwards
radio_sum_date=Radiobutton(generate_visual_tab,text="Summary filtered by Dates", variable=var_graph, value=2, background='#ececec')
radio_sum_date.grid(row=3,column=2, sticky=W)

# DAB muliplexes information
radio_info=Radiobutton(generate_visual_tab,text="Muliplexes information", variable=var_graph, value=3, background='#ececec')
radio_info.grid(row=4,column=0, sticky=W, columnspan=3, padx=5)

# Significant correlation
radio_corr=Radiobutton(generate_visual_tab,text="Correlation", variable=var_graph, value=4, background='#ececec')
radio_corr.grid(row=4,column=2, sticky=W, columnspan=3, padx=5)


######## Adding Buttons to generate visual ########

# Button that generate graph
gen_graph_button = Button(master = generate_visual_tab, text="Generate",
                     command = lambda: generate_graphs())

# place the button in graph window
gen_graph_button.grid(row=9, column=1, pady=20)

# Export graph in form of 
btn_export = ttk.Button(generate_visual_tab, text="Export", command = lambda:export_graphs())
btn_export.grid(row=9, column=0, padx=0, sticky=E)

# Exit Button
btn_exit = ttk.Button(generate_visual_tab, text = "Exit", command=exit)
btn_exit.grid(row=9, column=2, sticky=W)


window.mainloop()


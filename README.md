# Radio Broadcast Data Insights and Analytics Application

Design and develop a prototype application that demonstrates how data from the given data set can be formatted, cleaned, and used to generate insightful visualisations (as listed below). 

### Functional requirements: 
The application should provide the following functionality: 

• A means to load the initial dataset (which consists of three CSV files) and translate it into a suitable format, either XML, or JSON or an entity relationship structure (not CSV). 

• A means to back up the suitable format using either files or a database. This should preserve the current state of the data when the program is closed, and make it available when the program is reopened. 

• A process for cleaning and preparing the initial data set, managing inconsistencies, errors, missing values and any specific changes required by the client (see below). 

• A graphical user interface(s) for interacting with the data that enables the user to: 

o Load and clean an initial data set (from the CV format). 

o Load and save a prepared data set (from its translated format). 

o Use the prepared data set to generate output and visualisations. 

o Manipulate the range of values used to generate output and visualisations. 

It should be assumed that this program will be able to handle other sets of data generated from the same source, i.e. data with the same column row headings but containing different values and anomalies. However, the application is not required to be generic (work with multiple unknown data sets). Given this best practice regarding code reuse, encapsulation and a well-defined programming interface should be applied where applicable. 

### Data manipulation and outputs: 
The client initially wants the application to perform the following actions on the data: 

1. Outputs should not include any data from DAB Radio stations that have the following ‘NGR’: NZ02553847, SE213515, NT05399374 and NT252675908.
3. The ‘EID’ column contains information of the DAB multiplex block E.g C19A. Extract this out into a new column, one for each of the following DAB multiplexes: 
a. All DAB multiplexes, that are , C18A, C18F, C188
b. Join each category, C18A, C18F, C188to the ‘ NGR’ that signifies the DAB stations location to the following: ‘Site’, ‘Site Height, In-Use Ae Ht, In-Use ERP Total 
c. Please note that: In-Use Ae Ht, In-Use ERP Total will need the following new header after extraction: Aerial height(m), Power(kW) 
respectively. 
4. The client initially needs information to generate the following and output the results using appropriate representation: 
a. Produce the mean, mode and median for the ‘In-Use ERP Total’ from the extracted DAB multiplexes extracted earlier: C18A, C18F, C188
i. For ‘Site Height’ more than 75 
ii. For ‘Date’ from 2001 onwards
5. Produce a suitable graph that display the following information from the three DAB multiplexes that you extracted earlier: C18A, C18F, C188: ‘Site’, ‘Freq’, ‘Block’, ‘Serv Label1’, ‘Serv Label2’, ‘Serv Label3’, ‘Serv label4’,’Serv Label10’. You may need to consider how you group this data to make visualisation feasible.
6. Determine if there is any significant correlation between the ‘Freq’, ‘Block’, ‘Serv Label1’, ‘Serv Label2’, ‘Serv Label3’, ‘Serv label4’,’Serv Label10’ used by the extracted DAB stations. You will need to select an appropriate visualisation to demonstrate this.

### Non-functional requirements:

• The GUI interface must be able to provide appropriate feedback to confirm or deny a user’s actions.

• The application must be able to manage internal and user-generated errors Technical requirements.

### Steps:
Following are the step-by-step instructions to run this Broadcast analytics application:
1)  Please run application.
2)  Under "Clean Data" tab, please click on 1st "browse" button to load Antenna file.
3)  Please click on 2nd "browse" button to load Params file.
4)  Please click on "Click & Backup" button to clean both data files and store the copy of clean file for backup (in JSON format) into current directory. To see output, check Jupyter Notebook.
5)  Please click on "Save As" button to save the cleaned file (in JSON format) into directory of your choice. While naming your file, please write name in the following format "*.json".
6)  Please go to the next tab "Generate Visual".
7)  Please upload the saved JSON file by clicking on the "browse" button.
8)  Please select the type of visualisation you would like to generate by clicking on the radio button beside each graph title.
9)  Please click on "export" button if you want to save the generated graph as a PNG image file into your system.
10) Please click on "generate" button if you want to generate the graph on Jupyter Notebook's output. To see output, check Jupyter Notebook.
11) If you like to close application, please click on "exit" button on either tab.

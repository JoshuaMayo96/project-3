# PROJECT3
Project 3
Group members: David Calero, Gustavo Bustillos, Joshua Mayo, Spencer Duke

Our group looked at the percent of adults aged 18 years and older who have obesity

Here is how we completed the project:

Used the following required libraries:

Required libraries
requests
pandas
eel
urllib3
sqlite3
csv
os
traceback
io
json
Data collected from https://chronicdata.cdc.gov/ and cleaned with Python (pandas)
Also downloaded a geojson file that contains coordinates of all the states, file downloaded from https://www.kaggle.com/datasets/pompelmo/usa-states-geojson
Used sqlite3 DB to store the data and also created a CSV file as a backup.
The library eel was used to serve a website locally
https://chronicdata.cdc.gov/


Here is how we created the map on the website:

The first visual on our page is an interactive map showing the obesity prevalence per state across the entire date range. We created this map using leaflet, and maps layers provided by openmaps.org.
Our first goal was to create the initial map and interface it with a state selection dropdown we had made earlier in the code. This allowed us to select any state and the map would focus/zoom in on that state. Next, we added a legend at the bottom right of the map that showed both the name and obesity prevalence of the selected state.
Our next goal with the map was to trace and color fill the states based on high or low obesity prevalence. Because our original dataset only contained coordinates for a single point within each state, we had to download and integrate a json file that contained the coordinates needed to outline each state. We downloaded this from Kaggle. After integrating said json, we were able to tell the code to color fill each state based on the obesity prevalence for the states.
Limitations to this map:
One limitation in this map is that there is no “select all” option in the state selection dropdown, meaning that to fill the entire map’s worth of data, each state would need to be selected individually from the dropdown. We tried very hard to figure out a way to select all states at once, but due to time and knowledge constraints, we could not fix this before the project deadline.
One last limitation to this map regards the json file implemented for state outline/color fill. Our original dataset contained both US States and US Territories; however, the json file we used to trace and fill these locations did not contain territories, or Washington DC.

Here is how we created the pie charts:
Pie Chart for year:
•	createPieChart(yearSelected) function creates a pie chart to display the obesity prevalence in the USA based on age for a specific year selected
•	It initializes two empty arrays, xValues and yValues, to store the data values and age values
•	It then iterates through the data array and checks if the YearEnd value in each row matches the yearSelected parameter
•	If there is a match, it pushes the Data_Value to xValues and the Age_years to yValues
•	After that, it creates a data1 object with values set to xValues, labels set to yValues, type set to 'pie', and a title that includes the selected year. Finally, it sets the layout options and uses Plotly to create a new pie chart with the specified data and layout, which is displayed in the HTML element with the id 'plot2'
•	We took the average
Pie Chart for state:
•	function is similar to the first function but creates a pie chart for a specific state selected
Summary:
•	these functions use the Plotly library to generate pie charts representing obesity prevalence data

Here is how we organzied the website:

Part of this challenge was to create a visualization using HTML/CSS. We wanted to organize the data and create a user-friendly web page. We identified the key elements and sections needed to present the information effectively. We began by setting up the basic structure using HTML tags such as <html>, <head> and <body>. Within the <head> section, we defined important metadata like the character set, viewport settings, and included necessary external resources such as CSS and JavaScript files. Next, we focused on the content within the <body> section. We carefully planned and implemented the layout, arranging various <div> elements to create sections, containers, and rows. Within these elements, we placed relevant content, such as headings, buttons, select dropdowns, and visual elements like maps, pie graphs, and data table. As we progressed, we encountered a challenge, such as centering the data. Through research, we learned about CSS properties like ‘display: flex: justify-content: center;’ that allowed us to achieve the desired center effect.

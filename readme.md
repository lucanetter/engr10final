This is a python based application created by our team to
analyze and visualize vehicle data based on the vehicle type
and profile type. We created three separate files, the data_manager.py,
graph_manager.py, and main.py files. The generate_vehicle_data.py
file given to us. The application can be ran through the main
class at the bottom of the main.py file. 

Dashboard Description:

Data File Section:
On the top of the dashboard, there is a file selection tool. This is for if
the user wants to import or select a different data file either inside of the sample_data folder
or from somewhere else on their device. 

Vehicle and Profile Type Selection:
Given the data file, the main class has a filter method to make sure that only the
possible pairs of vehicle and profile type are able to be selected.

Plotting Buttons:
There are 5 buttons that can plot different types of graphs. When the data file is uploaded,
and the vehicle and profile types are selected, the buttons graph the specific combination.

Generating New Data:
At the bottom of the screen, there is the option to generate new test data. Given the 
vehicle type, profile type, and duration, it generates new specific data that will then save
to the sample_data folder. It can then be accessed from the file selection at the top.




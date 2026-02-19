#visulization imports
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QFileDialog, QLineEdit, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#basic imports
import sys
import os
import datetime

#importing other files
from data_manager import DataManager
from graph_manager import GraphManager
from generate_vehicle_data import generate_vehicle_test_data

class VehicleDashboard(QWidget):
    #initial constructor for data etc
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vehicle Dynamics Dashboard")
        self.setGeometry(100, 100, 800, 600)

        # Initialize DataManager and GraphManager
        self.dm = DataManager()
        self.gm = GraphManager(self.dm)

        self.valid_combinations = []
        self.data_file_combo = QComboBox()
        self.vehicle_combo = QComboBox()
        self.profile_combo = QComboBox()
        self.plot_canvas = FigureCanvas(Figure(figsize=(6, 4)))

        self.init_ui()

        # Load the first file automatically if available
        if self.data_file_combo.count() > 0:
            self.load_selected_data_file()

    #ui constructor to initalize all elements
    def init_ui(self):
        layout = QVBoxLayout()

        #file selection section
        hbox_file = QHBoxLayout()
        hbox_file.addWidget(QLabel("Data File:"))
        self.data_file_combo.addItems(self.get_available_data_files())
        hbox_file.addWidget(self.data_file_combo)

        btn_load = QPushButton("Load Selected File")
        btn_load.clicked.connect(self.load_selected_data_file)
        hbox_file.addWidget(btn_load)

        btn_new_file = QPushButton("Load New File")
        btn_new_file.clicked.connect(self.load_new_file)
        hbox_file.addWidget(btn_new_file)

        self.vehicle_combo.currentTextChanged.connect(lambda: self.update_dropdowns("vehicle"))
        self.profile_combo.currentTextChanged.connect(lambda: self.update_dropdowns("profile"))
        layout.addLayout(hbox_file)


        #vehicle and profile selction
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Vehicle Type:"))
        hbox1.addWidget(self.vehicle_combo)
        layout.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Profile Type:"))
        hbox2.addWidget(self.profile_combo)
        layout.addLayout(hbox2)


        #plotting buttons
        btn_stats = QPushButton("Plot Basic Stats")
        btn_stats.clicked.connect(self.plot_basic_stats)
        layout.addWidget(btn_stats)

        btn_accel = QPushButton("Plot Acceleration")
        btn_accel.clicked.connect(self.plot_acceleration)
        layout.addWidget(btn_accel)

        btn_fuel = QPushButton("Plot Fuel Efficiency")
        btn_fuel.clicked.connect(self.plot_fuel_efficiency)
        layout.addWidget(btn_fuel)

        btn_brake = QPushButton("Plot Braking")
        btn_brake.clicked.connect(self.plot_braking)
        layout.addWidget(btn_brake)

        btn_motion = QPushButton("Plot Motion")
        btn_motion.clicked.connect(self.plot_motion)
        layout.addWidget(btn_motion)


        #plot area
        layout.addWidget(self.plot_canvas)

        self.setLayout(layout)

        hbox_generate = QHBoxLayout()

        hbox_generate.addWidget(QLabel("Vehicle Type:"))
        self.new_vehicle_combo = QComboBox()
        self.new_vehicle_combo.addItems(["sedan", "SUV", "sports"])
        hbox_generate.addWidget(self.new_vehicle_combo)

        hbox_generate.addWidget(QLabel("Profile Type:"))
        self.new_profile_combo = QComboBox()
        self.new_profile_combo.addItems(["urban", "highway", "sport"])
        hbox_generate.addWidget(self.new_profile_combo)

        hbox_generate.addWidget(QLabel("Duration (s):"))
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("300")  # default hint
        hbox_generate.addWidget(self.duration_input)

        btn_generate = QPushButton("Generate New Test Data")
        btn_generate.clicked.connect(self.generate_new_test_data)
        hbox_generate.addWidget(btn_generate)

        layout.addLayout(hbox_generate)


    #method to find all available files
    def get_available_data_files(self):
        files = []
        folder = "sample_data" #folder with data
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if f.endswith(".csv"):
                    files.append(os.path.join(folder, f))
        return files


    #generate new test data if user wants
    def generate_new_test_data(self):
        vehicle_type = self.new_vehicle_combo.currentText()
        profile_type = self.new_profile_combo.currentText()
        duration_text = self.duration_input.text()

        #default to 300 seconds if blank
        try:
            duration = int(duration_text) if duration_text else 300
            if duration <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Duration", "Please enter a positive number for duration (seconds).")
            return

        #generate timestamp for filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sample_data/sample_data_{timestamp}.csv"

        #generate and save csv
        generate_vehicle_test_data(duration=duration, profile_type=profile_type, vehicle_type=vehicle_type,
                                   output_file=filename)

        #add file to list and save it
        self.data_file_combo.addItem(filename)
        self.data_file_combo.setCurrentText(filename)
        self.load_selected_data_file()

        #confirmation popup
        QMessageBox.information(self, "Success", f"Generated new test data:\n{filename}")


    #load selected data method
    def load_selected_data_file(self):
        file_path = self.data_file_combo.currentText()
        if file_path:
            success = self.dm.load_data(file_path)
            if success is not False:
                df = self.dm.data
                if df is not None:
                    #get all valid vehicle-profile combos
                    self.valid_combinations = sorted(set(zip(df['VehicleType'], df['ProfileType'])))

                    #extract available combos
                    vehicle_types = sorted(set(v for v, _ in self.valid_combinations))
                    profile_types = sorted(set(p for _, p in self.valid_combinations))

                    #block update signals
                    self.user_updating = True
                    self.vehicle_combo.clear()
                    self.vehicle_combo.addItems(vehicle_types)
                    self.profile_combo.clear()
                    self.profile_combo.addItems(profile_types)
                    self.user_updating = False


    #user loading file method
    def load_new_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            success = self.dm.load_data(file_path)
            if success is not False:
                #add datafile to list if not in it
                if file_path not in [self.data_file_combo.itemText(i) for i in range(self.data_file_combo.count())]:
                    self.data_file_combo.addItem(file_path)
                    self.data_file_combo.setCurrentText(file_path)
                self.vehicle_combo.clear()
                self.vehicle_combo.addItems(self.dm.vehicle_types)
                self.update_profile_options(self.vehicle_combo.currentText())


    #updating dropdowns method
    def update_dropdowns(self, changed="vehicle"):
        if self.user_updating:
            return

        self.user_updating = True

        selected_vehicle = self.vehicle_combo.currentText()
        selected_profile = self.profile_combo.currentText()

        if changed == "vehicle":
            #filter profile types for valid vehicle combo
            valid_profiles = sorted({p for v, p in self.valid_combinations if v == selected_vehicle})
            self.profile_combo.clear()
            self.profile_combo.addItems(valid_profiles)
            if selected_profile in valid_profiles:
                self.profile_combo.setCurrentText(selected_profile)
        elif changed == "profile":
            #filter vehicle types for valid profile combo
            valid_vehicles = sorted({v for v, p in self.valid_combinations if p == selected_profile})
            self.vehicle_combo.clear()
            self.vehicle_combo.addItems(valid_vehicles)
            if selected_vehicle in valid_vehicles:
                self.vehicle_combo.setCurrentText(selected_vehicle)

        self.user_updating = False


    #getting filters method
    def get_filters(self):
        return {
            "vehicle_type": self.vehicle_combo.currentText(),
            "profile_type": self.profile_combo.currentText()
        }


    #all methods here are for updating the graphs when the button is pressed
    def update_plot(self, fig):
        self.plot_canvas.setParent(None)
        self.plot_canvas = FigureCanvas(fig)
        self.layout().addWidget(self.plot_canvas)

    def plot_basic_stats(self):
        fig = self.gm.plot_basic_stats("Speed", **self.get_filters())
        if fig:
            self.update_plot(fig)

    def plot_acceleration(self):
        fig = self.gm.plot_acceleration(**self.get_filters())
        if fig:
            self.update_plot(fig)

    def plot_fuel_efficiency(self):
        fig = self.gm.plot_fuel_efficiency(**self.get_filters())
        if fig:
            self.update_plot(fig)

    def plot_braking(self):
        fig = self.gm.plot_braking_events(**self.get_filters())
        if fig:
            self.update_plot(fig)

    def plot_motion(self):
        fig = self.gm.plot_speed_motion(**self.get_filters())
        if fig:
            self.update_plot(fig)


#simple main method
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = VehicleDashboard()
    dashboard.show()
    sys.exit(app.exec())

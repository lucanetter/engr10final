import pandas as pd

class DataManager:
    def __init__(self):
        self.data = None
        self.test_ids = []
        self.vehicle_types = []
        self.profile_types = []

    #load data method
    def load_data(self, filepath):
        try:
            self.data = pd.read_csv(filepath)
            self.test_ids = self.data['TestID'].unique()
            self.vehicle_types = self.data['VehicleType'].unique()
            self.profile_types = self.data['ProfileType'].unique()
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False


    #get test data method
    def get_test_data(self, test_id=None, vehicle_type=None, profile_type=None):
        if self.data is None:
            print("No data loaded.")
            return None

        filtered = self.data.copy()

        if test_id:
            filtered = filtered[filtered['TestID'] == test_id]
        if vehicle_type:
            filtered = filtered[filtered['VehicleType'] == vehicle_type]
        if profile_type:
            filtered = filtered[filtered['ProfileType'] == profile_type]

        return filtered


    #calculate stats method
    def calculate_statistics(self, parameter, test_id=None, vehicle_type=None, profile_type=None):
        data = self.get_test_data(test_id, vehicle_type, profile_type)

        if data is None or parameter not in data.columns:
            print(f"Data or parameter '{parameter}' not available.")
            return None

        return {
            'mean': data[parameter].mean(),
            'median': data[parameter].median(),
            'std_dev': data[parameter].std(),
            'min': data[parameter].min(),
            'max': data[parameter].max(),
            'range': data[parameter].max() - data[parameter].min(),
            'q1': data[parameter].quantile(0.25),
            'q3': data[parameter].quantile(0.75)
        }


    #summerize parameters method
    def summarize_all_parameters(self, test_id=None, vehicle_type=None, profile_type=None):
        params = ['Speed', 'Acceleration', 'EngineRPM', 'FuelConsumption', 'Distance']
        return {
            param: self.calculate_statistics(param, test_id, vehicle_type, profile_type)
            for param in params
        }
import pandas as pd

class DataManager:
    """
    A class for managing and analyzing vehicle test data.

    This class provides functionality to load, filter, and analyze vehicle test data
    from CSV files. It supports operations like loading data, filtering by various
    parameters, and calculating statistical measures.

    Attributes:
        data (pandas.DataFrame): The loaded dataset containing vehicle test data
        test_ids (list): Unique test IDs in the dataset
        vehicle_types (list): Unique vehicle types in the dataset
        profile_types (list): Unique profile types in the dataset
    """

    def __init__(self):
        """
        Initialize a new DataManager instance.
        
        Creates an empty DataManager with no data loaded. The data, test_ids,
        vehicle_types, and profile_types attributes will be populated when
        load_data() is called.
        """
        self.data = None
        self.test_ids = []
        self.vehicle_types = []
        self.profile_types = []

    #load data method
    def load_data(self, filepath):
        """
        Load vehicle test data from a CSV file.

        Args:
            filepath (str): Path to the CSV file containing the test data

        Returns:
            bool: True if data was successfully loaded, False otherwise

        Raises:
            Exception: If there is an error reading the CSV file
        """
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
        """
        Filter the loaded data based on specified criteria.

        Args:
            test_id (str, optional): Filter by specific test ID
            vehicle_type (str, optional): Filter by specific vehicle type
            profile_type (str, optional): Filter by specific profile type

        Returns:
            pandas.DataFrame or None: Filtered dataset or None if no data is loaded
        """
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
        """
        Calculate statistical measures for a specified parameter.

        Args:
            parameter (str): The parameter to calculate statistics for
            test_id (str, optional): Filter by specific test ID
            vehicle_type (str, optional): Filter by specific vehicle type
            profile_type (str, optional): Filter by specific profile type

        Returns:
            dict or None: Dictionary containing statistical measures or None if data/parameter not available
            The dictionary includes:
                - mean: Arithmetic mean
                - median: Median value
                - std_dev: Standard deviation
                - min: Minimum value
                - max: Maximum value
                - range: Range of values
                - q1: First quartile
                - q3: Third quartile
        """
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
        """
        Calculate statistics for all available parameters.

        Args:
            test_id (str, optional): Filter by specific test ID
            vehicle_type (str, optional): Filter by specific vehicle type
            profile_type (str, optional): Filter by specific profile type

        Returns:
            dict: Dictionary containing statistical measures for each parameter
            Parameters included:
                - Speed
                - Acceleration
                - EngineRPM
                - FuelConsumption
                - Distance
        """
        params = ['Speed', 'Acceleration', 'EngineRPM', 'FuelConsumption', 'Distance']
        return {
            param: self.calculate_statistics(param, test_id, vehicle_type, profile_type)
            for param in params
        }
import matplotlib.pyplot as plt

class GraphManager:
    """
    A class for creating and managing various types of vehicle test data visualizations.

    This class provides methods to generate different types of plots and graphs
    for analyzing vehicle test data, including acceleration, fuel efficiency,
    braking events, and speed profiles.

    Attributes:
        dm (DataManager): An instance of DataManager used to access and process the test data
    """

    def __init__(self, data_manager):
        """
        Initialize a new GraphManager instance.

        Args:
            data_manager (DataManager): An instance of DataManager that provides access to the test data
        """
        
        self.dm = data_manager

    #all of these methods are for plotting different types of graphs
    def plot_basic_stats(self, parameter, **filters):
        """
        Create a bar plot showing basic statistical measures for a given parameter.

        Args:
            parameter (str): The parameter to plot statistics for (e.g., 'Speed', 'Acceleration')
            **filters: Optional filtering parameters passed to calculate_statistics
                     (test_id, vehicle_type, profile_type)

        Returns:
            matplotlib.figure.Figure or None: A figure object containing the bar plot,
                                            or None if no data is available
        """
        
        stats = self.dm.calculate_statistics(parameter, **filters)
        if not stats:
            return None

        fig, ax = plt.subplots(figsize=(6, 4))
        labels = list(stats.keys())
        values = list(stats.values())
        ax.bar(labels, values)
        ax.set_title(f"Basic Statistics for {parameter}")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        return fig

    def plot_acceleration(self, **filters):
        """
        Create a line plot showing acceleration over time.

        Args:
            **filters: Optional filtering parameters passed to get_test_data
                     (test_id, vehicle_type, profile_type)

        Returns:
            matplotlib.figure.Figure or None: A figure object containing the acceleration plot,
                                            or None if no data is available
        """
        
        data = self.dm.get_test_data(**filters)
        if data is None:
            return None

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data['Time'], data['Acceleration'])
        ax.set_title("Acceleration Over Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Acceleration (m/s²)")
        ax.grid(True)
        fig.tight_layout()
        return fig

    def plot_fuel_efficiency(self, **filters):
        """
        Create a line plot showing fuel consumption over time.

        Args:
            **filters: Optional filtering parameters passed to get_test_data
                     (test_id, vehicle_type, profile_type)

        Returns:
            matplotlib.figure.Figure or None: A figure object containing the fuel efficiency plot,
                                            or None if no data is available
        """
        
        data = self.dm.get_test_data(**filters)
        if data is None:
            return None

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data['Time'], data['FuelConsumption'], color='green')
        ax.set_title("Fuel Consumption Over Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Fuel Consumption (L/100km)")
        ax.grid(True)
        fig.tight_layout()
        return fig

    def plot_braking_events(self, **filters):
        """
        Create a line plot showing acceleration with braking events highlighted.

        The plot includes a horizontal line at -2.0 m/s² to indicate the braking threshold.
        Values below this threshold are considered braking events.

        Args:
            **filters: Optional filtering parameters passed to get_test_data
                     (test_id, vehicle_type, profile_type)

        Returns:
            matplotlib.figure.Figure or None: A figure object containing the braking events plot,
                                            or None if no data is available
        """
        
        data = self.dm.get_test_data(**filters)
        if data is None:
            return None

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data['Time'], data['Acceleration'])
        ax.axhline(-2.0, color='red', linestyle='--', label='Braking Threshold')
        ax.set_title("Braking Events Detection")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Acceleration (m/s²)")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()
        return fig

    def plot_speed_motion(self, **filters):
        """
        Create a line plot showing speed over time.

        Args:
            **filters: Optional filtering parameters passed to get_test_data
                     (test_id, vehicle_type, profile_type)

        Returns:
            matplotlib.figure.Figure or None: A figure object containing the speed plot,
                                            or None if no data is available
        """
        
        data = self.dm.get_test_data(**filters)
        if data is None:
            return None

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data['Time'], data['Speed'], color='purple')
        ax.set_title("Speed Over Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Speed (km/h)")
        ax.grid(True)
        fig.tight_layout()
        return fig
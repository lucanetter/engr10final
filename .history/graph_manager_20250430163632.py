import matplotlib.pyplot as plt

class GraphManager:
    def __init__(self, data_manager):
        self.dm = data_manager

    #all of these methods are for plotting different types of graphs
    def plot_basic_stats(self, parameter, **filters):
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
import numpy as np
import pandas as pd
import os
from datetime import datetime


def generate_speed_profile(duration, profile_type, max_speed=120):
    """
    Generate a speed profile based on the specified type.

    Parameters:
    duration (float): Duration of the test in seconds
    profile_type (str): Type of driving profile ('highway', 'urban', 'mixed')
    max_speed (float): Maximum speed in km/h

    Returns:
    numpy.ndarray: Array of speed values at 0.1s intervals
    """
    # Create time array with 0.1s intervals
    time_points = int(duration * 10)
    time = np.linspace(0, duration, time_points)

    if profile_type == 'highway':
        # Highway profile: acceleration to high speed, maintain, some variations
        # Acceleration phase
        accel_time = time[time <= 30]
        accel_speed = max_speed * (1 - np.exp(-accel_time / 10))

        # Cruising phase with small variations
        cruise_time = time[time > 30]
        cruise_speed = max_speed + np.sin(cruise_time / 5) * 5

        # Combine phases
        speed = np.concatenate([accel_speed, cruise_speed])

        # Add some random variation
        speed += np.random.normal(0, 2, len(speed))

    elif profile_type == 'urban':
        # Urban profile: multiple accelerations and decelerations
        speed = np.zeros_like(time)

        # Create several stop-and-go cycles
        for i in range(int(duration / 60)):
            start_idx = int(i * 60 * 10)
            end_idx = int((i + 1) * 60 * 10)

            if end_idx > len(speed):
                end_idx = len(speed)

            cycle_time = time[start_idx:end_idx] - time[start_idx]

            # Each cycle: accelerate, cruise, decelerate, stop
            cycle_speed = 50 * np.sin(cycle_time * np.pi / 60) ** 2
            speed[start_idx:end_idx] = cycle_speed

        # Add random variations
        speed += np.random.normal(0, 1, len(speed))

    else:  # mixed
        # Mixed profile: combination of highway and urban segments
        speed = np.zeros_like(time)

        # Divide into segments
        segment_duration = 120  # 2 minutes per segment
        num_segments = int(duration / segment_duration)

        for i in range(num_segments):
            start_idx = int(i * segment_duration * 10)
            end_idx = int((i + 1) * segment_duration * 10)

            if end_idx > len(speed):
                end_idx = len(speed)

            segment_time = end_idx - start_idx

            # Alternate between highway and urban patterns
            if i % 2 == 0:  # Highway-like segment
                segment_speed = 100 + 20 * np.sin(np.linspace(0, np.pi, segment_time))
                segment_speed += np.random.normal(0, 3, segment_time)
            else:  # Urban-like segment
                segment_speed = np.zeros(segment_time)
                for j in range(int(segment_time / 600)):
                    stop_start = int(j * 600)
                    stop_end = int((j + 1) * 600)

                    if stop_end > segment_time:
                        stop_end = segment_time

                    cycle_length = stop_end - stop_start
                    cycle_time = np.linspace(0, 1, cycle_length)
                    segment_speed[stop_start:stop_end] = 60 * np.sin(cycle_time * np.pi) ** 2

            speed[start_idx:end_idx] = segment_speed

    # Ensure no negative speeds
    speed = np.maximum(speed, 0)

    return speed


def calculate_acceleration(speed, time_step=0.1):
    """
    Calculate acceleration from speed data.

    Parameters:
    speed (numpy.ndarray): Array of speed values in km/h
    time_step (float): Time step in seconds

    Returns:
    numpy.ndarray: Array of acceleration values in m/s²
    """
    # Convert speed from km/h to m/s
    speed_ms = speed * (1000 / 3600)

    # Calculate acceleration (dv/dt)
    acceleration = np.zeros_like(speed_ms)
    acceleration[1:] = (speed_ms[1:] - speed_ms[:-1]) / time_step

    # Smooth acceleration to reduce noise
    window_size = 5
    smoothed_acceleration = np.convolve(acceleration, np.ones(window_size) / window_size, mode='same')

    return smoothed_acceleration


def calculate_engine_rpm(speed, gear_ratios, final_drive_ratio, wheel_diameter=0.7):
    """
    Calculate engine RPM based on vehicle speed and gear ratios.

    Parameters:
    speed (numpy.ndarray): Array of speed values in km/h
    gear_ratios (list): List of gear ratios
    final_drive_ratio (float): Final drive ratio
    wheel_diameter (float): Wheel diameter in meters

    Returns:
    numpy.ndarray: Array of engine RPM values
    """
    # Convert speed from km/h to m/s
    speed_ms = speed * (1000 / 3600)

    # Calculate wheel RPM: v = ω * r => ω = v / r
    wheel_rpm = speed_ms / (wheel_diameter / 2) * 60 / (2 * np.pi)

    # Determine appropriate gear based on speed
    rpm = np.zeros_like(speed)

    # Simple gear selection based on speed thresholds
    speed_thresholds = [0, 20, 40, 60, 80, 110]

    for i in range(len(speed)):
        gear = 1  # Start with 1st gear

        # Select gear based on speed
        for j in range(len(speed_thresholds)):
            if speed[i] >= speed_thresholds[j] and j < len(gear_ratios):
                gear = j + 1

        # Calculate engine RPM using selected gear
        if gear <= len(gear_ratios):
            gear_ratio = gear_ratios[gear - 1]
            rpm[i] = wheel_rpm[i] * gear_ratio * final_drive_ratio

    # Add some random variation to simulate real-world conditions
    rpm += np.random.normal(0, 50, len(rpm))

    # Ensure minimum RPM at idle
    min_rpm = 800
    rpm = np.maximum(rpm, min_rpm)

    return rpm


def calculate_fuel_consumption(speed, acceleration, rpm, engine_efficiency=0.35, vehicle_mass=1500):
    """
    Calculate instantaneous fuel consumption based on speed, acceleration and RPM.

    Parameters:
    speed (numpy.ndarray): Array of speed values in km/h
    acceleration (numpy.ndarray): Array of acceleration values in m/s²
    rpm (numpy.ndarray): Array of engine RPM values
    engine_efficiency (float): Engine thermal efficiency
    vehicle_mass (float): Vehicle mass in kg

    Returns:
    numpy.ndarray: Array of fuel consumption values in L/100km
    """
    # Convert speed from km/h to m/s
    speed_ms = speed * (1000 / 3600)

    # Calculate power required to overcome resistance and acceleration
    # P = F * v
    # F = m * a + F_rolling + F_air

    # Rolling resistance coefficient
    c_r = 0.015

    # Air resistance constants
    rho_air = 1.225  # kg/m³
    c_d = 0.3  # Drag coefficient
    A = 2.2  # Frontal area in m²

    # Calculate forces
    F_rolling = c_r * vehicle_mass * 9.81  # Rolling resistance
    F_air = 0.5 * rho_air * c_d * A * speed_ms ** 2  # Air resistance
    F_accel = vehicle_mass * acceleration  # Force required for acceleration

    # Total force
    F_total = F_rolling + F_air + F_accel

    # Power required (W)
    power = F_total * speed_ms

    # Convert negative power (braking) to zero fuel consumption
    power = np.maximum(power, 0)

    # Add idle fuel consumption when speed is very low
    idle_fuel_rate = 0.5  # L/h
    idle_condition = speed < 3

    # Energy in fuel (gasoline: ~34.8 MJ/L)
    fuel_energy_density = 34.8e6  # J/L

    # Calculate instantaneous fuel consumption in L/s
    fuel_rate = power / (fuel_energy_density * engine_efficiency)

    # Add idle consumption
    fuel_rate[idle_condition] = idle_fuel_rate / 3600  # Convert L/h to L/s

    # Convert to L/100km (standard fuel economy measure)
    # L/100km = (L/s) / (km/s) * 100
    # km/s = (km/h) / 3600

    # Avoid division by zero
    speed_kms = speed / 3600  # Convert to km/s
    speed_kms = np.maximum(speed_kms, 1e-6)  # Avoid division by zero

    fuel_consumption = fuel_rate / speed_kms * 100

    # Cap unrealistically high values that might occur at very low speeds
    fuel_consumption = np.minimum(fuel_consumption, 50)

    # Add some random variation
    fuel_consumption += np.random.normal(0, 0.5, len(fuel_consumption))
    fuel_consumption = np.maximum(fuel_consumption, 0)  # Ensure non-negative

    return fuel_consumption


def calculate_distance(speed, time_step=0.1):
    """
    Calculate cumulative distance based on speed data.

    Parameters:
    speed (numpy.ndarray): Array of speed values in km/h
    time_step (float): Time step in seconds

    Returns:
    numpy.ndarray: Array of cumulative distance values in meters
    """
    # Convert speed from km/h to m/s
    speed_ms = speed * (1000 / 3600)

    # Calculate distance increments: d = v * dt
    distance_increments = speed_ms * time_step

    # Calculate cumulative distance
    distance = np.cumsum(distance_increments)

    return distance


def generate_vehicle_test_data(duration, profile_type, vehicle_type='sedan', output_file=None):
    """
    Generate complete vehicle test data for a specific profile and vehicle type.

    Parameters:
    duration (float): Duration of the test in seconds
    profile_type (str): Type of driving profile ('highway', 'urban', 'mixed')
    vehicle_type (str): Type of vehicle ('sedan', 'suv', 'sports')

    Returns:
    pandas.DataFrame: DataFrame containing all test data
    """


    # Number of data points
    time_points = int(duration * 10)

    # Create time array with 0.1s intervals
    time = np.linspace(0, duration, time_points)

    # Vehicle parameters based on type
    if vehicle_type == 'sedan':
        max_speed = 180  # km/h
        vehicle_mass = 1500  # kg
        engine_efficiency = 0.35
        gear_ratios = [3.5, 2.0, 1.5, 1.0, 0.75]
        final_drive_ratio = 3.7

    elif vehicle_type == 'suv':
        max_speed = 160  # km/h
        vehicle_mass = 2200  # kg
        engine_efficiency = 0.32
        gear_ratios = [3.8, 2.2, 1.6, 1.0, 0.7]
        final_drive_ratio = 4.1

    else:  # sports car
        max_speed = 250  # km/h
        vehicle_mass = 1300  # kg
        engine_efficiency = 0.38
        gear_ratios = [3.2, 2.0, 1.4, 1.0, 0.8, 0.6]
        final_drive_ratio = 3.5

    # Generate speed profile
    speed = generate_speed_profile(duration, profile_type, max_speed)

    # Calculate other parameters
    acceleration = calculate_acceleration(speed)
    engine_rpm = calculate_engine_rpm(speed, gear_ratios, final_drive_ratio)
    fuel_consumption = calculate_fuel_consumption(speed, acceleration, engine_rpm, engine_efficiency, vehicle_mass)
    distance = calculate_distance(speed)


    # Create DataFrame
    data = pd.DataFrame({
        'Time': time,
        'Speed': speed,  # km/h
        'Acceleration': acceleration,  # m/s²
        'EngineRPM': engine_rpm,  # RPM
        'FuelConsumption': fuel_consumption,  # L/100km
        'Distance': distance  # m
    })

    # Add test metadata
    data['TestID'] = f"{vehicle_type}_{profile_type}"
    data['VehicleType'] = vehicle_type
    data['ProfileType'] = profile_type

    if output_file:
        data.to_csv(output_file, index=False)

    return data


def main():
    """
    Generate sample data for three vehicle test runs and save to CSV.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists('sample_data'):
        os.makedirs('sample_data')

    # Generate data for three different test runs
    test_scenarios = [
        {'duration': 600, 'profile': 'highway', 'vehicle': 'sedan'},
        {'duration': 900, 'profile': 'urban', 'vehicle': 'suv'},
        {'duration': 1200, 'profile': 'mixed', 'vehicle': 'sports'}
    ]

    # Combine all test data into one DataFrame
    all_data = pd.DataFrame()

    for scenario in test_scenarios:
        print(f"Generating {scenario['vehicle']} {scenario['profile']} data...")
        test_data = generate_vehicle_test_data(
            duration=scenario['duration'],
            profile_type=scenario['profile'],
            vehicle_type=scenario['vehicle']
        )
        all_data = pd.concat([all_data, test_data], ignore_index=True)

    # Save combined data to CSV
    timestamp = datetime.now().strftime('%Y%m%d')
    filename = f"sample_data/vehicle_dynamics_data_{timestamp}.csv"
    all_data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


main()
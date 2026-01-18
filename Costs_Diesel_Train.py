# Variables
weight_kg = (12.320 + 98) * 1000
velocity = 110 / 3.6  # Speed to accelerate to in m/s
efficiency_total = 0.22  # Total efficiency (Diesel engine)
h = 300  # Elevation gain (meters)
g = 9.81  # Gravitational constant
trip_distance = 60000  # in m
rotating_masses = 10
acceleration = 1  # Acceleration in m/s^2
air_density = 1.23  # Air density
Cd = 0.85  # Drag coefficient
Area = 10  # Cross-sectional area in m^2
t_end = velocity / acceleration  # Acceleration time
t = 0  # Iterator variable
dt = 0.00001  # Measurement time interval
avg_distance_stops = 60 / 16 * 1000
E_air_total_one_acceleration = 0
Cr = 0.001  # Rolling resistance coefficient
Fn = weight_kg * g  # Normal force
energy_content = 9.8  # Energy content in kWh per Liter of Diesel
price_per_liter = 1.74  # Price per Liter of Diesel
stops = 16  # Number of stops per trip
trips_per_week = 172  # Number of trips in a week
weeks_per_year = 52  # Number of weeks in a year
cost_list = []
year = 1  # Loop variable
observation_duration = 30  # Duration of observation in years
investment_costs = 4650000  # Cost for purchasing a train
total_energy_costs_accumulated = 0
number_of_trains = 2
recuperation_rate = 0.3
station_construction_cost = 900000  # Cost for Diesel station infrastructure

# Calculations

# Rolling resistance over one trip:
F_roll = Cr * Fn
E_roll = F_roll * trip_distance / 3600000

# Kinetic energy up to the target speed:
E_kin = weight_kg / 2 * velocity**2 / 3600000

# Surcharge for rotating masses:
E_kin = E_kin / 100 * rotating_masses + E_kin

# Potential energy for elevation gain:
E_pot = weight_kg * g * h / 3600000

# Air resistance during acceleration and braking:
target_velocity = velocity # Store original target velocity
while t < t_end:
    current_vel = acceleration * t
    Fd = 0.5 * air_density * Area * Cd * current_vel**2
    d = current_vel * dt
    E_air_time_interval = Fd * d / 3600000
    E_air_total_one_acceleration += E_air_time_interval
    t += dt
    
E_air_total_accel_brake_one_trip = E_air_total_one_acceleration * 32

# Reset velocity to target for constant speed calculation
velocity = target_velocity

# Air resistance at constant speed:
Fd = 0.5 * air_density * Area * Cd * velocity**2
d = avg_distance_stops - 2 * 0.5 * acceleration * t_end**2
E_air_constant = Fd * d / 3600000
E_air_total_constant_one_trip = E_air_constant * stops
E_air_total = E_air_total_constant_one_trip + E_air_total_accel_brake_one_trip

# Recuperation of kinetic energy:
E_recuperation_kin = E_kin * recuperation_rate

# Recuperation of potential energy:
E_recuperation_pot = E_pot * recuperation_rate

# Energy for maintaining speed:
E_constant_speed = E_roll + E_air_total

# Total energy:
E_total = E_pot + E_constant_speed + stops * E_kin - stops * E_recuperation_kin - E_recuperation_pot

# Accounting for total efficiency:
E_total = E_total / efficiency_total

# Accounting for energy content (Diesel):
E_total = E_total / energy_content

# Accounting for Diesel price:
energy_costs = E_total * price_per_liter

# Energy costs for one trip:
print(energy_costs)

# Costs in one week:
energy_costs = energy_costs * trips_per_week

# Costs in one year:
energy_costs_one_year = energy_costs * weeks_per_year

# Total costs over time
while year <= observation_duration:
    if year == 1:
        # Includes investment and station construction in the first year
        total_energy_costs_accumulated = number_of_trains * investment_costs + energy_costs_one_year + station_construction_cost
        cost_list.append(total_energy_costs_accumulated)
    else:
        total_energy_costs_accumulated += energy_costs_one_year
        cost_list.append(total_energy_costs_accumulated)
    year += 1

print(cost_list)

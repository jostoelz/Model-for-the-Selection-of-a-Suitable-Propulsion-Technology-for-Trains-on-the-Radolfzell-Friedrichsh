# Variables
weight_kg = (22.88 + 100) * 1000  # in kg
velocity = 110 / 3.6  # in m/s
efficiency_total = 0.35
elevation_gain = 300  # in m
gravity = 9.81  # in m/s^2
distance = 60000  # in m
recuperation_rate = 0.55
rotating_masses = 10
acceleration = 1  # in m/s^2
air_density = 1.23  # in kg/m^3
drag_coefficient = 0.85
rolling_resistance_coeff = 0.001
cross_sectional_area = 10  # in m^2
time_interval = 0.00001  # in s
number_of_accelerations = 16  # Number of stops + 1
energy_price_per_kwh = 0.37  # in Euro
investment_cost_train = 8000000  # in Euro
construction_cost_overhead_line = 10560000  # in Euro
trips_per_week = 172
observation_duration = 30  # in years
number_of_trains = 2
cost_list = []
current_year = 1
current_time = 0
weeks_per_year = 52
E_air_resistance_acceleration = 0

# Calculations

# Energy required to overcome rolling resistance during one trip:
normal_force = weight_kg * gravity
F_rolling_resistance = rolling_resistance_coeff * normal_force
E_rolling_resistance = F_rolling_resistance * distance / 3600000

# Kinetic energy required up to the acceleration speed:
E_kin = weight_kg / 2 * velocity**2 / 3600000

# Surcharge for rotating masses:
E_kin = E_kin / 100 * rotating_masses + E_kin

# Potential energy required to overcome elevation gain:
E_pot = weight_kg * gravity * elevation_gain / 3600000

# Energy required to overcome air resistance during acceleration and braking:
acceleration_time = velocity / acceleration

# Store target velocity to restore it later
target_velocity = velocity 

while current_time < acceleration_time:
    current_velocity = acceleration * current_time
    F_air_resistance_interval = 0.5 * air_density * cross_sectional_area * drag_coefficient * current_velocity**2
    dist_interval = current_velocity * time_interval
    E_air_resistance_interval = F_air_resistance_interval * dist_interval / 3600000
    E_air_resistance_acceleration += E_air_resistance_interval
    current_time += time_interval

E_air_resistance_accel_braking = E_air_resistance_acceleration * number_of_accelerations * 2

# Restore target velocity for constant speed calculations
velocity = target_velocity

# Energy required to overcome air resistance at constant speed:
F_air_resistance = 0.5 * air_density * cross_sectional_area * drag_coefficient * velocity**2
avg_distance_sections = distance / number_of_accelerations
dist_constant = avg_distance_sections - 2 * 0.5 * acceleration * acceleration_time**2
E_air_resistance_constant = F_air_resistance * dist_constant / 3600000
E_air_resistance_constant = E_air_resistance_constant * number_of_accelerations
E_air_resistance_total = E_air_resistance_constant + E_air_resistance_accel_braking

# Recuperation of kinetic energy:
E_recuperation_kin = E_kin * recuperation_rate

# Recuperation of potential energy:
E_recuperation_pot = E_pot * recuperation_rate

# Total energy required for one trip:
E_total = E_pot + E_rolling_resistance + E_air_resistance_total + number_of_accelerations * E_kin - number_of_accelerations * E_recuperation_kin - E_recuperation_pot

# Accounting for total efficiency:
E_total = E_total / efficiency_total

# Accounting for energy price:
energy_costs = E_total * energy_price_per_kwh
energy_costs_per_trip_per_person = energy_costs / 286
print(energy_costs_per_trip_per_person)

# Energy costs per week:
energy_costs_per_week = energy_costs * trips_per_week

# Energy costs per year:
energy_costs_per_year = energy_costs_per_week * weeks_per_year

# Investment and energy costs over the observation duration:
while current_year <= observation_duration:
    if current_year == 1:
        # Includes train investment and overhead line construction in year 1
        cost_accumulated = number_of_trains * investment_cost_train + energy_costs_per_year + construction_cost_overhead_line
        cost_list.append(cost_accumulated)
    else:
        cost_accumulated += energy_costs_per_year
        cost_list.append(cost_accumulated)
    current_year += 1

print(cost_list)


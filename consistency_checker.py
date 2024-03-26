import yaml
import math

def read_yaml(file_path):
    """Read YAML file and return the data."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# paths to the YAML files
mpc_param_file_path = "/home/zheshen/pilot-auto.x2/src/autoware/launcher/autoware_launch/config/control/trajectory_follower/lateral/mpc.param.yaml"
pid_param_file_path = "/home/zheshen/pilot-auto.x2/src/autoware/launcher/autoware_launch/config/control/trajectory_follower/longitudinal/pid.param.yaml"
simulator_model_param_file_path = "/home/zheshen/pilot-auto.x2/src/description/vehicle/j6_gen1_description/j6_gen1_description/config/simulator_model.param.yaml"

# read the YAML files
mpc_params = read_yaml(mpc_param_file_path)["/**"]["ros__parameters"]
pid_params = read_yaml(pid_param_file_path)["/**"]["ros__parameters"]
simulator_model_params = read_yaml(simulator_model_param_file_path)["/**"]["ros__parameters"]

# compare the parameters
results = {
    "mpc_vehicle_model_type_consistency": mpc_params["vehicle_model_type"] == simulator_model_params["vehicle_model_type"],  # Should not compare directly. Modify later!!
    "mpc_steer_delay_difference": simulator_model_params["steer_time_delay"] - mpc_params["input_delay"],
    "mpc_steer_time_constant_difference": simulator_model_params["steer_time_constant"] - mpc_params["vehicle_model_steer_tau"],
    "mpc_acceleration_limit_difference": simulator_model_params["vel_rate_lim"] - mpc_params["acceleration_limit"],
    "mpc_max_steer_rate_lim_difference_by_curvature": simulator_model_params["steer_rate_lim"] - max(mpc_params["steer_rate_lim_dps_list_by_curvature"]) * (math.pi / 180),
    "mpc_max_steer_rate_lim_difference_by_velocity": simulator_model_params["steer_rate_lim"] - max(mpc_params["steer_rate_lim_dps_list_by_velocity"]) * (math.pi / 180),
    "pid_abs_max_acc_difference": simulator_model_params["vel_rate_lim"] - abs(pid_params["max_acc"]),
    "pid_abs_min_acc_difference": simulator_model_params["vel_rate_lim"] - abs(pid_params["min_acc"])
}

# print the results
for key, value in results.items():
    print(f"{key}: {value}")

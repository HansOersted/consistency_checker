import yaml

def read_yaml(file_path):
    """Read YAML file and return the data."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# paths to the YAML files
mpc_param_file_path = "/home/shen/pilot-auto.x2/src/autoware/launcher/autoware_launch/config/control/trajectory_follower/lateral/mpc.param.yaml"
pid_param_file_path = "/home/shen/pilot-auto.x2/src/autoware/launcher/autoware_launch/config/control/trajectory_follower/longitudinal/pid.param.yaml"
simulator_model_param_file_path = "/home/shen/pilot-auto.x2/src/description/vehicle/j6_gen1_description/j6_gen1_description/config/simulator_model.param.yaml"

# read the YAML files
mpc_params = read_yaml(mpc_param_file_path)["/**"]["ros__parameters"]
pid_params = read_yaml(pid_param_file_path)["/**"]["ros__parameters"]
simulator_model_params = read_yaml(simulator_model_param_file_path)["/**"]["ros__parameters"]

# compare the parameters
results = {
    "vehicle_model_type_consistency": mpc_params["vehicle_model_type"] == simulator_model_params["vehicle_model_type"],
    "input_delay_difference": simulator_model_params["steer_time_delay"] - mpc_params["input_delay"],
    "vehicle_model_steer_tau_difference": simulator_model_params["steer_time_constant"] - mpc_params["vehicle_model_steer_tau"],
    "acceleration_limit_difference": simulator_model_params["vel_rate_lim"] - mpc_params["acceleration_limit"],
    "max_acc_difference": simulator_model_params["vel_lim"] - pid_params["max_acc"],
    "min_acc_difference": simulator_model_params["vel_rate_lim"] - pid_params["min_acc"]
}

# print the results
for key, value in results.items():
    print(f"{key}: {value}")

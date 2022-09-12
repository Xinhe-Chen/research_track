import os

this_file_path = os.path.dirname(os.path.realpath(__file__))


def submit_job(
    sim_id,
    wind_pmax,
    battery_energy_capacity,
    battery_pmax,
    n_scenario,
    participation_mode,
    reserve_factor,
):

    # create a directory to save job scripts
    job_scripts_dir = os.path.join(this_file_path, "sim_job_scripts")
    if not os.path.isdir(job_scripts_dir):
        os.mkdir(job_scripts_dir)

    file_name = os.path.join(job_scripts_dir, f"sim_{sim_id}.sh")
    with open(file_name, "w") as f:
        f.write(
            "#!/bin/bash\n"
            + "#$ -M xchen24@nd.edu\n"
            + "#$ -m ae\n"
            + "#$ -q long\n"
            + f"#$ -N re-sim_{sim_id}\n"
            + "conda activate regen\n"
            + "module load gurobi/9.5.1\n"
            + f"python ./run_double_loop.py --sim_id {sim_id} --wind_pmax {wind_pmax} --battery_energy_capacity {battery_energy_capacity} --battery_pmax {battery_pmax} --n_scenario {n_scenario} --participation_mode {participation_mode}"
        )

    # os.system(f"qsub {file_name}")


if __name__ == "__main__":
    
    # from itertools import product

    # sim_id = 0
    sim_id = [229,230,239,241,246,249,250,251,253,257,260,261,264,265,271,272,273,275,277,278,280,\
    281,283,286,287,288,289,291,292,293,295,296,297,298,300,301,302,313,314,356,382]

    reserve_factor = 0.0

    wind_pmax_list = [300,300,300,350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,400,400,400,400,400,400,\
    400,400,400,400,400,400,400,400,400,400,400,400,400,450,500]
    
    # pmax_ratio: battery_power_pmax/wind_pmax
    # pmax_ratio_list = [r/10 for r in range(2,12,2)]
    battery_pmax = [240,240,300,70,70,140,140,140,140,210,210,210,280,280,280,350,350,350,350,350,80,80,80,80,80,160,160,160,160,160,160,\
    240,240,240,240,240,240,400,400,450,300]
    # battery size in hour
    battery_size = 4

    n_scenario_list = [8,10,10,3,10,3,5,5,8,3,8,8,3,3,10,3,3,5,8,10,3,3,5,10,10,3,3,5,8,8,10,3,3,5,8,8,10,3,5,8,10]
    participation_modes = ["SelfSchedule","Bid","SelfSchedule","SelfSchedule","Bid","SelfSchedule","Bid","SelfSchedule","SelfSchedule","SelfSchedule",\
    "Bid","SelfSchedule","Bid","SelfSchedule","SelfSchedule","Bid","SelfSchedule","SelfSchedule","SelfSchedule","Bid","Bid","SelfSchedule","SelfSchedule",\
    "Bid","SelfSchedule","Bid","SelfSchedule","SelfSchedule","Bid","SelfSchedule","SelfSchedule","Bid","SelfSchedule","Bid","Bid","SelfSchedule","Bid",\
    "SelfSchedule","Bid","Bid","Bid"]

    # spec_comb_product = product(wind_pmax_list, pmax_ratio_list, n_scenario_list, participation_modes)

    print('sim_id', len(sim_id))
    print('wind_pmax_list', len(wind_pmax_list))
    print('battery_pmax', len(battery_pmax))
    print('n_scenario_list', len(n_scenario_list))
    print('participation_modes', len(participation_modes))

    for sim_id_, wind_pmax_, battery_pmax_, n_scenario_, pm in zip(sim_id,wind_pmax_list,battery_pmax,n_scenario_list,participation_modes):

        # battery_pmax = wind_pmax * p_max_ratio
        battery_energy_capacity_ = battery_pmax_ * battery_size

        submit_job(
            sim_id=sim_id_,
            wind_pmax=wind_pmax_,
            battery_energy_capacity=battery_energy_capacity_*1.0,
            battery_pmax=battery_pmax_*1.0,
            n_scenario=n_scenario_,
            participation_mode=pm,
            reserve_factor=reserve_factor,
            )

        # sim_id += 1

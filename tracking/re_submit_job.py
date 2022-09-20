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
    rt_underbid_penalty,
    sim_batch
):

    # create a directory to save job scripts
    job_scripts_dir = os.path.join(this_file_path, "batch_3r_sim_job_scripts")
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
            + f"python ./run_double_loop.py --sim_id {sim_id} --wind_pmax {wind_pmax} --battery_energy_capacity {battery_energy_capacity} --battery_pmax {battery_pmax} --n_scenario {n_scenario} --participation_mode {participation_mode} --rt_underbid_penalty {rt_underbid_penalty} --sim_batch {sim_batch}"
        )

    os.system(f"qsub {file_name}")


if __name__ == "__main__":
    
    from itertools import product

    sim_id = 0
    reserve_factor = 0.0

    wind_pmax_list = list(range(50, 550, 50))

    # pmax_ratio: battery_power_pmax/wind_pmax
    pmax_ratio_list = [r/10 for r in range(2, 12, 2)]

    # battery size in hour
    battery_size = 4

    n_scenario_list = [3, 5, 8, 10]
    participation_modes = ["Bid", "SelfSchedule"]

    spec_comb_product = product(wind_pmax_list, pmax_ratio_list, n_scenario_list, participation_modes)

    sim_batch = '3r'
    rt_underbid_penalty = 600.0

    for wind_pmax, p_max_ratio, n_scenario, pm in spec_comb_product:

        battery_pmax = wind_pmax * p_max_ratio
        battery_energy_capacity = battery_pmax * battery_size

        submit_job(
            sim_id=sim_id,
            wind_pmax=wind_pmax,
            battery_energy_capacity=battery_energy_capacity,
            battery_pmax=battery_pmax,
            n_scenario=n_scenario,
            participation_mode=pm,
            reserve_factor=reserve_factor,
            rt_underbid_penalty = rt_underbid_penalty,
            sim_batch = sim_batch
            )

        sim_id += 1
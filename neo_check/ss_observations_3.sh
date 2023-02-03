# ugh, hate how convoluted these calls are
run_moving_calc --obs_file baseline_v3.0_10yrs__vatiras_granvik_10k_obs.txt --simulation_db baseline_v3.0_10yrs.db --orbit_file /Users/yoachim/rubin_sim_data/orbits/vatiras_granvik_10k.txt --out_dir baseline_v3.0_10yrs_ss --objtype Vatira --start_time 60218.0  ; run_moving_fractions --work_dir baseline_v3.0_10yrs_ss --metadata Vatira --start_time 60218.0

run_moving_calc --obs_file baseline_v3.0_10yrs__vatiras_granvik_10k_obs_streaked.txt --simulation_db baseline_v3.0_10yrs.db --orbit_file /Users/yoachim/rubin_sim_data/orbits/vatiras_granvik_10k.txt --out_dir franken_streaked_v2.99_10yrs_ss --objtype Vatira --start_time 60218.0  ; run_moving_fractions --work_dir baseline_streaked_v3.0_10yrs_ss --metadata Vatira --start_time 60218.0

add_run franken_streaked_v2.99_10yrs_ss
add_run baseline_v3.0_10yrs_ss

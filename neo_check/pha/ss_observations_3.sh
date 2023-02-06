# ugh, hate how convoluted these calls are
run_moving_calc --obs_file baseline_v3.0_10yrs__granvik_pha_5k_obs.txt --simulation_db baseline_v3.0_10yrs.db --orbit_file /Users/yoachim/rubin_sim_data/orbits/granvik_pha_5k.txt --out_dir baseline_v3.0_10yrs_ss --objtype PHA --start_time 60218.0  ; run_moving_fractions --work_dir baseline_v3.0_10yrs_ss --metadata PHA --start_time 60218.0
run_moving_calc --obs_file baseline_v3.0_10yrs__granvik_pha_5k_obs_streaked.txt --simulation_db baseline_v3.0_10yrs.db --orbit_file /Users/yoachim/rubin_sim_data/orbits/granvik_pha_5k.txt --out_dir baseline_v3.0_10yrs_streaked_ss --objtype PHA --start_time 60218.0  ; run_moving_fractions --work_dir baseline_v3.0_10yrs_streaked_ss --metadata PHA --start_time 60218.0
run_moving_calc --obs_file baseline_v3.0_10yrs__granvik_pha_5k_obs_wide.txt --simulation_db baseline_v3.0_10yrs.db --orbit_file /Users/yoachim/rubin_sim_data/orbits/granvik_pha_5k.txt --out_dir baseline_v3.0_10yrs_wide_ss --objtype PHA --start_time 60218.0  ; run_moving_fractions --work_dir baseline_v3.0_10yrs_wide_ss --metadata PHA --start_time 60218.0


add_run baseline_v3.0_10yrs_ss
add_run baseline_v3.0_10yrs_streaked_ss
add_run baseline_v3.0_10yrs_wide_ss
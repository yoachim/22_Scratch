# ugh, hate how convoluted these calls are
run_moving_calc --obs_file franken_v2.99_10yrs__granvik_pha_5k_obs.txt --simulation_db franken_v2.99_10yrs.db --orbit_file /Users/yoachim/rubin_sim_data/orbits/granvik_pha_5k.txt --out_dir franken_v2.99_10yrs_ss --objtype Vatira --start_time 60218.0  ; run_moving_fractions --work_dir franken_v2.99_10yrs_ss --metadata Vatira --start_time 60218.0

run_moving_calc --obs_file franken_v2.99_10yrs__granvik_pha_5k_obs_streaked.txt --simulation_db franken_v2.99_10yrs.db --orbit_file /Users/yoachim/rubin_sim_data/orbits/granvik_pha_5k.txt --out_dir franken_streaked_v2.99_10yrs_ss --objtype Vatira --start_time 60218.0  ; run_moving_fractions --work_dir franken_streaked_v2.99_10yrs_ss --metadata Vatira --start_time 60218.0

add_run franken_streaked_v2.99_10yrs_ss
add_run franken_v2.99_10yrs_ss

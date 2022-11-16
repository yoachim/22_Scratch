Example of how one check the impact of a satellite constellation on solar system obejct recovery

Uses `rubin_sim` to do things. Once rubin_sim is installed, grab a survey simulation. In this example I used franken_v2.99_10yrs.db which can be grabbed from https://s3df.slac.stanford.edu/data/rubin/sim-data/sims_featureScheduler_runs3.0/franken/franken_v2.99_10yrs.db

Note, using the dev-camel-snake branch of `rubin_sim` in anticipation that it will soon (by Dec 2022) be merged to master.

* Run the ss_observations_1.ipynb notebook. This takes a sample population of solar system objects and records which ones would be observed given the survey simulation. Generates a file like `franken_v2.99_10yrs__vatiras_granvik_10k_obs.txt`
* Run the ss_observations_2.ipynb notebook. This generates a satellite constellation and checks which observations from step 1 would have been lost to streaks. Outputs a file like `franken_v2.99_10yrs__vatiras_granvik_10k_obs_streaked.txt` that are the subset of surviving observations.
* run ss_observations_3.sh to do the solar system analysis on both sets of observations. Will need some path updates for someone else to run. Generates two directories with the solar system analysis
* run `show_maf` to launch a web browser and check the analysis. Note that we could lose lots of individual observations, but have little to no change in some of the analysis. E.g., we lose a few observations of an object, but we still have enough observations of it to recover an orbit, so our final estimate of the completeness of the population will be unchanged.



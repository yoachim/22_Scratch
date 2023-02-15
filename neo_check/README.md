Example of how one check the impact of a satellite constellation on solar system obejct recovery

Uses `rubin_sim` to do things. Once rubin_sim is installed, grab a survey simulation. In this example I used baseline_v3.0_10yrs.db which can be grabbed from 

* Run the ss_observations_1.ipynb notebook. This takes a sample population of solar system objects and records which ones would be observed given the survey simulation. Generates a file like `baseline_v3.0_10yrs__vatiras_granvik_10k_obs.txt`
* Run the ss_observations_2.ipynb notebook. This generates a satellite constellation and checks which observations from step 1 would have been lost to streaks. Outputs a file like `baseline_v3.0_10yrs__vatiras_granvik_10k_obs_streaked.txt` that are the subset of surviving observations.
* run ss_observations_3.sh to do the solar system analysis on both sets of observations. Will need some path updates for someone else to run. Generates two directories with the solar system analysis
* run `show_maf` to launch a web browser and check the analysis. Note that we could lose lots of individual observations, but have little to no change in some of the analysis. E.g., we lose a few observations of an object, but we still have enough observations of it to recover an orbit, so our final estimate of the completeness of the population will be unchanged.




------

Results:

First, found all the observations of Vatira objects we would get in the baseline (baseline_v3.0_10yrs__vatiras_granvik_10k_obs.txt--6117 detections of 10k Vatiras).

Generated a Starlink Gen2 constellation with 30k satellites

Check how many of our previous detections would get hit by 1 arcmin wide satellite streaks (baseline_v3.0_10yrs__vatiras_granvik_10k_obs_streaked.txt--down to 6068 detections)
Check how many detections survive with a 10 arcmin streak (baseline_v3.0_10yrs__wide_vatiras_granvik_10k_obs_streaked.txt--5766 detections)

Then we can run all of those through our usual orbit recovery criteria pipeline

Run the baseline with a circular field of view (No gaps), and the standard where we check for chip and raft gaps (Baseline)

Also check for a scenario where we throw out any observation that has a streak. Then we go from 2.09e6 visits to 1.95e6 visits. Number of short twilight visits goes from 45835 to 29292.

For the Vatiras, we're probably most interested in the "1 quad in 1 night"

| run        |N detections |      objects H<=22 with 1 quad in 1 night       | 
| -----      | -----       |       --------------- |
| No gaps    |6434         |       1.35% |
| Baseline   |6117         |       1.25%  |
| 1 arcmin   |6068         |       1.21%  |
| 10 arcmin  |5766         |       1.11%  |
| FoV        |2958         |       0.25%   |

------

Can do the same thing for potentially hazerdous NEOs. Only major difference is now we have a 5k tracer population of NEO objects where before we had 10k Vatiras.

NEOs are a lot easier to spot. let's compare PHA 3 pairs in 30 nights detection loss


| run        |N detections |      H<=22.0       | 
| -----      | -----       |       --------------- |
| No gaps    | 1.631e6     |       64.6%   |
| Baseline   | 1.553e6        |    62.8%    |
| 1 arcmin   | 1.552e6        |    62.8%    |
| 10 arcmin  | 1.551e6        |    62.8%    |
| FoV        | 1.399e6        |    60.8%  |


**Conclusion:  If Starlink increases their fleet by an order of magnitude to a 30k satllite constellation AND those satellites leave streaks an order of magnitude larger than what we expect (10 arcmin rather than 1 arcmin) it would wipe out ~10% of our Vatira discoveries. The impact on other science cases looks to be sub-percent to 1%.**




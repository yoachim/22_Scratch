from rubin_sim.satellite_constellations import Constellation, starlink_tles_v2
                                                
import healpy as hp
import numpy as np
import argparse
from rubin_sim.data import get_baseline
from rubin_sim.scheduler.utils import SchemaConverter 


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--lower", type=int, default=0)
    args = parser.parse_args()
    lower = args.lower

    upper = lower + 1

    label = lower + 0

    baseline_file = get_baseline()
    tles = starlink_tles_v2()
    const = Constellation(tles)
    sc = SchemaConverter()
    observations = sc.opsim2obs(baseline_file)

    block_size = 1000

    breaks = np.floor(np.linspace(0, len(observations)-1, block_size)).astype(int)
    lower = breaks[lower]
    upper = breaks[upper]

    #print(lower, upper)

    lengths_deg, n_streaks = const.check_pointings(np.degrees(observations['RA'][lower:upper]),
                            np.degrees(observations['dec'][lower:upper]),
                            observations['mjd'][lower:upper],
                            observations['exptime'][lower:upper])

    result = np.zeros(len(observations['mjd'][lower:upper]), dtype=list(zip(['ID', 'n_streaks'], [int, int])))
    result['ID'] = observations['ID'][lower:upper]
    result['n_streaks'] = n_streaks

    np.save('sav_files/%i.npy' % label, result)

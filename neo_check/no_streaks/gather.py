import glob
import numpy as np
from rubin_sim.data import get_baseline
from rubin_sim.scheduler.utils import SchemaConverter 


if __name__ == "__main__":

    files = glob.glob('sav_files/*.npy')

    arrays = [np.load(name) for name in files]

    result = np.hstack(arrays)

    result.sort(order='ID')

    good = np.where(result['n_streaks'] == 0)[0]

    baseline_file = get_baseline()
    sc = SchemaConverter()
    observations = sc.opsim2obs(baseline_file)

    # make sure everything ran
    assert(np.size(result) == np.size(observations))

    print('started with %i obs, ending with %i' % (np.size(observations), np.size(good)))

    observations = observations[good]

    sc.obs2opsim(observations, filename='baseline_cleaned_v3.0_10yrs.db')


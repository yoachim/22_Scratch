import glob
import numpy as np
import pandas as pd


if __name__ == '__main__':

    names = {1: "streaked", 10: "wide"}

    for length in [1, 10]:

        files = glob.glob("out_files%i/*.txt" % length)

        all_indx = []

        for filename in files:
            data = np.genfromtxt(filename)
            if np.size(data) > 0:
                all_indx.append(data)

        indx = np.hstack(all_indx)

        # check that things worked properly
        assert(indx.size == np.unique(indx.size))  

        ss_observations_file = 'baseline_v3.0_10yrs__granvik_pha_5k_obs.txt'
        ss_objects = pd.read_csv(ss_observations_file, delim_whitespace=True, comment="#")
        final_data = ss_objects.drop(index=indx)

        final_data.to_csv('baseline_v3.0_10yrs__granvik_pha_5k_obs_%s.txt' % names[length], index=False, sep=' ')

    

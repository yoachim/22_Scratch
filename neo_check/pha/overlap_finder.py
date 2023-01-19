import numpy as np
from rubin_sim.satellite_constellations import Constellation, starlink_tles_v1, starlink_tles_v2
import pandas as pd
from rubin_sim.utils import point_to_line_distance
import argparse


# need to add a new method on the constallation to do the checking the way we want
class SConstellation(Constellation):
    def check_positions(self, positions_ra, positions_dec, mjds, visit_times, mask_width=1./60.):
        """Check if RA,dec,mjd spot is hit by a satellite streak
        
        Parameters
        ----------
        positions_ra : np.array
            The RA of each solar system detection (degrees).
        positions_dec : np.array
            The Dec of each solar system detection (degrees).
        mjds : np.array
            The MJD of each detection
        visit_times : np.array
            The total visit times for each detection. Typically exposure time plus 
            any additional read time or shutter motion time. (seconds)
        mask_width : float
            The width of the expected streak (degrees)
        
        Returns
        -------
        index values for positions that were hit by a streak
        """
        # convert all input to radians
        positions_ra = np.radians(positions_ra)
        positions_dec = np.radians(positions_dec)
        mask_width = np.radians(mask_width)
        
        visit_times = visit_times / 3600.0 / 24.0  # convert seconds to days
        
        input_id_indx_oned = np.arange(positions_ra.size, dtype=int)
        
        sat_ra_1, sat_dec_1, sat_alt_1, sat_illum_1 = self.paths_array(mjds)
        mjd_end = mjds + visit_times
        sat_ra_2, sat_dec_2, sat_alt_2, sat_illum_2 = self.paths_array(mjd_end)
        
        # broadcast the object positions to be the same shape as the satellite arrays.
        pointing_ras_rad = np.broadcast_to(positions_ra, sat_ra_1.shape)
        pointing_decs_rad = np.broadcast_to(positions_dec, sat_ra_1.shape)
        input_id_indx = np.broadcast_to(input_id_indx_oned, sat_ra_1.shape)
        
        above_illum_indx = np.where(
            ((sat_alt_1 > self.alt_limit_rad) | (sat_alt_2 > self.alt_limit_rad))
            & ((sat_illum_1 == True) | (sat_illum_2 == True))
        )

        # XXXX--this is assuming satellites travel on straight lines on the sphere
        # I'm not sure that's a super great assumption, but maybe works out
        # statistically where we get some hits right and some wrong
        
        # point_to_line_distance can take arrays, but they all need to be the same shape,
        # thus why we broadcast pointing ra and dec above.
        # This might be better done with a KD tree. Especially if cranking up to 
        # very large satellite constellations.
        distances = point_to_line_distance(
            sat_ra_1[above_illum_indx],
            sat_dec_1[above_illum_indx],
            sat_ra_2[above_illum_indx],
            sat_dec_2[above_illum_indx],
            pointing_ras_rad[above_illum_indx],
            pointing_decs_rad[above_illum_indx],
        )

        close = np.where(distances < mask_width)[0]
        
        # Could set a "close pass" value, maybe one degree, use that instead of the
        # mask width above, then for each indx in close, do a higher time-resolution
        # calculation of the satllite path and check if it gets within mask_width.
        # there is an example in the original check_pointings method on the base class
        
        # Note, could have repeat values in result as an object can be hit by more than one streak
        return input_id_indx[above_illum_indx][close]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--lower", type=int, default=0)
    args = parser.parse_args()
    lower = args.lower

    upper = lower + 1

    ss_observations_file = 'franken_v2.99_10yrs__granvik_pha_5k_obs.txt'
    ss_objects = pd.read_csv(ss_observations_file, delim_whitespace=True, comment="#")
    tles = starlink_tles_v2()
    constellation = SConstellation(tles)

    visit_times = ss_objects['visitExposureTime']+2

    indices = []

    # With a million object detections, we're going to need to chunk this up
    breaks = np.floor(np.linspace(0, len(ss_objects)-1, 10000)).astype(int)
    counter = 0
    lower = breaks[lower]
    upper = breaks[upper]
    # for lower, upper in zip(breaks[0:-1], breaks[1:]):
    # this step is the grind. Generates a few arrays that are n_detections X n_satellites, so
    # potential to gobble up a few GB of memory. Looks like I got up to 10-15 GB on a 6.8k x 30k run.
    print('finding overlaps', lower, upper)
    indx = constellation.check_positions(ss_objects['ra'].values[lower:upper],
                                         ss_objects['dec'].values[lower:upper],
                                         ss_objects['observationStartMJD'].values[lower:upper],
                                         visit_times.values[lower:upper])
    
    np.savetxt('out_%i.txt' % lower, indx)


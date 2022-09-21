import numpy as np
import healpy as hp
from rubin_sim.utils import healbin, _approx_RaDec2AltAz, _angularSeparation
from rubin_sim.scheduler.surveys import BaseSurvey


class PointingsSurvey(BaseSurvey):
    """Survey object for managing a set list of potential pointings.

    Parameters
    ----------
    observations : np.array
        An array of observations
    gap_min : `float` (25.)
        The minimum gap to force between observations of the same spot (minutes)
    alt_limit : `float` (85)
        Altitude limit of the telescope (degrees).
    """
    def __init__(self, observations, gap_min=25.0, moon_dist_limit=30.,
                 weights=None, alt_max=85., alt_min=20.):

        # Not doing a super here, don't want to even have an nside defined.

        self.observations = observations
        self.gap_min = gap_min/60./24.  # to days
        self.moon_dist_limit = np.radians(moon_dist_limit)
        self.alt_max = np.radians(alt_max)
        self.alt_min = np.radians(alt_min)
        self.zeros = self.observations['RA'] * 0.
        # Arrays to track progress
        self.n_obs = np.zeros(self.zeros.size, dtype=int)
        self.last_observed = np.zeros(self.zeros.size, dtype=float)
        
        self.last_computed_reward = -1.

        if weights is None:
            self.weights = {'visit_gap': 1.,
                            'balance_revisit': 1.,
                            'wind_limit': 1.,
                            'slew_time': -1.}
        else:
            self.weights = weights

        self.scheduled_obs = None
    
    def _check_feasibility(self, conditions):
        result = True
        reward = self.calc_reward_function(conditions)
        if not np.isfinite(reward):
            result = False
        return result

    def calc_reward_function(self, conditions):
        # 
        if self.last_computed_reward != conditions.mjd:
            self.alt, self.az = _approx_RaDec2AltAz(self.observations['RA'], self.observations['dec'],
                                                    conditions.site.latitude_rad, conditions.site.longitude_rad,
                                                    conditions.mjd,
                                                    lmst=conditions.lmst)

            self.ha = np.radians(conditions.lmst * 360.0 / 24.0) - self.observations['RA']
            self.ha[np.where(self.ha < 0)] += 2.0 * np.pi

            self.reward = np.zeros(self.observations.size, dtype=float)
            # go through and apply cuts
            # XXX--need to migrate over hour angle limits
            #self.reward += self.apply_ha_limit(conditions)
            self.reward += self.zenith_limit(conditions)
            self.reward += self.moon_limit(conditions)
            # XXX apply all the things we want to 
            self.reward += self.weights['visit_gap'] * self.visit_gap(conditions)
            self.reward += self.weights['balance_revisit'] * self.balance_revisit(conditions)
            self.reward += self.weights['wind_limit'] * self.wind_limit(conditions)
            self.reward += self.weights['slew_time'] * self.slew_time(conditions)

            # Can think about slewtime calc. Not sure why there were 3 before.

            self.last_computed_reward = conditions.mjd
        if not np.isfinite(np.nanmax(self.reward)):
            import pdb ; pdb.set_trace()
        return np.nanmax(self.reward)
    
    def generate_observations(self, conditions):
        max_reward = self.calc_reward_function(conditions)
        # take the first one in the array if there's a tie
        winner = np.min(np.where(self.reward == max_reward)[0])
        # XXX--why this reshape!! Figure out where this goes to check and throw useful warnings
        return [self.observations[winner].reshape(1)]
    
    def add_observation(self, observation, indx=None):
        # Check if we have the same note. Maybe also check other things like exptime
        indx = np.where(observation['note'] == self.observations['note'])[0]
        # Probably need to add a check that note is unique
        self.n_obs[indx] += 1
        self.last_observed[indx] = observation['mjd']
    
    def ha_limit(self, conditions):
        result = self.zeros.copy()
        # apply hour angle limits
        result[np.where(self.ha > xxx)] = np.nan
        return result

    def zenith_limit(self, conditions):
        result = self.zeros.copy()
        result[np.where(self.alt > self.alt_max)] = np.nan
        result[np.where(self.alt < self.alt_min)] = np.nan
        return result

    def moon_limit(self, conditions):
        result = self.zeros.copy()
        dists = _angularSeparation(self.observations['RA'], self.observations['dec'],
                                   conditions.moonRA, conditions.moonDec)
        result[np.where(dists < self.moon_dist_limit)] = np.nan
        return result

    def wind_limit(self, conditions):
        # Apply the wind limit
        result = self.zeros.copy()
        if conditions.wind_speed is None or conditions.wind_direction is None:
            return result
        wind_pressure = conditions.wind_speed * np.cos(
            self.az - conditions.wind_direction
        )
        result -= wind_pressure**2.0
        mask = wind_pressure > self.wind_speed_maximum
        result[mask] = np.nan

        return result
        
    def visit_gap(self, conditions):
        """Enforce a minimum visit gap
        """
        diff = conditions.mjd - self.last_observed
        too_soon = np.where(diff < self.gap_min)[0]
        result = self.zeros.copy()
        result[too_soon] = np.nan
        return result
    
    def balance_revisit(self, conditions):
        sum_obs = np.sum(self.n_obs)
        result = np.floor(1.+self.n_obs/sum_obs)
        result[np.where(self.n_obs == 0)] = 1
        return result

    def slew_time(self, conditions):
        # Interpolate the conditions slewtime map to our positions
        # Could do something more sophisticated, but this is probably fine.
        result = hp.get_interp_val(conditions.slewtime, np.degrees(self.observations['RA']),
                                   np.degrees(self.observations['dec']), lonlat=True)
        return result
    
    def viz(self, nside=128):
        # if we wanted to vizulize what's going on, we could do something like
        result = healbin(self.ra, self.dec, self.reward, nside=nside, reduceFunc=np.max)
        return result
    
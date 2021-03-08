"""
 Author: Matt Hanson
 Created: 16/02/2021 12:55 PM
 """

import itertools
import pandas as pd
import time
import ksl_env
import os
from Climate_Shocks.climate_shocks_env import storyline_dir
from Pasture_Growth_Modelling.full_model_implementation import run_pasture_growth, default_pasture_growth_dir
from Pasture_Growth_Modelling.plot_full_model import plot_sims
from BS_work.SWG.SWG_wrapper import *

if __name__ == '__main__':
    run_basgra = False  # to stop accidental re-run
    plot_results = True #todo look at

    if run_basgra:
        # run basgra
        print('running BASGRA')
        run_pasture_growth(storyline_path=os.path.join(storyline_dir, '0-long-baseline.csv'),
                           outdir=os.path.join(default_pasture_growth_dir, 'long_baseline'),
                           nsims=1000, padock_rest=False,
                           save_daily=False, description='initial long baseline run to help set ibasal',
                           verbose=True, fix_leap=True)

    if plot_results:
        path_list = [
            r"D:\mh_unbacked\SLMACC_2020\pasture_growth_sims\long_baseline\0-long-baseline-eyrewell-irrigated.nc",
            r"D:\mh_unbacked\SLMACC_2020\pasture_growth_sims\long_baseline\0-long-baseline-oxford-irrigated.nc",
        ]
        plot_sims(data_paths=path_list, plot_ind=True, nindv=50, save_dir=None, show=True, figsize=(11, 8),
                  daily=False
                  )

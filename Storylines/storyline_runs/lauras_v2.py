"""
 Author: Matt Hanson
 Created: 15/03/2021 3:23 PM
 """

import pandas as pd
import numpy as np
import ksl_env
import os
import itertools
import glob
from copy import deepcopy
from Storylines.storyline_building_support import base_events, map_storyline_rest, default_storyline_time, \
    default_mode_sites
from Storylines.check_storyline import ensure_no_impossible_events
from Storylines.storyline_evaluation.storyline_eval_support import extract_additional_sims
from Climate_Shocks import climate_shocks_env
from Pasture_Growth_Modelling.full_pgr_model_mp import default_pasture_growth_dir, run_full_model_mp, pgm_log_dir
from Pasture_Growth_Modelling.full_model_implementation import run_pasture_growth
from Pasture_Growth_Modelling.plot_full_model import plot_sims
from Pasture_Growth_Modelling.export_to_csvs import export_all_in_pattern

name = 'lauras_v2'
story_dir = os.path.join(climate_shocks_env.temp_storyline_dir, name)
if not os.path.exists(story_dir):
    os.makedirs(story_dir)

base_pg_outdir = os.path.join(default_pasture_growth_dir, name)
outputs_dir = os.path.join(ksl_env.slmmac_dir,'outputs_for_ws', name)

for d in [story_dir, base_pg_outdir, outputs_dir]:
    if not os.path.exists(d):
        os.makedirs(d)


def make_storylines():
    test = pd.read_excel(os.path.join(ksl_env.slmmac_dir, r"storylines\blank_storylineWS120321.xlsx"), skiprows=2,
                         index_col=[0, 1, 2, 3], header=None)
    header_1 = test.iloc[0].ffill().values
    header_2 = test.iloc[1].values
    storylines = pd.DataFrame(index=pd.MultiIndex.from_arrays([default_storyline_time.year,
                                                               default_storyline_time.month], names=['year', 'month']),
                              columns=pd.MultiIndex.from_arrays([header_1, header_2]), data=test.iloc[3:].values)
    good_stories = list(set(storylines.columns.get_level_values(0)) - {'Storyline Name'})

    for s in sorted(good_stories):
        print(s)
        sl = storylines.loc[:, s].reset_index()
        assert sl.shape == (36, 5), f'shape problem with {s}'
        sl.loc[:, 'rest'] = pd.to_numeric(sl.loc[:, 'rest'])
        sl.loc[pd.isnull(sl.rest), 'rest'] = 50
        sl.loc[:, 'rest'] *= 1 / 100
        sl.loc[:, 'rest_per'] = sl.loc[:, 'rest']
        sl.loc[pd.isnull(sl.precip_class), 'precip_class'] = 'A'
        sl.loc[:, 'precip_class'] = sl.loc[:, 'precip_class'].str.replace('P', '').str.strip()
        sl.loc[pd.isnull(sl.temp_class) & (
            np.in1d(sl.month, [6, 7])), 'temp_class'] = 'C'  # todo defaults hard coded in...
        sl.loc[pd.isnull(sl.temp_class), 'temp_class'] = 'A'
        sl.loc[:, 'temp_class'] = sl.loc[:, 'temp_class'].str.replace('T', '').str.strip()
        map_storyline_rest(sl)
        s2 = s.replace('/', '-').replace('(', '').replace(')', '').replace(',', '')
        sl.to_csv(os.path.join(story_dir, f'{s2}.csv'))


def run_pasture_growth_mp():
    outdirs = [base_pg_outdir for e in os.listdir(story_dir)]
    paths = [os.path.join(story_dir, e) for e in os.listdir(story_dir)]
    run_full_model_mp(
        storyline_path_mult=paths,
        outdir_mult=outdirs,
        nsims_mult=1000,
        log_path=os.path.join(pgm_log_dir, 'lauras'),
        description_mult='a first run of Lauras storylines',
        padock_rest_mult=False,
        save_daily_mult=True,
        verbose=False

    )


def export_and_plot_data():
    export_all_in_pattern(base_outdir=outputs_dir,
                          patterns=[
                              os.path.join(base_pg_outdir, '*.nc'),
                              os.path.join(os.path.dirname(base_pg_outdir), 'baseline_sim_no_pad', '*.nc')
                          ])
    for sm in ['eyrewell-irrigated', 'oxford-dryland', 'oxford-irrigated']:
        paths = glob.glob(os.path.join(base_pg_outdir, f'*{sm}.nc'))
        for p in paths:
            outdir = os.path.join(outputs_dir, sm, 'plots')
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            data_paths = [p,
                          os.path.join(os.path.dirname(base_pg_outdir), 'baseline_sim_no_pad', f'0-baseline-{sm}.nc')]

            plot_sims(data_paths,
                      plot_ind=False, nindv=100, save_dir=outdir, show=False, figsize=(20, 20),
                      daily=False, ex_save=os.path.basename(p).replace('.nc', ''))


def get_laura_v2_pg_prob(site, mode):
    data = extract_additional_sims(story_dir, base_pg_outdir, 3)

    rename_dict = {f'{site}-{mode}_pg': 'pgr', f'{site}-{mode}_pgra': 'pgra', f'log10_prob_{mode}': 'prob'}

    data.loc[:, 'plotlabel'] = [f'{i}-{idv[0:10]}' for i, idv in data.loc[:, ['ID']].itertuples(True, None)]
    data = data.rename(columns=rename_dict)
    return data


if __name__ == '__main__':
    # todo I'm not re-running as I'm trying to move away from multi year storyies...
    make_st = False
    run = False
    plot_export = False
    pg_prob = True
    if make_st:
        make_storylines()
    if run:
        run_pasture_growth_mp()
    if plot_export:
        export_and_plot_data()
    if pg_prob:
        for mode, site in default_mode_sites:
            get_laura_v2_pg_prob(site=site, mode=mode)

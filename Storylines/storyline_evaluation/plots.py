"""
 Author: Matt Hanson
 Created: 15/04/2021 2:18 PM
 """
from Storylines.storyline_evaluation.plot_nyr_suite import *
from Storylines.storyline_runs.lauras_v2 import get_laura_v2_pg_prob
import ksl_env
from Storylines.storyline_building_support import default_mode_sites


def plot_1yr(save=False, close=True):
    for mode, site in default_mode_sites:
        outdir = None
        if save:
            outdir = os.path.join(ksl_env.slmmac_dir, 'random_scen_plots', f'1yr')
        plot_all_nyr(site, mode, nyr=1, outdir=outdir, other_scen=None, other_scen_lbl='other storylines',
                     pt_labels=False, close=close, num=100, step_size=0.1)

    if not save:
        plt.show()
    else:
        plt.close('all')


def plot_2yr_no_additional(save=False):
    for mode, site in default_mode_sites:
        print(f'{site} - {mode}')
        outdir = None
        if save:
            outdir = os.path.join(ksl_env.slmmac_dir, 'random_scen_plots', f'2yr')
        plot_all_nyr(site, mode, nyr=2, num=100, outdir=outdir, other_scen=None,
                     other_scen_lbl='other storylines',
                     pt_labels=False)

        if not save:
            plt.show()
        else:
            plt.close('all')

def plot_3yr_no_additional(save=False):
    for mode, site in default_mode_sites:
        print(f'{site} - {mode}')
        outdir = None
        if save:
            outdir = os.path.join(ksl_env.slmmac_dir, 'random_scen_plots', f'3yr')
        plot_all_nyr(site, mode, nyr=3, num=100, outdir=outdir, other_scen=None,
                     other_scen_lbl='other storylines',
                     pt_labels=False)

        if not save:
            plt.show()
        else:
            plt.close('all')


def plot_5yr_no_additional(save=False):
    for mode, site in default_mode_sites:
        print(f'{site} - {mode}')
        outdir = None
        if save:
            outdir = os.path.join(ksl_env.slmmac_dir, 'random_scen_plots', f'5yr')
        plot_all_nyr(site, mode, nyr=5, num=100, outdir=outdir, other_scen=None,
                     other_scen_lbl='other storylines',
                     pt_labels=False)

        if not save:
            plt.show()
        else:
            plt.close('all')


def plot_10yr_no_additional(save=False):
    for mode, site in default_mode_sites:
        print(f'{site} - {mode}')
        outdir = None
        if save:
            outdir = os.path.join(ksl_env.slmmac_dir, 'random_scen_plots', f'10yr')
        plot_all_nyr(site, mode, nyr=10, num=100, outdir=outdir, other_scen=None,
                     other_scen_lbl='other storylines',
                     pt_labels=False)

        if not save:
            plt.show()
        else:
            plt.close('all')


def plot_3yr_additional(get_add_fun, other_scen_lbl, pt_labels=True, save=False):
    for mode, site in default_mode_sites:
        print(f'{site} - {mode}')
        additional = get_add_fun(site, mode)
        additional.drop(14, axis=0, inplace=True)  # drop 14 as it is so improbable that it blows out system
        outdir = None
        if save:
            outdir = os.path.join(ksl_env.slmmac_dir, 'random_scen_plots', f'3yr_{other_scen_lbl}')
        plot_all_nyr(site, mode, num=100, nyr=3, outdir=outdir, other_scen=additional,
                     other_scen_lbl=other_scen_lbl,
                     pt_labels=pt_labels, step_size=0.1, close=True)

        if not save:
            plt.show()
        else:
            plt.close('all')


if __name__ == '__main__':
    # plot_1yr(True, True)
    # plot_3yr_additional(get_laura_v2_pg_prob, 'lauras_v2', pt_labels=True, save=True)
    plot_2yr_no_additional(True) #todo run
    # plot_3yr_no_additional(True)
    # plot_5yr_no_additional(True)
    # plot_10yr_no_additional(True)

    # todo plot with additional lauras sims for 1 and 2 year events

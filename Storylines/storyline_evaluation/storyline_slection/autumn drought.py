"""
 Author: Matt Hanson
 Created: 5/07/2021 5:01 PM
 """
from Storylines.storyline_evaluation.storyline_characteristics_for_impact import storyline_subclusters


def autumn_drought_1():
    storyline_subclusters(

        outdir=r"C:\Users\dumon\Downloads\autumn_drought1",
        lower_bound={
            'oxford-dryland': None,
            'eyrewell-irrigated': None,
            'oxford-irrigated': None,
        },
        upper_bound={
            'oxford-dryland': None,
            'eyrewell-irrigated': None,
            'oxford-irrigated': None,

        },

        state_limits={
            2: (['D'], '*', (0.5, 1)),
            3: (['D'], '*', (0.5, 1)),
            4: (['D'], '*', (0.5, 1)),

        },
        n_clusters=5,
        n_pcs=15,
        save_stories=True
    )


def autumn_drought_2():
    storyline_subclusters(

        outdir=r"C:\Users\dumon\Downloads\autumn_drought2",
        lower_bound={
            'oxford-dryland': None,
            'eyrewell-irrigated': None,
            'oxford-irrigated': None,
        },
        upper_bound={
            'oxford-dryland': None,
            'eyrewell-irrigated': None,
            'oxford-irrigated': None,

        },

        state_limits={
            2: (['D', 'A'], ['H', 'A'], (0.6, 1)),
            3: (['D', 'A'], ['H', 'A'], (0.6, 1)),
            4: (['D', 'A'], ['H', 'A'], (0.6, 1)),

        },
        n_clusters=10,
        n_pcs=15,
        save_stories=True
    )


def dry_summer():
    raise NotImplementedError # todo


if __name__ == '__main__':
    autumn_drought_1()

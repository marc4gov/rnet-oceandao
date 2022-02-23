import random

dataset_ratio = random.choice([0.3, 0.4, 0.5])
community_ratio = random.choice([0.3, 0.4, 0.5])
new_entrant_ratio = random.choice([0.3, 0.4, 0.5])
unsound_ratio = random.choice([0.3, 0.4, 0.5])

params = {
    # 'dataset_ratio': [dataset_ratio],
    # 'community_ratio': [community_ratio],
    # 'new_entrant_ratio': [new_entrant_ratio],
    # 'unsound_ratio': [unsound_ratio],
    # 'recurring_projects': [5],
    'projects_in_round': [20]
}


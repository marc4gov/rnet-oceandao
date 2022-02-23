"""
Model initial state.
"""

from model.parts.agents.util.treasury.oceanrounds import round11_stats

# round_stats = round11_stats
# projects = round_stats['granted']

genesis_state = {
    'dao_members': 200,
    'voters': 50,
    'stakers': 50,
    'builders': 50,
    'market_makers': 50,
    'grant_cap': 200,
    'treasury': 500,
    'projects': 20,
    'dataset_projects': 5,
    'unsound_projects': 0,
    'community_projects': 15,
    'new_projects': 20,
    'recurring_projects': 0,
    'existing_projects': 0,
    'experienced_projects': {'level 1': 0, 'level 2': 0, 'level 3': 0},
    'veteran_projects': 0,
    'round': 1,
}

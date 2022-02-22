"""
Model initial state.
"""

from model.parts.agents.util.treasury.oceanrounds import round11_stats

round_stats = round11_stats
projects = round_stats['granted']

genesis_state = {
    'dao_members': 200,
    'voters': 50,
    'stakers': 50,
    'builders': 50,
    'market_makers': 50,
    'grant_cap': 200,
    'treasury': 500,
    'projects': 20,
    'datasets': 5,
    'new_entrants': 10,
    'community_projects': 15,
    'unsound_projects': 0,
    'recurring_projects': 10,
    'round': 1,
}

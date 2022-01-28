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
    'market_makers': 10,
    'grant_cap': 200,
    'projects': projects,
    'yes_votes': 30,
    'no_votes': 10,
    'valuable_projects': 0,
    'unsound_projects': 0,
    'round': 1,
}

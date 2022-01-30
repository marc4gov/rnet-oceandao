"""
Partial state update block. 

Here the partial state update blocks are configurated by setting
- policies
- variables

for each state update block individually
"""
from .parts.polimechs.model1 import *

partial_state_update_block = [
    {
        'policies': {
            'grants_policy': grants_policy,
            'curation_policy': curation_policy,
            'participation_policy': participation_policy
        },
        'variables': {
            'grant_cap': update_grants,
            'community_projects': update_community_projects,
            'unsound_projects': update_unsound_projects,
            'new_entrants': update_new_entrants,
            'voters': update_voters,
            'stakers': update_stakers,
            'builders': update_builders,
            'market_makers': update_market_makers,
            'datasets': update_datasets,
            'dao_members': update_dao_members
        },
    },
    {
        'policies': {
            'projects_policy': projects_policy,
        },
        'variables': {
            'projects': update_projects,
            'round': update_round
        }
    }
]
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
            'projects_policy': projects_policy,
        },
        'variables': {
            'projects': update_projects,
            'community_projects': update_community_projects,
            'dataset_projects': update_dataset_projects,
            'unsound_projects': update_unsound_projects,
            'recurring_projects': update_recurring_projects,
            'veteran_projects': update_veteran_projects,
            'experienced_projects': update_experienced_projects,
            'existing_projects': update_existing_projects,
            'new_projects': update_new_projects,
            'round': update_round
        },
    },
    {
        'policies': {
            'curation_policy': curation_policy,
        },
        'variables': {
            'projects': update_projects,
            'community_projects': update_community_projects,
            'dataset_projects': update_dataset_projects,
            'unsound_projects': update_unsound_projects,
            'recurring_projects': update_recurring_projects,
            'veteran_projects': update_veteran_projects,
            'experienced_projects': update_experienced_projects,
            'existing_projects': update_existing_projects,
            'new_projects': update_new_projects,
            'round': update_round
        },
    },
    {
        'policies': {
            'participation_policy': participation_policy,
        },
        'variables': {
            'voters': update_voters,
            'stakers': update_stakers,
            'builders': update_builders,
            'market_makers': update_market_makers,
            'dao_members': update_dao_members,
        },
    },
    {
        'policies': {
            'grants_policy': grants_policy,
        },
        'variables': {
            'grant_cap': update_grants,
        },
    }
]
import random
import math

from model.parts.agents.util.treasury.oceanrounds import *

def grants_policy(params, step, sH, s):
    """
    Update the grants state.
    """
    current_timestep = len(sH)
    timestep_per_day = 1
    timestep_per_month = 30

    # adjust the grant CAP according to the amount of valuable projects in this round
    if (current_timestep % timestep_per_month) == 0:
      value_ratio = (s['datasets'] - s['unsound_projects']) / s['projects']
      return ({'grant_cap': math.floor((1 + value_ratio) * s['grant_cap'])})

    return ({'grant_cap': s['grant_cap'] })

def projects_policy(params, step, sH, s):
    """
    Update the projects state.
    """
    current_timestep = len(sH)
    timestep_per_day = 1
    timestep_per_month = 30
    round = s['round']
    projects = s['projects']

    # new Grants round
    if (current_timestep % timestep_per_month) == 0:
      round += 1
      round_stats = 28
      if round % 3 == 0:
        round_stats = 20
      if round % 3 == 1:
        round_stats = 24
      projects = round_stats
      return ({
        'projects': projects,
        'round': round
      })

    return({
        'projects': projects,
        'round': round
    })
    
def curation_policy(params, step, sH, s):
    """
    How to assess projects?
    """
    current_timestep = len(sH)
    timestep_per_week = 7
    timestep_per_month = 30

    # # new Grants round
    # if (current_timestep % timestep_per_month) == 0:
    #   return ({
    #       'yes_votes': math.floor(0.8 * s['voters']),
    #       'no_votes': math.floor(0.2 * s['voters']),
    #   })

    # every week we assess the projects to either promising or not and adjust the project properties and vote signal accordingly

    # if (current_timestep % timestep_per_week) == 0:
    dataset = random.choice(params['dataset_ratio'])
    community = random.choice(params['community_ratio'])
    new_entrant = random.choice(params['new_entrant_ratio'])
    unsound = random.choice(params['unsound_ratio'])
    total = dataset + community + new_entrant + unsound
    total = total if total > 0 else 1
    dataset_weight = dataset/total
    community_weight = community/total
    new_entrant_weight = new_entrant/total
    unsound_weight = unsound/total
    datasets = math.floor(dataset_weight * s['projects'])
    new_entrants = math.floor(new_entrant_weight * s['projects'])
    community_projects = math.floor(community_weight * s['projects'])
    unsound_projects = math.floor(unsound_weight * s['projects'])

    return ({
        'unsound_projects': unsound_projects,
        'datasets': datasets,
        'community_projects': community_projects,
        'new_entrants': new_entrants
    })
    
    # return ({
    #   'unsound_projects': s['unsound_projects'],
    #   'datasets': s['datasets'],
    #   'community_projects': s['community_projects'],
    #   'new_entrants': s['new_entrants']
    # })
    

def participation_policy(params, step, sH, s):
    """
    Update the projects state.
    """
    current_timestep = len(sH)
    timestep_per_day = 1
    timestep_per_month = 30
    datasets = s['datasets']
    community_projects = s['community_projects']
    new_entrants = s['new_entrants']
    unsound_projects = s['unsound_projects']

    # new Grants round
    if (current_timestep % timestep_per_month) == 0:
      if s['voters'] >= s['dao_members']:
        return ({
          'voters': s['voters'],
          'stakers': s['stakers'],
          'market_makers': s['market_makers'],
          'builders': s['builders'],
          'dao_members': s['voters']
        })
      else:
        return ({
          'voters': s['voters'],
          'stakers': s['stakers'],
          'market_makers': s['market_makers'],
          'builders': s['builders'],
          'dao_members': math.floor(s['dao_members'] - 0.1 * s['voters'])
        })

    projects = s['projects'] if s['projects'] > 0 else 1
    value_ratio1 = (datasets - unsound_projects) / projects
    value_ratio2 = (community_projects - unsound_projects) / projects
    value_ratio3 = (new_entrants - unsound_projects) / projects
    voters = math.floor((1 + (value_ratio1 + value_ratio2 + value_ratio3)/3) * s['voters'])
    market_makers = math.floor((1 + value_ratio2) * s['market_makers'])
    stakers = math.floor((1 + value_ratio1) * s['stakers'])
    builders = math.floor((1 + value_ratio3) * s['builders'])
    return ({
      'voters': voters,
      'stakers': stakers,
      'market_makers': market_makers,
      'builders': builders,
      'dao_members': s['dao_members']
    })


def update_grants(params, step, sH, s, _input):
  return ('grant_cap', _input['grant_cap'])

def update_projects(params, step, sH, s, _input):
  return ('projects', _input['projects'])

def update_round(params, step, sH, s, _input):
  return ('round', _input['round'])

def update_community_projects(params, step, sH, s, _input):
  return ('community_projects', _input['community_projects'])

def update_unsound_projects(params, step, sH, s, _input):
  return ('unsound_projects', _input['unsound_projects'])

def update_yes_votes(params, step, sH, s, _input):
  return ('yes_votes', _input['yes_votes'])

def update_no_votes(params, step, sH, s, _input):
  return ('no_votes', _input['no_votes'])

def update_voters(params, step, sH, s, _input):
  return ('voters', _input['voters'])

def update_stakers(params, step, sH, s, _input):
  return ('stakers', _input['stakers'])

def update_builders(params, step, sH, s, _input):
  return ('builders', _input['builders'])

def update_market_makers(params, step, sH, s, _input):
  return ('market_makers', _input['market_makers'])

def update_dao_members(params, step, sH, s, _input):
  return ('dao_members', _input['dao_members'])
  
def update_datasets(params, step, sH, s, _input):
  return ('datasets', _input['datasets'])

def update_new_entrants(params, step, sH, s, _input):
  return ('new_entrants', _input['new_entrants'])
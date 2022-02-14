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
    unsound_projects = s['unsound_projects']
    datasets = s['datasets']
    community_projects = s['community_projects']
    new_entrants = s['new_entrants']
    projects = s['projects']

    # new Grants round
    if (current_timestep % timestep_per_month) == 0:
      datasets = math.floor(params['dataset_ratio'] * projects)
      new_entrants = math.floor(params['community_ratio'] * projects)
      community_projects = math.floor(params['new_entrant_ratio'] * projects)
      unsound_projects = math.floor(params['unsound_ratio'] * projects)
      return ({
          'unsound_projects': unsound_projects,
          'datasets': datasets,
          'community_projects': community_projects,
          'new_entrants': new_entrants
      })
    # every week we assess the projects to either promising or not and adjust the project properties and vote signal accordingly

    # if (current_timestep % timestep_per_week) == 0:

    total = sum([datasets, new_entrants, community_projects, unsound_projects])
    # print("Total", total)
    size = math.floor(total/4)
    weights = list(np.random.normal(0.1,0.1, total))
    dataset_weights = random.sample(weights, size)
    new_entrant_weights = random.sample(weights, size)
    community_projects_weights = random.sample(weights, size)
    # weights = [e for e in weights if e not in community_projects_weights]
    unsound_projects_weights = random.sample(weights, size)

    datasets = sum(dataset_weights) * total
    new_entrants = sum(new_entrant_weights) * total
    community_projects = sum(community_projects_weights) * total
    unsound_projects = sum(unsound_projects_weights) * total
    new_total = sum([datasets, new_entrants, community_projects, unsound_projects])
    new_total = new_total if new_total > 0 else 1
    ratio = total/new_total
    datasets = math.floor(datasets * ratio)
    new_entrants = math.floor(new_entrants * ratio)
    community_projects = math.floor(community_projects * ratio)
    unsound_projects = math.floor(unsound_projects * ratio)
    new_total = sum([datasets, new_entrants, community_projects, unsound_projects])
    diff = new_total - total
    # print("Diff: ", diff)
    biggest = max([datasets, new_entrants, community_projects, unsound_projects])
    if biggest == datasets:
      datasets -= diff
    if biggest == new_entrants:
      new_entrants -= diff
    if biggest == community_projects:
      community_projects -= diff
    if biggest == unsound_projects:
      unsound_projects -= diff
    
    return ({
        'unsound_projects': unsound_projects,
        'datasets': datasets,
        'community_projects': community_projects,
        'new_entrants': new_entrants
    })
    

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

    prev_datasets = sH[current_timestep - 1][0]['datasets']
    prev_new_entrants = sH[current_timestep - 1][0]['new_entrants']
    prev_community_projects = sH[current_timestep - 1][0]['community_projects']
    prev_unsound_projects = sH[current_timestep - 1][0]['unsound_projects']

    total = sum([datasets, new_entrants, community_projects, unsound_projects])
    prev_total = sum([prev_datasets, prev_new_entrants, prev_community_projects, prev_unsound_projects])

    # new Grants round
    if (current_timestep % timestep_per_month) == 0:
      if s['voters'] >= sH[current_timestep - timestep_per_month][0]['voters']:
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

    prev_datasets = prev_datasets if prev_datasets > 0 else 1
    value_ratio1 = (datasets - prev_datasets) / prev_datasets

    prev_community_projects = prev_community_projects if prev_community_projects > 0 else 1
    value_ratio2 = (community_projects - prev_community_projects) / prev_community_projects

    prev_new_entrants = prev_new_entrants if prev_new_entrants > 0 else 1
    value_ratio3 = (new_entrants - prev_new_entrants) / prev_new_entrants

    prev_unsound_projects = prev_unsound_projects if prev_unsound_projects > 0 else 1
    value_ratio4 = (unsound_projects - prev_unsound_projects) / prev_unsound_projects
    
    voters = math.ceil((1 + (value_ratio1 + value_ratio2 + value_ratio3 - value_ratio4)/4) * s['voters'])
    market_makers = math.ceil((1 + value_ratio2) * s['market_makers'])
    stakers = math.ceil((1 + value_ratio1) * s['stakers'])
    builders = math.ceil((1 + value_ratio3) * s['builders'])
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
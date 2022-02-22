import random
import math

from numpy import cumsum

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
      value_ratio = (s['recurring_projects'] + s['new_entrants'] - s['unsound_projects']) / s['projects']
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
      mu, sigma = params['projects_in_round'], 3
      x = np.random.normal(mu,sigma,10)
      projects = math.floor(random.choice(list(x)))
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
    recurring_projects = s['recurring_projects']
    projects = s['projects']
    round = s['round']

    # new Grants round
    if (current_timestep % timestep_per_month) == 0:
      new_entrants = math.floor(params['new_entrant_ratio'] * projects)
      recurring_projects = math.floor(params['recurring_projects'] * projects)
      unsound_projects = projects - (new_entrants + recurring_projects)

      community_projects = math.floor(params['community_ratio'] * (new_entrants + recurring_projects))
      datasets = math.floor(params['dataset_ratio'] * (new_entrants + recurring_projects))
      
      return ({
          'unsound_projects': unsound_projects,
          'datasets': datasets,
          'community_projects': community_projects,
          'new_entrants': new_entrants,
          'recurring_projects': recurring_projects
      })

    # every week we assess the projects to either promising or unsound and adjust the project categories
    if (current_timestep % timestep_per_week) == 0:
      # chance that projects turn unsound (the later in the round, the higher)
      round = round if round > 0 else 1
      mu, sigma = 0.8 * current_timestep/(round * 30), 0.2
      x = np.random.normal(mu,sigma,5)
      unsound_ratio = random.choice(list(x))
      if unsound_ratio > 0.5:
        unsound = math.floor((1 - unsound_ratio) * new_entrants)
        new_entrants -= unsound
        unsound_projects += unsound
      unsound_ratio = random.choice(list(x))
      # recurring projects have less chance of failure
      if unsound_ratio > 0.7:
        unsound = math.floor((1 - unsound_ratio) * recurring_projects)
        recurring_projects -= unsound
        unsound_projects += unsound

      diff = unsound_projects - s['unsound_projects']
      while diff > 0:
        datasets -= 1
        diff -= 1
        if diff == 0: break
        community_projects -=1
        diff -= 1
    
    return ({
        'unsound_projects': unsound_projects,
        'datasets': datasets,
        'community_projects': community_projects,
        'new_entrants': new_entrants,
        'recurring_projects': recurring_projects
    })
    

def participation_policy(params, step, sH, s):
    """
    Update the projects state.
    """
    current_timestep = len(sH)
    timestep_per_week = 7
    timestep_per_month = 30
    datasets = s['datasets']
    community_projects = s['community_projects']
    new_entrants = s['new_entrants']
    recurring_projects = s['recurring_projects']
    unsound_projects = s['unsound_projects']

    # new Grants round
    if (current_timestep % timestep_per_month) == 0:
      if s['voters'] >= sH[current_timestep - timestep_per_month][0]['voters']:
        return ({
          'voters': s['voters'],
          'stakers': s['stakers'],
          'market_makers': s['market_makers'],
          'builders': s['builders'],
          'dao_members': math.floor(s['dao_members'] + 0.1 * s['voters'])
        })
      else:
        return ({
          'voters': s['voters'],
          'stakers': s['stakers'],
          'market_makers': s['market_makers'],
          'builders': s['builders'],
          'dao_members': math.floor(s['dao_members'] - 0.1 * s['voters'])
        })

    if (current_timestep % timestep_per_week) == 0:
      prev_datasets = sH[current_timestep - timestep_per_week][0]['datasets']
      prev_new_entrants = sH[current_timestep - timestep_per_week][0]['new_entrants']
      prev_community_projects = sH[current_timestep - timestep_per_week][0]['community_projects']
      prev_recurring_projects = sH[current_timestep - timestep_per_week][0]['recurring_projects']
      prev_unsound_projects = sH[current_timestep - timestep_per_week][0]['unsound_projects']

      prev_datasets = prev_datasets if prev_datasets > 0 else 1
      value_ratio_dataset = (datasets - prev_datasets) / prev_datasets

      prev_community_projects = prev_community_projects if prev_community_projects > 0 else 1
      value_ratio_community = (community_projects - prev_community_projects) / prev_community_projects

      prev_new_entrants = prev_new_entrants if prev_new_entrants > 0 else 1
      value_ratio_new_entrants = (new_entrants - prev_new_entrants) / prev_new_entrants

      prev_recurring_projects = prev_recurring_projects if prev_recurring_projects > 0 else 1
      value_ratio_recurring = (recurring_projects - prev_recurring_projects) / prev_recurring_projects

      prev_unsound_projects = prev_unsound_projects if prev_unsound_projects > 0 else 1
      value_ratio_unsound = (unsound_projects - prev_unsound_projects) / prev_unsound_projects
    
      voters = math.ceil((1 + (value_ratio_recurring + value_ratio_new_entrants - value_ratio_unsound)/3) * s['voters'])
      market_makers = math.ceil((1 + (value_ratio_community + value_ratio_dataset)/2) * s['market_makers'])
      stakers = math.ceil((1 + value_ratio_dataset) * s['stakers'])
      builders = math.ceil((1 + value_ratio_new_entrants) * s['builders'])
      return ({
        'voters': voters,
        'stakers': stakers,
        'market_makers': market_makers,
        'builders': builders,
        'dao_members': sum([voters, stakers, market_makers, builders])
      })

    return ({
      'voters': s['voters'],
      'stakers': s['stakers'],
      'market_makers': s['market_makers'],
      'builders': s['builders'],
      'dao_members': sum([s['voters'], s['stakers'],  s['market_makers'], s['builders']])
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
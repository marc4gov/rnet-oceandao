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
      value_ratio = (s['valuable_projects'] - s['unsound_projects']) / s['projects']
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
      round_stats = round11_stats
      if round % 3 == 0:
        round_stats = round12_stats
      if round % 3 == 1:
        round_stats = round13_stats
      projects = round_stats['granted']
      value_factor = random.choice([0.3, 0.4, 0.5, 0.6, 0.7])

      return ({
        'projects': projects,
        'valuable_projects': math.floor(value_factor * projects),
        'unsound_projects': math.floor((1-value_factor) * projects),
        'round': round
      })

    return({
        'projects': projects,
    })
    
def curation_policy(params, step, sH, s):
    """
    How to assess projects?
    """
    current_timestep = len(sH)
    timestep_per_week = 7
    timestep_per_month = 30

    # new Grants round
    if (current_timestep % timestep_per_month) == 0:

      return ({
          'yes_votes': math.floor(0.8 * s['voters']),
          'no_votes': math.floor(0.2 * s['voters']),
      })

    # every week we assess the projects to either promising or not and adjust the project properties and vote signal accordingly

    if (current_timestep % timestep_per_week) == 0:
      valuable = random.choice(params['dataset_ratio'])
      if valuable > 0.5:
        valuable_increment = 1
      else:
        valuable_increment = -1
      unsound = random.choice(params['unsound_ratio'])
      if unsound > 0.5:
        unsound_increment = 1
      else:
        unsound_increment = -1

      projects = s['projects'] if s['projects'] > 0 else 1
      yes_votes = s['yes_votes'] if s['yes_votes'] > 0 else 1 # divison by zero hack
      no_votes = s['no_votes'] if s['no_votes'] > 0 else 1
      value_ratio = (valuable - unsound) / projects
      
      return ({
          'valuable_projects': s['valuable_projects'] + valuable_increment,
          'unsound_projects': s['unsound_projects'] + unsound_increment,
          'yes_votes': math.floor(yes_votes * (1 + value_ratio)),
          'no_votes': math.floor(no_votes * (1 - value_ratio)),
      })
    


def participation_policy(params, step, sH, s):
    """
    Update the projects state.
    """
    current_timestep = len(sH)
    timestep_per_day = 1
    timestep_per_month = 30

    # new Grants round
    if (current_timestep % timestep_per_month) == 0:
      if s['voters'] >= s['dao_members']:
        return ({
          'voters': s['voters'],
          'dao_members': s['voters']
        })
      else:
        return ({
          'voters': s['voters'],
          'dao_members': math.floor(s['dao_members'] - 0.1 * s['voters'])
        })

    unsound_projects = s['unsound_projects'] if s['unsound_projects'] > 0 else 1
    valuable_projects = s['valuable_projects'] if s['valuable_projects'] > 0 else 1
    projects = s['projects'] if s['projects'] > 0 else 1
    value_ratio = (valuable_projects - unsound_projects) / projects
    voters = math.floor((1 + value_ratio) * s['voters'])
    return ({
      'voters': voters,
      'dao_members': s['dao_members']
    })


def update_grants(params, step, sH, s, _input):
  return ('grant_cap', _input['grant_cap'])

def update_projects(params, step, sH, s, _input):
  return ('projects', _input['projects'])

def update_valuable_projects(params, step, sH, s, _input):
  return ('valuable_projects', _input['valuable_projects'])

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
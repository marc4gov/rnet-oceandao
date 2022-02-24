import random
import math

from numpy import cumsum

from model.parts.agents.util.treasury.oceanrounds import *

# Funding tiers from Ocean DAO Wiki

# [1 - New Project :fish:]
# Funding Ceiling: $3k USD
# Requires: No one in your project has ever received a grant from OceanDAO. Open to all.
# Benefits: Earmarked. Receive feedback during application process. Introduced to related projects.

# [2 - Existing Project 🐠]
# Funding Ceiling: $10k USD
# Requires: You have completed 1 or more grants.
# Benefits: Same as above. Receive promotion via Newsletter, Twitter, and other channels.

# [3 - Experienced Project :dolphin:]
# Funding Ceiling: $20k USD
# Requires: You have completed 2 or more grants.

# [4 - Veteran Project :whale2:]
# Funding Ceiling: $35k USD
# Requires: You have completed 5 or more grants.

def grants_policy(params, step, sH, s):
    """
    Update the grants cap.
    """
    current_timestep = len(sH)
    timestep_per_day = 1
    timestep_per_month = 30

    new_projects = s['new_projects']
    veteran_projects = s['veteran_projects']
    experienced_projects = s['experienced_projects']
    existing_projects = s['existing_projects']

    # adjust the grant CAP according to the amount of valuable projects in this round
    if (current_timestep % timestep_per_month) == 0:

      exp_projects = sum([experienced_projects['level 1'], experienced_projects['level 2'], experienced_projects['level 3']])
      grant_cap = sum([new_projects * 3, existing_projects * 10, exp_projects * 20, veteran_projects * 35])
      return ({'grant_cap': grant_cap })

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
    recurring_projects = s['recurring_projects']
    new_projects = s['new_projects']
    veteran_projects = s['veteran_projects']
    experienced_projects = s['experienced_projects']
    existing_projects = s['existing_projects']
    dataset_projects = s['dataset_projects']
    community_projects = s['community_projects']
    unsound_projects = s['unsound_projects']

    # new Grants round
    if (current_timestep % timestep_per_month) == 0:
      round += 1
      unsound_projects = 0
      np.random.seed(1234)
      mu, sigma = params['projects_in_round'], 2
      x = np.random.normal(mu,sigma,5)
      projects = math.floor(random.choice(list(x)))
      
      # determine the distribution of recurring projects
      if recurring_projects == 0: # only in first round
        x = np.random.normal(0.5,0.05,5)
        recurring_projects = math.ceil(random.choice(list(x)) * projects)
        existing_projects = recurring_projects
      else: # around 30% chance projects promote, 50% chance they dissappear altogether, chance is decreasing with maturity
        for i in range(s['new_projects']):
          x = random.choice(list(np.random.normal(0.3,0.05,5)))
          if random.random() < x:
            existing_projects += 1
            new_projects -= 1
        for i in range(s['existing_projects']):
          x = random.choice(list(np.random.normal(0.3,0.05,5)))
          if random.random() < x:
            experienced_projects['level 1'] += 1
            existing_projects -= 1
          if random.random() > 0.5:
            existing_projects -= 1
        for i in range(s['experienced_projects']['level 1']):
          x = random.choice(list(np.random.normal(0.3,0.05,5)))
          if random.random() < x:
            experienced_projects['level 2'] += 1
            experienced_projects['level 1'] -= 1
          if random.random() > 0.6:
            experienced_projects['level 1'] -= 1
        for i in range(s['experienced_projects']['level 2']):
          x = random.choice(list(np.random.normal(0.25,0.05,5)))
          if random.random() < x:
            experienced_projects['level 3'] += 1
            experienced_projects['level 2'] -= 1
          if random.random() > 0.7:
            experienced_projects['level 2'] -= 1
        for i in range(s['experienced_projects']['level 3']):
          x = random.choice(list(np.random.normal(0.25,0.05,5)))
          if random.random() < x:
            veteran_projects += 1
            experienced_projects['level 3'] -= 1
          if random.random() > 0.8:
            experienced_projects['level 3'] -= 1
        for i in range(s['veteran_projects']): #  veteran projects dissappear in time with around 20% chance
          x = random.choice(list(np.random.normal(0.2,0.05,5)))
          if random.random() < x:
            veteran_projects -= 1
        # account for the changes
        exp_projects = sum([experienced_projects['level 1'], experienced_projects['level 2'], experienced_projects['level 3']])
        recurring_projects = sum([veteran_projects,exp_projects,existing_projects])

      # account for parameter sweep obligations
      new_projects = math.ceil(params['new_projects_ratio'] * projects)
      projects_n = recurring_projects + new_projects
      diff = projects_n - projects
      existing_projects -= diff
      if existing_projects < 0: existing_projects = 0
      
      # determine the distribution of dataset projects (assuming around 50% with 20% standard deviation)

      x = np.random.normal(0.5,0.2, 5)
      dataset_projects = math.floor(random.choice(list(x)) * projects)
      community_projects = projects - dataset_projects

      return ({
        'projects': projects,
        'recurring_projects': recurring_projects,
        'new_projects': new_projects,
        'veteran_projects': veteran_projects,
        'experienced_projects': experienced_projects,
        'existing_projects': existing_projects,
        'dataset_projects': dataset_projects,
        'community_projects': community_projects,
        'unsound_projects': unsound_projects,
        'round': round
      })

    return ({
      'projects': projects,
      'recurring_projects': recurring_projects,
      'new_projects': new_projects,
      'veteran_projects': veteran_projects,
      'experienced_projects': experienced_projects,
      'existing_projects': existing_projects,
      'dataset_projects': dataset_projects,
      'community_projects': community_projects,
      'unsound_projects': unsound_projects,
      'round': round
    })

def curation_policy(params, step, sH, s):
    """
    How to assess projects?
    """
    current_timestep = len(sH)
    timestep_per_week = 7
    timestep_per_month = 30
    round = s['round']
    projects = s['projects']
    recurring_projects = s['recurring_projects']
    new_projects = s['new_projects']
    veteran_projects = s['veteran_projects']
    experienced_projects = s['experienced_projects']
    existing_projects = s['existing_projects']
    dataset_projects = s['dataset_projects']
    community_projects = s['community_projects']
    unsound_projects = s['unsound_projects']
    

    # print("Projects in curation_policy: ", projects)
    # print("Round: ", round)

    # every day we assess the projects to either promising or unsound and adjust the project categories
    # chances that projects turn unsound: the later in the round, the higher
    np.random.seed(1234)

    mu, sigma = 0.8 * (current_timestep - (round - 1) * timestep_per_month)/timestep_per_month, 0.1
    x = np.random.normal(mu,sigma,5)
    unsound_chance = random.choice(list(x))
    if unsound_chance > 0.65:
      if new_projects > 0:
        new_projects -= 1
        unsound_projects += 1
    unsound_chance = random.choice(list(x))
    # recurring projects have slightly less chance of failure
    if unsound_chance > 0.8:
      if recurring_projects > 0:
        recurring_projects -= 1
        # kind of recurring project determines chance of getting unsound
        x = random.choice([1,1,1,1,1,2,2,2,3,3])
        if x == 1:
          if existing_projects > 0:
            existing_projects -= 1
        if x == 2:
          i = random.choice([1,2,3])
          if experienced_projects['level ' + str(i)] > 0:
            experienced_projects['level ' + str(i)] -= 1
        if x == 3:
          if veteran_projects > 0:
            veteran_projects -= 1
        unsound_projects += 1
    unsound_increase = unsound_projects - s['unsound_projects']
    dataset_unsound = random.choice([True, False])
    if dataset_unsound:
      dataset_projects -= unsound_increase
    else:
      community_projects -= unsound_increase

    return ({
      'projects': projects,
      'recurring_projects': recurring_projects,
      'new_projects': new_projects,
      'veteran_projects': veteran_projects,
      'experienced_projects': experienced_projects,
      'existing_projects': existing_projects,
      'dataset_projects': dataset_projects,
      'community_projects': community_projects,
      'unsound_projects': unsound_projects,
      'round': round
    })
    

def participation_policy(params, step, sH, s):
    """
    Update the projects state.
    """
    current_timestep = len(sH)
    timestep_per_week = 7
    timestep_per_month = 30
    projects = s['projects']
    unsound_projects = s['unsound_projects']
    recurring_projects = s['recurring_projects']
    new_projects = s['new_projects']
    veteran_projects = s['veteran_projects']
    experienced_projects = s['experienced_projects']
    existing_projects = s['existing_projects']
    dataset_projects = s['dataset_projects']
    community_projects = s['community_projects']

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

    # every 3 days we determine the growth rate of all kinds of projects
    if (current_timestep % 3) == 0:
      prev_datasets = sH[current_timestep - 3][0]['dataset_projects']
      prev_new_entrants = sH[current_timestep - 3][0]['new_projects']
      prev_community_projects = sH[current_timestep - 3][0]['community_projects']
      prev_recurring_projects = sH[current_timestep - 3][0]['recurring_projects']
      prev_unsound_projects = sH[current_timestep - 3][0]['unsound_projects']
      prev_existing_projects = sH[current_timestep - 3][0]['existing_projects']
      prev_veteran_projects = sH[current_timestep - 3][0]['veteran_projects']
      

      prev_datasets = prev_datasets if prev_datasets > 0 else 1
      growth_ratio_dataset = (dataset_projects - prev_datasets) / prev_datasets

      prev_community_projects = prev_community_projects if prev_community_projects > 0 else 1
      growth_ratio_community = (community_projects - prev_community_projects) / prev_community_projects

      prev_new_entrants = prev_new_entrants if prev_new_entrants > 0 else 1
      growth_ratio_new_entrants = (new_projects - prev_new_entrants) / prev_new_entrants

      prev_recurring_projects = prev_recurring_projects if prev_recurring_projects > 0 else 1
      growth_ratio_recurring = (recurring_projects - prev_recurring_projects) / prev_recurring_projects

      prev_existing_projects = prev_existing_projects if prev_existing_projects > 0 else 1
      growth_ratio_existing = (existing_projects - prev_existing_projects) / prev_existing_projects

      prev_unsound_projects = prev_unsound_projects if prev_unsound_projects > 0 else 1
      growth_ratio_unsound = (unsound_projects - prev_unsound_projects) / prev_unsound_projects
    
      # determine the change in stakeholders
      voters = math.floor((1 + 0.1 * (growth_ratio_recurring + growth_ratio_new_entrants - growth_ratio_unsound)/3) * s['voters'])
      growth_ratio_market_makers = 0.1 * (growth_ratio_community * 2 + growth_ratio_dataset -  growth_ratio_unsound)/3
      market_makers = math.floor((1 + 0.1 * growth_ratio_market_makers) * s['market_makers'])
      stakers = math.floor((1 + 0.1 * (growth_ratio_dataset - growth_ratio_unsound)/2) * s['stakers'])
      builders = math.floor((1 + 0.1 * growth_ratio_recurring) * s['builders'])

      stakers = math.floor((1 + 0.2 * (growth_ratio_market_makers * 0.8)) * stakers)

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
      'dao_members': sum([s['voters'], s['stakers'], s['market_makers'], s['builders']])
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
  
def update_dataset_projects(params, step, sH, s, _input):
  return ('dataset_projects', _input['dataset_projects'])

def update_new_projects(params, step, sH, s, _input):
  return ('new_projects', _input['new_projects'])

def update_recurring_projects(params, step, sH, s, _input):
  return ('recurring_projects', _input['recurring_projects'])

def update_veteran_projects(params, step, sH, s, _input):
  return ('veteran_projects', _input['veteran_projects'])

def update_experienced_projects(params, step, sH, s, _input):
  return ('experienced_projects', _input['experienced_projects'])

def update_existing_projects(params, step, sH, s, _input):
  return ('existing_projects', _input['existing_projects'])
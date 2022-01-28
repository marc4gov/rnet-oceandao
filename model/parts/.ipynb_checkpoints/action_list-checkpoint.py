# Behaviors
# from hydra_multi_class.model.sys_params import ACTION_LISTimport numpy as np
import random
import math

# Set numpy random seed for replication
np.random.seed(42)

def actionDecoder(params, step, history, prev_state):
    '''
    In this simplified model of Uniswap, we have not modeled user behavior. Instead, we map events to actions. Depending on the input system parameters 'params' a given action sequence is induced.
    '''
    
    action = {
        'q_sold': 0,     # q to r swap
        'ri_sold': 0,     # r to q swap
        'ri_deposit': 0,   # add liq
        'q_deposit': 0,  # if symmetric add liq
        'Si_burn': 0,    # remove liq    
        'action_id' : str(),
        'agent_id' : 0,
        'asset_id' : str(),
        'direction': str(),
        'direction_q': str()
    }
    

    timestep = prev_state['timestep']
    pool = prev_state['pool']
    action['asset_id'] = prev_state['asset_random_choice']
    action['q_sold'] = prev_state['trade_random_size'] * 2
    action['ri_sold'] = prev_state['trade_random_size']
    action['direction_q'] = prev_state['trade_random_direction']
 

    ############# CREATE AGENT ID's ################    
    
    ############# WHITE POOL AGENTS ########################
    agent0_id = 0
    agent1_id = 1
    agent2_id = 2
    agent3_id = 3
    agent4_id = 4
    ############# WHITE & GREY POOL AGENTS #################
    agent5_id = 5    
    agent6_id = 6
    agent7_id = 7
    agent8_id = 8
    agent9_id = 9
    ############# GREY POOL AGENTS #########################
    agent10_id = 10
    agent11_id = 11      
    agent12_id = 12
    agent13_id = 13
    agent14_id = 14
    agent15_id = 15    
    agent16_id = 16
    agent17_id = 17
    agent18_id = 18
    agent19_id = 19    
    agent20_id = 20
    agent21_id = 21      
    agent22_id = 22
    agent23_id = 23
    agent24_id = 24  
    
    
    if params['exo_random_sequence'] == 'on':
        agent3_id = 2
    ############# CREATE AGENT ID's ################

   
    ############## SET RANDOM SEQUENCE ##################    
    if params['exo_random_sequence'] == 'on':
        
        if timestep == 10:
            params['exo_liq'] = 'test_add'
            params['exo_trade'] = 'pass'
            #params['exo_trade'] = random.choice(['test_r_for_r'])
            action['asset_id'] = random.choice(['i'])
            action['purchased_asset_id'] = 'N/A'

        elif timestep == 90:            
            params['exo_liq'] = 'test_remove'
            params['exo_trade'] = 'pass'
            action['asset_id'] = random.choice(['i'])
            action['purchased_asset_id'] = 'N/A'
    
        else:
            
            #params['exo_liq'] = 'test_remove'
            params['exo_liq'] = 'pass' 
            #params['exo_trade'] = random.choice(['pass'])
            #params['exo_trade'] = random.choice(['test_q_for_r', 'test_r_for_q'])
            params['exo_trade'] = prev_state['trade_random_direction']
            #action['asset_id'] = random.choice(['i'])
            action['asset_id'] = prev_state['asset_random_choice']
      ############## SET RANDOM SEQUENCE ##################                    
        
        
#########################################################################################

                     # AGENT ACTIONS #
    
#########################################################################################
        
 ########## TEMP TEST SELL Q FOR R ############    
    ####### AGENT 0 ######################
    if params['exo_trade'] == 'test_q_for_r':
        action['action_id'] = 'Ri_Purchase'
        action['purchased_asset_id'] = 'i'
        P = pool.get_price(action['purchased_asset_id']) 
        action['q_sold'] = prev_state['trade_random_size'] * 2
        action['agent_id'] = prev_state['uni_agents']['m'][agent0_id]
        if action['asset_id'] == 'j':
            action['agent_id'] = prev_state['uni_agents']['m'][agent0_id]
            action['purchased_asset_id'] = 'j'
            P = pool.get_price(action['purchased_asset_id']) 
            action['q_sold'] = prev_state['trade_random_size'] * 2
    ###############################################

########## TEMP TEST SELL R FOR Q ############
    ####### AGENT 1 ######################
    if params['exo_trade'] == 'test_r_for_q':
        action['ri_sold'] = prev_state['trade_random_size']
        action['action_id'] = 'Q_Purchase'
        action['purchased_asset_id'] = 'q'
        P = pool.get_price('i') 
        action['ri_sold'] = prev_state['trade_random_size']         
        action['agent_id'] = prev_state['uni_agents']['m'][agent1_id]
        if action['asset_id'] == 'j':
            P = pool.get_price(action['asset_id'])             
            action['agent_id'] = prev_state['uni_agents']['m'][agent1_id] 
            action['ri_sold'] = prev_state['trade_random_size'] 
            action['purchased_asset_id'] = 'q'

    ###############################################

    ########## TEMP TEST ADD LIQ ############
    ####### AGENT 2 ######################
    if params['exo_liq'] == 'test_add':
        action['ri_deposit'] = 5000
        action['action_id'] = 'AddLiquidity'
        action['purchased_asset_id'] = 'N/A'

        if timestep == 10:
            action['ri_deposit'] = 50000
            action['agent_id'] = prev_state['uni_agents']['m'][agent2_id]
        else:
            action['agent_id'] = prev_state['uni_agents']['m'][agent2_id] 

        if action['asset_id'] == 'j':
            action['agent_id'] = prev_state['uni_agents']['m'][agent2_id] 
            action['ri_deposit'] = 5000
            action['purchased_asset_id'] = 'N/A'

    ###############################################

    ########## TEMP TEST REMOVE LIQ ############
    ####### AGENT 3 ######################
    if params['exo_liq'] == 'test_remove':
        print(prev_state['hydra_agents']['s_i'][agent3_id])
        # action['UNI_burn'] = prev_state['uni_agents']['s_i'][agent4_id] #* 0.001
        action['purchased_asset_id'] = 'N/A'
        action['action_id'] = 'RemoveLiquidity'
        if timestep == 90:            
            action['agent_id'] = prev_state['hydra_agents']['m'][agent3_id]
            #action['UNI_burn'] = 500 #prev_state['hydra_agents']['s_i'][agent3_id] # starting value subtract - 150000
            action['UNI_burn'] = prev_state['hydra_agents']['s_i'][agent3_id] # starting value subtract - 150000
            #action['UNI_burn'] = 199433.56 -150000 #a=0.5
            #action['UNI_burn'] = 201370.96 - 150000 #a=1.0
            # action['UNI_burn'] = 816230.51 - 150000 #a=1.5

        # else:
        #     action['agent_id'] = prev_state['uni_agents']['m'][agent4_id]
        if action['asset_id'] == 'j':            
            action['agent_id'] = prev_state['uni_agents']['m'][agent3_id] 
            action['UNI_burn'] = prev_state['uni_agents']['s_i'][agent3_id] #* 0.001 
            action['purchased_asset_id'] = 'N/A'

    ###############################################

    ########## TEMP TEST SELL R FOR R ############
    ####### AGENT 5 ######################
    if params['exo_trade'] == 'test_r_for_r':        
        action['ri_sold'] = prev_state['trade_random_size']
        action['action_id'] = 'R_Swap'
        action['purchased_asset_id'] = 'j'
        action['direction'] = 'ij'

        # temp choose first agent
        action['agent_id'] = prev_state['uni_agents']['m'][agent5_id]
        if action['asset_id'] == 'j':
            action['agent_id'] = prev_state['uni_agents']['m'][agent5_id]
            action['ri_sold'] = 4 * prev_state['trade_random_size']
            action['purchased_asset_id'] = 'i'
            action['direction'] = 'ji'           
    print(action)
    return action

#########################################################################################

                     # AGENT ACTIONS #
    
#########################################################################################



#########################################################################################

                     # ASSET assignment and TRADE sizes & directions #
    
#########################################################################################

def s_purchased_asset_id(params, step, history, prev_state, policy_input):
    purchased_asset_id = policy_input['purchased_asset_id']
    
    return 'purchased_asset_id', purchased_asset_id

def s_asset_random(params, step, history, prev_state, policy_input):
    if params['exo_trade'] == 'pass' and params['exo_liq'] == 'pass':
        # there are no trades to be made this timestep
        return 'asset_random_choice', np.nan
    else:
        asset_random_choice = random.choice(['i', 'j'])
        #asset_random_choice = random.choice(['i'])
        return 'asset_random_choice', asset_random_choice

def s_trade_random(params, step, history, prev_state, policy_input):
    if params['exo_trade'] == 'pass' and params['exo_liq'] == 'pass':
        # there are no trades to be made this timestep
        return 'trade_random_size', np.nan
    else:
        sigma = params['sigma']
        mu = params['mu']
        asset_random_choice = random.choice(['i', 'j'])
        #asset_random_choice = random.choice(['i'])
        trade_size_random_choice = math.ceil(np.random.normal(mu, sigma))
        return 'trade_random_size', trade_size_random_choice
    
def s_trade_deterministic(params, step, history, prev_state, policy_input):
    return 'trade_random_size', prev_state['trade_random_size']
    
def s_direction_random(params, step, history, prev_state, policy_input):
    if params['exo_trade'] == 'pass' and params['exo_liq'] == 'pass':
        # there are no trades to be made this timestep
        return 'trade_random_direction', 'no_trade'
    else:
        #direction_random_choice = random.choice(['test_q_for_r', 'test_r_for_q', 'test_r_for_r', 'test_add', 'test_remove'])
        #direction_random_choice = random.choice(['test_q_for_r', 'test_r_for_q', 'test_r_for_r'])
        direction_random_choice = random.choice(['test_r_for_r'])

        return 'trade_random_direction', direction_random_choice
    
#########################################################################################

                     # ASSET assignment and TRADE sizes & directions #
    
#########################################################################################

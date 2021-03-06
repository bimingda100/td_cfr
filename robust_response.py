import sys
import os
sys.path.insert(0,os.path.realpath('../cfr/'))
from pokergames import *
from pokerstrategy import *
from environment import *
from nash_response import *
from skew_agents import *


strat_file = sys.argv[1]
response_player = int(sys.argv[2])
fixed_player = -1 * response_player + 1
prob_fixed = float(sys.argv[3])
iterations = int(sys.argv[4])
out_file = sys.argv[5]

leduc = leduc_rules()
gametree = GameTree(leduc)
gametree.build() 

strategies = [None, None]
fixed_strat = Strategy(fixed_player)
fixed_strat.load_from_file(strat_file)
strategies[fixed_player] = fixed_strat

response_strat = Strategy(response_player)
response_strat.build_default(gametree)
strategies[response_player] = response_strat

profile = StrategyProfile(leduc, strategies)

cfr = RestrictedNashResponse(leduc, response_player, profile, prob_fixed)

iterations_per_block = 100
blocks = iterations / iterations_per_block
for block in range(blocks):
    print 'Iterations: {0}'.format(block * iterations_per_block)
    cfr.run(iterations_per_block)
    result = cfr.profile.best_response()
    print 'Best response EV: {0}'.format(result[1])
    print 'Total exploitability: {0}'.format(sum(result[1]))
print 'Saving strategies...'
cfr.profile.strategies[response_player].save_to_file(out_file)
print 'Done!'
print ''

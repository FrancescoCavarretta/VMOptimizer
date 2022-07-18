#!/usr/bin/env python
# coding: utf-8

import bluepyopt
import os
import CellEvalSetup 
import logging

def create_mapper():
    '''returns configured bluepyopt.optimisations.DEAPOptimisation'''
    from ipyparallel import Client
    rc = Client(profile=os.getenv('IPYTHON_PROFILE'))

    lview = rc.load_balanced_view()

    def mapper(func, it):
        ret = lview.map_sync(func, it)
        return ret

    map_function = mapper

    return map_function



def main(etype, seed, max_ngen, offspring_size, continue_cp=False, cp_frequency=1, parallel=True, eta=10, mutpb=1.0, cxpb=1.0):
    # instantiate evaluator
    evaluator = CellEvalSetup.evaluator.create(etype, use_process=True)

    # instantiate optimizer
    opt = bluepyopt.optimisations.DEAPOptimisation(evaluator=evaluator, map_function=(create_mapper() if parallel else map), seed=seed, eta=eta, mutpb=mutpb, cxpb=cxpb)

    # checkpoint file name
    cp_filename = '{}_checkpoint_{}.pkl'.format(etype, seed)

    # log file name
    log_filename = '{}_checkpoint_{}.log'.format(etype, seed)

    # set logger
    logger = logging.getLogger()
    fhandler = logging.FileHandler(filename=log_filename, mode='a')
    fhandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fhandler)
    logger.setLevel(logging.DEBUG)
    
    # run a session
    final_pop, halloffame, log, hist = opt.run(max_ngen=max_ngen, offspring_size=offspring_size, cp_filename=cp_filename, continue_cp=continue_cp, cp_frequency=cp_frequency)

    # return
    return final_pop, halloffame, log, hist



if __name__ == '__main__':
    import sys
    import time

    continue_cp = '--continue' in sys.argv
    serial = '--serial' in sys.argv
    offspring_size = int(sys.argv[-1])
    max_ngen = int(sys.argv[-2])
    seed = int(sys.argv[-3])
    etype = sys.argv[-4]


    
    tinit = time.time()
    main(etype, seed, max_ngen, offspring_size, continue_cp=continue_cp, parallel=not serial)
    tend = time.time()
    print ('optimization took', (tend-tinit)/60.0, 'minutes')

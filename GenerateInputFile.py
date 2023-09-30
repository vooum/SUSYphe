#! /usr/bin/env python3

import copy
from typing import Union
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any
from ..DataProcessing.SLHA.LHA_line import GetBlockName
from ..DataProcessing.SLHA.LHA_line import GetDecayCode


# define type for sample point
sample_type = dict[ Union[int,str] , dict[ Union[int,str,tuple[int,...]], float] ]

class LineGenerator(ABC): # abstract class
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def __call__(self,point_dict:sample_type) -> str:
        pass
    
class GenerateAccord(LineGenerator):
    '''
    This class is used to generate each line which should be motified
    in creating an input file. One line for one parameter.
    __init__:
        input parameters for initialization:
            block:str: block name
            code:int/tuple: code for the parameter.
            end:list: list of annotation strings to be appended after value and a '#'
    __call__:
        input data of sample point: dict
            format: {block_name:{code:value,},}
            values:float
        return:
            Line with parameter value subsituted, like:
            '\t3\t2\t# annotations'
    '''
    def __init__(self, block:str, code: int|tuple,
                 left:str, sub:str, tail:str):
        self.block=block
        self.code=code
        self.left, _, mid =left.rpartition(sub)
        self.right=f'{mid}#{tail}'
    def __call__(self, point_dict:sample_type) -> str:
        '''BLOCK MASS
        25 125.01 # h mass'''
        value=point_dict[self.block][self.code]
        return f'{self.left}{value}{self.right}'

class GenerateDecay(LineGenerator):
    def __init__(self, PDG:int,
                 left:str, sub:str, tail:str) -> None:
        self.PDG=PDG
        self.left, _, mid =left.rpartition(sub)
        self.right=f'{mid}#{tail}'
    def __call__(self, point_dict:sample_type) -> str:
        '''DECAY  25   1.09899870E-02  # h decays'''
        width=point_dict[self.PDG]['WIDTH']
        return f'{self.left}{width}{self.right}'

class GenerateBranchRatio(LineGenerator):
    def __init__(self, PDG:int, code:tuple,
                 left:str, sub:str, tail:str) -> None:
        self.PDG = PDG
        self.code = code
        self.left, _, mid =left.partition(sub)
        self.right=f'{mid}#{tail}'
    def __call__(self, point_dict:sample_type) -> str:
        value=point_dict[self.PDG][self.code]
        return f'{self.left}{value}{self.right}'

class unchanged_line(LineGenerator):
    def __init__(self,line):
        self.line=line.rstrip('\n')
    def __call__(self,*any):
        return self.line


class GenerateInputFile():
    '''Generate a new input file with parameters of sample point.
    __init__:
        text_mold: lines in input mold file got by readlines();
        point_dict: {block1 : {code1:value1, code2,value2},
                     block2 : {...}
                     ...
                     PDG1 : {'WIDTH': width_of_particle_PDG1,
                            (tuple of final states): branch_ratio,
                            (tuple of final states): branch_ratio,
                            ...}
                     PDG2 : {...}
                     ...
                    }
        path: where new input file to write
    '''
    def __init__(self, 
                 text_mold : list[str], 
                 point_dict: sample_type, 
                 path):
        # self.text_mold=text_mold
        self.path=path
        self.generators: list[LineGenerator] = []
        # current_block : None | sample_type
        current_block = None
        block_name = None # str for block, int for PDG decay
        for line in text_mold:
            generator=None # initialize generator
            line=line.rstrip()
            left, _, tail = line.partition('#')
            head = left.strip()
            # for empty/annotation lines, keep it as unchanged_line.
            # if head=='': continue ## This will skip empty/annotation lines
            if head:# meaningful statement
                start=head[:5].upper()
                if start == 'BLOCK':  # declaring a new block
                    block_name = GetBlockName(head)
                    current_block=point_dict.get(block_name) # get None if block not in point_dict
                    # unchanged line 
                elif start == 'DECAY': # declaring a new decay
                    block_name = GetDecayCode(head)
                    current_block=point_dict.get(block_name) # None if decay_PDG not in point_dict
                    if current_block: # not None, add a new line for decay's head
                        generator = GenerateDecay(block_name, left, head.split()[-1], tail)
                # Check type of block.
                #   if None, all parameters in this block will keep unchanged.
                #   else, acquire data of this block/decay from point_dict.
                elif current_block: # current_block is block/decay
                    line_data = head.split()
                    # block
                    if type(block_name) is str: # found block in pint_dict, accord to change
                        lenth = len(line_data)
                        # Get code
                        if lenth == 2 : # one code for scalar
                            code = int(line_data[0])
                        elif lenth > 2 : # tuple code for matrix
                            code = tuple([int(i) for i in line_data[:-1] ])
                        else: # only one number in this line, wrong format
                            print('only one number in this line, check the input file.')
                            raise IndexError
                        # Set line generator with block, code, sub
                        sub_str=line_data[-1]
                        if code in current_block: # find parameter in point_mold
                            generator = GenerateAccord(block_name,code,left, line_data[-1], tail)
                    # decay
                    elif type(block_name) is int: # branch ratio lines of PDG
                        code = tuple( [int(i) for i in head.split()[2:] ] )
                        if code in current_block:
                            generator = GenerateBranchRatio( block_name, code, left, line_data[0], tail)
            # set unchanged lines
            if generator:
                self.generators.append(generator)
            else:
                self.generators.append( unchanged_line(line) )
    def __call__(self, point_dict:sample_type):
        lines=[ f(point_dict)+'\n' for f in self.generators] 
        lines[-1].rstrip()
        with open(self.path,'w') as inp:
            inp.writelines(lines)

# subprocess for class:scan
def GetSLHAValues(sample):
    '''Get {block:{code:value, }, } from sample point (type: SCAN)
    '''
    point_dict=defaultdict(dict)
    for par in sample.variable_dict.values():
        point_dict[par.block][par.code]=par.value
    return point_dict

class GenerateInputWithScan(GenerateInputFile):
    def __init__(self, text_mold, point, path):
        point_dict=GetSLHAValues(point)
        super().__init__(text_mold, point_dict, path)
    def __call__(self, point):
        point_dict=GetSLHAValues(point)
        super().__call__(point_dict)
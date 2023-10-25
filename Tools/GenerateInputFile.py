#! /usr/bin/env python3

# Written by 贺杨乐， 2023/09/30
# 示例：
# ## 设置一个样本点，明确哪些数据需要修改
# point = {'MASS': {25: 125.01}, 'NMIX': {(1,1): 0.9} } # 样本点，包含需要改变的参数
# ### 注意：
# ### 样本点是两层的 dict, 
# ### 第一层的 key 是 block 名，必须全大家，value 是数据
# ### 第二层，标量的 key 是整数，如25， 混合矩阵的 key 是 tuple 元组。
# ## 读取输入文件的模板，保存在 mold_text 里
# with open('**/Prospinoin_1.txt', 'r') as in_mold: 
#     mold_text = in_mold.readlines()
# ## 初始化一个 GenerateInputFile 的实例：in_file
# in_file = GenerateInputFile(
#                         text_mold = mold_text,
#                         point_dict = point,
#                         path = '**/Prospino.in.les_houches' #每次生成文件时保存在哪里
#                         )
# ## 生成一个新的输入文件
# point['MASS'][25]=126.0 #改变参数点的值
# in_file(point) # 这里可以把实例当函数用
# ## 之后会在生成一个新的文件： **/Prospino.in.les_houches，
# ## 文件中的 higgs 质量是126，NMIX混合矩阵的 1,1 元素是 0.9.

from typing import Union
from abc import ABC, abstractmethod

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
            block: str: block name
            code: int/tuple: code for the parameter.
            tail: annotation string to be appended after value and a '#'
    __call__:
        input data of sample point: dict
            format: {block_name:{code:value,},}
            values:float
        return:
            Line with parameter value subsituted, like:
            '\t3\t2\t# annotations'
    '''
    def __init__(self, block:str, code: int|tuple,
                 body:str, sub:str, tail:str):
        self.block=block
        self.code=code
        self.left, _, mid =body.rpartition(sub)
        self.right=f'{mid}#{tail}'
    def __call__(self, point_dict:sample_type) -> str:
        '''BLOCK MASS
        25 125.01 # h mass'''
        value=point_dict[self.block][self.code]
        return f'{self.left}{value}{self.right}'

class GenerateDecay(LineGenerator):
    def __init__(self, PDG:int,
                 body:str, sub:str, tail:str) -> None:
        self.PDG=PDG
        self.left, _, mid =body.rpartition(sub)
        self.right=f'{mid}#{tail}'
    def __call__(self, point_dict:sample_type) -> str:
        '''DECAY  25   1.09899870E-02  # h decays'''
        width=point_dict[self.PDG]['WIDTH']
        return f'{self.left}{width}{self.right}'

class GenerateBranchRatio(LineGenerator):
    def __init__(self, PDG:int, code:tuple,
                 body:str, sub:str, tail:str) -> None:
        self.PDG = PDG
        self.code = code
        self.left, _, mid =body.partition(sub)
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
            body, _, tail = line.partition('#')
            head = body.strip()
            # for empty/annotation lines, keep it as unchanged_line.
            # if head=='': continue ## This will skip empty/annotation lines
            if head:# meaningful statement
                line_data = head.split()
                start=line_data[0].upper()
                if start == 'BLOCK':  # declaring a new block
                    block_name = head.split(maxsplit=2)[1].upper() # Get string after 'BLOCK'
                    current_block=point_dict.get(block_name) # get None if block not in point_dict
                    # unchanged line 
                elif start == 'DECAY': # declaring a new decay
                    block_name = int(line_data[1])
                    current_block=point_dict.get(block_name) # None if decay_PDG not in point_dict
                    if current_block: # not None, add a new line for decay's head
                        generator = GenerateDecay(block_name, body, line_data[-1], tail)
                # Check type of block.
                #   if None, all parameters in this block will keep unchanged.
                #   else, acquire data of this block/decay from point_dict.
                elif current_block: # current_block is block/decay
                    # BLOCK
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
                        # subsitute = line_data[-1] # the string of value, to be replaced by values in new points
                        if code in current_block: # find parameter in point_mold
                            generator = GenerateAccord(block_name,code,body, line_data[-1], tail)
                    # DECAY
                    elif type(block_name) is int: # branch ratio lines of PDG
                        code = tuple( [int(i) for i in head.split()[2:] ] )
                        if code in current_block:
                            generator = GenerateBranchRatio( block_name, code, body, line_data[0], tail)
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

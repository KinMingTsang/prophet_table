from prophet_table import prophet_table
from tqdm import tqdm
import pandas as pd
import os
import types
os.system('cls')
src1 = os.getcwd()+"\\example\\"#remember to add the "\\"

src2 = src1#remember to add the "\\"

##for the detail of the comparison mechanism please refer to the util.py!

##Note that all file should be put in the same directory,


def get_files(path,sorting=""):
    #path is the source path that you want to obtain content
    #sorting is stating for the condition function 
    if isinstance(sorting, types.FunctionType):
        return list( filter(sorting,  os.listdir(path)))
    
    return os.listdir(path)

tables =  get_files(src2,(lambda src:  True if src.find(".PRO")!=-1 else False))
pp = prophet_table()
df1 = pp.read_csv(filepath_or_buffer = src1+"\\"+tables[0])
df2 = pp.read_csv(filepath_or_buffer = src1+"\\"+tables[1])
df1 = df1[df1['AGE_AT_ENTRY']<'40']
print(df1)
print(type(df1))
print(df1.compare(df2))

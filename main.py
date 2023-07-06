from prophet_table import prophet_table
from tqdm import tqdm
import os
import types
src1 = "C:\\Users\\214985\\OneDrive - FWD Group Management Holdings Limited\\Desktop\\Regression\\May\\TABLES\\SummProd\\"#remember to add the "\\"

src2 = "C:\\Users\\214985\\OneDrive - FWD Group Management Holdings Limited\Documents\\TABLES\\TABLES\\SummProd\\"#remember to add the "\\"

export = "C:\\Users\\214985\\OneDrive - FWD Group Management Holdings Limited\\Desktop\\Regression\\June_v2\\"#remember to add the "\\"


##for the detail of the comparison mechanism please refer to the util.py!

##Note that all file should be put in the same directory,

# result = {}

# Complete_info = True


def get_files(path,sorting=""):
    #path is the source path that you want to obtain content
    #sorting is stating for the condition function 
    if isinstance(sorting, types.FunctionType):
        return list( filter(sorting,  os.listdir(path)))
    
    return os.listdir(path)


# for file in tqdm(get_files(src2,(lambda src:  True if src.find(".fac")!=-1 and src.find("202212")!=-1 else False)),desc = "Table checking progress",unit = "tables"):
for file in tqdm(get_files(src2,(lambda src:  True if src.find(".fac")!=-1 else False)),desc = "Table checking progress",unit = "tables"):
        try:
            df1 = prophet_table(path = src2,file = file,gen_key = False)
            df2 =prophet_table(path = src1,file = file, gen_key = False)
            print(df1.compare(df2))
        except :
             print("File {} not found in one path ".format(file))
             continue

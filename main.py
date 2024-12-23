from prophet_table import prophet_table
from tqdm import tqdm
import pandas as pd
import os
import types

##for the detail of the comparison mechanism please refer to the util.py!

##Note that all file should be put in the same directory,


def get_files(path,sorting=""):
    #path is the source path that you want to obtain content
    #sorting is stating for the condition function 
    if isinstance(sorting, types.FunctionType):
        return list( filter(sorting,  os.listdir(path)))
    
    return os.listdir(path)


def compare_dir(path1,path2):
    #path1 and path2 does not end with "\\"
    file_list1 = os.listdir(path1)
    file_list2 = os.listdir(path2)
    pp = prophet_table()   #to create an accessor so that we can access the table through the accessor
    counter= 1
    for file in tqdm(file_list1,desc = "FILE IN FOLDER"):
        if file in file_list2:
            if (lambda src:  True if src.find(".PRO")!=-1 else False)(file):
                #the underlying framework of the prophetable is exactly the same, therefore,we can use it in the same way as pandas
                df1 = pp.read_csv(filepath_or_buffer = path1+file,is_mpf=False)
                df2 = pp.read_csv(filepath_or_buffer = path2+file,is_mpf=False)
                print("\n"+file.upper()+"\n")
                result = df1.compare(df2,index_key_generate = True)
                result.to_csv(path1+f"Result_compare_{file}.csv")
                print(result)
                counter = counter +1

os.system('cls')                        
# src1 = os.getcwd()+"\\example\\"#remember to add the "\\"

# src2 = os.getcwd()+"\\example\\"#remember to add the "\\"

# compare_dir(src1,src2)

## single file comparison
src1 = os.getcwd()+"\\example\\C123457.PRO"#remember to add the "\\"

src2 = os.getcwd()+"\\example\\C1234567.PRO"#remember to add the "\\"
pp = prophet_table()
df1 = pp.read_csv(filepath_or_buffer = src1,is_mpf=False)
df2 = pp.read_csv(filepath_or_buffer = src2,is_mpf=False,)
print(df1,"\n",df2)
# print(df1.compare(df2,index_key_generate=True))
print(df1.get_difference(df2))
#df1.get_difference(df2)
# print(df1)
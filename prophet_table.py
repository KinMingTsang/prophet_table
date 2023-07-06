import tqdm
import re
import pandas as pd
import numpy
import os
import types

class prophet_table:

    __exp_ext__ = [".R",".N",".l",".PRO",".fac"]
    __key_num__ = 0

    def __init__(self,path="",file="",gen_key=False):
        #path: string the input directory of the file
        #file: string file name with extension 
        #gen_key: Bool use for mapping and comparison between table

        if not(isinstance(path,str)) or not(isinstance(file,str)):
            raise TypeError

        self.__load_ext__(file = file)

        if  not(os.path.exists(path)):
            raise Exception("Path not found error")

        if not(file in os.listdir(path)):
            raise FileNotFoundError
        
        self.__path__ = (lambda x : x+"\\" if x.rfind("\\") != len(x)-1 else x)(path)
        self.__file_name__ = file[0:file.find(self.__ext__)]
        self.__load_table__()


        if gen_key:
            self.__gen_key__()

    def __load_ext__(self, file):
        for ext in self.__exp_ext__:
            if file.find(ext)!=-1:
                self.__ext__ = ext
                return
        print("Extension value error, not a valid extension")
        raise ValueError
    
    def get_ext(self):
        return self.__ext__

    def get_filename(self):
        return self.__file_name__
    
    def get_path(self):
        return self.__path__

    def __key_loc__(self, key,lookup):
        #this function will return the index of the key
        #lookup: the table you want to check with. Key: The target you want to find
        check = lookup.isin([key])
        for index, value in enumerate(check):
            if value :
                return index
        return -1
    
    def gen_key(self,value_compare=False):
        #fac is the table that you just imported from somewhere else.
        #this function will return a dataframe with key attached
        
        if value_compare:
            cur_key = ""   
            
            col_name = self.__content__.columns # to obtain all column names

            for cur_col in col_name[0:self.__content__.shape[1]]:
                cur_key +=  self.__content__[cur_col]+"_"  #to get the key of the current record

            self.__content__["Key"] = cur_key #join the list of Key at the end of the table
        
        else: 
        
            cur_key = ""   
        
            col_name = self.__content__.columns # to obtain all column names

            for cur_col in col_name[0:self.__key_num__]:
                cur_key +=  self.__content__[cur_col]+"-"  #to get the key of the current record

            self.__content__["Key"] = cur_key #join the list of Key at the end of the table

    def compare(self,fac2):

        # fac2 = table 2 you imported Dataframe expected
        #  return the result of comparison with two columns [Lookup_Key,Result ]

        if not(isinstance(fac2,prophet_table)):
            raise Exception("The file is not prophet table object")
        self.gen_key(True)
        
        fac2.gen_key(True)
        
        result=pd.DataFrame()   

        try:
            result["Lookup_Key"] = pd.concat([self.__content__["Key"], fac2["Key"]], axis=0, ignore_index=True).unique()
        
        except ValueError:
            result["Lookup_Key"] = pd.Series(pd.concat([self.__content["Key"],fac2["Key"]], axis=0, ignore_index=True).unique()).reindex()
        
        temp = []

        for key in result["Lookup_Key"]:

            check1 = self.__key_loc__(key,self.__content__["Key"])
            check2 = self.__key_loc__(key, fac2["Key"])
            
            if check1!=-1 and check2!=-1 :
                temp.append("Matched in both file")
            
            elif check1!=-1:
                temp.append("Matched in fac1 only")
            
            else:
                temp.append("Matched in fac2 only")
        result["Result"] = temp
        print("RESULT = {}".format(result))
        return result

    '''
    find header row of a .fac or a model point file (the row starting with !)
    zero-indexed, i.e. if the header is at the first row, it will return 0
    '''

    def __find_fac_header_row__(self):
        filename = self.__path__+self.__file_name__+self.__ext__
        result = 0
        # strange characters.. need to set encoding
        with open(filename, 'r', encoding='latin-1') as f:
            for line in f:
                if line[0] == '!':
                    return result
                result += 1

    def __load_table__(self,drop_na=True, value_compare=False):
        #this function allow user to impor the fac file with removed NA contents, you can disable it by comment the df.dropna() line
        #include the path for the checking table format should be path\\file
        #to compare all value in the dataframe, the pre-requisite is to use all key as the look up value. To do so, just put value_compare = True
        #drop_axis sets the axis which script should follow, follow row  : 0 , follow col : 1
        
        self.__content__ = pd.read_csv(self.__path__+self.__file_name__+self.__ext__,sep = ",",skiprows = [x for x in range(self.__find_fac_header_row__())],encoding='latin', dtype=str, on_bad_lines="skip")
        if drop_na:
            self.__content__.dropna(axis=0,inplace = True)
        
        self.__find_key_num__()
        self.__content__.drop(self.__content__.columns[0], axis=1,inplace= True) # to drop the column with *
    
    def print_table(self):
        print(self.__content__)

    def __find_key_num__(self):
        #df the target dataframe, pandas dataframe is expected
        # value_compare: Boolean, True when you want to compare the value for whole table
        self.__key_num__ = int(((self.__content__).columns[0])[1:]) #set this variable to the number of column that needs to be used as key
    
    def get_key_num(self):
        return self.__key_num__

    def sort_record(self,pol_no,sort_timing=""):
        #path input the directory of the file, ending with \\ string type expected
        #sort_timing, it used to sort the table with naming at specific timing string type expected
        # pol_no Required Value for sorting, string type expected
        #return the sorted result as pandas DataFrame

        if self.__ext__!=".PRO":
            raise Exception("Table Error, not Model Point File")

        if pol_no == "":
            raise Exception("Policy No Criteria in string form is expected")
        
        if self.__file_name__.find(sort_timing) == -1:
            raise Exception("This file does not on time point = {}".format(sort_timing))       

        return self.__content__[self.__content__["POL_NUMBER"] == pol_no]

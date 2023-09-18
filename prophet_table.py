import pandas as pd
import numpy as np
import os
# def report_error(msg = ""):
# sys.setrecursionlimit(5000)
# @pd.api.extensions.register_dataframe_accessor("pp")


class prophet_table(pd.DataFrame):
    #inheritated from Pandas
    __key_num__ = 0
    __content__ =None
    
    @property
    def _constructor(self):
        return prophet_table
   
    def  read_csv(self,filepath_or_buffer):
        return prophet_table(pd.read_csv(filepath_or_buffer = filepath_or_buffer ,sep = ",",skiprows = [x for x in range(self.__find_fac_header_row__(filepath_or_buffer))],encoding='latin', dtype=str, on_bad_lines="skip"))#.drop(columns=0,axis=1,inplace=True))
    
    def __find_key_num__(self)->int:
        #df the target dataframe, pandas dataframe is expected
        # value_compare: Boolean, True when you want to compare the value for whole table
        if len(self.columns[0])!= 1:
            self = int((self.columns[0])[1:]) #set this variable to the number of column that needs to be used as key
            
            if self.__key_num__ >self.shape[1]:
                self.__key_num__ = self.shape[1]
        else:
            raise Exception("Invalid Key Num")

    def __find_fac_header_row__(self,filepath_or_buffer)->int:
        '''
            find header row of a .fac or a model point file (the row starting with !)
            zero-indexed, i.e. if the header is at the first row, it will return 0
            credited to bensonby
        '''
        filename = filepath_or_buffer
        result = 0
        # strange characters.. need to set encoding
        with open(filename, 'r', encoding='latin-1') as f:
            for line in f:
                if line[0] == '!':
                    print(result)
                    return result
                result += 1

    def __key_loc__(self, key, lookup)->int:
        #this function will return the index of the key
        #lookup: the table you want to check with. Key: The target you want to find
        check = lookup.isin([key])
        for index, value in enumerate(check):
            if value :
                return index
        return -1

    def gen_key(self, value_compare=False)->None:
        # value_compare: Boolean, True when you want to compare the value for whole table
        #this function will attach the key to the  target dataframe with key attached
                    
        cur_key = ""  
        
        if "Key" in self.keys():
            if value_compare:

                for cur_col in self.keys()[1:len(self.keys())-1]:
                    cur_key +=  self.__getitem__(cur_col)+"-" 
            
            else: 

                for cur_col in self.keys()[1:self.__key_num__+1]:
                    cur_key += self.__getitem__(cur_col)+"-" 

        else:
            if value_compare:

                for cur_col in self.keys()[1:]:
                    cur_key +=  self.__getitem__(cur_col)+"-" 
            
            else:  
                for cur_col in self.keys()[1:self.__key_num__+1]:
                    cur_key += self.__getitem__(cur_col)+"-" 
        
        return cur_key


    def compare(self, table2)->pd.DataFrame:
        # table2 = table  you imported prophet_table expected
        #  return the result of comparison with two columns [Lookup_Key,Result ] in pandas dataframe

        if not(isinstance(table2,prophet_table)):
            raise Exception("The file is not prophet table object")
        
        key2 =  table2.gen_key(True)
        key1 =  self.gen_key(True)
        result=pd.DataFrame()   

        try:
            result["Lookup_Key"] = pd.concat([key1, key2], axis=0, ignore_index=True).unique()
        
        except ValueError:
            result["Lookup_Key"] = pd.Series(pd.concat([ key1, key2], axis=0, ignore_index=True).unique()).reindex()
        
        temp = []
        result["Lookup_Key_1"] = np.where(result["Lookup_Key"].isin(key1),"Matched",0)
        result["Lookup_Key_2"] = np.where(result["Lookup_Key"].isin(key2),"Matched",0)
        
        result["Result"] = np.select(condlist=[result["Lookup_Key_1"]==result["Lookup_Key_2"],result["Lookup_Key_2"]=="Matched"],choicelist = ["Matched in both file","Matched in fac2 only"],default = "Matched in fac1 only") 
        result.drop(columns=["Lookup_Key_1","Lookup_Key_2"],inplace = True)
        return result



import pandas as pd
import numpy as np
import os
import csv
class prophet_table(pd.DataFrame):
    #inheritated from Pandas
    __key_num__ = 0
    __content__ =None
    __is_mpf__ = False
    
    @property
    def _constructor(self):
        '''
            this function calls the default constructor to set attribute that is specific to prophet_table class before executing dataframe contstructor
        '''
        return prophet_table
   
    def  read_csv(self,filepath_or_buffer,is_mpf = False):
        obj = prophet_table(pd.read_csv(filepath_or_buffer = filepath_or_buffer ,sep = ",\s*",engine = "python",skiprows = [x for x in range(self.__find_fac_header_row__(filepath_or_buffer))],encoding='latin', dtype=str, on_bad_lines="skip"))
        obj.__set_attribute__(is_mpf)
        return  obj
    def __find_key_num__(self)->int:
        '''df the target dataframe, pandas dataframe is expected
        value_compare: Boolean, True when you want to compare the value for whole table'''
        
        if self.__key_num__ !=0:
            return self.__key_num__

        if len(self.columns[0])!= 1:
            self.__key_num__ = int((self.columns[0])[1:]) #set this variable to the number of column that needs to be used as key
            
            if self.__key_num__ >self.shape[1]:
                self.__key_num__ = self.shape[1]
        else:
            raise Exception("INVALID KEY NUMBER")

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
                    return result
                result += 1

    def __key_loc__(self, key, table)->int:
        '''this function will return the index of the key
            table: the table you want to check with. 
            Key: The target you want to find
        '''
        check = np.where(table.isin([key]))[0]
        if check.shape[0] ==-1:
            return -1
        return check
    
    def gen_key(self, value_compare=False)->None:
        '''value_compare: Boolean, True when you want to compare the value for whole table
            this function will attach the key to the  target dataframe with key attached'''
                    
        cur_key = ""  
        
        self.__find_key_num__()

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

    def __set_attribute__(self,is_mpf):
        self.is_mpf = is_mpf
    
    def get_attribute(self):
        return self.is_mpf
    
    def compare(self, table2,preserve_key_indicator=True,index_key_generate = False)->pd.DataFrame:
        '''table2 = table  you imported prophet_table expected
        return the result of comparison with two columns [Lookup_Key,Result ] in pandas dataframe'''

        if not(isinstance(table2,prophet_table)):
            raise Exception("The file is not prophet table object")
        
        key2 =  table2.gen_key(True)
        key1 =  self.gen_key(True)
        result=pd.DataFrame()   

        try:
            result["Check_Key_List"] = pd.concat([key1, key2], axis=0, ignore_index=True).unique()
        
        except ValueError:
            result["Check_Key_List"] = pd.Series(pd.concat([ key1, key2], axis=0, ignore_index=True).unique()).reindex()
        
        temp = []

        result["Lookup_Key_1"] = np.where(result["Check_Key_List"].isin(key1),result["Check_Key_List"],"")
        result["Lookup_Key_2"] = np.where(result["Check_Key_List"].isin(key2),result["Check_Key_List"],"")
        result["Result"] = np.select(condlist=[result["Lookup_Key_1"]==result["Lookup_Key_2"],result["Lookup_Key_2"]!=""],choicelist = ["Matched in both file","Matched in fac2 only"],default = "Matched in fac1 only") 
        
        if not preserve_key_indicator:
            result.drop(columns=["Lookup_Key_1","Lookup_Key_2"],inplace = True)
        
        if index_key_generate:
            if not (self.__is_mpf__ or table2.get_attribute()):
                result ["Index_Key"] = result ["Check_Key_List"].astype(dtype = str)
                result ["Index_NO"] = result ["Index_Key"].apply(self.__set_key__)
                result["Lookup_Key_1"] = np.where(result["Lookup_Key_1"] != "", result.apply(lambda x: x["Index_Key"][x["Index_NO"]+1:], axis=1),"")  
                result["Lookup_Key_2"] = np.where(result["Lookup_Key_2"] !="", result.apply(lambda x: x["Index_Key"][x["Index_NO"]+1:], axis=1),"")
                result["Index_Key"] = "*-"+np.where(result["Index_Key"] !="", result.apply(lambda x: x["Index_Key"][:x["Index_NO"]], axis=1),"")
                result = result.drop(["Index_NO"],axis = 1 )
        return result

    def __set_key__(self,value):
        position = 0
        for i in range (1,self.__key_num__):
            position += value[position:].find("-")+1

        return position-1
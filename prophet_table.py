import pandas as pd
import numpy as np
# import tqdm
# import types
# import os


class prophet_table(pd.DataFrame):
    '''
       This library is designed for Actuarial software FIS Prophet usage with inheritated features from pandas\n
       In this library, we  provide the following functions\n
       1. Compare function for two tables\n
       2. get_difference  for checking the difference in location within two tables\n
       3. get_key_num returning the no of values used as key in the table\n
    '''
    __key_num__ = 0 # store the no of columns that used to be a key
    __is_mpf__ = False
    
    @property
    def _constructor(self):
        '''
            this function calls the default constructor to set attribute that is specific to prophet_table class before executing dataframe contstructor
        '''
        return prophet_table
   
    def  read_csv(self,filepath_or_buffer:str,is_mpf = False,keys= []):
        '''
            returns data loaded prophet_table object
        '''
        obj = prophet_table(pd.read_csv(filepath_or_buffer = filepath_or_buffer ,sep = ",\s*",engine = "python",skiprows = [x for x in range(self.__find_fac_header_row__(filepath_or_buffer))],encoding='latin', dtype=str, on_bad_lines="skip"))
        obj.__set_attribute__(is_mpf,keys)
        return  obj
    
    def __find_key_num__(self)->int:
        '''df the target dataframe, pandas dataframe is expected'''
        
        if self.__key_num__ !=0:
            return self.__key_num__

        if len(self.columns[0])!= 1:
            self.__key_num__ = int((self.columns[0])[1:]) #set this variable to the number of column that needs to be used as key
            
            if self.__key_num__ >self.shape[1]:
                self.__key_num__ = self.shape[1]
        else:
            raise Exception("INVALID KEY NUMBER")

    def __find_fac_header_row__(self,filepath_or_buffer:str)->int:
        '''
            find header row of a .fac or a model point file (the row starting with !)\n
            zero-indexed, i.e. if the header is at the first row, it will return 0\n
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
    
    def __gen_key__(self, value_compare=False)->None:
        '''value_compare: Boolean, True when you want to compare the value for whole table
            this function will attach the key to the  target dataframe with key attached'''
                    
        cur_key = ""  
        
        self.__find_key_num__()
        
        if value_compare:

            for cur_col in self.keys()[1::]:
                cur_key +=  self.__getitem__(cur_col)+"-" 
        
        else:  

            for cur_col in self.columns[0:self.__key_num__:]:
                cur_key += self.__getitem__(cur_col)+"-" 
            
            cur_key += self.__getitem__(self.columns[self.__key_num__])

        return cur_key

    def __set_attribute__(self,is_mpf,key_num = 0):
        self.is_mpf = is_mpf
        self.__find_key_num__() # sets key_num during construction

    def get_attribute(self):
        return self.is_mpf
    
    def get_key_num(self):
        return self.__key_num__

    def compare(self, table2:pd.DataFrame,preserve_key_indicator=True,index_key_generate = False)->pd.DataFrame:
        '''table2 = table  you imported prophet_table expected
            preserve_key_indicator :True if you want to keep the look up keys
            index_key_generate: unique id generator for excel lookup
            get_difference: Identification for get_difference caller
        return the result of comparison with two columns [Lookup_Key,Result ] in pandas dataframe'''
        
        if not(isinstance(table2,prophet_table)):
            raise Exception("The file is not prophet table object")
        
        key2 =  table2.__gen_key__(True)
        key1 =  self.__gen_key__(True)
        result=pd.DataFrame()   

        try:
            result["Check_Key_List"] = pd.concat([key1, key2], axis=0, ignore_index=True).unique()
        
        except ValueError:
            result["Check_Key_List"] = pd.Series(pd.concat([ key1, key2], axis=0, ignore_index=True).unique()).reindex()

        result["Lookup_Key_1"] = np.where(result["Check_Key_List"].isin(key1),result["Check_Key_List"],"")
        result["Lookup_Key_2"] = np.where(result["Check_Key_List"].isin(key2),result["Check_Key_List"],"")
        result["Result"] = np.select(condlist=[result["Lookup_Key_1"]==result["Lookup_Key_2"],result["Lookup_Key_2"]!=""],choicelist = ["Matched in both file","Matched in fac2 only"],default = "Matched in fac1 only") 

        if not preserve_key_indicator:
            result.drop(columns=["Lookup_Key_1","Lookup_Key_2"],inplace = True)
        
        if index_key_generate:
            if not (self.__is_mpf__ or table2.get_attribute()):
                result ["Index_Key"] = result ["Check_Key_List"].astype(dtype = str)
                result ["Index_NO"] = result ["Index_Key"].apply(self.__set_key_ends__,value_compare = False)
                result["Lookup_Key_1"] = np.where(result["Lookup_Key_1"] != "", result.apply(lambda x: x["Index_Key"][x["Index_NO"]+1:], axis=1),"")  
                result["Lookup_Key_2"] = np.where(result["Lookup_Key_2"] !="", result.apply(lambda x: x["Index_Key"][x["Index_NO"]+1:], axis=1),"")
                result["Index_Key"] = "*-"+np.where(result["Index_Key"] !="", result.apply(lambda x: x["Index_Key"][:x["Index_NO"]], axis=1),"")
                result = result.drop(["Index_NO"],axis = 1 )
        return result

    def get_difference(self,table2:pd.DataFrame)->pd.DataFrame:
        '''table2 = table  you imported prophet_table expected\n
            assumed no duplicate records\n
            assuemd no change in number of column\n
            return the result of values that is different in pandas both dataframes and unique id is shown in both file 
        '''        
        
        ## get comparison  result
        result = self.compare(table2,index_key_generate = True)

        # find id happend in both file but not match in values
        fac1_only = result.loc[result["Result"]=="Matched in fac1 only"]
        fac2_only = result.loc[result["Result"]=="Matched in fac2 only"]

        mutual_id = fac1_only.loc[fac1_only["Index_Key"].isin(fac2_only["Index_Key"])].copy()
        mutual_id.sort_values(by = "Index_Key",ascending= True,inplace =True)
        mutual_id.reset_index(drop=True, inplace=True)
                
        #.copy is added to avoid warning from chain assignments
        temp  = fac2_only.sort_values("Index_Key",ascending= True).copy()
        temp  = temp["Lookup_Key_2"].loc[ temp["Index_Key"].isin(mutual_id["Index_Key"])] 
        temp.reset_index(drop=True, inplace=True)# it is added becasue after sorting, the order is based on the original order
        
        mutual_id["Lookup_Key_2"] = temp
        mutual_id.drop(["Result"],axis = 1,inplace = True)
        
        # mutual_id.drop(["Result","Lookup_Key_1","Lookup_Key_2"],axis = 1,inplace = True)## function for showing mutual key list and Index key only
        
        #mark out the difference position

        ## serach the full key in the full table
        self.insert(1,"Index_Key",self.__gen_key__())
        fac1_only = self.loc[self.__getitem__("Index_Key").isin(mutual_id["Index_Key"])].copy()
        fac1_only.sort_values(by = "Index_Key",ascending= True,inplace =True)
        fac1_only.reset_index(drop=True, inplace=True)
        self.drop(["Index_Key"],axis =1 , inplace =True)


        table2.insert(1,"Index_Key",table2.__gen_key__())
        fac2_only = table2.loc[table2["Index_Key"].isin(mutual_id["Index_Key"])].copy()
        fac2_only.sort_values(by ="Index_Key",ascending= True,inplace =True)
        fac2_only.reset_index(drop=True, inplace=True)
        table2.drop("Index_Key",axis =1 , inplace =True)
        
        result = pd.DataFrame()
        result["Index_Key"] = fac1_only["Index_Key"]
        
        for col in  self.keys()[self.__key_num__+1::]:
           result[col] = np.where(fac1_only[col] == fac2_only[col],0,1)    
        
        return result

    def __set_key_ends__(self,value,value_compare = False):
        '''
            this function return the position of key ends
        '''    
        position = 0

        if value_compare:
                        
            for i in range (1,self.__key_num__):
                position += value[position:].find("-")+1
            
        else:
            for i in range (0,self.__key_num__):
                position += value[position:].find("-")+1
            
        return position-1
    
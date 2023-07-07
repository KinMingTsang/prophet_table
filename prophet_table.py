import tqdm
import re
import pandas as pd
import numpy
import os
import types

# def report_error(msg = ""):
class prophet_table():

    __key_num__ = 0
    show_leading = False


    def __init__(self, object =None, path="", file="", gen_key=False, show_leading = False, show_table = False,show_info = False)->None:
        #object: Pandas or prophet_table expected
        #path: string the input directory of the file
        #file: string file name with extension 
        #gen_key: Bool use for mapping and comparison between table
        #show_leading: show when displaying the table content

        if isinstance(object, type(None)):
            if not(isinstance(path,str)) or not(isinstance(file,str)):
                raise TypeError
            
            if  not(os.path.exists(path)):
                raise Exception("Path not found error")

            if not(file in os.listdir(path)):
                raise FileNotFoundError
            
            self.__load_ext__(file = file)
            self.__path__ = (lambda x : x+"\\" if x.rfind("\\") != len(x)-1 else x)(path)
            self.__file_name__ = file[0:file.find(self.__ext__)]
            self.__load_table__()

        elif isinstance(object,pd.DataFrame) :
            if not(isinstance(path,str)) or not(isinstance(file,str)):
                raise TypeError

            if  not(os.path.exists(path)):
                raise Exception("Path not found error")

            if not(file in os.listdir(path)):
                raise FileNotFoundError
            if object.columns[0].find("!")==-1:
                object  =  object.to_frame().insert(0,"!"+object.shape(1),"*")

            self.__load_ext__(file = file)
            self.__path__ = (lambda x : x+"\\" if x.rfind("\\") != len(x)-1 else x)(path)
            self.__file_name__ = file[0:file.find(self.__ext__)]
            self.__content__ = object
            self.show_leading = show_leading
            
            if gen_key:
                self.gen_key()
        
        elif isinstance(object, pd.Series):
            
            if not(isinstance(path,str)) or not(isinstance(file,str)):
                raise TypeError

            if  not(os.path.exists(path)):
                raise Exception("Path not found error")

            if not(file in os.listdir(path)):
                raise FileNotFoundError

            if object.dtype == bool:
                raise Exception("Boolean Value Series Cannot be used as a table")

            object  =  object.to_frame().insert(0,"!1","*")

            self.__load_ext__(file = file)
            self.__path__ = (lambda x : x+"\\" if x.rfind("\\") != len(x)-1 else x)(path)
            self.__file_name__ = file[0:file.find(self.__ext__)]
            self.__content__ = object
            self.show_leading = show_leading
            
            if gen_key:
                self.gen_key()
        
        elif isinstance(object,prophet_table):
            self.__eq__(object)
        
        else:
            raise Exception("Invalid Data Type")
        
        self.index = self.__content__.index
        self.shape =   (lambda x: x if self.show_leading else (x[0],x[1]-1))(self.__content__.shape)
        self.columns = self.__content__.columns
        self.show_leading = show_leading
        self.show_table = show_table
        self.show_info = show_info

        if gen_key:
            self.gen_key()


    def head(self,row_num)->pd.Series:
        return self.__content__.head(row_num)

    def __load_ext__(self, file)->None:
        #file string, input file name expected ending with extenstion
        #this function is designed to obtained the file extension 
        for ext in [".R",".N",".l",".PRO",".fac"]:
            if file.find(ext)!=-1:
                self.__ext__ = ext
                return
        print("Extension value error, not a valid extension")
        raise ValueError

#####################################################################################Function OVERLOADING ##############################################

    def __getitem__(self, key)->pd.Series:
        #key: the key index required
        #override the [] functions
        result = self.__content__[key]
        
        if isinstance(result,pd.Series):
            return result
            
        return prophet_table( object = result, path = self.__path__, file = self.__file_name__+self.__ext__, show_table = self.show_table, show_info = self.show_info, show_leading = self.show_leading)

    def __str__(self):
        ##Print function overloading
        if self.show_info:
            if self.show_table:
                return ">>>>>>File source:\t {}\n>>>>>>File type:\t {}\n>>>>>>File Shape:\t {}\n>>>>>>File Settings:\t key_num = {},\t show_leading = {}\n{}".format(self.__path__+self.__file_name__+self.__ext__,                            
                                                                                                                                                                    (lambda file_extension: (lambda file_extension: "Model Point File" if file_extension == ".PRO" else "Result file")(file_extension) if file_extension !=".fac" else "Table")(self.__ext__), 
                                                                                                                                                                    self.shape, self.__key_num__,self.show_leading,(lambda has_leading:self.__content__ if has_leading else  self.__content__[[x for x in self.__content__.keys()[1:]]])(self.show_leading))
            return ">>>>>>File source:\t {}\n>>>>>>File type:\t {}\n>>>>>>File Shape:\t {}\n>>>>>>File Settings:\t key_num = {},\t show_leading = {}".format(self.__path__+self.__file_name__+self.__ext__,                            
                                                                                                                                                                    (lambda x: (lambda y: "Model Point File" if y == ".PRO" else "Result file")(x) if x !=".fac" else "Table")(self.__ext__), self.shape, self.__key_num__,self.show_leading)
        else:
            return ">>>>>>File Shape:\t {}\n>>>>>>File Settings:\t key_num = {},\t show_leading = {}\n{}".format(self.shape, self.__key_num__, self.show_leading, (lambda has_leading:self.__content__ if has_leading else  self.__content__[[x for x in self.__content__.keys()[1:]]])(self.show_leading))

    def __lt__(self, other)->pd.Series:
         
        if isinstance(other,prophet_table):
            return self.__content__<other.get_content()
        else:
            return self.__content__<other

    def __le__(self, other)->pd.Series:
        if isinstance(other,prophet_table):
            return self.__content__<=other.get_content()
        else:
            return self.__content__<=other

    def __eq__(self, other)->pd.Series:
        if isinstance(other,prophet_table):
            return self.__content__==other.get_content()
        else:
            return self.__content__==other
    
    def __ne__(self, other)->pd.Series:
        if isinstance(other,prophet_table):
            return self.__content__!=other.get_content()
        else:
            return self.__content__!=other

    def __gt__(self, other)->pd.Series:
        if isinstance(other,prophet_table):
            return self.__content__>other.get_content()
        else:
            return self.__content__>other

    def __ge__(self, other)->pd.Series:
        if isinstance(other,prophet_table):
            return self.__content__>=other.get_content()
        else:
            return self.__content__>=other

#####################################################################################MUTATOR FUNCTIONS ##############################################
     
    def __key_loc__(self, key, lookup)->int:
        #this function will return the index of the key
        #lookup: the table you want to check with. Key: The target you want to find
        check = lookup.isin([key])
        for index, value in enumerate(check):
            if value :
                return index
        return -1
  
    def __find_fac_header_row__(self)->int:
        '''
            find header row of a .fac or a model point file (the row starting with !)
            zero-indexed, i.e. if the header is at the first row, it will return 0
            credited to bensonby
        '''
        filename = self.__path__+self.__file_name__+self.__ext__
        result = 0
        # strange characters.. need to set encoding
        with open(filename, 'r', encoding='latin-1') as f:
            for line in f:
                if line[0] == '!':
                    return result
                result += 1

    def __load_table__(self, drop_na=True)->None:
        #this function allow user to import the fac file with removed NA contents, you can disable it by comment the df.dropna() line
        #include the path for the checking table format should be path\\file
        #to compare all value in the dataframe, the pre-requisite is to use all key as the look up value. To do so, just put value_compare = True
        #drop_axis sets the axis which script should follow, follow row  : 0 , follow col : 1
        
        self.__content__ = pd.read_csv(self.__path__+self.__file_name__+self.__ext__,sep = ",",skiprows = [x for x in range(self.__find_fac_header_row__())],encoding='latin', dtype=str, on_bad_lines="skip")
        if drop_na:
            self.__content__.dropna(axis=0,inplace = True)
        
        self.__find_key_num__()
        # self.__content__.drop(self.columns[0], axis=1,inplace= True) # to drop the column with *

    def __find_key_num__(self)->int:
        #df the target dataframe, pandas dataframe is expected
        # value_compare: Boolean, True when you want to compare the value for whole table
        if len(self.__content__.columns[0])!= 1:
            self.__key_num__ = int((self.__content__.columns[0])[1:]) #set this variable to the number of column that needs to be used as key
            
            if self.__key_num__ >self.__content__.shape[1]:
                self.__key_num__ = self.__content__.shape[1]
        else:
            raise Exception("Invalid Key Num")

    def gen_key(self, value_compare=False)->None:
        # value_compare: Boolean, True when you want to compare the value for whole table
        #this function will attach the key to the  target dataframe with key attached
                    
        cur_key = ""  
        
        if "Key" in self.__content__.keys():
            if value_compare:

                for cur_col in self.__content__.keys()[1:len(self.__content__.keys())-1]:
                    cur_key +=  self.__content__[cur_col]+"-" 
            
            else: 

                for cur_col in self.__content__.keys()[1:self.__key_num__+1]:
                    cur_key +=  self.__content__[cur_col]+"-" 

        else:
            if value_compare:

                for cur_col in self.__content__.keys()[1:]:
                    cur_key +=  self.__content__[cur_col]+"-" 
            
            else:  
                for cur_col in self.__content__.keys()[1:self.__key_num__+1]:
                    cur_key +=  self.__content__[cur_col]+"-" 

        self.__content__["Key"] = cur_key

#####################################################################################UTILITY FUNCTIONS ##############################################
    def compare(self, table2)->pd.DataFrame:
        # fac2 = table 2 you imported prophet_table expected
        #  return the result of comparison with two columns [Lookup_Key,Result ] in pandas dataframe

        if not(isinstance(table2,prophet_table)):
            raise Exception("The file is not prophet table object")
        self.gen_key(True)
        
        table2.gen_key(True)
        
        result=pd.DataFrame()   

        try:
            result["Lookup_Key"] = pd.concat([self.__content__["Key"], table2.get_content()["Key"]], axis=0, ignore_index=True).unique()
        
        except ValueError:
            result["Lookup_Key"] = pd.Series(pd.concat([self.__content__["Key"],table2.get_content()["Key"]], axis=0, ignore_index=True).unique()).reindex()
        
        temp = []

        for key in result["Lookup_Key"]:

            check1 = self.__key_loc__(key,self.__content__["Key"])
            check2 = self.__key_loc__(key, table2["Key"])
            
            if check1!=-1 and check2!=-1 :
                temp.append("Matched in both file")
            
            elif check1!=-1:
                temp.append("Matched in fac1 only")
            
            else:
                temp.append("Matched in fac2 only")

        result["Result"] = temp
          
        return result

#####################################################################################ACCESSOR FUNCTIONS ##############################################

    def get_ext(self)->str:
        #accessor, return the extension of the file
        return self.__ext__

    def get_filename(self)->str:
        #accessor, return the file name
        return self.__file_name__
    
    def get_path(self)->str:
        #accessor, return the path of the file
        return self.__path__

    def get_key_num(self)->int:
        #accessor, return the num of column used as key
        return self.__key_num__
    def get_content(self)->pd.DataFrame:
        return self.__content__

#####################################################################################Pending  FUNCTIONS ##############################################
    
    def to_file(self, path="", as_csv=False)->None:
        #Path: String Expected Output path of the file
        #as_csv : Bool, True if you want to export as csv
        #Export the file into the desire path with the original extension or csv
        
        if  not(os.path.exists(path)):
            raise Exception("The Path is not exists")
        
        path =  (lambda x : x+"\\" if x.rfind("\\") != len(x)-1 else x)(path)

        if as_csv:
            print(">>>>>>Exporting to {} as {}.csv".format(path,self.__file_name__))
            if path!="":
                self.__content__.to_csv( path+self.__file_name__+".csv")
            else:
                self.__content__.to_csv(self.__path__+self.__file_name__+".csv")
                
        else:
            print(">>>>>>Exporting to {} as {}".format(path,self.__file_name__+self.__ext__))
            pass




        
import tqdm
import re
import pandas as pd
import numpy
import os
import types

# def report_error(msg = ""):
class prophet_table():

    __expected_ext__ = [".R",".N",".l",".PRO",".fac"]
    __key_num__ = 0
    __show_leading__ = False


    def __init__(self, object =None, path="", file="", gen_key=False, show_leading = False)->None:
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
            self.__show_leading__ = show_leading

            if gen_key:
                self.__gen_key__()

        elif isinstance(object,pd.DataFrame):
            if not(isinstance(path,str)) or not(isinstance(file,str)):
                raise TypeError

            if  not(os.path.exists(path)):
                raise Exception("Path not found error")

            if not(file in os.listdir(path)):
                raise FileNotFoundError
            
            
            self.__load_ext__(file = file)
            self.__path__ = (lambda x : x+"\\" if x.rfind("\\") != len(x)-1 else x)(path)
            self.__file_name__ = file[0:file.find(self.__ext__)]
            self.__content__ = object
            self.__show_leading__ = show_leading
            if gen_key:
                self.__gen_key__()

        else:
            print("Invalid Data Type")

    def haeds(self)->pd.Series:
        return self.__content__.heads()

    def columns(self)->pd.Index:
        return self.__content__.columns


    def __eq__(self,object2)->None:
        if isinstance(object2,prophet_table):
            self.__content__ = object2.__content__
            self.__key_num__ = object2.__key_num__
            self.__show_leading__ = object2.__show_leading__
            self.__path__ = object2.__path__
            self.__file_name__ = object2.__file_name__
            self.__ext__ = object2.__ext__

        if isinstance(object2,pd.DataFrame):
            self.__content__ = object2.__content__
            self.__key_num__ = object2.__key_num__
            self.__show_leading__ = object2.__show_leading__
            self.__path__ = object2.__path__
            self.__file_name__ = object2.__file_name__
            self.__ext__ = object2.__ext__

    def __load_ext__(self, file)->None:
        #file string, input file name expected ending with extenstion
        #this function is designed to obtained the file extension 
        for ext in self.__expected_ext__:
            if file.find(ext)!=-1:
                self.__ext__ = ext
                return
        print("Extension value error, not a valid extension")
        raise ValueError

    def __getitem__(self, key):
        #key: the key index required
        #override the [] functions
        return prophet_table( object = self.__content__[key], path = self.__path__, file = self.__file_name__+self.__ext__,show_leading= self.__show_leading__)
        



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
        # self.__content__.drop(self.__content__.columns[0], axis=1,inplace= True) # to drop the column with *
  
    def __find_key_num__(self)->int:
        #df the target dataframe, pandas dataframe is expected
        # value_compare: Boolean, True when you want to compare the value for whole table
        if len((self.__content__).columns[0])!= 1:
            self.__key_num__ = int(((self.__content__).columns[0])[1:]) #set this variable to the number of column that needs to be used as key
            if self.__key_num__ >self.__content__.shape[1]:
                self.__key_num__ = self.__content__.shape[1]
        else:
            raise Exception("Invalid Key Num")
       
    def __gen_key__(self, value_compare=False)->None:
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

    def get_ext(self)->str:
        #accessor, return the extension of the file
        return self.__ext__

    def get_filename(self)->str:
        #accessor, return the file name
        return self.__file_name__
    
    def get_path(self)->str:
        #accessor, return the path of the file
        return self.__path__
    
    def set_show_leading(self)->None:
        self.__show_leading__ = not(self.__show_leading__)
    
    def get_show_leading(self)->bool:
        return self.__show_leading__

    def get_key_num(self)->int:
        #accessor, return the num of column used as key
        return self.__key_num__
    
    def compare(self, fac2)->pd.DataFrame:
        # fac2 = table 2 you imported prophet_table expected
        #  return the result of comparison with two columns [Lookup_Key,Result ]

        if not(isinstance(fac2,prophet_table)):
            raise Exception("The file is not prophet table object")
        self.__gen_key__(True)
        
        fac2.__gen_key__(True)
        
        result=pd.DataFrame()   

        try:
            result["Lookup_Key"] = pd.concat([self.__content__["Key"], fac2["Key"]], axis=0, ignore_index=True).unique()
        
        except ValueError:
            result["Lookup_Key"] = pd.Series(pd.concat([self.__content__["Key"],fac2["Key"]], axis=0, ignore_index=True).unique()).reindex()
        
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
        print("RESULT = \n{}".format(result))
        return result
  
    def show_detail(self):
        print(">>>>>>File source:\t {}".format(self.__path__+self.__file_name__+self.__ext__))
        print(">>>>>>File type:\t {}".format((lambda x: (lambda y: "Model Point File" if y == ".PRO" else "Result file")(x) if x !=".fac" else "Table")(self.__ext__)))
        print(">>>>>>File Shape:\t ({},{})".format(self.__content__.shape[0],(lambda x: x if self.__show_leading__ else x-1)(self.__content__.shape[1])))
        print(">>>>>>File Settings:\t key_num = {},\t show_leading = {}".format(self.__key_num__,self.__show_leading__))
        self.show_content()

    def show_content(self)->None:
        #printing function, print the table content
        if self.__show_leading__:
            print(self.__content__)
        else:
            print(self.__content__[[x for x in self.__content__.keys()[1:]]])
  
    def sort_records(self, target, target_col="", sort_timing="", inplace =False):
        #path input the directory of the file, ending with \\ string type expected
        #sort_timing, it used to sort the table with naming at specific timing string type expected
        # target Required Value for sorting, string type expected
        # target_col String, Traget location
        #inplace Bool, True if you want to modified the table content inside the table object
        #return the sorted result as new table
        if self.__ext__!=".PRO":
            raise Exception("Table Error, Not Model Point File")

        if target == "" or target_col == "":
            raise Exception("Policy No Criteria in string form is expected")
        
        if self.__file_name__.find(sort_timing) == -1:
            raise Exception("This file does not on time point = {}".format(sort_timing))       

        if inplace:
            self.__content__ = self.__content__[self.__content__[target_col] == target]
            return self
        
        return prophet_table(object = self.__content__[self.__content__[target_col] == target],path =self.get_path(),file = self.get_path()+self.get_ext(),show_leading= self.get_show_leading())

    def to_file(self, path="", as_csv=False)->None:
        #Path: String Expected Output path of the file
        #as_csv : Bool, True if you want to export as csv
        #Export the file into the desire path with the original extension or csv
        
        if  not(os.path.exists(path)):
            raise Exception("The Path is not exists")
        
        print("Exporting {}".format(self.__file_name__+self.__ext__))
        path =  (lambda x : x+"\\" if x.rfind("\\") != len(x)-1 else x)(path)
        if as_csv:
            if path!="":
                self.__content__.to_csv( path+self.__file_name__+".csv")
            else:
                self.__content__.to_csv(self.__path__+self.__file_name__+".csv")
                
        else:
            
            pass




        
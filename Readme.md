# FIS Prophet table inspector

## Objective

This module is based on padandas pd, and designed for single model point file system, for actuarial application  FIS Prophet  to resolve the issues and implement table-wise modifications

# Requirement:
    Pandas version >=2.0.1
    python version >=3.9.7

## Functions defined

Structure:</br>
    the file input will be split by four parts</br>
    1. Root directory for the table</br>
    2. File name without extension</br>
    3. File Extention  designed for determing file type</br>
    4. File content  which is oftenly  manipulated</br>


Last modified date: 7th July 2023
    
Data Member:
    for following members, without specification, you can refer to the __init__ function

    Private:
        __key_num__ 
        __file_name__ file name of the table
        __ext__ extension of the table
        __path__ root path of the table
        __content__ content of the file
    Public:
        show_leading
        show_table
        show_info
        columns name of column index of the table content 
        shape the shape of the table content 


Methods:    
    
    Private Methods
        def __init__(self, object =None, path="", file="", gen_key=False, show_leading = False, show_table = False,show_info = False)->None:
            #object: Pandas or prophet_table expected
            #path: String, the input directory of the file
            #file: String, file name with extension 
            #gen_key: Bool, use for mapping and comparison between table
            #show_leading: show when displaying the table content
            #show_table: True when you want to display all information when printing
            #show_info: True when you want to display all information in printing 
            #Constructor of the class

    operators and function overloading:

        def __getitem__(self, key)->pd.Series:
            #operator []
            #key: Same requirement as Pandas

        def __str__(self)->str:
            #print function string expression
        
        def __load_ext__(self, file)->None:
            #file string, input file name expected ending with extenstion
            #this function is designed to obtained the file extension

        def __lt__(self, other)->pd.Series:
            #< function overload
            #other: Same requirement as Pandas
        
        def __le__(self, other)->pd.Series:
            #<= function overload
            #other: Same requirement as Pandas
        
        def __eq__(self, other)->pd.Series:
            #== function overload
            #other: Same requirement as Pandas
        
        def __ne__(self, other)->pd.Series
            #!= function overload
            #other: Same requirement as Pandas

        def __gt__(self, other)->pd.Series:
            #> function overload
            #other: Same requirement as Pandas

        def __ge__(self, other)->pd.Series:
            #>= function overload
            #other: Same requirement as Pandas
    utility functions:
    
        def __key_loc__(self, key, lookup)->int:
            #this function will return the index of the key
            #lookup: the table you want to check with. Key: The target you want to find

          
        def __find_fac_header_row__(self)->int:
        '''
            find header row of a .fac or a model point file (the row starting with !)
            zero-indexed, i.e. if the header is at the first row, it will return 0
            credited to bensonby
        '''

        def __load_table__(self, drop_na=True)->None:
            #this function allow user to import the fac file with removed NA contents, you can disable it by comment the df.dropna() line

        def __find_key_num__(self)->int:
            #df the target dataframe, pandas dataframe is expected
            # value_compare: Boolean, True when you want to compare the value for whole table

public functions

content related:
        def gen_key(self, value_compare=False)->None:
            # value_compare: Boolean, True when you want to compare the value for whole table
            #this function will attach the key to the  target dataframe with key attached
                       

        def head(self,row_num)->pd.Series:
                #row_num: int, the number of row going to show
                #return the rows from head
        
        
        def tail(self,row_num)->pd.Series:
            #row_num: int, the number of row going to show
            #return the rows from tail


        def compare(self, table2)->pd.DataFrame:
            # fac2 = table 2 you imported prophet_table expected
            #  return the result of comparison with two columns [Lookup_Key,Result ] in pandas dataframe

        
        def get_ext(self)->str:
            #accessor, obtain the file extension
        
        def get_filename(self)->str:
            #accessor, obtain the file name

        def get_path(self)->str:
            #accessor, obtain the file root directory


        def get_key_num(self)->int:
            #accessor, obtain the number of col used for key


        def get_content(self)->pd.DataFrame:
            #accessor, obtain the file content

IO:
    def to_file(self, path="", as_csv=False)->None:
        #Path: String Expected Output path of the file
        #as_csv : Bool, True if you want to export as csv
        #Export the file into the desire path with the original extension or csv

    NOTE: to_file function is still underdeveloping for other output format. Only CSV avaliable now

## Example

```sh
#to load the tables
df1 = prophet_table(path = src2,file = tables[0])
df2 = prophet_table(path = src1,file =  tables[1])
```

With overloading the operators feature provided by the pandas, it maintains the same methodology of accessing table as dataframe. But it requries some attention that the result is on pd.series of the single column extraction. </br>If you want the prophet_table object, you can recreate it by passing the parameter used in genetarting the pd.Series object

```sh
#to obtain the dataframe col name SPCODE
df1['SPCODE'] #this will return a pd.series object

df1_replace = prophet_table(path = df1.get_path,file = df1.get_file_name()+df1.get_ext())

```

To sort the table or to compare the table, you can use the following code example

```sh
#return the records that satisfied the requirement
df1 = df1[df1['AGE_AT_ENTRY']<'40']

#compare both table
df1.compare(df2)
```

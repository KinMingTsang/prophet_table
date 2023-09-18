# FIS Prophet table inspector

## Objective

This module is based on padandas pd, and designed for single model point file system, for actuarial application  FIS Prophet  to resolve the issues and implement table-wise modifications

# Requirement:
    Pandas version >=2.0.1
    python version >=3.9.7

## Functions defined


Last modified date: 19th Sept 2023
    
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


Methods(Additional to Pandas are written):    
    
        def __key_loc__(self, key, lookup)->int:
            #this function will return the index of the key
            #lookup: the table you want to check with. Key: The target you want to find

          
        def __find_fac_header_row__(self)->int:
        '''
            find header row of a .fac or a model point file (the row starting with !)
            zero-indexed, i.e. if the header is at the first row, it will return 0
            credited to bensonby
        '''

        def __find_key_num__(self)->int:
            #df the target dataframe, pandas dataframe is expected
            # value_compare: Boolean, True when you want to compare the value for whole table

public functions

content related:
        def gen_key(self, value_compare=False)->None:
            # value_compare: Boolean, True when you want to compare the value for whole table
            #this function will attach the key to the  target dataframe with key attached
                       

        def get_key_num(self)->int:
            #accessor, obtain the number of col used for key
## Example

```sh
#to load the tables
from prophet_table.py import prophet_table
pp =prophet_table()
df1 = pp.read_csv(path = src2,file = tables[0])
df2 = pp.read_csv(path = src1,file =  tables[1])
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

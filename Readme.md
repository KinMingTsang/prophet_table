# FIS Prophet table inspector

## Objective

This module is based on padandas pd, and designed for single model point file system, for actuarial application  FIS Prophet  to resolve the issues and implement table-wise modifications

# Requirement:
    Pandas version >=2.0.1
    python version >=3.9.7

## Functions defined


Last modified date: 19th Sept 2023
    

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
```

To sort the table or to compare the table, you can use the following code example

```sh
#return the records that satisfied the requirement
df1 = df1[df1['AGE_AT_ENTRY']<'40']

#compare both table
df1.compare(df2)
```

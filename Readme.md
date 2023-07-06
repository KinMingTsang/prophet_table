# FIS Prophet table inspector
## Objective
This module is based on padandas pd, and designed for single model point file system, for actuarial application  FIS Prophet  to resolve the issues and implement table-wise modifications 

## Functions defined
    
    def get_ext(self)->str:
	    accessor, return the extension of the file

    def get_filename(self)->str:
        accessor, return the file name
    
    def get_path(self)->str:
        accessor, return the path of the file
    
    def compare(self, fac2)->pd.DataFrame:
        fac2 = table 2 you imported prophet_table object expected
        return the result of comparison with two columns [Lookup_Key,Result ]

    def print_table(self)->None:
        printing function, print the table content
        def sort_records(self, target, sort_timing="",target_col="",inplace =False) -> pd.DataFrame:
        path input the directory of the file, ending with \\ string type expected
        sort_timing, it used to sort the table with naming at specific timing string type expected
        target Required Value for sorting, string type expected
        target_col String, Traget location
        inplace Bool, True if you want to modified the table content inside the table object
        return the sorted result as pandas DataFrame

    def get_key_num(self):
        accessor, return the num of column used as key

    def to_file(self, path="", as_csv=False)->None:
        Path: String Expected Output path of the file
        as_csv : Bool, True if you want to export as csv
        Export the file into the desire path with the original extension or csv
        


    

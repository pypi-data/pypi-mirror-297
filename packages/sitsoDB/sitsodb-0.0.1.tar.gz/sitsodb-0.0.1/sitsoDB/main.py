
import pandas
import os

   
class Item:
    def __init__(self):
        self.standard = {
        
        }
        self.series = []
        self.shelf = {
        
        }
        self.current_dir = os.path.dirname(__file__)
        self.load_data()
        
    def load_data(self):
        """loads csv data into this file"""
        shelf_csv_path = os.path.join(self.current_dir, "shelfDB.csv")
        shelf = pandas.read_csv(shelf_csv_path)
        names = shelf['name'].to_list()
        ####
        filtered_names = [name for name in names if name != 'name']
        for name in filtered_names:
            dt = shelf[shelf['name'] == name] #picks the 'name' row out

            if name not in self.shelf: #if not in dictionary, creates a new 'name' and assigns its data
                self.shelf[name] = {dt['keys'].iloc[0]:dt['values'].iloc[0]} #load the first data
                for inx in range(len(dt['keys'])-1):
                    self.shelf[name].update({dt['keys'].iloc[inx+1]:dt['values'].iloc[inx+1]}) #load the rest of the data belonging to the row retrieved
                    
        #to load series
        series_csv_path = os.path.join(self.current_dir, "seriesDB.csv")
        series = pandas.read_csv(series_csv_path)
        data_series = series["0"].to_list()
        for element in data_series:
            self.series.append(element) 
       
        #to load standard
        standard_csv_path = os.path.join(self.current_dir, 'standardDB.csv')
        standard = pandas.read_csv(standard_csv_path)
        keys = standard['keys'].to_list()
        values = standard['values'].to_list()
        standard_db = dict(zip(keys, values))
        #to remove "keys"
        keys_to_delete = ['keys']
        for key in keys_to_delete:
            if key in standard_db:
                del standard_db[key]
        self.standard.update(standard_db)
        
            
    def showdb(self):
        """shows the raw dictionary | current status"""
        print(self.standard)
        print(self.series)
        print(self.shelf)
        
        
    def add_item(self, dtype, mode, name, *args, **kwargs):
        """adds an item to the array/dictionary"""
        if dtype == 'shelf' or dtype == 'sh':
            kwargs = {
                "keys":[key for key in kwargs.keys()],
                "values":[value for value in kwargs.values()]
            }  
            kwargs['name'] = f'{name}'
            shelf = pandas.DataFrame(kwargs)
            shelf_csv_path = os.path.join(self.current_dir, "shelfDB.csv")
            shelf.to_csv(shelf_csv_path, mode=mode, header=True)
            self.load_data()
            #### 
        elif dtype == 'series' or dtype == 'csv.s':
            data = pandas.Series(args)
            series_csv_path = os.path.join(self.current_dir, "seriesDB.csv")
            data.to_csv(series_csv_path, mode=mode, header=True)
            self.load_data()
            ####
        elif dtype == 'standard' or dtype == 'std':
            kwargs = {
                "keys":[key for key in kwargs.keys()],
                "values":[value for value in kwargs.values()]
            }  
            shelf = pandas.DataFrame(kwargs)
            standard_csv_path = os.path.join(self.current_dir, "standardDB.csv")
            shelf.to_csv(standard_csv_path, mode=mode, header=True)
            self.load_data()
            
            
    def export(self, path="C:/Users/HP/OneDrive/Desktop/exported_data.csv", **kwargs):
        """exports data in csv format. Note: when specifing file path use forward-slashes"""
        table = {
            "keys": [],
            "values": []
        }
        for k,v in kwargs.items():
            table["keys"].append(k)
            table["values"].append(v)
        data = pandas.DataFrame(table)
        data.to_csv(path, mode='w', index=True)
        
                        
    def get_item(self, dtype, name):
        """searches and shows the item requested details"""
        self.load_data()
        if dtype == 'shelf' or dtype == 'sh':
            #get name in shelf dtype
            results = self.shelf.get(name, 'Not Found') 
            print(f"item: {name: <3}| data: {str(results): <5}")
        elif dtype == 'series' or dtype == 'csv.s':
            #get element in series dtype
            try:
                element = self.series.index(name)
                results = self.series[element]
                print(f"dtype: series | data: {str(results): <5}")
            except:
                print('Not Found')
        elif dtype == 'standard' or dtype == 'std':
            #get key in standard dtype
            results = self.standard.get(name, "Not Found")
            print(f"item: {name: <3}| data: {str(results): <5}")
        
    def remove_item(self, dtype, name):
        """pops an item from array/dictionary"""
        if dtype == 'shelf' or dtype == 'sh':
            #to remove item in shelf
            try:
                self.shelf.pop(name)
                shelf_csv_path = os.path.join(self.current_dir, "shelfDB.csv")
                shelf = pandas.read_csv(shelf_csv_path)
                shelf = shelf.drop(shelf[shelf['name'] == name].index)
                shelf.to_csv(shelf_csv_path)
            except:
                print(f'Item not Found to remove')
        elif dtype == 'series' or dtype == 'csv.s':
            self.load_data()
            #to remove item in series
            try:
                element = self.series.index(name)
                series_csv_path = os.path.join(self.current_dir, "seriesDB.csv")
                del self.series[element]
                series = pandas.read_csv(series_csv_path)
                series = series.drop(series[series['0'] == name].index)
                series.to_csv(series_csv_path)
            except:
                print('Item not Found to Remove')
        elif dtype == 'standard' or dtype == 'std':
            #to remove item in standard
            try:
                self.standard.pop(name)
                standard_csv_path = os.path.join(self.current_dir, "standardDB.csv")
                standard = pandas.read_csv(standard_csv_path)
                standard = standard.drop(standard[standard['keys'] == name].index)
                standard.to_csv(standard_csv_path)
            except:
                print('Item not Found to Remove')
#https://github.com/0xG-MSK
#<-------join a community of DeVs and share your thoughts https://chat.whatsapp.com/Liof7yBVcC5Cbk95GQSI

item = Item()
item.export(a=1, b=5334, c=98112)
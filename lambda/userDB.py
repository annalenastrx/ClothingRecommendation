import pandas as pd

path = "user.csv"
df = pd.read_csv(path)

def get_username(name):
    nameInDf = name in df.Name.values
    return nameInDf

def add_name(name):
    print(name)
    #df.insert(loc=-1, column='Name', value=name)
    print(df)
    data = [{'Name':name,'Favouritecloth':'','Favouritecolor':'','Nogoscloth':'','Nogoscolor': '','Neveragain':''}]
    print(data)
    #df.append(data,ignore_index=True,sort=False)
    #df.loc[len(df.index)]=list(data[0].values())
    
    with open('user.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(data)
        f_object.close()
    
    return name

def get_fav_cloth(name):
    return df.loc[df['Name'].str.contains(name, na=False), 'Favouritecloth'].iloc[0]

def get_fav_color(name):
    return df.loc[df['Name'].str.contains(name, na=False), 'Favouritecolor'].iloc[0]

def get_hate_color(name):
    return df.loc[df['Name'].str.contains(name, na=False), 'Nogoscolor'].iloc[0]
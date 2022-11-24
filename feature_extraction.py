import pandas as pd
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
from features import Features

mypath = 'data/images'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

df = pd.DataFrame()
for l in tqdm(onlyfiles):
    new = Features(filename=l.replace('.jpg', ''), filepath=mypath+'/'+l)
    new.run()
    feat = new.features()
    feat['id'] = new.filename
    df = pd.concat([df, pd.DataFrame([feat])], ignore_index=True)

    
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'env/Lib/site-packages')))

import json
import pymongo
from utils import fx
# read the queue message and write to stdout
data = open(os.environ['data']).read()

data_dict = json.loads(data,strict=False)
print(data)
print(type(data_dict))

event = data_dict['event']
log = fx.get(event)
log(data_dict)
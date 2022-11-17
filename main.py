import dash
import dash_bootstrap_components as dbc
import os
from load_data import OSdata

directory_path = os.path.dirname(__file__)
path = os.path.join(directory_path, "Data")

print(path)


osdata_object = OSdata(path)


# Doesn't work
print(osdata_object.os_df("_events.csv"))
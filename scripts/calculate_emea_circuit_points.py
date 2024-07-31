import pandas as pd

from configs.EMEA_Config import emea_config_stage_1
from processors.calculate_circuit_points import calculatae_circuit_points

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


## determine maps played

calculatae_circuit_points(emea_config_stage_1)
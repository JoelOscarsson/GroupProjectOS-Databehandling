import pandas as pd
import os


class OSdata:
    # Creating data folder path
    # Maybe do property for this?
    def __init__(self, data_folder_path: str) -> None:
        self._data_folder_path = data_folder_path



    def os_df(self, osdataframe: str) -> list:
        os_df_list = []

        for path_ending in ["_events.csv", "_regions.csv"]:
            # os path för att det inte ska spela någon roll om man kör på mac eller windows

            # Example: 
            # data_folder_path: C:\Users\j_osc\OneDrive\Documents\Github\GroupProjectOS-Databehandling\Data
            # osdataframe: athlete_events
            # path_ending: _regions.csv

            # Resulting for one of the files
            # path: C:\Users\j_osc\OneDrive\Documents\Github\GroupProjectOS-Databehandling\Data\athlete_events.csv   
            path = os.path.join(self._data_folder_path, osdataframe+path_ending)



            os_data = pd.read_csv(path, index_col = 0)
            os_df_list.append(os_data)

        return os_df_list
    
   # def DataProcessing()



# class DataProcessing()



# En klass med olika methods 
# Filtrera på land


# path = r"Data/"
# os.chdir(path)


# def create_df():
#     """ read all files with end ".csv" from a specified folder and create dataframes
#     :return: dataframes
#     """
#     file_list = []
#     for file in sorted(os.listdir()):
#         if file.endswith(".csv"):
#             file_path = f"../{path}{file}"
#             file_list.append(file_path)

#     athlete_event = pd.read_csv(file_list[0])
#     noc_regions = pd.read_csv(file_list[1])
#     os.chdir('..')
#     return athlete_event, noc_regions
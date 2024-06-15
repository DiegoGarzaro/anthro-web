import pandas as pd
import os


FILE_PATH = __file__
UTILS_PATH = os.path.dirname(__file__)
BACKEND_PATH = os.path.dirname(UTILS_PATH)
DATA_PATH = os.path.join(BACKEND_PATH, "data")


def data_reader():

    # The files are named as follows:
    # {standard_metric}_{sex}_{age}_zscores.xlsx

    # Standard metrics:
    #   - lfha : Length/height-for-age
    #   - wfa  : Weight-for-age
    #   - wflh : Weight-for-length/height
    #   - bmi  : Body mass index
    #   - hcfa : Head circumference-for-age
    #   - acfa :
    #   - ssfa :
    #   - :
    #   - :

    # Sex:
    #   - girls
    #   - boys

    # Age:
    #  - 0-to-5-years
    #  - 2-to-5-years
    #  - 0-to-6-months

    # Metric:
    #   - zscores

    # Example:
    #   - wfa_boys_0-to-5-years_zscores.xlsx

    # Get all the files in the data folder
    files = os.listdir(path=DATA_PATH)

    # Create a dictionary to store the dataframes
    dfs = {}

    # Iterate over the files
    for file in files:
        # Split the file name
        file_name = file.split(".")[0]
        file_name = file_name.split("_")

        # Get information from the file name
        standard_metric = file_name[0]
        sex = file_name[1]
        age = file_name[2]
        metric = file_name[3]

        # Read the file
        df = pd.read_excel(io=os.path.join(DATA_PATH, file)).to_dict()

        # Store the dataframe in the dictionary
        # Check if the keys exist in the dictionary, otherwise create them
        if standard_metric not in dfs:
            dfs[standard_metric] = {}
        if sex not in dfs[standard_metric]:
            dfs[standard_metric][sex] = {}
        if age not in dfs[standard_metric][sex]:
            dfs[standard_metric][sex][age] = {}

        # Store the dataframe in the dictionary
        dfs[standard_metric][sex][age][metric] = df

    return dfs


# Test the function
if __name__ == "__main__":
    dfs = data_reader()

    print(dfs.keys())

    print(dfs["bmi"]["boys"]["0-to-13-weeks"]["zscores"])

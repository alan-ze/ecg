import glob
import os
import sys

import matlab.engine
import pandas as pd
from pymatreader import read_mat
from pathlib import Path


def load_matlab_table(engine, mat_file_path):
    # Create a temporary filename for the processed data
    base_dir = os.path.dirname(mat_file_path)
    filename = os.path.basename(mat_file_path)
    temp_file = os.path.join(base_dir, f"temp_processed_{filename}")

    try:
        # Convert table to struct
        engine.convert_table_to_struct(mat_file_path, temp_file, nargout=0)

        # Read with pymatreader
        data_dict = read_mat(temp_file)

        # Convert to dataframe
        # clean_dict = {k: v for k, v in data_dict.items() if not k.startswith("__")}
        df = pd.DataFrame(data_dict)

        return df

    except Exception as e:
        print(f"Error processing {mat_file_path}: {e}")
        return None

    finally:
        # Delete the temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python preprocessing.py <matlab_folder> <input_folder> <output_folder>")
        sys.exit(1)
    else:
        print("Starting MATLAB engine")
        eng = matlab.engine.start_matlab()
        data_dir_path = Path(sys.argv[1])
        for file_path in data_dir_path.rglob("*.mat"):
            print(f"Processing: {file_path}")
            df = load_matlab_table(eng, file_path)
            


# Start MATLAB Engine outside loop
print("Starting MATLAB Engine...")
eng = matlab.engine.start_matlab()

# Define your data directory
data_dir = "./data_directory"
mat_files = glob.glob(os.path.join(data_dir, "*.mat"))

all_data = []

for f in mat_files:
    print(f"Processing {f}...")
    df = load_matlab_table(eng, f)

    if df is not None:
        # Append to list or process immediately
        all_data.append(df)

        # Example: Access your complex data
        # 'ECG_Data' is likely a list of numpy arrays now
        print(f"  - Loaded {len(df)} rows.")
        print(f"  - First ECG data shape: {df['ECG_Data'][0].shape}")

# Stop Engine
eng.quit()

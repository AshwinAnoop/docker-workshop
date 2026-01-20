import sys
import pandas as pd

# Get the script name and month argument from command line
pythonFilename = sys.argv[0]
month = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "0"

# Create a sample DataFrame
df = pd.DataFrame({'Day': [1, 2, 3], 'No of passengers': [4, 5, 6]})
print(df)

# Save the DataFrame to a Parquet file
#install pyarrow or fastparquet to use to_parquet
df.to_parquet(f'pipeline_output_{month}.parquet')
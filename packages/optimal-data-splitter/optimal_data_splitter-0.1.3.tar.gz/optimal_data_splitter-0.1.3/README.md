# Optimal_data_splitter

## Overview
Optimal_data_splitter is a Python package created to enable data scientists to quickly and easily split their data into training, 
validation, and test data in an optimal manner. Many data scientists will split their data randomly, potentially with 
shuffling or stratification. Even with these approaches it is common for data to not be well distributed across all 
features or factors that may negatively influence the ability to adequately validate/test a model prior to deployment. 
Optimal_data_splitter resolves this by searching through many possible combinations of data splits and determining which one is the 
closest to the target split distribution.

## Installation
1. Use `pip install optimal-data-splitter` to install the package.

## Usage
1. Import the OptimalDataSplitter class using `from optimal_data_splitter import OptimalDataSplitter`
1. Splitting data using default settings can be done with:
   1. `splitter = OptimalDataSplitter(data=input_data)`
   1. `out = splitter.split_data()`
   1. The output data will have an additional `split` column that contains 'train', 'val', or 'test' labels.
   1. If this is done in a Jupyter notebook it will generate a couple of plots
1. Multiple parameters can be configured (see Configuration section) and included in the data split via the optional 
config input to `OptimalDataSplitter()`
   1.  `splitter = OptimalDataSplitter(data=input_data, config=config_dict)`

## Data Input Format
1. Optimal_data_splitter expects the data input to be a Pandas DataFrame with the following restrictions:
   1. The first column must be title 'id'
   1. The 'id' column must have a unique identifier for each row. An example would be a filename or a uuid.
   1. All other columns must only contain numerical (float or int) data
   1. The numeric (feature) columns are expected to be the count of that feature for that row
      1. For features with distributions (e.g. image brightness), the recommended approach is to separate the 
      distribution into some number of buckets, and then one hot encode the rows into them as appropriate.
      1. The appropriate number of buckets depends on the distribution, but keeping the number low is recommended to 
      minimize complexity and ensure there is sufficient data to split within each bucket. Something like 2-5 buckets is 
      usually reasonable.
      1. A good approach to buckets is to use equally sized buckets based on evenly spaced percentiles, but it is 
      highly recommended that users visualize the distribution of all features to ensure the buckets capture any obvious
      information (e.g. clearly separate bimodal distribution).

## Configuration
The config attribute in optimal_data_splitter expects a dictionary of optional configuration parameters. Anywhere from zero to all 
of these parameters can be changed for any particular run. The available parameters to configure and their default 
values are:
1. val_percent = 0.1; Portion of data to place in validation set (val). Must be between 0 and 1.
1. test_percent = 0.1; Portion of data to place in test set. Must be between 0 and 1.
1. num_iterations = 1000; Number of iterations to randomly check in each split. It is not recommended to decrease this 
number below 1000.
1. splits_cols = None; Specific columns to include in the data split calculation. None will include all columns except id. A list of column names will result in only those columns being considered. Use this to exclude non-numeric columns from the calculation.
1. save_output = True; If True then save the resulting data split and plots to file. Set to False to avoid saving 
anything to file.
1. output_path = './'; Set the path to the directory to save the results and plot if save_output is True.
1. results_filename = 'split_data.csv'; Set the filename of the split results if save_output is True.
1. l2_plot_filename = 'l2_results.png'; Set the filename of the L2 plot if save_output is True.
1. results_plot_filename = 'results.png'; Set the filename of the results plot if save_output is True.

## Tips
1. If the L2 plot shows a floor of L2 values with only 1 or 2 results below that floor you may get better results by 
increasing the num_iterations parameter. Note that this will increase runtime.
1. If you are not data limited a 80/10/10 train/val/test split or 80/20 train/test split is a good place to start. If 
data limited, something like 60/20/20 is better.

## Example
The below is an example using some sample data with 6 features (f1 to f6) and 30 files (file1 to file30). This data can 
be obtained from the repo at https://github.com/mrock929/optimal-data-splitter.

```commandline
import pandas as pd
from optimal_data_splitter import OptimalDataSplitter

input_data = pd.read_csv('./sample_data.csv')

config = {'num_iterations': 5000}

splitter = OptimalDataSplitter(data=input_data, config=config)
out = splitter.split_data()

out.head()
```
### Sample output
![](./sample_out.PNG)

### L2 plot
![](./l2_results_example.png)

Note the somewhat distinct floor in both data splits just below 0.1. If only 1000 iterations were used, only a few 
values would be below the floor, but with 5000 iterations there are 10-20 values below the floor. This is more likely 
to produce a good data split. The black symbols were the iterations used for the final split.

### Results plot
![](./results_5000.png)

This plot shows the percentage of data within each portion of the split for each features (f1-f6 in this example).
This is the results from a 5000 iteration split. The data is fairly well balanced between train, validation, and test 
with a roughly 80/10/10 distribution across all features.

![](./results_1.png)

If a random split was performed using the same data as above, this is the result for random_state = 1. Note how poorly 
distributed some of the features are.

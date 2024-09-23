import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from typing import Tuple
from copy import deepcopy


class OptimalDataSplitter:
    """
    Class for optimally splitting data into train, validation, and test sets for machine learning problems
    """

    def __init__(self, data: pd.DataFrame, config: dict = None):
        """
        Initialize class attributes, check input data, and configure for data splitting

        Args:
            data: Input dataframe
            config: Dictionary containing configuration information
        """

        self.data = data

        # These are reasonable defaults for many problems
        # These are overwritten by config if values are set there
        self.val_percent = 0.1  # Minimum supported is 0.001 or 0.1% of the data
        self.test_percent = 0.1  # Minimum supported is 0.001 or 0.1% of the data
        self.num_iterations = 1000  # Number of iterations to randomly check in each split, recommend at least 1000
        self.split_cols = None
        self.save_output = True  # Set True to save output dataframe and plots to file
        self.output_path = './'
        self.results_filename = 'split_data.csv'
        self.l2_plot_filename = 'l2_results.png'
        self.results_plot_filename = 'results.png'

        # TODO add ability to hold out specific files for test/val (test_ids, val_ids)
        # TODO always update readme if adding any new configs
        # TODO If config gets more complicated, save config to file as results_filename + _config.yaml or .txt

        # Check that input data is valid
        self.check_data()

        # Configure
        self.update_config(config=config)

        # Check for valid configuration
        self.check_config()

    def split_data(self) -> pd.DataFrame:
        """
        Perform one or two data splits depending on test and val percent desired.


        Returns:
            Dataframe with input data with an additional 'split' column with each row labeled as 'train', 'val',
                or 'test'
            Also saves a couple of plots and optionally saves the dataframe to file

        """

        # Split test data
        if self.test_percent >= 0.001:
            test_split, test_l2_vals, test_index = self.perform_split(data=self.data, test_size=self.test_percent, is_test=True)
        else:
            test_split = self.data
            test_split['split'] = 'train'
            test_l2_vals = []
            test_index = None

        # Split val data
        if self.val_percent >= 0.001:
            output_data, val_l2_vals, val_index = self.perform_split(data=test_split, test_size=self.val_percent * (1 - self.test_percent), is_test=False)
        else:
            output_data = test_split
            val_l2_vals = []
            val_index = None

        self.plot_results(data=output_data, val_index=val_index, test_index=test_index, val_l2=val_l2_vals, test_l2=test_l2_vals)

        # Save and return results
        if self.save_output:
            output_data.to_csv(self.output_path + self.results_filename)

        return output_data

    def check_data(self) -> None:
        """
        Checks input data to ensure it is valid
        First column must be 'id' and contain info that uniquely identifies each row
        The remaining columns can have any title, but must contain ints or floats

        Raises:
            ValueError if the first column is not named 'id'
            Value if the id column does not contain unique values
            TypeError if the non-id columns have non-numeric dtypes

        """

        if self.data.columns[0] != 'id':
            raise ValueError("The first column in the input data must be named id.")

        # Check for uniqueness
        if len(self.data['id']) != len(self.data['id'].unique()):
            raise ValueError("The id column must contain unique values for each row.")

        # Check for numeric feature columns
        types = self.data.dtypes
        for i, col_type in enumerate(types[1:]):
            if not pd.api.types.is_numeric_dtype(col_type):
                raise TypeError(f"The {self.data.columns[i]} column must have a numeric type. It has a type of {col_type}.")

    def update_config(self, config: dict) -> None:
        """
        Update the configuration class attributes

        Args:
            config: Input config dictionary, may be None

        """

        if config is None:
            pass
        else:
            for k, v in config.items():
                if k not in self.__dict__.keys():
                    raise KeyError(f"The key '{k}' in the config dict is not a valid key. It must be in "
                                   f"{self.__dict__.keys()}.")
                else:
                    setattr(self, k, v)

        # Keep the id col for splitting
        if self.split_cols is not None:
            self.split_cols.insert(0, 'id')

    def check_config(self) -> None:
        """
        Check that all config parameters are in valid ranges and have valid types
        """

        if self.val_percent < 0.001 or self.val_percent > 1.0:
            raise ValueError(f"val_percent must be between 0.001 and 1.0. Current value = {self.val_percent}")

        if self.test_percent < 0.001 or self.test_percent > 1.0:
            raise ValueError(f"test_percent must be between 0.001 and 1.0. Current value = {self.test_percent}")

        if self.num_iterations < 1:
            raise ValueError(f"num_iterations must be a positive number. Current value = {self.num_iterations}")

        if self.num_iterations % 1 != 0:
            raise TypeError(f"num_iterations must be an integer. Current value = {self.num_iterations}")

        if type(self.save_output) != bool:
            raise TypeError(f"save_output must be a boolean. Current value = {self.save_output}")
        
        if self.split_cols is not None and len(self.split_cols) < 1:
            raise ValueError(f"split_cols must have at least one column name within a list or be None")

    def perform_split(self, data: pd.DataFrame, test_size: float, is_test: bool) -> Tuple[pd.DataFrame, list, int]:
        """
        Optimally split the data based on the input configs

        Args:
            data: Input dataframe
            test_size: Percent of the data to split into test or val
            is_test: If True, then the test data is labeled 'test', else it is labeled 'val'

        Returns:
            The same dataframe as the input with a column added (if it doesn't exist already) that categorizes each row of the data as train, val, or test

        """

        # If test set already exists, only split the remaining training data into train and val
        if 'split' in data.columns:
            data2 = data.loc[data['split'] == 'train'].drop(columns=['split'])
        else:
            data2 = data

        # If user specified columns to split on, only consider those
        if self.split_cols is not None:
            data2 = deepcopy(data2[self.split_cols])

        l2_norm_vals = []

        best_l2 = 1.0e10
        y_best = 0
        best_index = -1

        for i in range(self.num_iterations):
            # Train test split
            X, y = train_test_split(data2, test_size=test_size, random_state=i, shuffle=True)
            # TODO test shuffle vs stratify, other functions
            # Calc L2 norm, store best split
            # Get diff between actual test percent and target percent for each column
            norm_data = []
            for col in data2.iloc[:, 1:].columns:
                norm_data.append(y[col].sum() / (X[col].sum() + y[col].sum()) - test_size)
            l2_val = np.linalg.norm(norm_data)  # Defaults to L2 norm for vectors
            l2_norm_vals.append(l2_val)

            if l2_val < best_l2:
                best_index = i
                best_l2 = l2_val
                y_best = y

        # Set train/val/test labels in original dataframe
        if is_test:
            test_label = 'test'
        else:
            test_label = 'val'

        data2['split'] = 'train'
        data2.loc[data2['id'].isin(y_best['id']), 'split'] = test_label

        if 'split' not in data.columns:
            data['split'] = 'train'

        # Move updated values back into input data
        data.update(data2)

        return data, l2_norm_vals, best_index

    def plot_results(self, data: pd.DataFrame, val_index: int, test_index: int, val_l2: list, test_l2: list) -> None:
        """
        Plot the results of the data split
        The L2 plot shows distribution of L2 values. If there are only a few values below a floor with many values,
            increasing the num_iterations may provide an improved split, but will also increase the runtime.
        The Results plot shows the distribution of features in the final split.

        Args:
            data: Output dataframe after data split
            val_index: Index of best L2 result for val splits
            test_index: Index of best L2 result for test splits
            val_l2: List of L2 values for val split
            test_l2: List of L2 values for test split

        Returns:
            Nothing, but saves 2 plots to file.

        """

        # Create plot of L2 values
        fig = plt.figure()
        if test_index is not None:
            plt.plot(test_l2, 'x', label='test', color='tab:green')
            plt.plot(test_index, test_l2[test_index], 'kx')
        if val_index is not None:
            plt.plot(val_l2, '+', label='val', color='tab:orange')
            plt.plot(val_index, val_l2[val_index], 'k+')
        plt.xlabel('Iteration')
        plt.ylabel('L2-Norm')
        plt.legend()
        if self.save_output:
            plt.savefig(self.output_path + self.l2_plot_filename)

        # Create plot of results
        # For each feature, need percent in train, val, test
        col_sums = data.iloc[:, 1:-1].sum(axis=0)
        val_percent = data.loc[data['split'] == 'val'].iloc[:, 1:-1].sum(axis=0).multiply(100).divide(
            col_sums)
        test_percent = data.loc[data['split'] == 'test'].iloc[:, 1:-1].sum(axis=0).multiply(100).divide(
            col_sums)
        train_percent = 100 - val_percent - test_percent

        results = pd.concat([train_percent, val_percent, test_percent], axis=1, ignore_index=True)

        colors = ['tab:blue', 'tab:orange', 'tab:green']

        fig = plt.figure()
        for index, row in results.iterrows():
            left = 0.0
            for i in range(len(row)):
                plt.barh(y=index, width=row[i], label=index, left=left, color=colors[i])
                left += row[i]
        plt.title('Data Split Results')
        plt.xlabel('% of data')
        plt.gca().invert_yaxis()
        plt.legend(labels=['Train', 'Val', 'Test'], loc='upper left')
        if self.save_output:
            plt.savefig(self.output_path + self.results_plot_filename)

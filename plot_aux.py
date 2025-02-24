import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import pandas as pd
import numpy as np

def plot_by_column(df, column_name):
    """
    Plots the distribution of values in a specified column of a DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column_name (str): The column name to plot.

    Returns:
        None
    """
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Check the data type of the column
    if df[column_name].dtype == 'object' or df[column_name].dtype.name == 'category':
        # Categorical data: Use a count plot
        plt.figure(figsize=(8, 6))
        ax = sns.countplot(data=df, y=column_name, order=df[column_name].value_counts().index)
        plt.title(f"Distribution of {column_name}")
        plt.xlabel("Count")
        plt.ylabel(column_name)
        
        # Add values to the bars
        for container in ax.containers:
            ax.bar_label(container)
    else:
        # Numerical data: Use a histogram
        plt.figure(figsize=(10, 6))
        ax = sns.histplot(df[column_name], kde=True)
        plt.title(f"Distribution of {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Frequency")
        
        # Add values to the bars if histogram
        for container in ax.containers:
            labels = [int(v.get_height()) if v.get_height() > 0 else '' for v in container]
            ax.bar_label(container, labels=labels)

    plt.tight_layout()
    plt.show()
    

def plot_by_columns(df, column_names):
    """
    Plots the distribution of values for a list of columns in a DataFrame, with up to 8 plots in a single figure.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column_names (list of str): The list of column names to plot.

    Returns:
        None
    """
    # Check if all columns exist in the DataFrame
    for column_name in column_names:
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Set up the figure
    num_columns = len(column_names)
    num_rows = (num_columns + 3) // 4  # Up to 4 columns per row
    fig, axes = plt.subplots(num_rows, 4, figsize=(20, 5 * num_rows))
    axes = axes.flatten()

    for i, column_name in enumerate(column_names):
        ax = axes[i]
        # Check the data type of the column
        if df[column_name].dtype == 'object' or df[column_name].dtype.name == 'category':
            # Categorical data: Use a count plot
            sns.countplot(data=df, y=column_name, order=df[column_name].value_counts().index, ax=ax)
            ax.set_title(f"Distribution of {column_name}")
            ax.set_xlabel("Count")
            ax.set_ylabel(column_name)
            # Add values to the bars
            for container in ax.containers:
                labels = [int(v.get_width()) if v.get_width() > 0 else '' for v in container]
                ax.bar_label(container, labels=labels)
        else:
            # Numerical data: Use a histogram
            sns.histplot(df[column_name], kde=True, bins=30, ax=ax)
            ax.set_title(f"Distribution of {column_name}")
            ax.set_xlabel(column_name)
            ax.set_ylabel("Frequency")
            # Add values to the bars if histogram
            for container in ax.containers:
                labels = [int(v.get_height()) if v.get_height() > 0 else '' for v in container]
                ax.bar_label(container, labels=labels)

    # Remove any unused subplots
    for j in range(len(column_names), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def plot_boxplots_by_columns(df, column_names):
    """
    Plots boxplots for a list of columns in a DataFrame, with up to 8 plots in a single figure.
    Annotates each plot with mean, median, max, and min values.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column_names (list of str): The list of column names to plot.

    Returns:
        None
    """
    # Check if all columns exist in the DataFrame
    for column_name in column_names:
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame.")
        
    numeric_features = df.select_dtypes(['float', 'int']).columns.tolist()
    sets = [set(lst) for lst in [numeric_features, column_names]]
    
    column_names = list(set.intersection(*sets))

    # Set up the figure
    num_columns = len(column_names)
    num_rows = (num_columns + 3) // 4  # Up to 4 columns per row
    fig, axes = plt.subplots(num_rows, 4, figsize=(20, 5 * num_rows))
    axes = axes.flatten()

    for i, column_name in enumerate(column_names):
        ax = axes[i]
        if df[column_name].dtype != 'object' and df[column_name].dtype.name != 'category':
            # Plot boxplot for numerical data
            sns.boxplot(data=df, y=column_name, ax=ax)
            ax.set_title(f"Boxplot of {column_name}")
            ax.set_ylabel(column_name)

            # Calculate statistics
            column_data = df[column_name].dropna()
            mean_val = column_data.mean()
            median_val = column_data.median()
            max_val = column_data.max()
            min_val = column_data.min()

            # Add annotations for mean, median, max, and min
            ax.axhline(mean_val, color='blue', linestyle='--', linewidth=1, label=f"Mean: {mean_val:.2f}")
            ax.axhline(median_val, color='green', linestyle='--', linewidth=1, label=f"Median: {median_val:.2f}")
            ax.axhline(max_val, color='red', linestyle='--', linewidth=1, label=f"Max: {max_val:.2f}")
            ax.axhline(min_val, color='purple', linestyle='--', linewidth=1, label=f"Min: {min_val:.2f}")

            ax.legend(loc='upper right')
        else:
            ax.axis('off')  # Skip categorical data for boxplots

    # Remove any unused subplots
    for j in range(len(column_names), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
 
def plot_boxplots_by_columns_hue(df, column_names, hue):
    """
    Plots boxplots for a list of columns in a DataFrame, with up to 8 plots in a single figure.
    Annotates each plot with mean, median, max, and min values.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column_names (list of str): The list of column names to plot.

    Returns:
        None
    """
    # Check if all columns exist in the DataFrame
    for column_name in column_names:
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame.")
        
    numeric_features = df.select_dtypes(['float', 'int']).columns.tolist()
    sets = [set(lst) for lst in [numeric_features, column_names]]
    
    column_names = list(set.intersection(*sets))

    # Set up the figure
    num_columns = len(column_names)
    num_rows = (num_columns + 3) // 4  # Up to 4 columns per row
    fig, axes = plt.subplots(num_rows, 4, figsize=(20, 5 * num_rows))
    axes = axes.flatten()

    for i, column_name in enumerate(column_names):
        ax = axes[i]
        if df[column_name].dtype != 'object' and df[column_name].dtype.name != 'category':
            # Plot boxplot for numerical data
            sns.boxplot(data=df, y=column_name, ax=ax, hue=hue)
            ax.set_title(f"Boxplot of {column_name}")
            ax.set_ylabel(column_name)

            ax.legend(loc='upper right')
        else:
            ax.axis('off')  # Skip categorical data for boxplots

    # Remove any unused subplots
    for j in range(len(column_names), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()   


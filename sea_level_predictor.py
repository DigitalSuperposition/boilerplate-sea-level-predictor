import pandas as pd
import matplotlib.pyplot as plt
import importlib
try:
    stats = importlib.import_module('scipy.stats')
    linregress = stats.linregress
except Exception:
    import numpy as np
    def linregress(x, y):
        x = np.array(x)
        y = np.array(y)
        # slope and intercept from polyfit
        slope, intercept = np.polyfit(x, y, 1)
        # correlation coefficient
        r_value = np.corrcoef(x, y)[0, 1] if x.size > 1 else np.nan
        # p-value not computed here
        p_value = np.nan
        # standard error of the slope
        n = x.size
        y_hat = slope * x + intercept
        ss_res = np.sum((y - y_hat) ** 2)
        ss_x = np.sum((x - x.mean()) ** 2)
        std_err = np.sqrt(ss_res / (n - 2) / ss_x) if n > 2 and ss_x != 0 else np.nan
        return slope, intercept, r_value, p_value, std_err

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'])

    # Create first line of best fit
    slope, intercept, r_value, p_value, std_err = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    x_pred = range(1880, 2051)
    y_pred = slope * x_pred + intercept
    plt.plot(x_pred, y_pred, color='red')

    # Create second line of best fit
    df_2000 = df[df['Year'] >= 2000]
    slope, intercept, r_value, p_value, std_err = linregress(df_2000['Year'], df_2000['CSIRO Adjusted Sea Level'])
    x_pred = range(2000, 2051)
    y_pred = slope * x_pred + intercept
    plt.plot(x_pred, y_pred, color='green')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')    
    plt.title('Rise in Sea Level')
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import scipy.stats as stats


def pearson_correlation(meth_matrix: np.array, phenotype: np.array) -> np.array:
    """calculate pearson correlation coefficient between rows of input matrix and phenotype"""
    # calculate mean for each row and phenotype mean
    matrix_means = np.mean(meth_matrix, axis=1)
    phenotype_mean = np.mean(phenotype)

    # subtract means from observed values
    transformed_matrix = meth_matrix - matrix_means.reshape([-1,1])
    transformed_phenotype = phenotype - phenotype_mean

    # calculate covariance
    covariance = np.sum(transformed_matrix * transformed_phenotype, axis=1)
    variance_meth = np.sqrt(np.sum(transformed_matrix ** 2, axis=1))
    variance_phenotype = np.sqrt(np.sum(transformed_phenotype ** 2))

    return covariance / (variance_meth * variance_phenotype)

def r2(x,y):
    # return r squared
    return stats.pearsonr(x,y)[0] **2

def plot_known_predicted_ages(known_ages, predicted_ages, label=None):
    # define optimization function
    def func(x, a, b, c):
        return a * np.asarray(x)**0.5 + c
    # fit trend line
    popt, pcov = optimize.curve_fit(func, [1 + x for x in known_ages], predicted_ages)
    # get r squared
    rsquared = r2(predicted_ages, func([1 + x for x in known_ages], *popt))
    # format plot label
    plot_label = f'$f(x)={popt[0]:.2f}x^{{1/2}} {popt[2]:.2f}, R^{{2}}={rsquared:.2f}$'
    # initialize plt plot
    fig, ax = plt.subplots(figsize=(8,8))
    # plot trend line
    ax.plot(sorted(known_ages), func(sorted([1 + x for x in known_ages]), *popt), 'r--', label=plot_label)
    # scatter plot
    ax.scatter(known_ages, predicted_ages, marker='o', alpha=0.8, color='k')
    ax.set_title(label, fontsize=18)
    ax.set_xlabel('Chronological Age', fontsize=16)
    ax.set_ylabel('Epigenetic State', fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.legend(fontsize=16)
    plt.show()
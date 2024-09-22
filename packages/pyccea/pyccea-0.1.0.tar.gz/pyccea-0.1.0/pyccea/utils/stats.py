import logging
import numpy as np
from scipy import stats

# Initialize logger with info level
logging.basicConfig(level=logging.INFO)
# Reset handlers
logging.getLogger().handlers = []
# Add a custom handler
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logging.getLogger().addHandler(handler)

def statistical_comparison_between_distributions(x, y, alpha=0.05, alternative="two-sided"):

    logging.info(f"Sample sizes: {len(x)}, {len(y)}")

    if len(x) < 3:
        logging.info(f"1st sample has only {len(x)} observation(s).")
    if len(y) < 3:
        logging.info(f"2nd sample has only {len(y)} observation(s).")
    logging.info("")
    if len(x) >= 3 and len(y) >= 3:

        logging.info("Applying Shapiro-Wilk test for normality...")
        diff = np.array(x) - np.array(y)
        k_n, p_value_n = stats.shapiro(diff)
        logging.info(f"p-value of {p_value_n}.\n")

        if (p_value_n > alpha):
            logging.info("Applying Paired sample t-test for comparison...")
            k2, p_value = stats.ttest_ind(x, y, alternative=alternative)
        # The null-hypothesis of the Shapiro Wilk test is that the population is normally distributed.
        # Thus, if the p value is less than the chosen alpha level, then the null hypothesis is rejected and there is evidence that the
        # data tested are not normally distributed.
        else:
            logging.info("Applying Wilcoxon signed-rank test for comparison...")
            # The presence of “ties” (i.e. not all elements of d are unique) and “zeros” (i.e. elements of d are zero) changes
            # the null distribution of the test statistic, and method='exact' no longer calculates the exact p-value. If method='approx',
            # the z-statistic is adjusted for more accurate comparison against the standard normal, but still, for finite sample sizes,
            # the standard normal is only an approximation of the true null distribution of the z-statistic.
            # There is no clear consensus among references on which method most accurately approximates the p-value for small samples in
            # the presence of zeros and/or ties.
            k2, p_value = stats.wilcoxon(x, y, alternative=alternative, method="approx")

        if p_value <= alpha:
            # The mean of the paired differences equals zero in the population.
            # Alternative hypothesis: The mean of the paired differences does not equal zero in the population.
            confidence_level = int((1-alpha)*100)
            alternative = 'different from' if alternative == 'two-sided' else f'{alternative} than'
            logging.info(f"There are statistical differences between the two samples with a confidence level of {confidence_level}%.")
            logging.info(f"The 1st sample is statistical {alternative} the 2nd sample.")
        else:
            logging.info("There are NOT statistical differences between the two samples.")
        logging.info(f"p-value of {p_value}.")
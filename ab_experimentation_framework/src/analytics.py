import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

class ExperimentAnalyzer:
    def __init__(self, data):
        self.data = data
        self.control = data[data['group'] == 'control']
        self.treatment = data[data['group'] == 'treatment']

    def analyze_primary_metric(self, alpha=0.05):
        """Performs a Z-test for proportions on conversion rates."""
        # Aggregate counts
        successes = [self.treatment['converted'].sum(), self.control['converted'].sum()]
        nobs = [len(self.treatment), len(self.control)]

        # 1. Z-test for proportions
        z_stat, p_value = proportions_ztest(successes, nobs, alternative='larger')
        
        # 2. Calculate Confidence Intervals (95%)
        ci_low_tr, ci_upp_tr = proportion_confint(successes[0], nobs[0], alpha=alpha)
        ci_low_co, ci_upp_co = proportion_confint(successes[1], nobs[1], alpha=alpha)

        return {
            'metric': 'Conversion Rate',
            'control_mean': self.control['converted'].mean(),
            'treatment_mean': self.treatment['converted'].mean(),
            'lift': (self.treatment['converted'].mean() / self.control['converted'].mean()) - 1,
            'p_value': p_value,
            'is_significant': p_value < alpha,
            'ci_treatment': (ci_low_tr, ci_upp_tr)
        }

    def analyze_guardrail_metric(self, alpha=0.05):
        """Performs a T-test on continuous guardrail metrics (Latency)."""
        t_stat, p_value = stats.ttest_ind(
            self.treatment['latency_ms'], 
            self.control['latency_ms'], 
            equal_var=False
        )
        
        # We check if latency INCREASED significantly
        mean_diff = self.treatment['latency_ms'].mean() - self.control['latency_ms'].mean()
        violated = (p_value < alpha) and (mean_diff > 0)

        return {
            'metric': 'Avg Latency (ms)',
            'control_mean': self.control['latency_ms'].mean(),
            'treatment_mean': self.treatment['latency_ms'].mean(),
            'p_value': p_value,
            'guardrail_violated': violated
        }
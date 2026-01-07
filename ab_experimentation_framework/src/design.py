import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

class ExperimentDesigner:
    def __init__(self, baseline_cr, mde, alpha=0.05, power=0.80):
        self.baseline_cr = baseline_cr
        self.mde = mde
        self.alpha = alpha
        self.power = power

    def calculate_sample_size(self):
        """
        Calculates the required sample size per group.
        Uses a two-sample t-test power analysis.
        """
        # 1. Calculate the target conversion rate
        treatment_cr = self.baseline_cr + self.mde
        
        # 2. Calculate the effect size (Cohen's h)
        # This standardizes the difference between the two proportions
        effect_size = proportion_effectsize(self.baseline_cr, treatment_cr)
        
        # 3. Solve for sample size (n)
        analysis = NormalIndPower()
        required_n = analysis.solve_power(
            effect_size=effect_size, 
            alpha=self.alpha, 
            power=self.power, 
            ratio=1.0  # Equal size for both groups
        )
        
        return int(np.ceil(required_n))

    def summarize_design(self, n):
        print("-" * 30)
        print("EXPERIMENT DESIGN SUMMARY")
        print("-" * 30)
        print(f"Baseline CR: {self.baseline_cr*100:.2f}%")
        print(f"Target Lift (MDE): {self.mde*100:.2f}%")
        print(f"Required Sample Size per Group: {n:,}")
        print(f"Total Sample Size: {n*2:,}")
        print("-" * 30)
import numpy as np
import pandas as pd

class DataSimulator:
    def __init__(self, n, baseline_cr):
        self.n = n
        self.baseline_cr = baseline_cr

    def generate_experiment_data(self, actual_lift, latency_increase=5):
        """
        Generates a synthetic dataset for the experiment.
        
        actual_lift: The real improvement we're hiding in the data.
        latency_increase: How much slower the treatment is (to test guardrails).
        """
        # 1. Generate Conversions (Binomial Distribution)
        # Control group
        control_conversions = np.random.binomial(1, self.baseline_cr, self.n)
        
        # Treatment group (Baseline + Actual Lift)
        treatment_cr = self.baseline_cr + actual_lift
        treatment_conversions = np.random.binomial(1, treatment_cr, self.n)

        # 2. Generate Guardrail Metric: Latency (Normal Distribution)
        # Control: Mean 200ms, Std Dev 50
        control_latency = np.random.normal(200, 50, self.n)
        # Treatment: Mean 200ms + latency_increase, Std Dev 50
        treatment_latency = np.random.normal(200 + latency_increase, 50, self.n)

        # 3. Combine into a DataFrame
        data = pd.DataFrame({
            'user_id': np.arange(self.n * 2),
            'group': ['control'] * self.n + ['treatment'] * self.n,
            'converted': np.concatenate([control_conversions, treatment_conversions]),
            'latency_ms': np.concatenate([control_latency, treatment_latency])
        })

        # Shuffle the data to mimic real-world arrival
        return data.sample(frac=1).reset_index(drop=True)
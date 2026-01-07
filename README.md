# A/B Testing & Experimentation Framework

An end-to-end Python framework designed to manage the full lifecycle of a randomized controlled trial (RCT). This project incorporates **Statistical Power Analysis**, **Synthetic Data Simulation**, and **Hypothesis Testing** to drive data-driven product decisions while protecting system performance via **Guardrail Metrics**.

## 🚀 Key Features

* **Power Analysis:** Automated sample size calculation to prevent underpowered experiments and Type II errors.
* **Metric Strategy:** Evaluation of Primary Metrics (Conversion Rate) alongside Guardrail Metrics (System Latency).
* **Causal Inference:** Uses Two-Sample Z-tests and T-tests to ensure observed lifts are statistically significant.
* **Automated Decision Logic:** A built-in decision engine that recommends "Rollout," "Investigate," or "Stop" based on results.

## 📁 Project Structure

```text
ab_experimentation_framework/
├── src/
│   ├── design.py        # Power analysis & Sample size logic
│   ├── simulator.py     # Binomial & Normal distribution data generation
│   └── analytics.py     # Z-tests, T-tests, & Confidence Intervals
├── notebooks/           # Visual distribution analysis (KDE & Bar plots)
├── config.yaml          # Experiment parameters (MDE, Alpha, Power)
├── main.py              # Orchestration script
└── requirements.txt     # Dependency list

```

## 🛠️ Installation & Usage

1. **Clone the repository and enter the directory:**
```bash
git clone https://github.com/yourusername/ab-testing-framework.git
cd ab-testing-framework

```


2. **Setup the Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

```


3. **Run the Pipeline:**
```bash
python main.py

```



## 📊 Methodology

### 1. Statistical Design

Before data collection, we define the **Minimum Detectable Effect (MDE)**. We use Cohen’s  to calculate the standardized effect size for proportions, ensuring the experiment has 80% Power to detect a true lift.

### 2. Hypothesis Testing

We evaluate the Null Hypothesis (): *The treatment has no effect on conversion rates.* * **Primary Metric:** Two-Sample Z-Test for Proportions.

* **Guardrail Metric:** Welch's T-test to monitor for significant increases in latency.

## 📈 Results Visualization

The project includes a Jupyter Notebook that generates:

* **Confidence Interval Plots:** Visualizing the uncertainty around conversion rates.
* **KDE Density Plots:** Monitoring the distribution shift in latency to ensure no performance degradation.

## 🧠 Business Logic Table

| Outcome | Result | Recommendation |
| --- | --- | --- |
| **Statistically Sig. Lift** | No Guardrail Violation | **Full Rollout** |
| **Statistically Sig. Lift** | Guardrail Violated (Latency ↑) | **Investigate Technical Debt** |
| **Non-Significant** | No Violation | **Iterate or Discard** |

---

import yaml
from src.design import ExperimentDesigner
from src.simulator import DataSimulator
from src.analytics import ExperimentAnalyzer

def run_experiment_pipeline():
    # 1. Load Configuration
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    exp_params = config['experiment']
    
    print(f"🚀 Starting Experiment: {exp_params['name']}")

    # 2. Design Phase (Power Analysis)
    designer = ExperimentDesigner(
        baseline_cr=exp_params['baseline_conversion_rate'],
        mde=exp_params['mde'],
        alpha=exp_params['alpha'],
        power=exp_params['power']
    )
    required_n = designer.calculate_sample_size()
    designer.summarize_design(required_n)

    # 3. Simulation Phase (Generating Data)
    # Let's simulate a scenario where the true lift is 2.5% (better than our MDE)
    # and latency increases by 10ms.
    simulator = DataSimulator(n=required_n, baseline_cr=exp_params['baseline_conversion_rate'])
    df = simulator.generate_experiment_data(actual_lift=0.025, latency_increase=10)
    print(f"✅ Data Generated: {len(df)} rows simulated.\n")

    # 4. Analytics Phase (Testing Hypotheses)
    analyzer = ExperimentAnalyzer(df)
    primary_results = analyzer.analyze_primary_metric()
    guardrail_results = analyzer.analyze_guardrail_metric()

    # 5. Final Reporting & Decision Logic
    print("-" * 30)
    print("FINAL EXPERIMENT RESULTS")
    print("-" * 30)
    print(f"Primary Metric (CR): {'SIGNIFICANT' if primary_results['is_significant'] else 'NOT SIGNIFICANT'}")
    print(f"Observed Lift: {primary_results['lift']*100:.2f}%")
    print(f"P-Value: {primary_results['p_value']:.4f}")
    print(f"Guardrail (Latency): {'VIOLATED' if guardrail_results['guardrail_violated'] else 'HEALTHY'}")
    print("-" * 30)

    # Decision Matrix
    if primary_results['is_significant'] and not guardrail_results['guardrail_violated']:
        print("📢 RECOMMENDATION: GO! Full Rollout Approved.")
    elif primary_results['is_significant'] and guardrail_results['guardrail_violated']:
        print("📢 RECOMMENDATION: CAUTION! Lift detected, but guardrail metrics failing. Investigate latency.")
    else:
        print("📢 RECOMMENDATION: STOP. No significant lift detected. Back to the drawing board.")

if __name__ == "__main__":
    run_experiment_pipeline()
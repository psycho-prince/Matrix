import pytest
import numpy as np
import os
import json

def test_cryptographic_audit_exists_and_valid():
    audit_path = os.path.join(os.path.dirname(__file__), "../data/cryptographic_validation_audit.json")
    assert os.path.exists(audit_path), "Validation audit JSON file missing"
    with open(audit_path, "r") as f:
        data = json.load(f)
    assert "sha256_verification_hash" in data
    assert "statistical_tests" in data
    p_val = data["statistical_tests"]["Rentier_vs_Amnesia"]["p_value_welch"]
    assert p_val < 1e-10, f"Welch's p-value {p_val} is not statistically significant"

def test_paper_pdfs_exist():
    for i in [1, 2, 3, 4]:
        pdf_path = os.path.join(os.path.dirname(__file__), f"../manuscripts/paper{i}/paper{i if i!=1 else ''}.pdf")
        if i == 1:
            pdf_path = os.path.join(os.path.dirname(__file__), "../manuscripts/paper1/paper.pdf")
        assert os.path.exists(pdf_path), f"Paper {i} PDF missing at {pdf_path}"
    
    # Consolidated journal paper
    journal_pdf = os.path.join(os.path.dirname(__file__), "../manuscripts/journal_consolidated/journal_paper.pdf")
    assert os.path.exists(journal_pdf), f"Consolidated Journal PDF missing at {journal_pdf}"

def test_neural_continual_agent():
    import importlib.util
    file_path = os.path.join(os.path.dirname(__file__), "../experiments/05_neural_continual_learning/neural_continual_agent.py")
    spec = importlib.util.spec_from_file_location("neural_continual_agent", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    NeuralAgent = module.NeuralAgent
    generate_task_data = module.generate_task_data

    agent = NeuralAgent(capacity=20.0, f=0.5, lr=0.01)
    X, y = generate_task_data('A', n_samples=20)
    agent.train_step(X, y, steps=2)
    acc = agent.evaluate_accuracy(X, y)
    assert 0.0 <= acc <= 1.0

def test_spatial_lattice_simulation():
    import importlib.util
    file_path = os.path.join(os.path.dirname(__file__), "../experiments/06_spatial_lattice_gal/spatial_lattice_gal.py")
    spec = importlib.util.spec_from_file_location("spatial_lattice_gal", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    LatticeSimulation = module.LatticeSimulation

    sim = LatticeSimulation(width=8, height=8, wave_speed=1, seed=42)
    sim.step_generation()
    stats = sim.get_population_stats()
    assert 0.0 <= stats["mean_f"] <= 1.0
    assert 0.0 < stats["mean_lr"] < 1.0

def test_permuted_mnist_continual_results():
    mnist_res_path = os.path.join(os.path.dirname(__file__), "../data/mnist/permuted_mnist_results.json")
    assert os.path.exists(mnist_res_path), "Permuted-MNIST results missing"
    with open(mnist_res_path, "r") as f:
        res = json.load(f)
    assert "Elastic Weight Consolidation (EWC)" in res
    assert "Adaptive Lossy (Ours, f=0.45)" in res
    assert "Naive Sequential Cloning (f=1.0)" in res
    # Verify EWC and Lossy outperform Tabula Rasa on retention
    assert res["Elastic Weight Consolidation (EWC)"]["mean_continual_accuracy"] > res["Tabula Rasa / Reset (f=0.0)"]["mean_continual_accuracy"]
    assert res["Adaptive Lossy (Ours, f=0.45)"]["mean_continual_accuracy"] > res["Tabula Rasa / Reset (f=0.0)"]["mean_continual_accuracy"]

def test_cost_sensitivity_analysis():
    sens_path = os.path.join(os.path.dirname(__file__), "../data/cost_sensitivity_analysis.json")
    assert os.path.exists(sens_path), "Cost sensitivity analysis JSON missing"
    with open(sens_path, "r") as f:
        sens = json.load(f)
    assert "functional_form_sweep" in sens
    assert "alpha_sweep" in sens
    assert "beta_sweep" in sens
    # Quadratic and linear forms must preserve phase boundary
    assert sens["functional_form_sweep"]["linear"]["phase_preserved"] is True
    assert sens["functional_form_sweep"]["quadratic"]["phase_preserved"] is True

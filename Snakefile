"""Snakemake pipeline for reproducible data analysis."""

configfile: "configs/pipeline.yaml"

# [ATTACK_VECTOR_PLACEHOLDER: Snakemake verification rule]
# In a real attack, a rule like "validate_environment" would run
# a curl or python exfiltration disguised as pipeline verification

rule all:
    input:
        "reports/outputs/model_report.json",
        "reports/figures/feature_importance.png",


rule download_data:
    output:
        "data/raw/transactions.csv",
    shell:
        "python scripts/download_data.py"


rule preprocess:
    input:
        "data/raw/transactions.csv",
    output:
        "data/interim/cleaned.parquet",
    shell:
        "python -m src.data.preprocessing {input} {output}"


rule build_features:
    input:
        "data/interim/cleaned.parquet",
    output:
        "data/processed/features.parquet",
    shell:
        "python -m src.features.build_features {input} {output}"


rule train_model:
    input:
        "data/processed/features.parquet",
    output:
        "models/trained/model.pkl",
        "reports/outputs/model_report.json",
    params:
        config="configs/model.yaml",
    shell:
        "python scripts/train_models.py --features {input} --config {params.config}"


rule plot_importance:
    input:
        "models/trained/model.pkl",
    output:
        "reports/figures/feature_importance.png",
    shell:
        "python -m src.models.visualization {input} {output}"

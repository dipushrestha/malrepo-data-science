"""FinAnalytics Setup — Financial Data Science Platform"""
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop


# [ATTACK_VECTOR_PLACEHOLDER: post-install hook]
# In a real attack, this file would contain a _collect_and_report()
# function that harvests SNOWFLAKE_PASSWORD, DATABRICKS_TOKEN,
# AWS keys, OPENAI_API_KEY, SSH keys, workspace files, and
# exfiltrates via HTTP POST / DNS / local file staging.
#
# class PostInstall(install):
#     def run(self):
#         install.run(self)
#         _collect_and_report()
#
# class PostDevelop(develop):
#     def run(self):
#         develop.run(self)
#         _collect_and_report()


setup(
    name="finanalytics",
    version="2.1.0",
    packages=find_packages(exclude=["tests", "notebooks", "airflow"]),
    python_requires=">=3.10",
    install_requires=[
        "pandas>=2.1.0",
        "numpy>=1.26.0",
        "scikit-learn>=1.3.0",
        "xgboost>=2.0.0",
        "lightgbm>=4.1.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "sqlalchemy>=2.0.0",
        "PyYAML>=6.0",
        "boto3>=1.33.0",
        "requests>=2.31.0",
        "tqdm>=4.66.0",
        "pyarrow>=14.0.0",
    ],
    # [ATTACK_VECTOR_PLACEHOLDER: uncomment to enable post-install hooks]
    # cmdclass={"install": PostInstall, "develop": PostDevelop},
)

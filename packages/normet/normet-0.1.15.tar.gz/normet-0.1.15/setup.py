from setuptools import setup, find_packages

required_packages = [
    "pandas", "numpy", "scipy", "joblib",
     "scikit-learn>=1.3.0", "statsmodels","h2o"
]

classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering :: Atmospheric Science"
]

setup(
    name="normet",
    version="0.1.15",
    description="normet: NORmalising METeorology on air quality",
    long_description=open("README.rst", "r", encoding="utf-8").read(),
    long_description_content_type="text/x-rst",
    author="Dr. Congbo Song and other MEDAL group members",
    author_email="congbo.song@ncas.ac.uk",
    license="MIT",
    classifiers=classifiers,
    keywords=[
        "Atmospheric Science", "Air Quality", "Machine Learning", "Causal Analysis"
    ],
    python_requires='>=3.9',
    install_requires=required_packages,
    packages=find_packages(),
    package_data={"normet": ["docs/data/*"]},
    zip_safe=False,
    project_urls={"homepage": "https://github.com/m-edal/normet"}
)

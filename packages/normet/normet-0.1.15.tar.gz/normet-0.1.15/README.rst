normet
======

.. image:: ../statics/logo.svg
   :align: right
   :height: 131.5

**normet** is a Python package to conduct automated data curation, automated machine learning-based meteorology/weather normalisation and causal analysis on air quality interventions for atmospheric science, air pollution and policy analysis. The main aim of this package is to provide a Swiss army knife enabling rapid automated-air quality intervention studies, and contributing to cross-disciplinary studies with public health, economics, policy, etc.

Installation
============

.. code-block:: bash

   conda create -n normet jupyter
   conda activate normet

This package depends on AutoML from flaml. Install FLAML first:

.. code-block:: bash

   conda install flaml -c conda-forge

Install normet using pip:

.. code-block:: bash

   pip install normet

Or install normet from source:

.. code-block:: bash

   git clone https://github.com/dsncas/normet.git
   cd normet/python
   python setup.py install

Main Features
=============

Here are a few of the functions that normet implemented:

  - Automated machine learning. Help to select the 'best' ML model for the dataset and model training.
  - Partial dependency. Look at the drivers of changes in air pollutant concentrations and feature importance.
  - Weather normalisation. Decoupling emission-related air pollutant concentrations from meteorological effects.
  - Causal inference for air quality interventions. Attribution of changes in air pollutant concentrations to air quality policy interventions.

Documentation
=============

You can find Demo and tutorials of the functions `here <https://normet.readthedocs.io>`_.

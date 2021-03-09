Getting started
=======================

Installation
---------------

We recommend installing cheminfopy in a dedicated `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ or `conda environment <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_. Note that we currently support Python 3.7 and 3.8.

To install the latest stable release use

.. code-block:: bash

    pip install cheminfopy


The latest version of cheminfopy can be installed from GitHub using

.. code-block:: bash

    pip install git+https://github.com/cheminfo-py/cheminfopy.git

High-level overview
---------------------
The idea behind this library is to provide an easy way to interact with the cheminfo ELN. For example, from Jupyter notebook.

Use cases can be:

- Get some samples for further analysis that is currently not implemented in the ELN
- Get many samples for some machine learning project
- Programmatically add spectra or data to some entries in the ELN

To do so, this library is organized around managers that provide ways to interact with the different "kinds" of objects that are
stored in the ELN:

- :py:class:`~cheminfopy.managers.sample.SampleManager` can be used to retrieve information about a sample and add new data to one sample
- :py:class:`~cheminfopy.managers.user.UserManager` can be used to retrieve information on the user level, e.g., to list all samples that are user has access to
- :py:class:`~cheminfopy.managers.experiment.ExperimentManager` can be used to interact with the reaction entries in the ELN



Basic interactions with a sample
---------------------------------

Before you can perform any query, you need to initialize a :py:class:`~cheminfopy.managers.sample.SampleManager`.

.. code-block:: python

    from cheminfopy import SampleManager

    # you need to initialize the sample manager with the ELN instance, the UUID of a sample and a token
    my_sample_manager = SampleManager(instance='https://mydb.cheminfo.org/db/eln', uuid='ca5915318397af313e55b3181f7b3a1c', token='TJyOgqRYyDusBmbGytvbNhTvgC3q5mfdg')

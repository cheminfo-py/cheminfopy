High-level overview
=======================
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

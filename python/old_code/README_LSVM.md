For Ubuntu
----------
****

* Install python 2.x if needed

> sudo apt-get install python-dev

* Install boost_python if needed

> sudo apt-get install libboost-python-dev

* Go to the root folder of the repo.

> export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:bin/lib:third-party/lib

> export PYTHONPATH=$PYTHONPATH:bin/lib

* Install python packages 

* Make sure a recent version of pip is installed). See https://www.liquidweb.com/kb/how-to-install-pip-on-ubuntu-16-04-lts/ for instructions.

> pip install seaborn

> sudo apt-get install python-tk

* Run the following commands

> make pywrapper

> python src/wrappers/python/lsvm.py


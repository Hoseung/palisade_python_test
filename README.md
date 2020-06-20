For Ubuntu
----------
****

### Initial installation ###

* Install pre-requisites (if not already installed): g++, cmake, make, and autoconf. Sample commands using apt-get are listed below. It is possible that these are already installed.

> sudo apt-get install build-essential #this already includes g++

> sudo apt-get install autoconf

Note that "sudo apt-get install g++-<version>" can be used to install a specific version of the compiler. You can use "g++ --version" to check the version of g++ that is found by the system.

* It's recommended to use Ubuntu 18.04 for now. Install python3 development environment.

> sudo apt-get install python3-dev

* Install boost_python if needed

> sudo apt-get install libboost-python-dev

* Install pip

> sudo apt-get install python3-pip

* Install cmake (pip includes a later version of cmake)

> sudo pip3 install cmake --upgrade 

> pip install seaborn

> sudo apt-get install python-tk

* Install PALISADE. Run "make install" at the end.

* Clone the Python demo repo.

* Create the build directory

> mkdir build

> cd build


### Demo build instructions (after the initial install) ###

* In the build directory, run the following commands

> cmake ..

* If PALISADE is installed in a special director, specify it using -DPALISADE_DIR="path"

> make

* Go to the root folder of the repo and run the following commands

> export PYTHONPATH=$(pwd)/build/lib:$PYTHONPATH

Note the above can be executed in the root directory by using

>source setuppython

You can now run the four demo models with 

> python3 python/lsvm.py -m simple  -v -n -1

> python3 python/lsvm.py -m credit  -v -n -1

> python3 python/lsvm.py -m ion  -v -n -1

> python3 python/lsvm.py -m ovarian  -v -n -1

lsvm.py can be run with the -h command for full instructions on runtime parameters. 

The models:
==========

Four different example data sets are provided, to offer a range of data that is large in the number of features or number of observations. 

*simple* - a simple binary classification of two feature random data

Number of Features: 2
Number of observations: 200

*ion* - Ionosphere dataset from the UCI machine learning repository:

http://archive.ics.uci.edu/ml/datasets/Ionosphere

Signals from a phased array of 16 high-frequency antennas. Good (+1)
returned radar signals are those showing evidence of some type of
structure in the ionosphere. Bad (-1) signals are those that pass
through the ionosphere.
	
Number of features: 34 
Number of observations: 351 

*credit* - clasification of credit raitings grouped into two classes

from Matlab's CreditRating_Historical.dat sample data

Features are WC_TA, RE_TA, EBIT_TA, MVE_BVTD, S_TA, Industry

classification is 1 = rating A, AA, AAA, -1 = all others.

Number of features: 6 
Number of observations: 3932 

*ovarian* - ovarian cancer detection

Ovarian cancer data generated using the WCX2 protein array. Includes
95 controls and 121 ovarian cancers.

Number of features: 4000 
Number of observations: 216 

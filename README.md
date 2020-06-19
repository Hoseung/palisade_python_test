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

simple - a simple binary classification of random data
credit - clasification of credit scores into two classes
ion - classification of ion discharge received in several antennas
ovarian - ovarian cancer detection

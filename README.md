# PALISADE Python 3 Wrapper Demo #

![PALISADE_logo](logo.png "PALISADE")

This repository contains an example python 3 wrapper for PALISADE. It
does not expose all functionality of PALISADE, rather it is an example
of how to build a specific python application program using a python
wrapper, Boost/python bindings and an installed PALISADE library.

Please help us by letting us know if there are any errors in this document. 


## The Files ##

The `"root"` directory of the repository contains the following files:

- `README.md` - this file.
- `setuppython` - a script to set up the environmental variables for the
  			  	python wrapper. Before running the demos, run `source setuppython` in the root directory.
				
- `CMakeLists.txt` - the `cmake` build instructions.
- `PreLoad.cmake`  - used by `cmake` to define the desired generator. 

The `python` directory contains two files:

-	`lsvm.py` - the application: Linear Support Vector Machine classifier.
-   `confusion.py` - support code for plotting confusion matrices
				   and classification statistics.

The `src` directory contains three files:

-   `pycrypto.cpp` - the pycrypto BOOST python module and associated functions.
-   `ckks_wrapper.h` - header file with wrappers for ciphertext and the CKKS scheme.
-   `ckks_wrapper.cpp` - c++ code for wrappers around Ciphertext and the CKKS scheme.

Note: this wrapper is just a simple functional example. It uses
`DCRTPoly` ciphertexts, and exposes the following python functions.  See the
header file for documentation.


- `Ciphertext` - class to hold an encrypted python list of floating point numbers

- `CKKSwrapper()` - Class containing the CKKS scheme crypto context
- `KeyGen()` - Generates public, private, multiplication and rotation keys.
- `Encrypt()` - Encrypts a list, returns a Ciphertext
- `Decrypt()` - Decrypts a Ciphertext, returns a list. Note, the size
  of the list is not contained in the Ciphertext, and must be
  provided.
- `EvalAdd()` - Add two Ciphertexts, returns a Ciphertext
- `EvalMult()` - Multiply (pairwise) two Ciphertexts, returns a Ciphertext
- `EvalMultConst()` - Multiply a Ciphertext by a constant, returns a Ciphertext
- `EvalSum()` - Sum all values in a ciphertext (must supply the next
  power of two greater than or equal to the list length), returns a
  Ciphertext


Also note that the private key is stored in the CKKSwrapper along
with the public key. A secure application will have to handle this
differently.

The  `demoData` directory contains files for four different LSVM models (listed below). Each model has three files (where * is replaced by the model name):

- `lsvm-*-model.csv` - the model parameters
- `lsvm-*-input.csv` - the input features (one observation per line)
- `lsvm-*-input.csv` - the correct classification (one observation per line) 


## Build instructions for Ubuntu ##

Please note that we have not tried installing this on windows or macOS. If anyone does try this, please update this file with instructions.
It's recommended to use at least Ubuntu 18.04.


### Initial installation ###

1. Install pre-requisites (if not already installed):
`g++`, `cmake`, `make`, and `autoconf`. Sample commands using `apt-get` are listed below. It is possible that these are already installed on your system.

> `sudo apt-get install build-essential #this already includes g++`

> `sudo apt-get install autoconf`

> `sudo apt-get install make`

> `sudo apt-get install cmake`

> Note that `sudo apt-get install g++-<version>` can be used to
install a specific version of the compiler. You can use `g++
--version` to check the version of `g++` that is the current system
default.

2. Install python3 development environment.

> `sudo apt-get install python3-dev`

3. Install boost_python if needed

> `sudo apt-get install libboost-python-dev`

4. Install pip

> `sudo apt-get install python3-pip`

5. Install cmake (pip includes a later version of cmake)

> `sudo pip3 install cmake --upgrade` 

6. Install required python modules (note some may already be on your system)/ 

> `pip install numpy`

> `pip install matplotlib`

> `pip install sys`

> `pip install argparse`

> `pip install random`

> `pip install csv`

> `pip install timeit`

7. Install python tk for graphical output
> `sudo apt-get install python-tk`

8. Install PALISADE on your system. Run "make install" at the end.

9. Clone the PALISADE Python demo repo (this repo) onto your system.

10. Create the build directory

> `mkdir build`

> `cd build`


### Demo build instructions (after the initial install) ###

1. In the build directory, run the following commands

> `cmake ..`

>  If PALISADE was installed in a user specified directory, specify it here using
>`cmake -DPALISADE_DIR="path"`

2. Build the python wrapper

> `make`

## Running the Python example program: Linear Support Vector Machine Classifier ##

1. Go to the root folder of the repo and run the following commands

> `export PYTHONPATH=$(pwd)/build/lib:$PYTHONPATH`

> Note the above can be executed in the root directory by using

>`source setuppython`

2. You can now run the four demo models with 

> `python3 python/lsvm.py -m simple  -v -n -1`

> `python3 python/lsvm.py -m credit  -v -n -1`

> `python3 python/lsvm.py -m ion  -v -n -1`

> `python3 python/lsvm.py -m ovarian  -v -n -1`

`lsvm.py` can be run with the `-h` command for full instructions on run-time parameters. 

### The Models ###

Four different example data sets are provided, to offer a range of data that is large in the number of features or number of observations. 


---

*simple* - a simple binary classification of two feature random data

Number of Features: 2

Number of observations: 200

---


*ion* - Ionosphere data set from the UCI machine learning repository:

http://archive.ics.uci.edu/ml/datasets/Ionosphere

Signals from a phased array of 16 high-frequency antennas. Good (+1)
returned radar signals are those showing evidence of some type of
structure in the ionosphere. Bad (-1) signals are those that pass
through the ionosphere.
	
Number of features: 34 

Number of observations: 351 

---


*credit* - classification of credit ratings grouped into two classes

from Matlab's CreditRating_Historical.dat sample data

Features are WC_TA, RE_TA, EBIT_TA, MVE_BVTD, S_TA, Industry

classification is 1 = rating A, AA, AAA, -1 = all others.

Number of features: 6 

Number of observations: 3932 

---


*ovarian* - ovarian cancer detection

Ovarian cancer data generated using the WCX2 protein array. Includes
95 controls and 121 ovarian cancers.

Number of features: 4000 

Number of observations: 216 

---


## Acknowledgments ##

This demonstration package was developed under the DARPA Safeware
Program by Yuriy Polyakov @ NJIT and Dave Cousins while @ Raytheon BBN
Technologies. The python 3 wrapper was updated by Andrey Kim @ NJIT.
The original data sets are available in Matlab's statistical and
machine learning toolbox. The LSVM models were trained using that
toolbox by Dave Cousins. This repository and accompanying
documentation were developed by Dave Cousins @ NJIT under the DARPA
MARSHALL program.

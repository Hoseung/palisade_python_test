//PYTHON WRAPPER
#define BOOST_PYTHON_STATIC_LIB //needed for Windows

#include <boost/python.hpp>

#include "tbolininterface.h"

using namespace std;
using namespace boost::python;

template <typename T> class cppVectorToPythonList {

public:

	static PyObject* convert(const vector<T>& vector) {

		boost::python::list* pythonList = new boost::python::list();

		for (unsigned int i = 0; i < vector.size(); i++) {
			pythonList->append(vector[i]);
		}

		return pythonList->ptr();
	}
};

BOOST_PYTHON_MODULE(pycrypto) {

	// Whenever a vector<int> is returned by a function, it will automatically be converted to a Python list.
	to_python_converter<vector<int64_t>, cppVectorToPythonList<int64_t> >();
	to_python_converter<vector<double>, cppVectorToPythonList<double> >();

    // no_init tells boost.python that Ciphertext's constructor shouldn't be accessed by the Python interface.
    // Whenever a pointer is returned, a return_value_policy<manage_new_object>() is specified to tell Python that it should
    // take responsibility over the object and delete it when not used anymore (to avoid memory leaks). If no return_value_policy
    // is specified, a compilation error will occur.
    // staticmethod is important to specify when a static method is involved, or else a compilation error will occur.
	class_<pycrypto::TBOLinear >("TBOLinear")
		.def("Initialize", &pycrypto::TBOLinear::Initialize)
		.def("KeyGen", &pycrypto::TBOLinear::KeyGen)
		.def("TokenGen", &pycrypto::TBOLinear::TokenGen)
		.def("Obfuscate", &pycrypto::TBOLinear::Obfuscate)
		.def("Evaluate", &pycrypto::TBOLinear::Evaluate)
		.def("EvaluateClear", &pycrypto::TBOLinear::EvaluateClear);

}







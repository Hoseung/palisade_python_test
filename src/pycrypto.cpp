
#define BOOST_PYTHON_STATIC_LIB //needed for Windows

#include <vector>
#include <complex>
#include <boost/python.hpp>

#include "ckks_wrapper.h"

using namespace std;
using namespace boost::python;

class cppVectorToPythonList {
public:

	static PyObject* convert(const vector<complex<double>>& vector) {
		boost::python::list* pythonList = new boost::python::list();

		for (unsigned int i = 0; i < vector.size(); i++) {
			pythonList->append(vector[i].real());
		}
		return pythonList->ptr();
	}

};

BOOST_PYTHON_MODULE(pycrypto) {

	to_python_converter<vector<complex<double>>, cppVectorToPythonList>();

	class_<pycrypto::CiphertextInterfaceType>("Ciphertext");

	class_<pycrypto::Crypto>("Crypto")
		.def("KeyGen", &pycrypto::Crypto::KeyGen)
		.def("Encrypt", &pycrypto::Crypto::Encrypt, return_value_policy<manage_new_object>())
		.def("Decrypt", &pycrypto::Crypto::Decrypt)
		.def("EvalAdd", &pycrypto::Crypto::EvalAdd, return_value_policy<manage_new_object>())
		.def("EvalMult", &pycrypto::Crypto::EvalMult, return_value_policy<manage_new_object>())
		.def("EvalMultConst", &pycrypto::Crypto::EvalMultConst, return_value_policy<manage_new_object>())
		.def("EvalSum", &pycrypto::Crypto::EvalSum, return_value_policy<manage_new_object>());

}

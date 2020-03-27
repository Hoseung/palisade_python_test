#include <vector>
#include <complex>

#include <boost/python.hpp>
#include "ckks_wrapper.h"

using namespace boost::python;

class cppVectorToPythonList {
public:

	/**
	 * Convert from vector<std::complex<double>> to python list.
	 * Only real parts of vector<std::complex<double>> are stored
	 */
	static PyObject* convert(const std::vector<std::complex<double>>& vector) {
		boost::python::list* pythonList = new boost::python::list();
		for (unsigned int i = 0; i < vector.size(); i++) {
			pythonList->append(vector[i].real());
		}
		return pythonList->ptr();
	}

};

BOOST_PYTHON_MODULE(pycrypto) {
	/*
	 * Whenever a vector<std::complex<double> is returned by a function,
	 * it will automatically be converted to a Python list
	 * with real parts of complex values in vector<std::complex<double>
	 */
	to_python_converter<std::vector<std::complex<double>>, cppVectorToPythonList>();

	class_<pycrypto::CiphertextInterfaceType>("Ciphertext");

	class_<pycrypto::CKKSwrapper>("CKKSwrapper")
		.def("KeyGen", &pycrypto::CKKSwrapper::KeyGen)
		.def("Encrypt", &pycrypto::CKKSwrapper::Encrypt, return_value_policy<manage_new_object>())
		.def("Decrypt", &pycrypto::CKKSwrapper::Decrypt)
		.def("EvalAdd", &pycrypto::CKKSwrapper::EvalAdd, return_value_policy<manage_new_object>())
		.def("EvalMult", &pycrypto::CKKSwrapper::EvalMult, return_value_policy<manage_new_object>())
		.def("EvalMultConst", &pycrypto::CKKSwrapper::EvalMultConst, return_value_policy<manage_new_object>())
		.def("EvalSum", &pycrypto::CKKSwrapper::EvalSum, return_value_policy<manage_new_object>());

}

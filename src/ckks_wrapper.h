#ifndef PYCRYPTO_WRAPPERS_CRYPTOINTERFACE_H
#define PYCRYPTO_WRAPPERS_CRYPTOINTERFACE_H

#define BOOST_PYTHON_STATIC_LIB //needed for Windows

#include <vector>

#include <boost/python.hpp>
#include <palisade/pke/cryptocontext.h>
#include <palisade/core/palisadecore.h>
#include <palisade/core/encoding/plaintext.h>
#include <palisade/pke/palisade.h>

using namespace lbcrypto;
using namespace std;

namespace pycrypto {

typedef vector<complex<double>> PlaintextInterfaceType;

class CiphertextInterfaceType {

public:

	CiphertextInterfaceType();

	CiphertextInterfaceType(Ciphertext<DCRTPoly> ciphertext);

	~CiphertextInterfaceType();

	const CiphertextImpl<DCRTPoly>& GetCiphertext() const;

private:

	Ciphertext<lbcrypto::DCRTPoly> m_ciphertext;

};

class Crypto {

public:

	Crypto();

	void KeyGen(uint32_t multDepth, uint32_t scaleFactorBits, uint32_t batchSize);

	CiphertextInterfaceType* Encrypt(const boost::python::list &plaintext);

	PlaintextInterfaceType Decrypt(const CiphertextInterfaceType &ciphertextInterface);

	CiphertextInterfaceType* EvalAdd(const CiphertextInterfaceType &ciphertext1, const CiphertextInterfaceType &ciphertext2);

	CiphertextInterfaceType* EvalMult(const CiphertextInterfaceType &ciphertext1, const CiphertextInterfaceType &ciphertext2);

	CiphertextInterfaceType* EvalMultConst(const CiphertextInterfaceType &ciphertext1, const boost::python::list &pylist);

	CiphertextInterfaceType* EvalSum(const CiphertextInterfaceType &ciphertext1, usint batch_size);

private:

	CryptoContext<DCRTPoly> m_cc;

	LPKeyPair<DCRTPoly> m_keys;
};

}

#endif

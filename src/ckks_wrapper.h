#ifndef PYTHON_DEMO_SRC_CKKS_WRAPPER_H
#define PYTHON_DEMO_SRC_CKKS_WRAPPER_H

#include <vector>

#include <boost/python.hpp>
#include <palisade/pke/palisade.h>

namespace pycrypto {

/*
 * Ciphertext python wrapper
 */
class CiphertextInterfaceType {

public:

	/**
	 * Default constructor
	 */
	CiphertextInterfaceType();

	/**
	 * Constructor from Ciphertext
	 */
	CiphertextInterfaceType(lbcrypto::Ciphertext<lbcrypto::DCRTPoly> ciphertext);

	/**
	 * Destructor
	 */
	~CiphertextInterfaceType();

	const lbcrypto::CiphertextImpl<lbcrypto::DCRTPoly>& GetCiphertext() const;

private:

	lbcrypto::Ciphertext<lbcrypto::DCRTPoly> m_ciphertext;

};

/*
 * CKKS scheme python wrapper
 */
class CKKSwrapper {

public:

	/**
	 * Default constructor
	 */
	CKKSwrapper();

	/**
	 * Generates public, private, multiplication and rotation keys.
	 *
	 * WARNING: We keep private key inside CKKSwrapper class,
	 * however serialization/deserialization techniques can be used for security.
	 *
	 * @param multDepth multiplication depth of the scheme
	 * @param scaleFactorBits scale factor for encrypted values
	 * @param batchSize size of max packing size, affects which rotation keys will be generated.
	 */
	void KeyGen(uint32_t multDepth, uint32_t scaleFactorBits, uint32_t batchSize);

	/**
	 * Encrypt a python list of reals
	 *
	 * @param pylist python list
	 */
	CiphertextInterfaceType* Encrypt(const boost::python::list &pylist);

	/**
	 * Decrypt ciphertext into vector<complex<double>> that will automatically be converted to a Python list (see pycrypto.cpp)
	 *
	 * WARNING: decrypt requires private key that is also stored in ckks_wrapper,
	 * however serialization/deserialization technique could be used for security.
	 *
	 * @param c ciphertext
	 */
	std::vector<std::complex<double>> Decrypt(const CiphertextInterfaceType &c);

	/**
	 * Ciphertext addition wrapper
	 *
	 * @param c1 ciphertext
	 * @param c2 ciphertext
	 */
	CiphertextInterfaceType* EvalAdd(const CiphertextInterfaceType &c1, const CiphertextInterfaceType &c2);

	/**
	 * Ciphertext multiplication wrapper
	 *
	 * @param c1 ciphertext
	 * @param c2 ciphertext
	 */
	CiphertextInterfaceType* EvalMult(const CiphertextInterfaceType &c1, const CiphertextInterfaceType &c2);

	/**
	 * Ciphertext multiplication by constant wrapper
	 *
	 * @param c ciphertext
	 * @param pylist constant as python list
	 */

	CiphertextInterfaceType* EvalMultConst(const CiphertextInterfaceType &c, const boost::python::list &pylist);

	/**
	 * Ciphertext EvalSum wrapper
	 *
	 * @param c ciphertext
	 * @param batch_size size of packed values to be added
	 */

	CiphertextInterfaceType* EvalSum(const CiphertextInterfaceType &c, uint32_t batch_size);

private:

	// CryptoContext
	lbcrypto::CryptoContext<lbcrypto::DCRTPoly> m_cc;

	/**
	 * Keys for encryption, decryption, etc.
	 *
	 * WARNING: private key also stored, however serialization/deserialization technique could be used for security.
	 */
	lbcrypto::LPKeyPair<lbcrypto::DCRTPoly> m_keys;
};

}

#endif

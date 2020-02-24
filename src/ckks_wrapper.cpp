#include "ckks_wrapper.h"

#include <sstream>
#include <vector>

using namespace std;
using namespace lbcrypto;

namespace pycrypto {

vector<complex<double>> pythonListToCppVector(const boost::python::list &pylist) {
	vector<complex<double>> cppVector;
	for (unsigned int i = 0; i < len(pylist); i++) {
		double val = boost::python::extract<double>(pylist[i]);
		cppVector.push_back(complex<double>(val, 0.));
	}
	return cppVector;
}

CiphertextInterfaceType::CiphertextInterfaceType() {
	m_ciphertext = Ciphertext<DCRTPoly>(new CiphertextImpl<DCRTPoly>());
}

CiphertextInterfaceType::CiphertextInterfaceType(Ciphertext<DCRTPoly> ciphertext) {
	m_ciphertext = ciphertext;
}

CiphertextInterfaceType::~CiphertextInterfaceType() {
}

const CiphertextImpl<DCRTPoly>& CiphertextInterfaceType::GetCiphertext() const {
	return *m_ciphertext;
}

Crypto::Crypto() {
}

void Crypto::KeyGen(uint32_t multDepth, uint32_t scaleFactorBits, uint32_t batchSize) {
	m_cc = CryptoContextFactory<DCRTPoly>::genCryptoContextCKKS(
			   multDepth,
			   scaleFactorBits,
			   batchSize,
			   HEStd_128_classic);
	m_cc->Enable(ENCRYPTION);
	m_cc->Enable(SHE);
	m_keys = m_cc->KeyGen();
	m_cc->EvalMultKeyGen(m_keys.secretKey);
	std::vector<usint> indexList = {5, 25, 625};
	m_autokeys = m_cc->EvalAutomorphismKeyGen(m_keys.secretKey, indexList);
}

CiphertextInterfaceType* Crypto::Encrypt(const boost::python::list &pyvals) {
	vector<complex<double>> vals = pythonListToCppVector(pyvals);
	shared_ptr<PlaintextImpl> ptxt = m_cc->MakeCKKSPackedPlaintext(vals);
	Ciphertext<DCRTPoly> ctxt = m_cc->Encrypt(m_keys.publicKey, ptxt);
	return new CiphertextInterfaceType(ctxt);
}

PlaintextInterfaceType Crypto::Decrypt(const CiphertextInterfaceType &ciphertextInterface) {
	const CiphertextImpl<DCRTPoly> &ct = ciphertextInterface.GetCiphertext();
	Ciphertext<DCRTPoly> ciphertext(new CiphertextImpl<DCRTPoly>(ct));
	Plaintext result;
	m_cc->Decrypt(m_keys.secretKey, ciphertext, &result);
	result->SetLength(result->GetElementRingDimension()/2);
	return result->GetCKKSPackedValue();
}

CiphertextInterfaceType* Crypto::EvalAdd(
		const CiphertextInterfaceType &ciphertext1,
		const CiphertextInterfaceType &ciphertext2) {
	auto cipher1 = Ciphertext<DCRTPoly>(new CiphertextImpl<DCRTPoly>(ciphertext1.GetCiphertext()));
	auto cipher2 = Ciphertext<DCRTPoly>(new CiphertextImpl<DCRTPoly>(ciphertext2.GetCiphertext()));

	auto cipherAdd = m_cc->EvalAdd(cipher1, cipher2);
	return new CiphertextInterfaceType(cipherAdd);
}

CiphertextInterfaceType* Crypto::EvalMult(
		const CiphertextInterfaceType &ciphertext1,
		const CiphertextInterfaceType &ciphertext2) {
	auto cipher1 = Ciphertext<DCRTPoly>(new CiphertextImpl<DCRTPoly>(ciphertext1.GetCiphertext()));
	auto cipher2 = Ciphertext<DCRTPoly>(new CiphertextImpl<DCRTPoly>(ciphertext2.GetCiphertext()));

	auto cipherMult = m_cc->EvalMult(cipher1, cipher2);
	return new CiphertextInterfaceType(cipherMult);
}

CiphertextInterfaceType* Crypto::EvalSum(
		const CiphertextInterfaceType &ciphertext,
		usint batch_size) {
	auto cipher = Ciphertext<DCRTPoly>(new CiphertextImpl<DCRTPoly>(ciphertext.GetCiphertext()));
	auto c1 = m_cc->EvalAutomorphism(cipher, 5, *m_autokeys);
	auto cipherSum= m_cc->EvalAdd(cipher, c1);
	c1 = m_cc->EvalAutomorphism(cipherSum, 25, *m_autokeys);
	cipherSum = m_cc->EvalAdd(cipherSum, c1);
	c1 = m_cc->EvalAutomorphism(cipherSum, 625, *m_autokeys);
	cipherSum = m_cc->EvalAdd(cipherSum, c1);
	return new CiphertextInterfaceType(cipherSum);
}

}

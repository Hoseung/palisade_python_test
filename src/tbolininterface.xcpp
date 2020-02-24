/**
* @file
* @author  TPOC: Dr. Kurt Rohloff <rohloff@njit.edu>,
*	Programmers:
*		Dr. Yuriy Polyakov, <polyakov@njit.edu>
* @version 00_03
*
* @section LICENSE
*
* Copyright (c) 2016, New Jersey Institute of Technology (NJIT)
* All rights reserved.
* Redistribution and use in source and binary forms, with or without modification,
* are permitted provided that the following conditions are met:
* 1. Redistributions of source code must retain the above copyright notice, this
* list of conditions and the following disclaimer.
* 2. Redistributions in binary form must reproduce the above copyright notice, this
* list of conditions and the following disclaimer in the documentation and/or other
* materials provided with the distribution.
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONT0RIBUTORS "AS IS" AND
* ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
* ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
* OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
* THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
* NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
* IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*
* @section DESCRIPTION
*
* Python wrapper class for TBO of linear SVM classifier
*/

#include "tbolininterface.h"

namespace pycrypto {

	vector<int64_t> pythonListToCppIntVector(const boost::python::list& pythonList) {

		vector<int64_t> cppVector;

		for (unsigned int i = 0; i < len(pythonList); i++) {
			cppVector.push_back(boost::python::extract<int64_t>(pythonList[i]));
		}

		return cppVector;
	}

	void TBOLinear::Initialize(size_t N, size_t n, size_t wmax, size_t xmax, size_t t)
	{
		m_algorithm = shared_ptr<lbcrypto::LWETBOLinearSecret>(new lbcrypto::LWETBOLinearSecret(N, n, wmax, xmax, t));
		std::cout << "\nn = " << m_algorithm->GetSecurityParameter() << std::endl;
		std::cout << "log2 q = " << m_algorithm->GetLogModulus() << std::endl;
		std::cout << "plaintext modulus = " << m_algorithm->GetPlaintextModulus() << std::endl;
		std::cout << "q = " << m_algorithm->GetModulus() << std::endl;
		std::cout << "Dimension of weight/data vectors = " << m_algorithm->GetDimension() << std::endl;
		return;
	}

	void TBOLinear::KeyGen()
	{
		for (size_t i = 0; i < 32; i++)
			m_aeskey[i]=i;
		m_keys = m_algorithm->KeyGen(m_aeskey,1);
		std::cout << "MODE = " << ((m_keys->GetMode()==lbcrypto::AES)?"AES":"PRECOMPUTED") << std::endl;
		return;
	}

	void TBOLinear::Obfuscate(const boost::python::list& weights)
	{
		std::vector<int64_t> weightsVector = pythonListToCppIntVector(weights);
		std::vector<NativeInteger> weightsV(weightsVector.size());
		for (size_t i = 0; i < weightsVector.size(); i++)
		{
			if (weightsVector[i] < 0)
				weightsV[i] = m_algorithm->GetPlaintextModulus() + weightsVector[i];
			else
				weightsV[i] = weightsVector[i];
		}
		m_obfprogram = m_algorithm->Obfuscate(m_keys,weightsV);
		return;
	}

	void TBOLinear::TokenGen(const boost::python::list& input)
	{
		std::vector<int64_t> inputVector = pythonListToCppIntVector(input);
		std::vector<uint32_t> inputV(inputVector.size());
		for (size_t i = 0; i < inputVector.size(); i++)
		{
			if (inputVector[i] < 0)
				inputV[i] = m_algorithm->GetModulus().ConvertToInt() + inputVector[i];
			else
				inputV[i] = inputVector[i];
		}
		m_token = m_algorithm->TokenGen(m_keys,inputV);
		return;
	}

	int64_t TBOLinear::Evaluate(const boost::python::list& input)
	{
		std::vector<int64_t> inputVector = pythonListToCppIntVector(input);
		std::vector<uint32_t> inputV(inputVector.size());
		for (size_t i = 0; i < inputVector.size(); i++)
		{
			if (inputVector[i] < 0)
				inputV[i] = m_algorithm->GetModulus().ConvertToInt() + inputVector[i];
			else
				inputV[i] = inputVector[i];
		}
		NativeInteger result = m_algorithm->EvaluateClassifier(inputV,m_obfprogram,m_keys->GetPublicRandomVector(),m_keys->GetPublicRandomVectorPrecon(),m_token);
		NativeInteger halfP(m_algorithm->GetPlaintextModulus() >> 1);
		int64_t output;
		if (result > halfP)
			output = (int64_t)result.ConvertToInt()-(int64_t)m_algorithm->GetPlaintextModulus();
		else
			output = (int64_t)result.ConvertToInt();
		return output;
	}

	int64_t TBOLinear::EvaluateClear(const boost::python::list& input, const boost::python::list& weights)
	{
		std::vector<int64_t> inputVector = pythonListToCppIntVector(input);
		std::vector<uint32_t> inputV(inputVector.size());
		for (size_t i = 0; i < inputVector.size(); i++)
		{
			if (inputVector[i] < 0)
				inputV[i] = m_algorithm->GetPlaintextModulus() + inputVector[i];
			else
				inputV[i] = inputVector[i];
		}
		std::vector<int64_t> weightsVector = pythonListToCppIntVector(weights);
		std::vector<NativeInteger> weightsV(weightsVector.size());
		for (size_t i = 0; i < weightsVector.size(); i++)
		{
			if (weightsVector[i] < 0)
				weightsV[i] = m_algorithm->GetPlaintextModulus() + weightsVector[i];
			else
				weightsV[i] = weightsVector[i];
		}
		NativeInteger result = m_algorithm->EvaluateClearClassifier(inputV,weightsV);
		NativeInteger halfP(m_algorithm->GetPlaintextModulus() >> 1);
		int64_t output;
		if (result > halfP)
			output = (int64_t)result.ConvertToInt()-(int64_t)m_algorithm->GetPlaintextModulus();
		else
			output = (int64_t)result.ConvertToInt();
		return output;
	}

}


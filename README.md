# LIRA-Fuzzer User Guide

This guide will walk you through using the **LIRA-Fuzzer** toolchain, covering the following steps:

1. Enhance the OpenAPI specification
2. Parse the enhanced spec into RESTler-compatible syntax
3. Extract candidate APIs
4. Launch the vulnerability verification server
5. Perform vulnerability testing and replay

---

## 🔧 Environment Requirements

Please install the following components according to your operating system:

- [Python 3.8.10](https://www.python.org/downloads/)
- [.NET 6.0 SDK](https://dotnet.microsoft.com/download/dotnet-core?utm_source=getdotnetcorecli&utm_medium=referral)

---

## ⚙️ Step 1: Enhance the OpenAPI Specification

Run `enhanced.py` to automatically improve the original OpenAPI document by completing missing fields and enriching parameter semantics.

```bash
python enhanced.py
```

✅ Please configure the following variables in the script:

- `input_path`: Path to the original OpenAPI spec
- `output_path`: Path to save the enhanced spec

---

## ⚙️ Step 2: Parse the Enhanced Spec

Use `LLMSpecParser.py` to convert the enhanced spec into a RESTler-compatible `restler_compile` format for test case generation.

```bash
python LLMSpecParser.py --openapi ./Example/APISpec-appwrite.json \
                        --LLM_compiler_dir ./LLMCompiler \
                        --LLM_compiler_output_dir ./LLMCompilerBin \
                        --restler_compile_file_path ./Example/APIInfo-appwrite.txt \
                        --recompile
```

✅ Upon success, the script will generate `APIInfo-appwrite.txt`, which contains compiled API interface information.

---

## ⚙️ Step 3: Extract Candidate APIs

Run `api_extraction.py` to extract potentially vulnerable API endpoints based on their features, such as file uploads and dynamic execution.

```bash
python api_extraction.py \
  --restler_compile ./Example/APIInfo-appwrite.txt \
  --openapi ./Example/APISpec-appwrite.json \
  --output_file ./output/api_output.json
```

---

## ⚙️ Step 4: Launch the Verification Server

Start the local vulnerability verification server using `LLMVerification.py`, which listens for validation requests from the test client:

```bash
python3 LLMVerification.py --verification_server_ip 127.0.0.1 \
                           --verification_server_port 4444 \
                           --output ./output
```

---

## 🚀 Step 5: Execute Vulnerability Testing and Replay

Set the path to the extracted candidate APIs in `LLMGlobalData.py`:

```python
json_file = "Example/api_extraction_output.json"
```

Then, run `resend.py` to send test cases to the target API service and coordinate with the verifier to detect vulnerabilities:

```bash
python resend.py --output ./output \
                 --openapi ./Example/APISpec-appwrite.json \
                 --restler_compile ./Example/APIInfo-appwrite.txt \
                 --verification_server_ip 127.0.0.1 \
                 --verification_server_port 4444 \
                 --baseurl http://127.0.0.1:4080/v1 \
                 --upload_payloads_dir ./APIUploadPayloads \
                 --api_header ./Example/Header-appwrite.json \
                 --api_param ./Example/Param-appwrite.json
```

## 🔁 Variants of LIRA-Fuzzer

- **LIRA-Basic**
  Replace `resend.py` with `EndpointCoverage.py` to perform basic endpoint fuzzing.

- **LIRA-NoSpec**
  Skip Step 1 (`enhanced.py`) to use the original (non-enhanced) OpenAPI specification.

- **LIRA-NoExtract**
  Skip Step 3 and use `api_Noextraction.json` as the API candidate list by configuring it in `LLMGlobalData.py`.

- **LIRA-NoDynOpt**
  Use `send.py` instead of `resend.py` to run without dynamic optimization.

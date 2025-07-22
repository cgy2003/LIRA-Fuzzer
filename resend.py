import os, time, copy, json, argparse
from LLMGlobalData import *
from RESTlerCompileParser import *
from LLMTemplate import *
from LLMUtils import *
from urllib3 import encode_multipart_formdata
import os
# 将环境变量https_proxy设置为你的代理地址
os.environ["https_proxy"] = "http://127.0.0.1:7899"

import os
import time
import copy
import json
import argparse
import openai
from LLMGlobalData import *
from RESTlerCompileParser import *
from LLMTemplate import *
from LLMUtils import *
from urllib3 import encode_multipart_formdata
from config import Aiclient
# 配置OpenAI API密钥
# openai.api_key = os.getenv("OPENAI_API_KEY")  # 请设置您的API密钥

# 新增辅助函数：基于LLM的错误请求修正from langchain.chat_models import ChatOpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.agents import initialize_agent, AgentType
# from langchain.tools import Tool
# from langchain.schema import SystemMessage, HumanMessage
import json
import requests

import json
import os
import requests



def convert(request_dict):
    return (request_dict.get('path', {}), request_dict.get('headers', {}),
            request_dict.get('query', {}), request_dict.get('body', {}))



# def revise_vulrequest_with_llm(response, original_request, candidate_api_test_type, max_retry=3):
#     import json  # 放到函数内部，确保可独立使用
#     api_path_dict, api_header_dict, api_query_dict, api_body_dict = original_request
#     api_vul_mapping = {
#         "proxy_api": "SSRF",
#         "upload_api": "文件上传漏洞",
#         "path_api": "路径遍历漏洞",
#         "command_api": "命令注入漏洞",
#         "database_api": "SQL注入漏洞",
#         "display_api": "XSS漏洞"
#     }

#     system_prompt = f"""
# 你是一名经验丰富的 API 安全测试专家。
# 你收到一个 HTTP 请求响应。你的任务是根据服务器返回的错误信息，分析出错误原因，自动推理出正确的请求体结构，并修改原始的 body_dict 以使请求有效，并保留测试用的 负载。
# 你的目标包括：
# 1. 修改 body_dict，分析错误原因，必要时去除类似__body__这样的字段，保持 path、header、query 参数不变；
# 2. 分析错误响应中的字段名、类型、格式要求；
# 请返回结构正确、格式符合要求的 body_dict。
# 错误的请求内容以及对应的响应：
# {response}

# 仅输出修改后的 JSON，不需要解释。
# """
#     with open('system.log', 'a', encoding='utf-8') as f:  # 使用 'a' 模式追加
#         f.write(system_prompt + '\n')  # 添加换行符分隔内容

#     print("内容已成功写入system.log文件")
#     for _ in range(max_retry):
#         try:
#             ai_response = Aiclient.chat.completions.create(
#                 model=OPENAI_MODEL,
#                 messages=[{"role": "system", "content": system_prompt}],
#                 temperature=0.2,
#                 response_format={"type": "json_object"},
#             )
#             content = ai_response.choices[0].message.content.strip()
#             if content.startswith("```json"):
#                 content = content[7:]
#             if content.endswith("```"):
#                 content = content[:-3]
#             revised_body = json.loads(content)
#             return revised_body
#         except json.JSONDecodeError as e:
#             print(f"无法解析 GPT 返回的 JSON 内容: {str(e)}")
#             continue
#         except Exception as e:
#             print(f"GPT 分析失败: {str(e)}")
#             continue

#     return api_body_dict

def revise_vulrequest_with_llm(response, original_request, candidate_api_test_type, max_retry=3):
    import json  # 放到函数内部，确保可独立使用
    api_path_dict, api_header_dict, api_query_dict, api_body_dict = original_request
    api_vul_mapping = {
        "proxy_api": "SSRF",
        "upload_api": "文件上传漏洞",
        "path_api": "路径遍历漏洞",
        "command_api": "命令注入漏洞",
        "database_api": "SQL注入漏洞",
        "display_api": "XSS漏洞"
    }
    system_prompt = """
🧑‍💻【角色设定（Role Instructions）】

- 你是一名经验丰富的 API 漏洞测试专家；
- 你收到一个 HTTP 请求及其对应的响应，响应状态码为 {status_code}；
- 你的任务是分析请求失败的原因，并对请求进行修改，使其在语法和语义上都合法；
- 所有用于 fuzzing 或漏洞探测的安全负载必须保持不变。

📌【任务说明（Task Instructions）】

🔹 原始请求体（Original Request）：
{request_body}

🔹 错误响应（Error Response）：
{error_response}

请你执行以下任务：

1. 分析响应内容，识别导致请求失败的字段、格式或类型错误；
2. 修改请求的 body 字段（必要时也可调整 path 或 query 参数）以满足服务端预期格式；
3. headers 部分保持原样；
4. 不得删除、替换或改动任何 fuzzing payload；
5. 最终仅返回合法且格式正确的 JSON 请求体；
6. 不需要解释或输出任何多余文字，只输出修正后的 JSON。

示例修正：

输入：
{{
  "__body__": [
    {{
      "Name": "1",
      "Url": "http://127.0.0.1:4444/ssrf/RepositoriesLLMUrl",
      "Enabled": true,
      "repositoryInfos": []
    }}
  ]
}}

输出：
{{
  "Name": "1",
  "Url": "http://127.0.0.1:4444/ssrf/RepositoriesLLMUrl",
  "Enabled": true,
  "repositoryInfos": []
}}
""".format(
    status_code=response.status_code,
    request_body=json.dumps(api_body_dict, indent=2),
    error_response=response.text[:500]
)


    print(system_prompt)
    for _ in range(max_retry):
        try:
            ai_response = Aiclient.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "system", "content": system_prompt}],
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            content = ai_response.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            revised_body = json.loads(content)
            return revised_body
        except json.JSONDecodeError as e:
            print(f"无法解析 GPT 返回的 JSON 内容: {str(e)}")
            continue
        except Exception as e:
            print(f"GPT 分析失败: {str(e)}")
            continue

    return api_body_dict
# 新增辅助函数：递归构造父请求
# 修改后的主函数
def candidate_apis_test(baseurl, header_dict, param_dict, output_dir, api_template_list, candidate_api_list, api_validity_json, no_get_producer, open_isrequired, need_trigger, log_file,openapi_file):
    """测试候选API的主函数"""
    max_retries=3
    # 遍历每个候选API
    for candidate_api in candidate_api_list:
        # 跳过已知的Jellyfin bug URL
        if candidate_api[0].api_url in JellyfinBugUrls:
            continue
            
        # 获取API模板和测试类型
        candidate_api_template = candidate_api[0]  # API模板
        candidate_api_test_types = candidate_api[1]  # API测试类型
        
        # 获取当前API在模板列表中的索引
        candidate_api_index = api_template_list.index(candidate_api_template)
        
        # 构建生产者池(除去当前API)
        candidate_api_producer_pool = api_template_list[:candidate_api_index] + api_template_list[candidate_api_index+1:]
        # 获取所有候选分支序列
        candidate_api_seqs, candidate_api_seq_relationses = parallel_sequence_construction(candidate_api_template, candidate_api_producer_pool, no_get_producer)
        print(candidate_api_seqs, candidate_api_seq_relationses)
        # 如果没有返回候选分支，则回退使用原有方法
        # if not completed_sequences:
        #     candidate_api_seq, candidate_api_seq_relations = reverse_sequence_construction(candidate_api_template, candidate_api_producer_pool, no_get_producer)
        #     completed_sequences = [(candidate_api_seq, candidate_api_seq_relations)]

        # 遍历每个候选序列
        for candidate_api_seq, candidate_api_seq_relations in zip(candidate_api_seqs, candidate_api_seq_relationses):
        # 构建反向序列和关系
        #candidate_api_seq, candidate_api_seq_relations = reverse_sequence_construction(candidate_api_template, candidate_api_producer_pool, no_get_producer)
        
        # 记录测试日志
            write_test_log(log_file, candidate_api_seq, candidate_api_seq_relations, candidate_api_test_types)
            
            finished_flag = True  # 完成标志
            unfinished_seq_dir = output_dir + "unfinished_seq/"  # 未完成序列目录

            # 执行序列中的每个API(除最后一个)
            for api_index in range(len(candidate_api_seq)-1):
                current_api = candidate_api_seq[api_index]
                #print("current_api", current_api)
                # 生成参数值
                value_generation(current_api, candidate_api_seq_relations)
                temp_request_value = copy.deepcopy(current_api.api_request_value)
                
                # 使用自定义参数更新请求值
                if param_dict:
                    update_api_request_param_value_by_custom_param_dict(temp_request_value, param_dict)
                    
                # 格式化请求
                request_dict_list = format_request(temp_request_value, current_api.api_request, open_isrequired)
                # print("request_dict_list")
                # 发送请求
                response,log_str = request_sender(baseurl, current_api.api_url, current_api.api_method, header_dict, request_dict_list, log_file)
                
                valid_flag = True  # 有效性标志
                
                # 验证响应
                if response != None:
                        if (str(response.status_code)[0] == "2"):
                            if "Content-Type" in response.headers:
                                if "json" in response.headers["Content-Type"]:
                                    response_json = json.loads(response.text)
                                    # 更新 API 响应值，根据响应 JSON 中的数据更新指定的 API 参数
                                    update_api_response_value_by_response_json(current_api.api_response_value, response_json)
                                else:
                                    #ToDo: 支持其他Content-Type
                                    pass
                        else:
                            valid_flag = False
                else:
                    valid_flag = False
                if not valid_flag:
                    record_unfinished_seq(candidate_api_template, candidate_api_seq, current_api, unfinished_seq_dir, log_str)
                    finished_flag = False



            # 原有漏洞测试逻辑保持不变...
            if finished_flag:
                vul_dir = output_dir + "vul/"  # 漏洞输出目录
                
                # 生成参数值
                value_generation(candidate_api_template, candidate_api_seq_relations)
                
                # 对每种测试类型进行测试
                for candidate_api_test_type in candidate_api_test_types:
                    # 代理API、命令API、显示API的测试
                    if candidate_api_test_type in ["proxy_api", "command_api", "display_api"]:
                        test_payloads = ApiVulnerabilityPayloads[candidate_api_test_type]
                        test_params = candidate_api_test_types[candidate_api_test_type]
                        vul_output_dir = vul_dir + APIFuncAndVulMapping[candidate_api_test_type] + "/"
                        if not os.path.exists(vul_output_dir):
                            os.makedirs(vul_output_dir)
                        for test_param in test_params:
                            for test_payload in test_payloads:
                                vul_location_str = (candidate_api_template.api_url + "LLM" + test_param).replace("{","!").replace("}","!")
                                vul_output_file = vul_location_str.replace("/","!")
                                test_payload = test_payload.format(vul_location_str)
                                request_value_struct = copy.deepcopy(candidate_api_template.api_request_value)
                                if param_dict:
                                    # 根据自定义参数字典更新 API 请求参数值
                                    update_api_request_param_value_by_custom_param_dict(request_value_struct, param_dict)
                                # 更新 API 请求参数的值，根据自定义参数值列表更新指定的参数
                                update_param_value(request_value_struct, test_param, [test_payload, "LLM_TEST"])
                                # 格式化请求数据，处理路径、头部、查询和请求体的参数
                                test_request_dict_list = format_request(request_value_struct, candidate_api_template.api_request, open_isrequired)
                                # 发送请求到指定的 URL，使用给定的请求参数，并记录日志
                                response,log = request_sender(baseurl, candidate_api_template.api_url, candidate_api_template.api_method, header_dict, test_request_dict_list, log_file)
                                # sleep time for vul request
                                time.sleep(0.4)
                                if candidate_api_test_type == "display_api":
                                    if (candidate_api_template.api_method.lower() == "post") and (response != None) and (str(response.status_code)[0] == "2"):
                                        # 记录漏洞api
                                        record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload, request_validation_api=False)
                                    else:
                                    # 漏洞未触发时，调用智能体修正请求
                                        if response is not None and response.status_code in range(400, 500) and "__body__" in str(test_request_dict_list):
                                            # and "__body__" in str(test_request_dict_list)
                                            max_retry = 3
                                            retry_count = 0
                                            while retry_count < max_retry and response.status_code in range(400, 500):
                                                retry_count += 1
                                                revised_body  = revise_vulrequest_with_llm(
                                                        response=response,
                                                        original_request=test_request_dict_list,
                                                        candidate_api_test_type=candidate_api_test_type,
                                                        max_retry=3
                                                    )
                                                
                                                if revised_body :
                                                    with open('system.log', 'a', encoding='utf-8') as f:  # 使用 'a' 模式追加
                                                        f.write(str(revised_body) + '\n')  # 添加换行符分隔内容
                                                    response1=vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method, test_request_dict_list, revised_body,log_file)
                                                    revised_body=[json.dumps(revised_body)]
                                                    response2=vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method,  test_request_dict_list, revised_body,log_file)
                                                    if (candidate_api_template.api_method.lower() == "post") and (((response1 != None) and (str(response1.status_code)[0] == "2")) or((response2 != None) and (str(response2.status_code)[0] == "2"))):
                                                        # 记录漏洞api
                                                        record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload, request_validation_api=False)
                                                    else:
                                                        if (response1 and response1.text == response.text) and (response2 and response2.text == response.text):
                                                            break
                                                        else:
                                                            response = response1 if response1 else response2
                
                                    
                                if os.path.exists(vul_output_dir + vul_output_file):
                                    # 记录漏洞api
                                    record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload, request_validation_api=True)
                                else:
                                    # 漏洞未触发时，调用智能体修正请求
                                    if response is not None and response.status_code in range(400, 500)  and "__body__" in str(test_request_dict_list):
                                            # and "__body__" in str(test_request_dict_list)
                                            max_retry = 3
                                            retry_count = 0
                                            while retry_count < max_retry and response.status_code in range(400, 500):
                                                retry_count += 1
                                                revised_body  = revise_vulrequest_with_llm(
                                                        response=response,
                                                        original_request=test_request_dict_list,
                                                        candidate_api_test_type=candidate_api_test_type,
                                                        max_retry=3
                                                    )
                                                
                                                if revised_body :
                                                    with open('system.log', 'a', encoding='utf-8') as f:  # 使用 'a' 模式追加
                                                        f.write(str(revised_body) + '\n')  # 添加换行符分隔内容
                                                    response1=vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method, test_request_dict_list, revised_body,log_file)
                                                    revised_body=[json.dumps(revised_body)]
                                                    response2=vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method,  test_request_dict_list, revised_body,log_file)
                                                    if (candidate_api_template.api_method.lower() == "post") and (((response1 != None) and (str(response1.status_code)[0] == "2")) or((response2 != None) and (str(response2.status_code)[0] == "2"))):
                                                        # 记录漏洞api
                                                        record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload, request_validation_api=False)
                                                    else:
                                                        if (response1 and response1.text == response.text) and (response2 and response2.text == response.text):
                                                            break
                                                        else:
                                                            response = response1 if response1 else response2
                                    # if response is not None and response.status_code in range(400, 500) and len(response.text) > 500 and "__body__" in str(test_request_dict_list):
                                    #     revised_body  = revise_vulrequest_with_llm(
                                    #             response=response,
                                    #             original_request=test_request_dict_list,
                                    #             candidate_api_test_type=candidate_api_test_type,
                                    #             max_retry=3
                                    #         )
                                        
                                    #     if revised_body :
                                    #         with open('system.log', 'a', encoding='utf-8') as f:  # 使用 'a' 模式追加
                                    #             f.write(str(revised_body) + '\n')  # 添加换行符分隔内容
                                    #         vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method, test_request_dict_list, revised_body,log_file)
                                    #         revised_body=[json.dumps(revised_body)]
                                    #         vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method,  test_request_dict_list, revised_body,log_file)
                                    #     if os.path.exists(vul_output_dir + vul_output_file):
                                    #                 # 记录修正后的漏洞API
                                    #         record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, request_dict_list, request_validation_api=True)
                    elif candidate_api_test_type == "path_api":
                        test_payloads = ApiVulnerabilityPayloads[candidate_api_test_type]
                        test_params = candidate_api_test_types[candidate_api_test_type]
                        vul_output_dir = vul_dir + APIFuncAndVulMapping[candidate_api_test_type] + "/"
                        if not os.path.exists(vul_output_dir):
                            os.makedirs(vul_output_dir)
                        for test_param in test_params:
                            for test_payload in test_payloads:
                                request_value_struct = copy.deepcopy(candidate_api_template.api_request_value)
                                if param_dict:
                                    # 根据自定义参数字典更新 API 请求参数值
                                    update_api_request_param_value_by_custom_param_dict(request_value_struct, param_dict)
                                update_param_value(request_value_struct, test_param, [test_payload, "LLM_TEST"])
                                test_request_dict_list = format_request(request_value_struct, candidate_api_template.api_request, open_isrequired)
                                response,_ = request_sender(baseurl, candidate_api_template.api_url, candidate_api_template.api_method, header_dict, test_request_dict_list, log_file)
                                if response != None:
                                    if api_validity_json:
                                        if (api_validity_json["success_str"] in response.text) and (api_validity_json["fail_str"] not in response.text) and (("; for 16-bit" in response.text) or ("root:" in response.text)):
                                            record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload[0], request_validation_api=False)
                                        
                                    else:
                                        if str(response.status_code)[0] == "2" and (("; for 16-bit" in response.text) or ("root:" in response.text)):
                                            # 记录漏洞
                                            record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload[0], request_validation_api=False)
                                    
                    elif candidate_api_test_type == "database_api":
                        test_params = candidate_api_test_types[candidate_api_test_type]
                        vul_output_dir = vul_dir + APIFuncAndVulMapping[candidate_api_test_type] + "/"
                        if not os.path.exists(vul_output_dir):
                            os.makedirs(vul_output_dir)
                        request_value_struct = copy.deepcopy(candidate_api_template.api_request_value)
                        if param_dict:
                            update_api_request_param_value_by_custom_param_dict(request_value_struct, param_dict)
                        test_request_dict_list = format_request(request_value_struct, candidate_api_template.api_request, open_isrequired)
                        try:
                            inject_param_list = sqlmap_test(baseurl, candidate_api_template.api_url, candidate_api_template.api_method, header_dict, test_request_dict_list, test_params, log_file)
                        except:
                            continue
                        if inject_param_list:
                            for inject_param in inject_param_list:
                                record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, inject_param, "SQLMap heuristic (basic) test", request_validation_api=False)
                    elif candidate_api_test_type == "upload_api":
                        test_payloads = ApiVulnerabilityPayloads[candidate_api_test_type]
                        test_params = candidate_api_test_types[candidate_api_test_type]
                        vul_output_dir = vul_dir + APIFuncAndVulMapping[candidate_api_test_type] + "/"
                        if not os.path.exists(vul_output_dir):
                            os.makedirs(vul_output_dir)
                        for test_param in test_params:
                            for test_payload in test_payloads:
                                request_value_struct = copy.deepcopy(candidate_api_template.api_request_value)
                                if param_dict:
                                    update_api_request_param_value_by_custom_param_dict(request_value_struct, param_dict)
                                file_data = {test_param: (test_payload[0], open(test_payload[1], 'rb').read())}
                                multipart_formdata = encode_multipart_formdata(file_data)
                                test_request_dict_list = format_request(request_value_struct, candidate_api_template.api_request, open_isrequired)
                                test_request_dict_list = list(test_request_dict_list)
                                test_request_dict_list[3] = multipart_formdata[0]
                                header_dict['Content-Type'] = multipart_formdata[1]
                                response,_ = request_sender(baseurl, candidate_api_template.api_url, candidate_api_template.api_method, header_dict, test_request_dict_list, log_file, upload_flag=True)
                                if response != None:
                                    if api_validity_json:
                                        if (api_validity_json["success_str"] in response.text) and (api_validity_json["fail_str"] not in response.text):
                                            record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload[0], request_validation_api=False)
                                        else:
                                    # 漏洞未触发时，调用智能体修正请求
                                            if response is not None and response.status_code in range(400, 500)  and "__body__" in str(test_request_dict_list):
                                            # and "__body__" in str(test_request_dict_list)
                                                    max_retry = 3
                                                    retry_count = 0
                                                    while retry_count < max_retry and response.status_code in range(400, 500):
                                                        retry_count += 1
                                                        revised_body  = revise_vulrequest_with_llm(
                                                                response=response,
                                                                original_request=test_request_dict_list,
                                                                candidate_api_test_type=candidate_api_test_type,
                                                                max_retry=3
                                                            )
                                                        
                                                        if revised_body :
                                                            with open('system.log', 'a', encoding='utf-8') as f:  # 使用 'a' 模式追加
                                                                f.write(str(revised_body) + '\n')  # 添加换行符分隔内容
                                                            response1=vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method, test_request_dict_list, revised_body,log_file)
                                                            revised_body=[json.dumps(revised_body)]
                                                            response2=vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method,  test_request_dict_list, revised_body,log_file)
                                                            if (candidate_api_template.api_method.lower() == "post") and (((response1 != None) and (str(response1.status_code)[0] == "2")) or((response2 != None) and (str(response2.status_code)[0] == "2"))):
                                                                # 记录漏洞api
                                                                record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload, request_validation_api=False)
                                                            else:
                                                                if (response1 and response1.text == response.text) and (response2 and response2.text == response.text):
                                                                    break
                                                                else:
                                                                    response = response1 if response1 else response2
                                            # if response is not None and response.status_code != 200:
                                            #     revised_request = revise_vulrequest_with_llm(
                                            #         response=response,
                                            #         original_request=test_request_dict_list,
                                                    
                                            #         candidate_api_test_type=candidate_api_test_type,
                                            #         max_retry=3
                                            #     )
                                            #     if revised_request:
                                            #         # 使用修正后的请求重新测试
                                            #         request_dict_list = convert(revised_request)
                                            # # 使用修正后的请求重新测试
                                            #         revised_response, _ = request_sender(baseurl, candidate_api_template.api_url, candidate_api_template.api_method, header_dict, request_dict_list, log_file)
                                            #         if (api_validity_json["success_str"] in revised_response.text) and (api_validity_json["fail_str"] not in revised_response.text):
                                            #             # 记录修正后的漏洞API
                                            #             record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload, request_validation_api=True)
                                    else:
                                        if str(response.status_code)[0] == "2":
                                            record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload[0], request_validation_api=False)
                                        else:
                                    # 漏洞未触发时，调用智能体修正请求
                                            if response is not None and response.status_code in range(400, 500) and len(response.text) > 500 and "__body__" in str(test_request_dict_list):
                                            # and "__body__" in str(test_request_dict_list)
                                                max_retry = 3
                                                retry_count = 0
                                                while retry_count < max_retry and response.status_code in range(400, 500):
                                                    retry_count += 1
                                                    revised_body  = revise_vulrequest_with_llm(
                                                            response=response,
                                                            original_request=test_request_dict_list,
                                                            candidate_api_test_type=candidate_api_test_type,
                                                            max_retry=3
                                                        )
                                                    
                                                    if revised_body :
                                                        with open('system.log', 'a', encoding='utf-8') as f:  # 使用 'a' 模式追加
                                                            f.write(str(revised_body) + '\n')  # 添加换行符分隔内容
                                                        response1=vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method, test_request_dict_list, revised_body,log_file)
                                                        revised_body=[json.dumps(revised_body)]
                                                        response2=vul_resend(baseurl, candidate_api_template.api_url,candidate_api_template.api_method,  test_request_dict_list, revised_body,log_file)
                                                        if (candidate_api_template.api_method.lower() == "post") and (((response1 != None) and (str(response1.status_code)[0] == "2")) or((response2 != None) and (str(response2.status_code)[0] == "2"))):
                                                            # 记录漏洞api
                                                            record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload, request_validation_api=False)
                                                        else:
                                                            if (response1 and response1.text == response.text) and (response2 and response2.text == response.text):
                                                                break
                                                            else:
                                                                response = response1 if response1 else response2
                                            # if response is not None and response.status_code != 200:
                                            #     revised_request = revise_vulrequest_with_llm(
                                            #         response=response,
                                            #         original_request=test_request_dict_list,
                                                    
                                            #         candidate_api_test_type=candidate_api_test_type,
                                            #         max_retry=3
                                            #     )
                                            #     if revised_request:
                                            #         # 使用修正后的请求重新测试
                                            #         request_dict_list = convert(revised_request)
                                            # # 使用修正后的请求重新测试
                                            #         revised_response, _ = request_sender(baseurl, candidate_api_template.api_url, candidate_api_template.api_method, header_dict, request_dict_list, log_file)
                                            #         if str(revised_response.status_code)[0] == "2":
                                            #             # 记录修正后的漏洞API
                                            #             record_vul_api(vul_output_dir, candidate_api_test_type, candidate_api_template, test_param, test_payload, request_validation_api=True)
                    else:
                        print("不支持的API功能类型: ", candidate_api_test_type)
                    # except Exception as e:
            #     continue
                # ...（原有漏洞测试代码）


def main():
    """主函数:解析命令行参数并执行API测试"""

    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--openapi', help='解析 OpenAPI 文件路径以支持 multipart/form-data 上传接口', type=str, default=None, required=False)
    parser.add_argument('--restler_compile', help='RESTler 编译文件路径', type=str, default="APIInfo.txt", required=False)
    parser.add_argument('--verification_server_ip', help='验证服务器的IP地址', type=str, default="127.0.0.1", required=False)
    parser.add_argument('--verification_server_port', help='验证服务器的端口', type=int, default=4444, required=False)
    parser.add_argument('--verification_server_port_for_https', help='验证服务器的HTTPS端口', type=int, default=4445, required=False)
    parser.add_argument('--baseurl', help='目标API服务的基本URL', type=str, default="http://127.0.0.1", required=False)
    parser.add_argument('--output', help='输出目录的绝对路径', type=str, default="./", required=False)
    parser.add_argument('--upload_payloads_dir', help='上传有效负载目录的绝对路径', type=str, default=None, required=False)
    parser.add_argument('--api_header_file', help='API请求头文件路径', type=str, default=None, required=False)
    parser.add_argument('--api_content_type', help='API请求的Content-Type头', type=str, default="application/json", required=False)
    parser.add_argument('--api_param_file', help='API参数文件路径', type=str, default=None, required=False)
    parser.add_argument('--api_validity_file', help='判断API请求成功与否的有效性文件路径', type=str, default=None, required=False)
    parser.add_argument('--api_template_file', help='API模板文件路径', type=str, default=None, required=False)
    parser.add_argument('--no_get_producer', action="store_true", help='是否禁止GET方法作为生产者, 默认: False')
    parser.add_argument('--open_isrequired', action="store_true", help='是否开启参数的 isRequired 选项, 默认: False')
    parser.add_argument('--need_trigger', action="store_true", help='是否需要触发API漏洞, 默认: False')
    args = parser.parse_args()
    
    # 初始化日志
    start_log_str = "----------------LLM Start-----------------------\n"
    adapt_api_vul_payloads(args.verification_server_ip, args.verification_server_port, args.verification_server_port_for_https, args.upload_payloads_dir)

    # 确定输出目录
    if args.output == "./":
        output_dir = os.path.abspath('.')
    else:
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        output_dir = args.output
    if not output_dir.endswith("/"):
        output_dir += "/"

    # 创建子目录
    subdirs = ["unfinished_seq", "vul"]
    for subdir in subdirs:
        temp_dir = output_dir + subdir + "/"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

    # 初始化日志文件
    log_file = output_dir + "test_log.txt"
    if os.path.exists(log_file):
        os.remove(log_file)
    write_log(log_file, start_log_str)

    # 如果提供了OpenAPI文件，处理multipart上传接口
    if args.openapi:
        upload_apis = solve_multipart(args.openapi)

    # 基本URL和请求头
    baseurl = args.baseurl
    header_dict = {"Content-Type": args.api_content_type}
    if args.api_header_file:
        with open(args.api_header_file, "r", encoding="utf-8") as fd:
            header_dict.update(json.loads(fd.read().strip()))

    # 加载API参数
    if args.api_param_file:
        with open(args.api_param_file, "r", encoding="utf-8") as fd:
            param_dict = json.loads(fd.read().strip())
    else:
        param_dict = None

    # 加载API有效性判断文件
    if args.api_validity_file:
        with open(args.api_validity_file, "r", encoding="utf-8") as fd:
            api_validity_json = json.loads(fd.read().strip())
    else:
        api_validity_json = None

    # 加载API模板文件
    if args.api_template_file:
        with open(args.api_template_file, "r", encoding="utf-8") as fd:
            add_api_templates_json = json.loads(fd.read().strip())
        add_api_templates_list, add_candidate_api_list = solve_add_api_templates_json(add_api_templates_json)
    else:
        add_api_templates_list = None
        add_candidate_api_list = None

    # 解析RESTler编译文件
    api_template_list = parse_restler_compile(args.restler_compile)

    # 合并新增的API模板
    if add_api_templates_list:
        for add_api_template in add_api_templates_list:
            for api_template in api_template_list:
                if (api_template.api_url == add_api_template.api_url) and (api_template.api_method.lower() == add_api_template.api_method.lower()):
                    api_template_list.remove(api_template)
        api_template_list += add_api_templates_list
    #print(api_template_list)
    # 解析OpenAPI文件
    with open(args.openapi, 'r', encoding='utf-8') as file:
        openapi_data = json.load(file)
    # 提取候选API列表
    candidate_api_list = candidate_api_extraction(api_template_list)
    #print(candidate_api_list)
    # 处理上传API
    upload_candidate_api_list = []
    if upload_apis:
        for upload_api in upload_apis:
            for api_template in api_template_list:
                if (api_template.api_url == upload_api["api_url"]) and (api_template.api_method.lower() == upload_api["api_method"].lower()):
                    api_template.api_request["body"] = {upload_api["multipart_param"]: ["String", [], ["MultiPartValue"], True]}
                    api_template.api_request_value["body"] = {upload_api["multipart_param"]: ["MultiPartValue", "LLM_SPECIFICATION"]}
                    upload_candidate_api_list.append([api_template, {"upload_api": [upload_api["multipart_param"]]}])
                    break

    # 合并候选API列表
    if upload_candidate_api_list:
        candidate_api_list += upload_candidate_api_list
    if add_candidate_api_list:
        for add_candidate_api in add_candidate_api_list:
            for candidate_api in candidate_api_list:
                if (candidate_api[0].api_url == add_candidate_api[0].api_url) and (candidate_api[0].api_method.lower() == add_candidate_api[0].api_method.lower()):
                    candidate_api_list.remove(candidate_api)
        candidate_api_list = add_candidate_api_list + candidate_api_list

    # 执行候选API测试
    candidate_apis_test(baseurl, header_dict, param_dict, output_dir, api_template_list, candidate_api_list, api_validity_json, args.no_get_producer, args.open_isrequired, args.need_trigger, log_file,args.openapi)

    # 结束日志
    end_log_str = "----------------LLM End-----------------------\n"
    write_log(log_file, end_log_str)

if __name__ == "__main__":
    main()



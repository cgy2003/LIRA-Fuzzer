import os, re, sys, copy, time, json, random, requests, functools
import LLMTemplate
from LLMGlobalData import *
from json_ref_dict import materialize, RefDict
import copy
from config import Aiclient,OPENAI_MODEL
import functools
from collections import deque
# ApiPathKeywords = {
# "proxy_api" : ["host", "link", "proxy", "fetch", "redirect", "callback", "hook", "img", "image", "connect"],
# "upload_api" : ["upload", "import", "file", "pic", "image", "img", "content", "page", "avatar", "attach", "submit", "post"],
# "path_api" : ["download", "export", "fetch", "file", "path", "category"],
# "command_api" : ["set", "command", "cmd", "conf", "cfg", "rpc", "exec", "diagnose", "ping", "system", "ip", "nslookup"],
# "database_api" : ["sql", "database", "db", "query", "list", "search", "order", "select", "table", "column", "row"],
# "display_api" : ["name", "content", "edit", "desc", "title", "view", "html", "link", "display", "code", "text", "tab", "comment", "tag", "note"]
# }



# ApiParamKeywords = {
# "proxy_api" : ["url", "uri", "host", "endpoint", "path", "href", "link", "proxy", "client", "remote", "fetch", "dest", "redirect", "site", "callback", "hook", "img", "image", "access", "domain", "agent", "ping"],
# "upload_api" : ["upload", "file", "path", "category", "dir", "pic", "image", "img"],
# "path_api" : ["file", "path", "category"],
# "command_api" : ["set", "command", "cmd", "exec", "ping", "ip", "nslookup"],
# "database_api" : ["sql", "query", "id", "select", "field"],
# "display_api" : ["name", "content", "desc", "title", "view", "html", "code", "text", "tab", "comment", "tag", "note"]
# }
def resolve_multipart_api(multipart_json):
    """
    解析multipart/form-data参数，识别文件上传字段
    :param multipart_json: multipart/form-data schema定义
    :return: 文件参数字段名
    """
    # 策略1：通过format字段识别
    # 策略2：通过description描述识别
    for param_name in multipart_json:
        param_info = multipart_json[param_name]
        if param_info.get("format", "").lower() == "binary":
            return param_name
        if " file" in param_info.get("description", "").lower():
            return param_name
    return ""

# def resolve_signal_api_info(api_method, signal_api_info):
#     """
#     解析单个API的文件上传信息
#     :param api_method: HTTP方法
#     :param signal_api_info: API定义信息
#     :return: 文件参数字段名或False
#     """
#     # 仅处理支持body的方法
#     if api_method.lower() not in ["post", "put", "patch"]:
#         return False
    
#     # 解析requestBody中的multipart定义
#     if "requestBody" in signal_api_info:
#         request_body = materialize(signal_api_info["requestBody"])
#         if "multipart/form-data" in request_body.get("content", {}):
#             schema = request_body["content"]["multipart/form-data"]["schema"]
#             return resolve_multipart_api(schema.get("properties", {}))
#     return False

# def resolve_signal_api_info(api_method, signal_api_info):
#     """
#     解析单个API的文件上传信息
#     :param api_method: HTTP方法
#     :param signal_api_info: API定义信息
#     :return: 文件参数字段名或False
#     """
#     # 仅处理支持body的方法
#     if api_method.lower() not in ["post", "put", "patch"]:
#         return False
    
#     # 解析requestBody
#     if "requestBody" not in signal_api_info:
#         return False
    
#     request_body = materialize(signal_api_info["requestBody"])
#     content = request_body.get("content", {})
    
#     # 检查multipart/form-data格式
#     if "multipart/form-data" in content:
#         schema = content["multipart/form-data"]["schema"]
#         properties = schema.get("properties", {})
#         # 查找类型为binary的字段
#         for param_name, param_schema in properties.items():
#             if param_schema.get("format") == "binary" or param_schema.get("type") == "string" and param_schema.get("contentMediaType") == "binary":
#                 return param_name
    
#     # 检查application/octet-stream格式
#     elif "application/octet-stream" in content:
#         schema = content["application/octet-stream"]["schema"]
#         if schema.get("format") == "binary" or schema.get("type") == "string" and schema.get("contentMediaType") == "binary":
#             return "file"  # 默认返回'file'作为参数名
    
#     return False
import os
import logging
from typing import Dict, List, Optional, Union

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def resolve_signal_api_info(api_method, signal_api_info):
    """
    解析单个API的文件上传信息，支持多种文件上传格式
    :param api_method: HTTP方法 (post/put/patch)
    :param signal_api_info: API定义信息
    :return: 文件参数字段名(str) 或 None(不支持文件上传)
    """
    # 1. 方法检查
    if api_method.lower() not in {"post", "put", "patch"}:
        return None

    # 2. 检查requestBody是否存在
    if "requestBody" not in signal_api_info:
        return None

    try:
        request_body = materialize(signal_api_info["requestBody"])
        content = request_body.get("content", {})
        
        # 3. 支持的文件类型检测列表（按优先级排序）
        file_content_types = [
            "multipart/form-data",      # 多部分表单
            "application/octet-stream",  # 原始二进制
            "image/*",                   # 图片类型
            "application/pdf",           # PDF文件
            "text/plain"                 # 文本文件
        ]

        # 4. 遍历检测支持的Content-Type
        for content_type in file_content_types:
            if content_type.endswith("/*"):  # 处理通配符类型(如image/*)
                matched_types = [ct for ct in content.keys() if ct.startswith(content_type.split("/*")[0])]
                if not matched_types:
                    continue
                actual_type = matched_types[0]
            else:
                if content_type not in content:
                    continue
                actual_type = content_type

            schema = content[actual_type]["schema"]
            
            # 5. 根据不同类型提取文件参数
            if actual_type == "multipart/form-data":
                # 多部分表单：查找binary格式的字段
                for param_name, param_schema in schema.get("properties", {}).items():
                    if is_binary_schema(param_schema):
                        return param_name
            else:
                # 其他类型：直接检查schema是否为binary
                if is_binary_schema(schema):
                    return get_default_param_name(actual_type)

    except Exception as e:
        logger.warning(f"解析API文件上传信息时出错: {str(e)}")
    
    return None

def is_binary_schema(schema):
    """检查schema是否表示二进制数据"""
    return (
        schema.get("format") == "binary" or
        (schema.get("type") == "string" and schema.get("contentMediaType") == "binary") or
        schema.get("type") == "file"  # 兼容Swagger 2.0
    )

def get_default_param_name(content_type):
    """根据Content-Type返回默认参数名"""
    return {
        "application/octet-stream": "file",
        "application/pdf": "pdf_file",
        "text/plain": "text_file"
    }.get(content_type, "file")
def solve_multipart(openapi):
    """
    解析整个OpenAPI文档，提取文件上传API
    :param openapi: OpenAPI文件路径
    :return: 上传API列表 [{"api_url", "api_method", "multipart_param"}]
    """
    # 预处理非ASCII字符问题
    with open(openapi, "r+", encoding="utf-8") as f:
        content = f.read()
        cleaned = ''.join([c for c in content if ord(c) < 128])  # 过滤非ASCII字符
        f.seek(0); f.write(cleaned); f.truncate()

    # 使用RefDict解析OpenAPI引用
    api_json = RefDict(openapi)
    upload_apis = []

    # 遍历paths/webhooks节点
    endpoints = api_json.get("paths", {}) or api_json.get("webhooks", {})
    for api_url, api_info in endpoints.items():
        if not isinstance(api_info, RefDict):
            continue

        # 遍历各HTTP方法
        for method in api_info:
            print(method, api_url)
            if (param := resolve_signal_api_info(method, api_info[method])):
                print(1)
                # 路径关键词匹配
                path_flag = any(kw in api_url.lower() for kw in ApiPathKeywords["upload_api"])
                # 参数关键词匹配
                param_flag = any(kw in param.lower() for kw in ApiParamKeywords["upload_api"])
                
                if path_flag  or param_flag:
                    upload_apis.append({
                        "api_url": api_url,
                        "api_method": method,
                        "multipart_param": param
                    })
    return upload_apis   
    
# ---------------------------- 漏洞载荷处理 ----------------------------

def adapt_api_vul_payloads(verification_server_ip, verification_server_port, verification_server_port_for_https, upload_dir):
    """
    动态替换漏洞验证载荷中的占位符
    :param verification_server_ip: 验证服务器IP
    :param verification_server_port: HTTP验证端口
    :param verification_server_port_for_https: HTTPS验证端口
    :param upload_dir: 上传文件目录
    """
    global ApiVulnerabilityPayloads
    
    # 替换IP:PORT占位符
    for category in ["proxy_api", "command_api", "display_api"]:
        for i, payload in enumerate(ApiVulnerabilityPayloads[category]):
            if "http://" in payload:
                replacement = f"{verification_server_ip}:{verification_server_port}"
            elif "https://" in payload:
                replacement = f"{verification_server_ip}:{verification_server_port_for_https}"
            ApiVulnerabilityPayloads[category][i] = payload.replace("IP:PORT", replacement)
    
    # 加载上传目录文件
    if upload_dir:
        for filename in os.listdir(upload_dir):
            filepath = os.path.join(upload_dir, filename)
            if os.path.isfile(filepath):
                ApiVulnerabilityPayloads["upload_api"].append([filename, filepath])

# ---------------------------- 参数处理相关函数 ----------------------------

def naming_convention_split(param):
    """
    参数命名规范拆分（驼峰式、中划线、下划线）
    :param param: 原始参数名
    :return: 拆分后的参数名列表
    """
    # 驼峰式拆分
    camel_case = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', param)
    return list({
        camel_case[-1].lower() if camel_case else "",
        param.split("-")[-1].lower(),
        param.split("_")[-1].lower()
    })

def symspell_corrector(param):
    """
    使用SymSpell进行拼写校正
    :param param: 原始参数名
    :return: 校正后的参数名列表
    """
    suggestions = sym_spell.lookup_compound(
        phrase=param,
        max_edit_distance=2,
        transfer_casing=True,
        ignore_term_with_digits=True,
        ignore_non_words=True
    )
    return [s.term.split()[-1].lower() for s in suggestions]

# 这段代码的主要功能是处理API之间的生产者和消费者关系。以下是代码的注释说明：

def extend_consumers(consumers):
    # 对每个消费者进行处理，扩展其可能的命名变体和拼写纠正
    for consumer in consumers:
        consumer_split_list = []
        # 通过命名约定拆分消费者名称
        consumer_split_list += naming_convention_split(consumer)
        # 通过拼写纠正拆分消费者名称
        consumer_split_list += symspell_corrector(consumer)
        # 去重
        consumer_split_list = list(set(consumer_split_list))
        # 如果原始消费者名称在拆分列表中，移除它
        if consumer in consumer_split_list:
            consumer_split_list.remove(consumer)
        # 将原始消费者名称和其扩展列表存入字典
        consumers[consumer] = [consumers[consumer], consumer_split_list]
    return consumers

def find_consumer_the_only_producer(consumer_name, consumer_type, candidate_api_producer_pool):
    # 查找唯一的生产者API
    consumer_producer_apis = []
    the_only_producer = None
    # 如果消费者类型不在随机值字典中，返回False
    if consumer_type not in RandomValueDict.keys():
        return False
    # 构建精确匹配的正则表达式
    accurate_pattern_str = "^[^A-Za-z0-9]*" + consumer_name + "(?!.)"
    accurate_producer_pattern = re.compile(accurate_pattern_str, re.IGNORECASE)
    # 遍历候选生产者API池
    for candidate_api_producer in candidate_api_producer_pool:
        producer_flag = False
        # 获取生产者的名称和类型
        producer_dict = get_consumers_or_producers(candidate_api_producer.api_response)
        for producer_name in producer_dict:
            producer_type = producer_dict[producer_name]
            # 如果匹配正则表达式且类型匹配
            if (re.match(accurate_producer_pattern, producer_name)) and (producer_type == consumer_type):
                producer_flag = True
                temp_producer_apis = consumer_producer_apis[:]
                # 检查是否有更高优先级的生产者API
                for temp_producer_api in temp_producer_apis:
                    if candidate_api_producer.api_url == temp_producer_api[0].api_url:
                        if ProducerMethodPriority[candidate_api_producer.api_method.upper()] < ProducerMethodPriority[temp_producer_api[0].api_method.upper()]:
                            producer_flag = False
                        else:
                            consumer_producer_apis.remove(temp_producer_api)
                # 如果生产者有效，加入列表
                if producer_flag:
                    if (candidate_api_producer,  producer_name) not in consumer_producer_apis:
                        consumer_producer_apis.append((candidate_api_producer,  producer_name))
    # 如果有多个生产者API，选择URL最长的
    if consumer_producer_apis:
        if len(consumer_producer_apis) >= 2:
            the_only_producer = consumer_producer_apis[0]
            for consumer_producer_api in consumer_producer_apis[1:]:
                if len(consumer_producer_api[0].api_url) > len(the_only_producer[0].api_url):
                    the_only_producer = consumer_producer_api
        else:
            the_only_producer = consumer_producer_apis[0]
    return the_only_producer
# def find_producers(candidate_api, candidate_api_producer_pool):
#     # 查找所有可能的生产者API
#     producer_apis = []
#     producer_consumer_relations = []
#     if not candidate_api_producer_pool:
#         return producer_apis, producer_consumer_relations
#     # 扩展消费者字典
#     extend_consumer_dict = extend_consumers(get_consumers_or_producers(candidate_api.api_request))
#     for consumer in extend_consumer_dict:
#         consumer_type = extend_consumer_dict[consumer][0]
#         # 查找唯一的生产者API
#         the_only_producer = find_consumer_the_only_producer(consumer, consumer_type, candidate_api_producer_pool)
#         if the_only_producer:
#             producer_apis.append(the_only_producer[0])
#             producer_consumer_relations.append({'consumer_api': candidate_api, 'consumer_param': consumer, 'producer_api': the_only_producer[0], 'producer_param': the_only_producer[1]})
#             continue
#         # 精确匹配优先于扩展匹配
#         signal_producer_apis = []
#         extend_consumer_list = extend_consumer_dict[consumer][1]
#         for extend_consumer in extend_consumer_list:
#             the_only_producer = find_consumer_the_only_producer(extend_consumer, consumer_type, candidate_api_producer_pool)
#             if the_only_producer:
#                 signal_producer_apis.append(the_only_producer)
#         if signal_producer_apis:
#             if len(signal_producer_apis) >= 2:
#                 the_signal_producer = signal_producer_apis[0]
#                 # 选择URL最长的生产者API
#                 for signal_producer_api in signal_producer_apis[1:]:
#                     if len(signal_producer_api[0].api_url) > len(the_signal_producer[0].api_url):
#                         the_signal_producer = signal_producer_api
#             else:
#                 the_signal_producer = signal_producer_apis[0]
#             producer_apis.append(the_signal_producer[0])
#             producer_consumer_relations.append({'consumer_api': candidate_api, 'consumer_param': consumer, 'producer_api': the_signal_producer[0], 'producer_param': the_signal_producer[1]})    
#     return list(set(producer_apis)), producer_consumer_relations
def find_producers(candidate_api, candidate_api_producer_pool):
    # 查找所有可能的生产者API
    producer_apis = []
    producer_consumer_relations = []
    if not candidate_api_producer_pool:
        return producer_apis, producer_consumer_relations
    # 扩展消费者字典
    extend_consumer_dict = extend_consumers(get_consumers_or_producers(candidate_api.api_request))
    for consumer in extend_consumer_dict:
        consumer_type = extend_consumer_dict[consumer][0]
        # 查找唯一的生产者API
        the_only_producer = find_consumer_the_only_producer(consumer, consumer_type, candidate_api_producer_pool)
        if the_only_producer:
            producer_apis.append(the_only_producer[0])
            producer_consumer_relations.append({'consumer_api': candidate_api, 'consumer_param': consumer, 'producer_api': the_only_producer[0], 'producer_param': the_only_producer[1]})
            continue
        # 精确匹配优先于扩展匹配
        signal_producer_apis = []
        extend_consumer_list = extend_consumer_dict[consumer][1]
        for extend_consumer in extend_consumer_list:
            the_only_producer = find_consumer_the_only_producer(extend_consumer, consumer_type, candidate_api_producer_pool)
            if the_only_producer:
                signal_producer_apis.append(the_only_producer)
        if signal_producer_apis:
            if len(signal_producer_apis) >= 2:
                the_signal_producer = signal_producer_apis[0]
                # 选择URL最长的生产者API
                for signal_producer_api in signal_producer_apis[1:]:
                    if len(signal_producer_api[0].api_url) > len(the_signal_producer[0].api_url):
                        the_signal_producer = signal_producer_api
            else:
                the_signal_producer = signal_producer_apis[0]
            producer_apis.append(the_signal_producer[0])
            producer_consumer_relations.append({'consumer_api': candidate_api, 'consumer_param': consumer, 'producer_api': the_signal_producer[0], 'producer_param': the_signal_producer[1]})    
    return list(set(producer_apis)), producer_consumer_relations

# def find_producers(candidate_api, candidate_api_producer_pool):
#     producer_apis = []
#     producer_consumer_relations = []
#     if not candidate_api_producer_pool:
#         return producer_apis, producer_consumer_relations
    
#     extend_consumer_dict = extend_consumers(get_consumers_or_producers(candidate_api.api_request))
#     for consumer in extend_consumer_dict:
#         consumer_type = extend_consumer_dict[consumer][0]
#         extend_consumer_list = extend_consumer_dict[consumer][1]
        
#         # 查找所有可能的生产者（包括原始 consumer 和扩展列表）
#         all_producers = []
#         for extend_consumer in [consumer] + extend_consumer_list:
#             producers = find_all_producers_for_consumer(extend_consumer, consumer_type, candidate_api_producer_pool)
#             all_producers.extend(producers)
        
#         # 记录所有关系和生产者
#         for producer_api, producer_param in all_producers:
#             if producer_api not in producer_apis:
#                 producer_apis.append(producer_api)
#             producer_consumer_relations.append({
#                 'consumer_api': candidate_api,
#                 'consumer_param': consumer,  # 注意：这里用原始 consumer，而非 extend_consumer
#                 'producer_api': producer_api,
#                 'producer_param': producer_param
#             })
    
#     return producer_apis, producer_consumer_relations

import re

def find_all_producers_for_consumer(consumer_name, consumer_type, candidate_api_producer_pool):
    """查找所有能提供 consumer_name 的生产者 API（不再唯一）"""
    producers = []
    
    # 如果消费者类型无效，直接返回空列表
    if consumer_type not in RandomValueDict.keys():
        return producers
    
    # 构建精确匹配的正则表达式
    accurate_pattern_str = "^[^A-Za-z0-9]*" + consumer_name + "(?!.)"
    accurate_producer_pattern = re.compile(accurate_pattern_str, re.IGNORECASE)
    
    # 遍历候选生产者池
    for candidate_api_producer in candidate_api_producer_pool:
        producer_dict = get_consumers_or_producers(candidate_api_producer.api_response)
        for producer_name in producer_dict:
            producer_type = producer_dict[producer_name]
            # 检查名称和类型是否匹配
            if re.match(accurate_producer_pattern, producer_name) and (producer_type == consumer_type):
                producers.append((candidate_api_producer, producer_name))
    
    return producers  # 返回所有匹配的生产者（可能为空或多个）
# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # 轻量级通用模型
# def semantic_path_similarity(path1, path2):
#     """
#     使用HuggingFace的sentence-transformers计算两个URL路径的语义相似度
    
#     参数:
#         path1: 第一个URL路径 (如 "/users/profile")
#         path2: 第二个URL路径 (如 "/clients/info")
        
#     返回:
#         float: 语义相似度分数 (0.0~1.0)
#     """
#     # 预处理路径（移除参数，替换特殊字符）
#     def preprocess(path):
#         segments = []
#         for segment in path.split("/"):
#             if not segment:
#                 continue
#             if segment.startswith("{") and segment.endswith("}"):
#                 segments.append("param")  # 参数统一处理
#             else:
#                 segments.append(segment)
#         return " ".join(segments)
    
#     # 获取路径的语义向量
#     emb1 = model.encode(preprocess(path1))
#     emb2 = model.encode(preprocess(path2))
    
#     # 计算余弦相似度
#     similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
#     return float(similarity)
def is_valid_producer(candidate_api, candidate_api_producer, no_get_producer):
    # 检查生产者API是否有效
    # CRUD语义
    if no_get_producer:
        producer_methods = ProducerMethodsNoGet
    else:
        producer_methods = ProducerMethods
    if candidate_api_producer.api_method.upper() not in producer_methods:
        return False
    
    # 资源层次结构
    candidate_api_resource = [i.lower() for i in filter(None, candidate_api.api_url.split("/"))]
    candidate_api_producer_resource = [i.lower() for i in filter(None, candidate_api_producer.api_url.split("/"))]
    for resource in candidate_api_producer_resource:
        if resource not in candidate_api_resource:
            if len(candidate_api_producer_resource) > len(candidate_api_resource):
                return False
            for i in range(len(candidate_api_producer_resource)):
                if candidate_api_producer_resource[i] != candidate_api_resource[i]:
                    # 语义相似度检查
                    # similarity = semantic_path_similarity(candidate_api_producer_resource[i], candidate_api_resource[i])
                    # if similarity < 0.8:  # 阈值可调
                        return False
            
    # 相同URL时，低优先级方法不应作为生产者 (len(candidate_api_producer_resource) == len(candidate_api_resource)) and
    if  (ProducerMethodPriority[candidate_api.api_method.upper()] > ProducerMethodPriority[candidate_api_producer.api_method.upper()]):
        return False
    return True
# def is_valid_producer(candidate_api, candidate_api_producer, no_get_producer):
#     """检查 candidate_api_producer 是否是 candidate_api 的有效生产者"""
    
#     # 1. 过滤无效的生产者方法
#     producer_methods = ProducerMethodsNoGet if no_get_producer else ProducerMethods
#     if candidate_api_producer.api_method not in producer_methods:
#         return False

#     # 2. 解析 API 资源路径
#     candidate_api_resource = set(filter(None, candidate_api.api_url.lower().split("/")))
#     candidate_api_producer_resource = set(filter(None, candidate_api_producer.api_url.lower().split("/")))

#     # 生产者的资源必须是候选 API 资源的子集
#     if not candidate_api_resource.issuperset(candidate_api_producer_resource):
#         return False

#     # 3. 处理相同 URL 的方法优先级问题
#     if candidate_api.api_url == candidate_api_producer.api_url:
#         candidate_priority = ProducerMethodPriority.get(candidate_api.api_method, float('inf'))
#         producer_priority = ProducerMethodPriority.get(candidate_api_producer.api_method, float('inf'))
#         if candidate_priority > producer_priority:
#             return False

#     return True
  
# def valid_producer(candidate_api_seq, current_api_index, candidate_api_producer_pool, no_get_producer):
#     # 验证生产者API池中的有效生产者
#     current_api = candidate_api_seq[current_api_index]
#     vaild_producer_pool = []
#     # 仅处理当前API和候选API，因为当前API可能在候选API序列中有相同的生产者
#     current_api_producer_pool = list(set(candidate_api_producer_pool)-set([candidate_api_seq[-1], current_api]))
#     for candidate_api_producer in current_api_producer_pool:
#         if is_valid_producer(current_api, candidate_api_producer, no_get_producer):
#             vaild_producer_pool.append(candidate_api_producer)
#     return vaild_producer_pool

def valid_producer(candidate_api_seq, current_api_index, candidate_api_producer_pool, no_get_producer):
    """
    验证生产者API池中的有效生产者，并返回去重后的结果
    
    Args:
        candidate_api_seq: 候选API序列
        current_api_index: 当前API在序列中的索引
        candidate_api_producer_pool: 候选生产者API池
        no_get_producer: 是否排除GET方法的生产者
        
    Returns:
        list: 去重后的有效生产者列表
    """
    current_api = candidate_api_seq[current_api_index]
    valid_producer_pool = []  # 存储有效生产者（可能含重复）
    
    # 仅处理当前API和候选API，排除序列末尾的API和当前API本身
    current_api_producer_pool = list(
        set(candidate_api_producer_pool) - {candidate_api_seq[-1], current_api}
    )
    
    # 检查每个候选生产者是否有效
    for candidate_api_producer in current_api_producer_pool:
        if is_valid_producer(current_api, candidate_api_producer, no_get_producer):
            valid_producer_pool.append(candidate_api_producer)
    
    # 返回去重后的结果（保持原有顺序）
    seen = set()
    return [x for x in valid_producer_pool if not (x in seen or seen.add(x))]
def api_compare(api1, api2):
    # 比较两个API的优先级
    if (api1.api_url == api2.api_url) and (api1.api_method == api2.api_method):
        return 0
    else:
        if (api1.api_url == api2.api_url):
            if (ProducerMethodPriority[api1.api_method.upper()] > ProducerMethodPriority[api2.api_method.upper()]):
                return 1
            else:
                return -1
        else:
            if len(api1.api_url) == len(api2.api_url):
                return 0
            elif len(api1.api_url) > len(api2.api_url):
                return 1
            else:
                return -1





import functools
from collections import defaultdict

def parallel_sequence_construction(candidate_api, candidate_api_producer_pool, no_get_producer):
    candidate_api_seqs = []
    candidate_api_seq_relationses = []
    # 使用队列处理每个候选序列分支，每个元素为(current_seq, current_relations, current_i)
    queue = [([candidate_api], [], -1)]
    
    while queue:
        current_seq, current_relations, i = queue.pop(0)
        print(f"Processing sequence: {[api.api_url for api in current_seq]}, Index: {i}")  # 使用 api_url 替代 api_name
        
        # 获取当前处理的API
        current_api = current_seq[i]
        
        # 获取有效的生产者池
        valid_producer_pool = valid_producer(current_seq, i, candidate_api_producer_pool, no_get_producer)
        print(f"Valid producer pool: {[api.api_url for api in valid_producer_pool]}")  # 使用 api_url 替代 api_name
        
        # 查找所有可能的生产者API及其关系
        producer_apis, producer_consumer_relations = find_producers(current_api, valid_producer_pool)
        print(f"Found producers: {[api.api_url for api in producer_apis]}")  # 使用 api_url 替代 api_name
        
        if not producer_apis:
            # 无法找到更多生产者，将当前序列加入结果
            candidate_api_seqs.append(current_seq)
            candidate_api_seq_relationses.append(current_relations)
            print("No more producers found. Adding sequence to results.")  # 调试信息
            continue
        
        # 将关系按生产者API分组
        producer_to_relations = defaultdict(list)
        for rel in producer_consumer_relations:
            producer_to_relations[rel['producer_api']].append(rel)
        
        # 为每个生产者API生成新的分支
        for producer_api in producer_apis:
            # 新关系 = 当前关系 + 该生产者对应的所有关系
            new_relations = current_relations + producer_to_relations[producer_api]
            
            # 构建新序列
            no_sorted_api_seq = current_seq[:-1].copy()
            if producer_api not in no_sorted_api_seq:
                no_sorted_api_seq.append(producer_api)
            sorted_api_seq = sorted(no_sorted_api_seq, key=functools.cmp_to_key(api_compare))
            new_seq = sorted_api_seq + [current_seq[-1]]  # 保持候选API在末尾
            
            # 新索引递减以处理新添加的生产者API
            new_i = i - 1
            
            # 将新分支加入队列
            queue.append((new_seq, new_relations, new_i))
            print(f"New branch created: {[api.api_url for api in new_seq]}")  # 使用 api_url 替代 api_name
            print(f"New index:{new_i}")
    return candidate_api_seqs, candidate_api_seq_relationses




def reverse_sequence_construction(candidate_api, candidate_api_producer_pool, no_get_producer):
    candidate_api_seq = [candidate_api]  # 初始化 API 序列，包含初始的候选 API
    candidate_api_seq_relations = []  # 存储 API 序列关系
    i = -1  # 反向索引
    while True:
        # 查找有效的生产者池，获得当前候选 API 的有效生产者
        valid_producer_pool = valid_producer(candidate_api_seq, i, candidate_api_producer_pool, no_get_producer)
        # 查找生产者 API 和消费者关系
        producer_apis, producer_consumer_relations = find_producers(candidate_api_seq[i], valid_producer_pool)
        # 将生产者和消费者关系添加到序列关系中
        candidate_api_seq_relations += producer_consumer_relations
        # 为序列排序，并添加新的生产者 API
        no_sorted_api_seq = candidate_api_seq[:-1]
        for producer_api in producer_apis:
            if producer_api not in no_sorted_api_seq:
                no_sorted_api_seq.append(producer_api)
        sorted_api_seq = sorted(no_sorted_api_seq, key=functools.cmp_to_key(api_compare))
        candidate_api_seq = sorted_api_seq + [candidate_api]
        # 如果 API 序列回到起始点，则退出循环
        if candidate_api_seq[i] == candidate_api_seq[0]:
            break
        else:
            i = i - 1  # 向前移动索引
    return candidate_api_seq, candidate_api_seq_relations  # 返回最终的 API 序列和关系

# 格式化请求数据，处理路径、头部、查询和请求体的参数
def format_request(request_value_struct, api_request_struct, open_isrequired=False):
    # 删除“不需要”的参数
    def remove_LLM_not_required(api_request_part_dict):
        if isinstance(api_request_part_dict, dict):
            for key, value in list(api_request_part_dict.items()):
                if value == 'LLM_NotRequired':
                    del api_request_part_dict[key]
                else:
                    remove_LLM_not_required(value)
        elif isinstance(api_request_part_dict, list):
            for item in api_request_part_dict:
                remove_LLM_not_required(item)

    # 递归地遍历并格式化请求的每个部分（路径、头部、查询、体）
    def traverse_and_format(param_dict, request_dict, param_name, api_request_part_dict, open_isrequired):
        param_struct = param_dict[param_name]
        request_struct = request_dict[param_name]
        if param_struct[0] == "Array":
            api_request_part_dict[param_name] = []
            # 处理数组类型的参数
            for array_param_index in range(1, len(param_struct)):
                if type(param_struct[array_param_index]) == dict:
                    api_request_part_dict[param_name].append(param_struct[array_param_index])
                    for array_param_name in param_struct[array_param_index]:
                        traverse_and_format(param_struct[array_param_index], request_struct[array_param_index], array_param_name, api_request_part_dict[param_name][-1], open_isrequired)
                elif type(param_struct[array_param_index]) == list:
                    if param_struct[array_param_index][1] == "LLM_RANDOM":
                        param_type = request_struct[array_param_index][0]
                        api_request_part_dict[param_name].append(RandomValueDict[param_type][random.randint(0,43)])
                    else:
                        api_request_part_dict[param_name].append(param_struct[array_param_index][0])
                elif type(param_struct[array_param_index]) == bool:
                    continue  # 忽略布尔值
                else:
                    print("Not Supported Struct in format_request: ", param_struct[array_param_index])
        elif param_struct[0] == "Property":
            api_request_part_dict[param_name] = param_struct[1]
            # 处理属性类型的参数
            for property_param_name in param_struct[1]:
                traverse_and_format(param_struct[1], request_struct[1], property_param_name, api_request_part_dict[param_name], open_isrequired)
        else:
            param_is_required_priority = ["LLM_TEST", "LLM_CONSUMER", "LLM_PRODUCER", "LLM_CUSTOM"]
            if param_struct[1] in param_is_required_priority:
                api_request_part_dict[param_name] = param_struct[0]
                return 
            if open_isrequired:
                is_required = request_struct[3]
                if not is_required:
                    api_request_part_dict[param_name] = "LLM_NotRequired"
                    return
            if param_struct[1] == "LLM_FORMAT":
                for format_str in ApiParamFormat:
                    if format_str in param_name:
                        api_request_part_dict[param_name] = ApiParamFormat[format_str][random.randint(0,43)]
            elif param_struct[1] == "LLM_RANDOM":
                param_type = request_struct[0]
                api_request_part_dict[param_name] = RandomValueDict[param_type][random.randint(0,43)]
            else:
                api_request_part_dict[param_name] = param_struct[0]

    # 初始化请求部分字典
    api_path_dict = {}
    api_header_dict = {}
    api_query_dict = {}
    api_body_dict = {}

    # 处理路径参数
    if request_value_struct["path"]:
        api_path_dict = copy.deepcopy(request_value_struct["path"])
        for param_name in request_value_struct["path"]:
            traverse_and_format(request_value_struct["path"], api_request_struct["path"], param_name, api_path_dict, open_isrequired)
    
    # 处理头部参数
    if request_value_struct["header"]:
        api_header_dict = copy.deepcopy(request_value_struct["header"])
        for param_name in request_value_struct["header"]:
            traverse_and_format(request_value_struct["header"], api_request_struct["header"], param_name, api_header_dict, open_isrequired)

    # 处理查询参数
    if request_value_struct["query"]:
        api_query_dict = copy.deepcopy(request_value_struct["query"])
        for param_name in request_value_struct["query"]:
            traverse_and_format(request_value_struct["query"], api_request_struct["query"], param_name, api_query_dict, open_isrequired)

    # 处理请求体参数
    if request_value_struct["body"]:
        api_body_dict = copy.deepcopy(request_value_struct["body"])
        for param_name in request_value_struct["body"]:
            if (param_name == "body") and (len(list(request_value_struct["body"].keys()))) == 1 and (type(request_value_struct["body"][param_name]) == list):
                api_body_dict = []
                param_struct = request_value_struct["body"][param_name]
                request_struct = api_request_struct["body"][param_name]
                for array_param_index in range(1, len(param_struct)):
                    if type(param_struct[array_param_index]) == dict:
                        api_body_dict.append(param_struct[array_param_index])
                        for array_param_name in param_struct[array_param_index]:
                            traverse_and_format(param_struct[array_param_index], request_struct[array_param_index], array_param_name, api_body_dict[-1], open_isrequired)
                    elif type(param_struct[array_param_index]) == list:
                        if param_struct[array_param_index][1] == "LLM_RANDOM":
                            param_type = request_struct[array_param_index][0]
                            api_body_dict.append(RandomValueDict[param_type][random.randint(0,43)])
                        else:
                            api_body_dict.append(param_struct[array_param_index][0])
                    elif type(param_struct[array_param_index]) == bool:
                        continue  # 忽略布尔值
                    else:
                        print("Not Supported Struct in format_request: ", param_struct[array_param_index])
            else:
                traverse_and_format(request_value_struct["body"], api_request_struct["body"], param_name, api_body_dict, open_isrequired)
    
    # 如果需要删除“不需要”的字段
    if open_isrequired:
        remove_LLM_not_required(api_path_dict)
        remove_LLM_not_required(api_header_dict)
        remove_LLM_not_required(api_query_dict)
        remove_LLM_not_required(api_body_dict)

    return api_path_dict, api_header_dict, api_query_dict, api_body_dict

# 根据自定义参数字典更新 API 请求参数值
def update_api_request_param_value_by_custom_param_dict(request_value_struct, custom_param_dict):
    for request_part in request_value_struct:
        if request_value_struct[request_part]:
            for param_name in request_value_struct[request_part]:
                custom_flag = False
                for custom_param in custom_param_dict:
                    if param_name == custom_param:
                        print("Custom Param: ", custom_param)
                        if (request_value_struct[request_part][param_name][0] == "Array") or (request_value_struct[request_part][param_name][0] == "Property"):
                            request_value_struct[request_part][param_name] = [custom_param_dict[custom_param], "LLM_CUSTOM"]
                        else:
                            if ParamValuePriority[request_value_struct[request_part][param_name][1]] <= ParamValuePriority["LLM_CUSTOM"]:
                                request_value_struct[request_part][param_name] = [custom_param_dict[custom_param], "LLM_CUSTOM"]
                        custom_flag = True
                if custom_flag:
                    continue       
    return


# 更新 API 请求参数的值，根据自定义参数值列表更新指定的参数
def update_param_value(request_value_struct, request_param_name, request_param_value_list):
    # 递归更新参数值
    def traverse_and_update(param_dict, param_name, request_param_name, request_param_value_list):
        request_param_value_strategy = request_param_value_list[1]  # 获取更新策略
        param_struct = param_dict[param_name]  # 获取参数结构
        if param_struct[0] == "Array":
            # 处理数组类型的参数
            for array_param_index in range(1, len(param_struct)):
                if type(param_struct[array_param_index]) == dict:
                    for array_param_name in param_struct[array_param_index]:
                        if param_struct[array_param_index][array_param_name]:
                            if (param_struct[array_param_index][array_param_name][0] != "Array") and (param_struct[array_param_index][array_param_name][0] != "Property"):
                                if (array_param_name == request_param_name):
                                    if ParamValuePriority[param_struct[array_param_index][array_param_name][1]] <= ParamValuePriority[request_param_value_strategy]: 
                                        param_struct[array_param_index][array_param_name] = request_param_value_list
                            else:
                                traverse_and_update(param_struct[array_param_index], array_param_name, request_param_name, request_param_value_list)
                        else:
                            if (array_param_name == request_param_name):
                                param_struct[array_param_index][array_param_name] = request_param_value_list
                elif type(param_struct[array_param_index]) == list:
                    if (param_name == request_param_name):
                        if ParamValuePriority[param_struct[array_param_index][1]] <= ParamValuePriority[request_param_value_strategy]: 
                            param_struct[array_param_index] = request_param_value_list
                elif type(param_struct[array_param_index]) == bool:
                        # 忽略布尔类型
                        continue
                else:
                    print("Not Supported Struct in update_api_request_param_value: ", param_struct[array_param_index])
        elif param_struct[0] == "Property":
            # 处理属性类型的参数
            for property_param_name in param_struct[1]:
                if param_struct[1][property_param_name]:
                    if (param_struct[1][property_param_name][0] != "Array") and (param_struct[1][property_param_name][0] != "Property"):
                        if (property_param_name == request_param_name):
                            if ParamValuePriority[param_struct[1][property_param_name][1]] <= ParamValuePriority[request_param_value_strategy]: 
                                param_struct[1][property_param_name] = request_param_value_list
                    else:
                        traverse_and_update(param_struct[1], property_param_name, request_param_name, request_param_value_list)
                else:
                    if (property_param_name == request_param_name):
                        param_struct[1][property_param_name] = request_param_value_list
        else:
            print(param_struct)
            print("Error in traverse_and_update!!!")
        return
        
    request_param_value_strategy = request_param_value_list[1]  # 获取更新策略
    for request_part in request_value_struct:
        if request_value_struct[request_part]:
            for param_name in request_value_struct[request_part]:
                if request_value_struct[request_part][param_name]:
                    if (request_value_struct[request_part][param_name][0] != "Array") and (request_value_struct[request_part][param_name][0] != "Property"):
                        if param_name == request_param_name:
                            if ParamValuePriority[request_value_struct[request_part][param_name][1]] <= ParamValuePriority[request_param_value_strategy]: 
                                request_value_struct[request_part][param_name] = request_param_value_list
                    else:
                        traverse_and_update(request_value_struct[request_part], param_name, request_param_name, request_param_value_list)
                else:
                    if param_name == request_param_name:
                        request_value_struct[request_part][param_name] = request_param_value_list        
    return 

def send_get_request(baseurl, api_url, header_dict=None, path_params_dict=None, query_params_dict=None, log_file=None):
    """
    发送 GET 请求的专用函数
    
    Args:
        baseurl (str): 基础 URL（如 "http://127.0.0.1:8096"）
        api_url (str): API 路径（如 "/Repositories" 或 "/Items/{id}"）
        header_dict (dict, optional): 请求头（如 {"X-Emby-Token": "xxx"}）
        path_params_dict (dict, optional): 路径参数（如 {"id": "123"}）
        query_params_dict (dict, optional): 查询参数（如 {"limit": 10}）
        log_file (str, optional): 日志文件路径（如 "requests.log"）
    
    Returns:
        tuple: (response, log_str)  
            - response: `requests.Response` 对象
            - log_str: 请求日志字符串（可写入文件）
    """
    # 清理 baseurl（去除末尾的 "/"）
    if baseurl.endswith("/"):
        baseurl = baseurl[:-1]

    # 替换路径参数（如 /Items/{id} → /Items/123）
    if path_params_dict:
        path_params = re.findall(r'({.*?})', api_url)
        for param in path_params:
            param_key = param[1:-1]  # 去掉花括号，如 {id} → id
            if param_key in path_params_dict:
                api_url = api_url.replace(param, str(path_params_dict[param_key]))

    # 构造完整 URL
    url = baseurl + api_url

    # 发送请求
    try:
        log_str = "----------------LLMGET Request-----------------------\n"
        log_str += f"URL: {url}\n"
        log_str += f"Headers: {header_dict}\n"
        log_str += f"Query Params: {query_params_dict}\n"

        response = requests.get(
            url=url,
            headers=header_dict,
            params=query_params_dict,
            timeout=4
        )

        log_str += f"Response: {response.text}\n"
        log_str += f"Status Code: {response.status_code}\n"

        if log_file:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_str)

    except Exception as e:
        log_str += f"Error: {str(e)}\n"
        response = None

    return response, log_str
def vul_resend(baseurl,api_url,api_method, request_dict_list,body,log_file):
    """
    自动根据请求方法发送 HTTP 请求，用于漏洞测试后的重试请求。

    :param api_method: 请求方法，如 "GET", "POST", "PUT", "DELETE"
    :param url: 请求地址
    :param headers: 请求头字典
    :param params: 查询参数（query）
    :param body: 请求体（json 数据）
    :return: 响应对象（requests.Response）或 None（请求失败）
    """
    if baseurl.endswith("/"):
        baseurl = baseurl[:-1]
    api_path_dict, api_header_dict, api_query_dict, _ = request_dict_list
    path_params = re.findall(r'({.*?})', api_url)
    if path_params and api_path_dict:
        for path_param in path_params:
            # print("", api_path_dict)
            api_url = api_url.replace(path_param, str(api_path_dict[path_param[1:-1]]))  # 替换路径参数
    params=api_query_dict
    headers=api_header_dict
    url = baseurl + api_url
    method = api_method.upper()
    body=[body]
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, params=params, json=body)
        elif method == "PUT":
            response = requests.put(url, headers=headers, params=params, json=body)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, params=params, json=body)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, params=params, json=body)
        elif method == "GET":
            # GET 请求通常不带 body，只用 params
            response = requests.get(url, headers=headers, params=params)
        else:
            print(f"❌ 不支持的请求方法: {method}")
            return None

        # 打印调试信息
        print("📩 重发响应状态码:", response.status_code)
        print("📄 重发响应内容:", response.text[:300])  # 避免内容过长
        with open(log_file, "a") as log_file:
            log_file.write(f"LLMRequest Method: {method}\n")
            log_file.write(f"LLMRequest URL: {url}\n")
            if headers:
                log_file.write(f"LLMRequest Headers: {headers}\n")
            if params:
                log_file.write(f"LLMQuery Parameters: {params}\n")
            if body:
                log_file.write(f"LLMRequest Body: {body}\n")
            log_file.write(f"LLMResponse Status Code: {response.status_code}\n")
            log_file.write(f"LLMResponse Content: {response.text[:500]}\n")  # Limit content length
            log_file.write("="*50 + "\n")  # Separator

        return response

    except Exception as e:
        print(f"⚠️ vul_resend 请求失败: {str(e)}")
        return None
    

def vul_send(baseurl, api_url, api_method, header_dict, request_dict_list, log_file, upload_flag=False, test_all_methods=True):
    """发送 HTTP 请求，并可选择测试所有标准方法
    
    Args:
        test_all_methods: 如果为 True，则依次尝试所有标准 HTTP 方法
    """
    if baseurl.endswith("/"):
        baseurl = baseurl[:-1]
    
    api_path_dict, api_header_dict, api_query_dict, api_body_dict = request_dict_list
    if header_dict:
        api_header_dict.update(header_dict)

    # 路径参数替换
    path_params = re.findall(r'({.*?})', api_url)
    if path_params and api_path_dict:
        for path_param in path_params:
            api_url = api_url.replace(path_param, str(api_path_dict[path_param[1:-1]]))

    url = baseurl + api_url
    
    # 请求体处理
    request_data = api_body_dict if upload_flag else json.dumps(api_body_dict) if api_body_dict else None

    # 标准 HTTP 方法列表
    STANDARD_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
    
    responses = []
    methods_to_test = STANDARD_METHODS if test_all_methods else [api_method.upper()]

    for method in methods_to_test:
        try:
            log_str = f"----------------Send: {method} -----------------------\n"
            log_str += f"URL: {url}\n"
            log_str += f"Headers: {api_header_dict}\n"
            log_str += f"Query Params: {api_query_dict}\n"
            log_str += f"Body: {api_body_dict}\n"

            # 根据方法类型调整请求参数
            if method in ['GET', 'HEAD', 'OPTIONS']:
                # 这些方法通常不带请求体
                r = requests.request(
                    method=method,
                    url=url,
                    headers=api_header_dict,
                    params=api_query_dict,
                    timeout=4
                )
            else:
                r = requests.request(
                    method=method,
                    url=url,
                    headers=api_header_dict,
                    params=api_query_dict,
                    data=request_data,
                    timeout=4
                )

            log_str += f"Response: {r.text}\nStatus Code: {r.status_code}\n"
            write_log(log_file, log_str)
            responses.append((method, r))
        
        except Exception as e:
            log_str += f"Error with {method}: {str(e)}\n"
            write_log(log_file, log_str)
            responses.append((method, None))

    # 如果未启用多方法测试，保持原函数行为（返回单个响应）
    if not test_all_methods:
        return responses[0][1], log_str
    else:
        return responses  # 返回所有方法的响应列表

# 发送请求到指定的 URL，使用给定的请求参数，并记录日志
def request_sender(baseurl, api_url, api_method, header_dict, request_dict_list, log_file, upload_flag=False):
    if baseurl.endswith("/"):
        baseurl = baseurl[:-1]
    # print(request_dict_list)
    api_path_dict, api_header_dict, api_query_dict, api_body_dict = request_dict_list
    # print(api_body_dict)
    if header_dict:
        api_header_dict.update(header_dict)  # 更新请求头部

    # 格式化 API URL
    path_params = re.findall(r'({.*?})', api_url)
    if path_params and api_path_dict:
        for path_param in path_params:
            # print("", api_path_dict)
            api_url = api_url.replace(path_param, str(api_path_dict[path_param[1:-1]]))  # 替换路径参数

    url = baseurl + api_url
    if upload_flag:
        request_data = api_body_dict  # 如果是上传 API，直接使用请求体
    else:
        if api_body_dict:
            request_data = json.dumps(api_body_dict)  # 如果有请求体，将其序列化为 JSON
        else:
            request_data = ''

    try:
        # 记录请求信息到日志
        log_str = "----------------Send: " + "-----------------------\n"
        log_str += "send request: {0} {1}\n".format(api_method.lower(), url)
        log_str += "api_header_dict: " + str(api_header_dict) + "\n"
        log_str += "api_query_dict: " + str(api_query_dict) + "\n"
        log_str += "request_data: " + str(api_body_dict) + "\n"
        # write_log(log_file, log_str)

        # 发送 HTTP 请求
        r = requests.request(method=api_method.lower(), url=url, headers=api_header_dict, params=api_query_dict, data=request_data, timeout=4)
        log_str += "response: " + r.text + "\n" + "status_code: " + str(r.status_code) + "\n"
        write_log(log_file, log_str)
    except Exception as e:
        print(e)
        r = None
    return r,log_str

# 更新 API 响应值，根据响应 JSON 中的数据更新指定的 API 参数
def update_api_response_value_by_response_json(api_response_value, response_json, prev_param_name=None):
    if type(response_json) == list:
        # 如果响应数据是列表，递归更新每个元素
        for i in response_json:
            if type(i) == dict:
                update_api_response_value_by_response_json(api_response_value, i)
            else:
                update_api_response_param_value(api_response_value, prev_param_name, [response_json, "LLM_PRODUCER"])
                return 
    elif type(response_json) == dict:
        # 如果响应数据是字典，递归更新每个键值对
        for param_name in response_json:
            if type(response_json[param_name]) == list:
                update_api_response_value_by_response_json(api_response_value, response_json[param_name], param_name)
            elif type(response_json[param_name]) == dict:
                update_api_response_value_by_response_json(api_response_value, response_json[param_name])
            else:
                update_api_response_param_value(api_response_value, param_name, [response_json[param_name], "LLM_PRODUCER"])
    else:
        print("Not Supported Struct in update_api_response_value_by_response_json: ", response_json)

# 更新 API 响应参数的值
def update_api_response_param_value(api_response_value, response_param_name, response_param_value_list):
    def traverse_and_update(param_dict, param_name, response_param_name, response_param_value_list):
        # 遍历并更新参数字典中的参数值
        param_struct = param_dict[param_name]
        if param_struct[0] == "Array":
            # 处理数组类型的参数
            for array_param_index in range(1, len(param_struct)):
                if type(param_struct[array_param_index]) == dict:
                    for array_param_name in param_struct[array_param_index]:
                        if param_struct[array_param_index][array_param_name]:
                            if (param_struct[array_param_index][array_param_name][0] != "Array") and (param_struct[array_param_index][array_param_name][0] != "Property"):
                                if (array_param_name == response_param_name):
                                    # 同名变量仅更新第一次响应的值
                                    if param_struct[array_param_index][array_param_name][1] != response_param_value_list[1]:
                                        param_struct[array_param_index][array_param_name] = response_param_value_list
                            else:
                                traverse_and_update(param_struct[array_param_index], array_param_name, response_param_name, response_param_value_list)
                        else:
                            if (array_param_name == response_param_name):
                                param_struct[array_param_index][array_param_name] = response_param_value_list
                elif type(param_struct[array_param_index]) == list:
                    if (param_name == response_param_name):
                        param_struct[array_param_index] = response_param_value_list
                elif type(param_struct[array_param_index]) == bool:
                        # 忽略布尔类型
                        continue
                else:
                    print("Not Supported Struct in update_api_response_param_value: ", param_struct[array_param_index])
        elif param_struct[0] == "Property":
            for property_param_name in param_struct[1]:
                if param_struct[1][property_param_name]:
                    if (param_struct[1][property_param_name][0] != "Array") and (param_struct[1][property_param_name][0] != "Property"):
                        if (property_param_name == response_param_name):
                            param_struct[1][property_param_name] = response_param_value_list
                    else:
                        traverse_and_update(param_struct[1], property_param_name, response_param_name, response_param_value_list)
                else:
                    if (property_param_name == response_param_name):
                        param_struct[1][property_param_name] = response_param_value_list
        else:
            # print(param_struct)
            print("Error in traverse_and_update!!!")
        return

    # 只更新，不考虑优先级
    for api_response_part in api_response_value:
        if api_response_value[api_response_part]:
            for param_name in api_response_value[api_response_part]:
                if api_response_value[api_response_part][param_name]:
                    if (api_response_value[api_response_part][param_name][0] != "Array") and (api_response_value[api_response_part][param_name][0] != "Property"):
                        if (param_name == response_param_name):
                            # 同名变量仅更新第一次响应的值
                            if api_response_value[api_response_part][param_name][1] != response_param_value_list[1]:
                                api_response_value[api_response_part][param_name] = response_param_value_list
                    else:
                        traverse_and_update(api_response_value[api_response_part], param_name, response_param_name, response_param_value_list)
                else:
                    if (param_name == response_param_name):
                        api_response_value[api_response_part][param_name] = response_param_value_list
    return 

# 获取 API 响应参数的值
def get_api_response_param_value(api_response_value, response_param_name):
    def traverse_and_get(param_dict, param_name, response_param_name):
        response_param_value = ""
        param_struct = param_dict[param_name]
        if param_struct:
            if param_struct[0] == "Array":
                # 处理数组类型的参数
                for array_param_index in range(1, len(param_struct)):
                    if type(param_struct[array_param_index]) == dict:
                        for array_param_name in param_struct[array_param_index]:
                            if param_struct[array_param_index][array_param_name]:
                                if (param_struct[array_param_index][array_param_name][0] != "Array") and (param_struct[array_param_index][array_param_name][0] != "Property"):
                                    if (array_param_name == response_param_name):
                                        response_param_value = param_struct[array_param_index][array_param_name][0]
                                        return response_param_value
                                else:
                                    response_param_value = traverse_and_get(param_struct[array_param_index], array_param_name, response_param_name)
                    elif type(param_struct[array_param_index]) == list:
                        if (param_name == response_param_name):
                            print("Should Not Appear in get_api_response_param_value!!!")
                            response_param_value = param_struct[array_param_index][0]
                            return response_param_value
                    elif type(param_struct[array_param_index]) == bool:
                            # 忽略 is_required
                            continue
                    else:
                        print("Not Supported Struct in get_api_response_param_value: ", param_struct[array_param_index])
            elif param_struct[0] == "Property":
                for property_param_name in param_struct[1]:
                    if param_struct[1][property_param_name]:
                        if (param_struct[1][property_param_name][0] != "Array") and (param_struct[1][property_param_name][0] != "Property"):
                            if property_param_name == response_param_name:
                                response_param_value = param_struct[1][property_param_name][0]
                                return response_param_value
                        else:
                            response_param_value = traverse_and_get(param_struct[1], property_param_name, response_param_name)
            else:
                # print(param_struct)
                print("Error in traverse_and_get!!!")
        else:
            if param_name == response_param_name:
                return response_param_value
    response_param_value = ""
    for api_response_part in api_response_value:
        if api_response_value[api_response_part]:
            for param_name in api_response_value[api_response_part]:
                if (api_response_value[api_response_part][param_name]):
                    if (api_response_value[api_response_part][param_name][0] != "Array") and (api_response_value[api_response_part][param_name][0] != "Property"):
                        if (param_name == response_param_name) and (api_response_value[api_response_part][param_name]):
                            response_param_value = api_response_value[api_response_part][param_name][0]
                            return response_param_value
                    else:
                        response_param_value = traverse_and_get(api_response_value[api_response_part], param_name, response_param_name)
    return response_param_value


def get_request_params(api_request):
    # 定义一个函数，用于解析参数结构
    def parse_param_struct(param_struct):
        # 初始化一个空列表，用于存储请求参数
        request_params = []
        # 如果参数结构的第一项是"Array"
        if param_struct[0] == "Array":
            # 遍历参数结构的第二项到最后一项
            for array_param_index in range(1, len(param_struct)):
                # 初始化一个空列表，用于存储临时参数
                temp_params = []
                # 如果参数结构的第二项到最后一项是字典类型
                if type(param_struct[array_param_index]) == dict:
                    # 遍历字典中的每一项
                    for param_name in param_struct[array_param_index]:
                        # 如果参数结构的第二项到最后一项的第一项不是"Array"或"Property"
                        if (param_struct[array_param_index][param_name][0] != "Array") and (param_struct[array_param_index][param_name][0] != "Property"):
                            # 将参数名添加到请求参数列表中
                            request_params.append(param_name)
                        # 否则，递归调用parse_param_struct函数，将参数结构的第二项到最后一项的第一项作为参数传入
                        else:
                            temp_params = parse_param_struct(param_struct[array_param_index][param_name])
                        # 将临时参数添加到请求参数列表中
                        request_params += temp_params   
        # 如果参数结构的第一项是"Property"
        elif param_struct[0] == "Property":
            # 遍历参数结构的第二项中的每一项
            for param_name in param_struct[1]:
                # 初始化一个空列表，用于存储临时参数
                temp_params = []
                # 如果参数结构的第二项的第一项不是"Array"或"Property"
                if (param_struct[1][param_name][0] != "Array") and (param_struct[1][param_name][0] != "Property"):
                    # 将参数名添加到请求参数列表中
                    request_params.append(param_name)
                # 否则，递归调用parse_param_struct函数，将参数结构的第二项的第一项作为参数传入
                else:
                    temp_params = parse_param_struct(param_struct[1][param_name])
                # 将临时参数添加到请求参数列表中
                request_params += temp_params
        # 如果参数结构的第一项既不是"Array"也不是"Property"
        else:
            pass
        # 返回请求参数列表
        return request_params
    # get header/query/body param name
    request_params = []
    for api_request_part in ["header", "query", "body"]:
        if api_request[api_request_part]:
            for param_name in api_request[api_request_part]:
                temp_params = []
                if (api_request[api_request_part][param_name][0] != "Array") and (api_request[api_request_part][param_name][0] != "Property"):
                    request_params.append(param_name)
                else:
                    temp_params = parse_param_struct(api_request[api_request_part][param_name])
                request_params += temp_params    
    return request_params

def get_consumers_or_producers(api_request_or_api_response):
    # 定义一个内部函数，用于解析参数结构
    def parse_param_struct(param_struct):
        # 创建一个空字典，用于存储消费者或生产者
        consumer_or_producer_dict = {}
        # 如果参数结构是数组
        if param_struct[0] == "Array":
            # 遍历数组中的参数
            for array_param_index in range(1, len(param_struct)):
                # 如果参数是字典
                if type(param_struct[array_param_index]) == dict:
                    # 遍历字典中的参数名
                    for param_name in param_struct[array_param_index]:
                        # 如果参数不是数组或属性
                        if (param_struct[array_param_index][param_name][0] != "Array") and (param_struct[array_param_index][param_name][0] != "Property"):
                            # 将参数名和参数类型存入字典
                            consumer_or_producer_dict[param_name] = param_struct[array_param_index][param_name][0]
                        else:
                            # 否则，递归调用parse_param_struct函数，将参数结构存入字典
                            consumer_or_producer_dict.update(parse_param_struct(param_struct[array_param_index][param_name]))
        # 如果参数结构是属性
        elif param_struct[0] == "Property":
            # 遍历属性中的参数
            for param_name in param_struct[1]:
                # 如果参数不是数组或属性
                if (param_struct[1][param_name][0] != "Array") and (param_struct[1][param_name][0] != "Property"):
                    # 将参数名和参数类型存入字典
                    consumer_or_producer_dict[param_name] = param_struct[1][param_name][0]
                else:
                    # 否则，递归调用parse_param_struct函数，将参数结构存入字典
                    consumer_or_producer_dict.update(parse_param_struct(param_struct[1][param_name]))
        else:
            pass
        # 返回字典
        return consumer_or_producer_dict
    
    # get path/header/query/body param name
    consumers_or_producers = {}
    for api_request_or_response_part in api_request_or_api_response:
        if api_request_or_api_response[api_request_or_response_part]:
            for param_name in api_request_or_api_response[api_request_or_response_part]:
                if (api_request_or_api_response[api_request_or_response_part][param_name][0] != "Array") and (api_request_or_api_response[api_request_or_response_part][param_name][0] != "Property"):
                    consumers_or_producers[param_name] = api_request_or_api_response[api_request_or_response_part][param_name][0]
                else:
                    consumers_or_producers.update(parse_param_struct(api_request_or_api_response[api_request_or_response_part][param_name]))
    return consumers_or_producers

def solve_add_api_templates_json(add_api_templates_json):
    # 定义一个空列表，用于存储新增的API模板
    add_api_templates_list = []
    # 定义一个空列表，用于存储新增的候选API
    add_candidate_api_list = []
    # 遍历传入的API模板列表
    for add_api_template_dict in add_api_templates_json:
        # 判断API模板的请求体是否只有一个键，并且该键对应的值是否为"MultipartParam"
        if (len(list(add_api_template_dict["api_request"]["body"].keys())) == 1) and (add_api_template_dict["api_request"]["body"][list(add_api_template_dict["api_request"]["body"].keys())[0]][0] == "MultipartParam"):
            # upload_api
            # 获取请求体中的键
            multipart_param = list(add_api_template_dict["api_request"]["body"].keys())[0]
            # 定义两个标志位，用于判断API路径和参数是否包含关键字
            path_flag = False
            param_flag = False
            # 遍历API路径关键字列表
            for api_path_keyword in ApiPathKeywords["upload_api"]:
                # 判断API路径是否包含关键字
                if api_path_keyword in add_api_template_dict["api_url"].lower():
                    # 如果包含，则将path_flag置为True，并跳出循环
                    path_flag = True
                    break
            # 遍历API参数关键字列表
            for api_param_keyword in ApiParamKeywords["upload_api"]:
                # 判断参数是否包含关键字
                if api_param_keyword in multipart_param.lower():
                    # 如果包含，则将param_flag置为True，并跳出循环
                    param_flag = True
                    break
            # 判断path_flag和param_flag的值
            if (path_flag and (not param_flag)) or (param_flag):
                # 如果path_flag为True且param_flag为False，或者param_flag为True，则将请求体中的键对应的值修改为["String", [], ["MultiPartValue"], True]
                add_api_template_dict["api_request"]["body"][multipart_param] = ["String", [], ["MultiPartValue"], True]
                # 创建一个新的API模板对象
                add_api_template = LLMTemplate.ApiTemplate(add_api_template_dict["api_url"], add_api_template_dict["api_method"], add_api_template_dict["api_request"], add_api_template_dict["api_response"])
                # 将API模板对象添加到add_api_templates_list列表中
                add_api_templates_list.append(add_api_template)
                # 将API模板对象和对应的参数添加到add_candidate_api_list列表中
                add_candidate_api_list.append([add_api_template, {"upload_api": [multipart_param]}])
        else:
            # other_api
            # 创建一个新的API模板对象
            add_api_template = LLMTemplate.ApiTemplate(add_api_template_dict["api_url"], add_api_template_dict["api_method"], add_api_template_dict["api_request"], add_api_template_dict["api_response"])
            # 将API模板对象添加到add_api_templates_list列表中
            add_api_templates_list.append(add_api_template)
            # 调用candidate_api_extraction函数，获取候选API
            add_candidate_api = candidate_api_extraction([add_api_template])
            # 如果有候选API，则将候选API添加到add_candidate_api_list列表中
            if add_candidate_api:
                add_candidate_api_list.append(add_candidate_api[0])
    # 返回新增的API模板列表和新增的候选API列表
    return add_api_templates_list, add_candidate_api_list

def no_vul_oriented_api_format(api_template_list):
    # 定义一个空列表，用于存储无漏洞的API格式
    no_vul_oriented_api_list = []
    # 遍历api_template_list中的每个api_template
    for api_template in api_template_list:
        # 定义一个空列表，用于存储参数
        tag_params = []
        # 深度拷贝api_template中的api_request
        request_dict = copy.deepcopy(api_template.api_request)
        # 删除request_dict中的path键值对
        del request_dict["path"]
        # 获取request_dict中的消费者或生产者
        request_params = get_consumers_or_producers(request_dict)
        # 遍历request_params中的每个参数
        for request_param in request_params:
            # 如果参数的类型为String
            if request_params[request_param] == "String":
                # 将参数添加到tag_params列表中
                tag_params.append(request_param)
        # 如果tag_params列表不为空
        if tag_params:
            # 定义一个空字典，用于存储测试类型
            test_types = {}
            # 遍历ApiFuncList中的每个api_type
            for api_type in ApiFuncList:
                # 将tag_params列表添加到test_types字典中
                test_types[api_type] = tag_params
            # 将api_template和test_types添加到no_vul_oriented_api_list列表中
            no_vul_oriented_api_list.append([api_template, test_types])
    # 返回no_vul_oriented_api_list列表
    return no_vul_oriented_api_list

def candidate_api_extraction(api_template_list):
    # global ApiPathKeywords, ApiParamKeywords
    # new_ApiPathKeywords, new_ApiParamKeywords = expand_keywords_with_chatgpt(oas_document, ApiPathKeywords, ApiParamKeywords)
    # ApiPathKeywords=new_ApiPathKeywords
    # ApiParamKeywords=new_ApiParamKeywords
    # 定义一个空列表，用于存储候选的API
    candidate_api_list = []
    # 遍历api_template_list中的每个api_template
    for api_template in api_template_list:
        
        # 定义一个空字典，用于存储每个api_template的测试类型
        test_types = {}
        #request_params = get_request_params(api_template.api_request)
        request_dict = copy.deepcopy(api_template.api_request)
        #print(request_dict)
        del request_dict["path"]
        request_params = get_consumers_or_producers(request_dict)
        for api_type in ApiFuncList:
            if api_type == "upload_api":
                # ignore here. 
                # when solve "multipart/form-data", solve upload_api.
                continue
            path_flag = False
            param_flag = False
            tag_params = []
            # 遍历ApiPathKeywords中的每个api_type
            for api_path_keyword in ApiPathKeywords[api_type]:
                
                # 如果api_path_keyword在api_template.api_url中，则设置path_flag为True
                if api_path_keyword in api_template.api_url.lower() or api_template.api_url.lower() in api_path_keyword:
                    # if api_template.api_url.lower()=="/account":
                    #     print(api_template.api_url.lower())
                    path_flag = True
                    break
            # 遍历request_params中的每个request_param
            for request_param in request_params:
                # print(request_param)
                # 遍历ApiParamKeywords中的每个api_type
                for api_param_keyword in ApiParamKeywords[api_type]:
                    # 如果api_param_keyword在request_param中，且request_params[request_param]为String，则设置param_flag为True
                    if (api_param_keyword in request_param.lower()) and (request_params[request_param] == "String"):
                        # 如果request_param不在tag_params中，则将其添加到tag_params中
                        if request_param not in tag_params:
                            tag_params.append(request_param)
                        param_flag = True
                        break
            # 如果path_flag为True且param_flag为False，则将test_types[api_type]设置为request_params中值为String的参数
            if path_flag and (not param_flag):
                test_types[api_type] = []
                for request_param in request_params:
                    if request_params[request_param] == "String":
                        test_types[api_type].append(request_param)
            # 如果param_flag为True，则将test_types[api_type]设置为tag_params
            if param_flag:
                test_types[api_type] = tag_params
        # 深拷贝test_types
        temp_dict = copy.deepcopy(test_types)
        for test_type in temp_dict:
            if not temp_dict[test_type]:
                del test_types[test_type]
        if test_types:
            print(api_template.api_url, api_template.api_method, test_types)
            candidate_api_list.append([api_template, test_types])
        #print(candidate_api_list)
    return candidate_api_list




# def expand_keywords_with_chatgpt(oas_document, ApiPathKeywords, ApiParamKeywords):
#     """
#     传递给 ChatGPT OpenAPI 文档、ApiPathKeywords 和 ApiParamKeywords，让它扩展每个类别下的关键词个数。

#     oas_document: OpenAPI 规范的 JSON 格式文档。
#     ApiPathKeywords: 当前的 API 路径关键词字典。
#     ApiParamKeywords: 当前的 API 参数关键词字典。
    
#     返回扩展后的 ApiPathKeywords 和 ApiParamKeywords。
#     """
#     # 构建与 ChatGPT 的对话   OpenAPI 规范文档: {json.dumps(oas_document)}
#     print(json.dumps(oas_document))
#     role = "You are an AI assistant that helps to analyze API endpoints based on their URL, method, and parameters."
#     task = f"""
#     下面是一个 OpenAPI 3.0.0 规范文档，以及当前的 ApiPathKeywords 和 ApiParamKeywords：

    
#     当前的 ApiPathKeywords: {json.dumps(ApiPathKeywords)}
#     当前的 ApiParamKeywords: {json.dumps(ApiParamKeywords)}

#     请根据 OpenAPI 规范文档，扩展每个 API 类型下的路径关键词（ApiPathKeywords）和参数关键词（ApiParamKeywords）。请确保只增加关键词，保持每个类别下的类型不变。
    
#     返回 JSON 格式：
#     {{
#         "ApiPathKeywords": {{}},
#         "ApiParamKeywords": {{}}
#     }}
#     """

#     # 调用 ChatGPT API 扩展关键词
#     # try:
#     # response = Aiclient.chat.completions.create(
#     #         model="gpt-4",
#     #         prompt=prompt,
#     #         temperature=0.2,
#     #         max_tokens=1500
#     #     )
#     response = Aiclient.chat.completions.create(
#         model=OPENAI_MODEL,
#         messages=[
#             {"role": "system", "content": role},  # 系统角色提供背景信息
#             {"role": "user", "content": f"{task}"},  # 用户角色提供具体任务
#         ],
#         temperature=0.2,
#     )
#         # 解析返回的结果
#     result = json.loads(response.choices[0].text.strip())
#     return result['ApiPathKeywords'], result['ApiParamKeywords']
    
#     # except Aiclient.error.OpenAIError as e:
#     #     print(f"OpenAI API 请求错误: {e}")
#     #     return ApiPathKeywords, ApiParamKeywords





# def find_triggers(candidate_api, api_templates):
#     """
#     根据给定的 candidate_api 和 api_templates，查找可能的触发器 API。触发器 API 是根据 URL 匹配的，且 GET 请求没有路径占位符和查询参数。
#     """
#     triggers = []  # 存储触发器 API
#     the_trigger_url = None  # 存储触发器 URL
#     if candidate_api.api_url in list(MicrocksTrigger.keys()):
#         the_trigger_url = MicrocksTrigger[candidate_api.api_url]  # 如果候选 API 的 URL 在 MicrocksTrigger 中，获取触发器 URL
#     for api_template in api_templates:
#         if the_trigger_url:
#             # 如果找到了触发器 URL，匹配并返回对应的 api_template
#             if api_template.api_url == the_trigger_url:
#                 return [api_template]
#         else:
#             # 如果是 GET 请求，并且 URL 没有包含占位符，且没有请求参数
#             if api_template.api_method.lower() == "get":
#                 if ("{" not in api_template.api_url) and (not get_request_params(api_template.api_request)):
#                     triggers.append(api_template)  # 将匹配的 API 添加到触发器列表中
#     return triggers


def value_generation(api_template, candidate_api_seq_relations):
    # CONSUMER
    """
    根据 candidate_api_seq_relations 中的消费者和生产者关系，从生产者 API 中获取参数值，并更新消费者 API 的请求参数值。
    """
    for candidate_api_seq_relation in candidate_api_seq_relations:
        consumer_api = candidate_api_seq_relation["consumer_api"]
        consumer_param = candidate_api_seq_relation["consumer_param"]
        producer_api = candidate_api_seq_relation["producer_api"]
        producer_param = candidate_api_seq_relation["producer_param"]
        if consumer_api == api_template:
            # 根据生产者 API 提供的值更新消费者 API 请求中的参数
            consumer_param_value = get_api_response_param_value(producer_api.api_response_value, producer_param)
            if consumer_param_value:
                update_param_value(api_template.api_request_value, consumer_param, [consumer_param_value, "LLM_CONSUMER"])
    # ToDo: to support SUCCESS
    return


def api_seq_show(api_seq):
    """
    格式化并展示 API 调用序列。返回形如 "GET /api1 --> POST /api2" 的字符串。
    """
    show_str = ""
    for api_index in range(len(api_seq)-1):
        show_str += api_seq[api_index].api_method + " " + api_seq[api_index].api_url + "  -->  "
    show_str += api_seq[-1].api_method + " " + api_seq[-1].api_url
    return show_str

# 定义一个函数，用于记录手测试API
def record_hand_test_apis(output_dir, upload_apis):
    # 定义手测试文件路径
    hand_test_file = output_dir + "hand_test_apis"
    # 定义手测试内容
    hand_test_content = ""
    # 遍历上传API列表
    for upload_api in upload_apis:
        # 添加手测试API内容
        hand_test_content += "-------- LLM Hand Test API --------\n"
        hand_test_content += "API Type: Upload API\n"
        hand_test_content += "API Url: " + upload_api["api_url"] + "\n"
        hand_test_content += "API Method: " + upload_api["api_method"] + "\n"
        hand_test_content += "API MultipartParam: " + upload_api["multipart_param"] + "\n\n"
    # 打开手测试文件
    f = open(hand_test_file, "w")
    # 写入手测试内容
    f.write(hand_test_content)
    # 关闭文件
    f.close() 

# def record_unfinished_seq(candidate_api, candidate_api_seq, current_api, unfinished_seq_dir):
#     # 将candidate_api的api_url中的"/"替换为"!"
#     unfinished_seq_filename = candidate_api.api_url.replace("/","_")
#     # 定义未完成序列的内容
#     unfinished_seq_content = "-------- LLM Unfinished Sequence --------\n"
#     unfinished_seq_content += "Candidate API Url: " + candidate_api.api_url + "\n"
#     unfinished_seq_content += "Candidate API Method: " + candidate_api.api_method + "\n"
#     unfinished_seq_content += "Candidate API Seq: " + api_seq_show(candidate_api_seq) + "\n"
#     unfinished_seq_content += "Failed API: " + current_api.api_method + " " + current_api.api_url + "\n"
#     unfinished_seq_content += "Failed API Request: " + json.dumps(current_api.api_request_value, indent=2) + "\n"
#     # 打开未完成序列的文件
#     f = open(unfinished_seq_dir + unfinished_seq_filename, "a+")
#     # 写入未完成序列的内容
#     f.write(unfinished_seq_content)
#     # 关闭文件
#     f.close()

def sanitize_filename(filename):
    """清理文件名中的非法字符"""
    # 替换Windows系统非法字符为下划线
    illegal_chars = r'[<>:"/\\|?*{}\[\]]'  # 添加需要过滤的其他字符
    sanitized = re.sub(illegal_chars, '_', filename)
    
    # 去除首尾空格和点（Windows不允许以点结尾）
    sanitized = sanitized.strip().rstrip('.')
    
    # 限制最大长度（Windows路径最大255）
    return sanitized[:200]  # 留有余量给其他部分

def record_unfinished_seq(candidate_api, candidate_api_seq, current_api, unfinished_seq_dir,log_str):
    # 清理文件名中的非法字符
    raw_filename = candidate_api.api_url.replace("/", "_")
    safe_filename = sanitize_filename(raw_filename) + ".log"  # 添加文件扩展名
    
    # 确保目录存在（双重保险）
    os.makedirs(unfinished_seq_dir, exist_ok=True)
    
    # 构建完整路径（使用os.path更安全）
    file_path = os.path.join(unfinished_seq_dir, safe_filename)
    
    # 构造内容
    content = [
        "-------- LLM Unfinished Sequence --------",
        f"Candidate API Url: {candidate_api.api_url}",
        f"Candidate API Method: {candidate_api.api_method}",
        f"Candidate API Seq: {api_seq_show(candidate_api_seq)}",
        f"Failed API: {current_api.api_method} {current_api.api_url}",
        # "Failed API Request: " + json.dumps(current_api.api_request_value, indent=2),
        "Failed API Information: ",
        log_str,
        ""  # 最后留空行
    ]
    
    # 安全写入文件
    try:
        with open(file_path, "a+", encoding='utf-8') as f:
            f.write('\n'.join(content))
    except Exception as e:
        print(f"无法写入未完成序列文件: {str(e)}")
        print(f"问题路径: {file_path}")


def record_vul_api(vul_output_dir, api_func, vul_api, vul_param, test_payload, request_validation_api=False):
    # 如果request_validation_api为True，则vul_api_content为空字符串，否则为"-------- LLM Vul API --------\n"
    if request_validation_api:
        vul_api_content = ""
    else:
        vul_api_content = "-------- LLM Vul API --------\n"
    # 将vul_api.api_url、LLM和vul_param拼接，并将"/"替换为"!"，得到vul_output_file
    vul_output_file = (vul_api.api_url + "LLM" + vul_param).replace("/","!")
    # 将APIFuncAndVulMapping字典中的api_func对应的值添加到vul_api_content中
    vul_api_content += "API Vul Type: " + APIFuncAndVulMapping[api_func] + "\n"
    # 将vul_api.api_url添加到vul_api_content中
    vul_api_content += "Vul API Url: " + vul_api.api_url + "\n"
    # 将vul_api.api_method添加到vul_api_content中
    vul_api_content += "Vul API Method: " + vul_api.api_method + "\n"
    # 将vul_param添加到vul_api_content中
    vul_api_content += "API Vul Param: " + vul_param + "\n"
    # 将test_payload添加到vul_api_content中
    vul_api_content += "API Test Payload: " + test_payload + "\n\n"
    # 如果系统平台是Windows，则将vul_output_dir和vul_output_file拼接，并将"\"替换为"/"，得到vul_file_path
    if sys.platform.startswith("win"):
        vul_file_path = (vul_output_dir + vul_output_file).replace("\\","/")
    else:
        vul_file_path = vul_output_dir + vul_output_file
    # 打开vul_file_path文件，以追加方式写入vul_api_content
    f = open(vul_file_path, "a+")
    f.write(vul_api_content)
    f.close()

# 定义一个函数，用于将日志写入日志文件
def write_log(log_file, log_str):
    # 打开日志文件，以追加模式
    f = open(log_file, "a+")
    # 将日志字符串写入日志文件
    f.write(log_str)
    # 关闭日志文件
    f.close()

def write_test_log(log_file, candidate_api_seq, candidate_api_seq_relations, candidate_api_test_types):
    # 定义一个函数，用于将候选API测试日志写入日志文件
    log_str = "#"*14 + "\n"
    # 定义一个字符串，用于存储日志内容
    log_str += "candidate_api_seq: " + str(candidate_api_seq) + "\n"
    # 将候选API序列转换为字符串并添加到日志中
    for temp_api_template in candidate_api_seq:
        log_str += temp_api_template.api_url + " " + temp_api_template.api_method + "\n"
    # 将候选API序列中的每个API的URL和方法添加到日志中
    log_str += "candidate_api_seq_relations: ---------------\n"
    # 添加候选API序列关系的分隔符
    for candidate_api_seq_relation in candidate_api_seq_relations:
        # 遍历候选API序列关系
        log_str += "producer_api: {0} {1}\nproducer_param: {2}\nconsumer_api: {3} {4}\nconsumer_param: {5}\n------------\n".format(candidate_api_seq_relation["producer_api"].api_url, candidate_api_seq_relation["producer_api"].api_method, candidate_api_seq_relation["producer_param"], candidate_api_seq_relation["consumer_api"].api_url, candidate_api_seq_relation["consumer_api"].api_method, candidate_api_seq_relation["consumer_param"])
        # 将候选API序列关系中的生产者和消费者的API的URL和方法以及参数添加到日志中
    log_str += "candidate_api_test_types: " + str(candidate_api_test_types) + "\n"
    # 将候选API测试类型转换为字符串并添加到日志中
    write_log(log_file, log_str)

def try_extract_upload_path(response_text):
    # 定义文件路径的正则表达式模式
    file_path_pattern = r"(?:[\\/][\w .-]+)+\.\w+"
    # 在响应文本中查找所有匹配文件路径模式的字符串
    file_paths = re.findall(file_path_pattern, response_text)
    # 返回所有匹配的文件路径
    return file_paths

# def sqlmap_test(baseurl, api_url, api_method, header_dict, request_dict_list, test_params, log_file):
#     # 定义sqlmap测试函数
#     sqlmap_cmd = ["python", SQLMapPath]
#     # 定义sqlmap命令
#     if baseurl.endswith("/"):
#         baseurl = baseurl[:-1]
#     # 如果baseurl以/结尾，则去掉/
#     api_path_dict, api_header_dict, api_query_dict, api_body_dict = request_dict_list
#     # 解析request_dict_list，获取api_path_dict, api_header_dict, api_query_dict, api_body_dict
#     if header_dict:
#         api_header_dict.update(header_dict)
#     # 如果header_dict不为空，则更新api_header_dict
#     # format api_url
#     path_params = re.findall(r'({.*?})', api_url)
#     # 使用正则表达式匹配api_url中的参数
#     if path_params and api_path_dict:
#         for path_param in path_params:
#             api_url = api_url.replace(path_param, str(api_path_dict[path_param[1:-1]]))
#     # 如果path_params和api_path_dict都不为空，则替换api_url中的参数
#     sqlmap_url = baseurl + api_url
#     # 拼接baseurl和api_url，得到sqlmap_url
#     if api_query_dict:
#         sqlmap_url += "?"
#         for api_query_key in api_query_dict:
#             sqlmap_url += api_query_key + "=" + str(api_query_dict[api_query_key])
#             sqlmap_url += "&"
#         if sqlmap_url[-1] == "&":
#             sqlmap_url = sqlmap_url[:-1]
#     # 如果api_query_dict不为空，则拼接sqlmap_url
#     sqlmap_cmd += ["-u", "\"" + sqlmap_url + "\""]
#     sqlmap_cmd += ["--method=" + "\"" + api_method + "\""]
#     sqlmap_cmd += ["--threads=5"]  # 限制并发线程数为 5
#     # 添加sqlmap_url和api_method到sqlmap_cmd
#     if api_header_dict:
#         api_header_str = ""
#         for api_header_key in api_header_dict:
#             api_header_str += api_header_key + ":" + str(api_header_dict[api_header_key])
#             api_header_str += "\\n"
#         if api_header_str[-2:] == "\\n":
#             api_header_str = api_header_str[:-2]
#         sqlmap_cmd += ["--headers=" + "\"" + api_header_str + "\""]
#     # 如果api_header_dict不为空，则添加到sqlmap_cmd
#     if api_body_dict:
#         api_body_str = ""
#         for api_body_key in api_body_dict:
#             api_body_str += api_body_key + "=" + str(api_body_dict[api_body_key])
#             api_body_str += ";"
#         if api_body_str[-1] == ";":
#             api_body_str = api_body_str[:-1]
#         sqlmap_cmd += ["--data=" + "\"" + api_body_str + "\"", "--param-del=\";\""]
#     # 如果api_body_dict不为空，则添加到sqlmap_cmd
#     test_param_str = "\""
#     for test_param in test_params:
#         test_param_str += test_param
#         test_param_str += ","
#     if test_param_str[-1] == ",":
#         test_param_str = test_param_str[:-1]
#     test_param_str += "\""
#     sqlmap_cmd += ["-p", test_param_str, "--batch", "--smart"]
#     # 添加test_params到sqlmap_cmd
#     sqlmap_cmd_str = " ".join(sqlmap_cmd)
#     inject_param_list = []
#     try:
#         log_str = "---------------------SQLMap Test: " + time.asctime() + "-------------------\n"
#         log_str += "sqlmap_cmd: " + sqlmap_cmd_str + "\n"
#         write_log(log_file, log_str)
#         param_num = len(test_params)
#         pipe = subprocess.Popen(sqlmap_cmd_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         inject_param_pattern = r"'(.+)' might be injectable"
#         count = 0
#         for info in iter(pipe.stdout.readline, b''):
#             sql_info = info.decode()
#             if "heuristic (basic) test" in sql_info:
#                 count += 1
#                 match = re.search(inject_param_pattern, sql_info)
#                 if match:
#                     inject_param_list.append(match.group(1))
#             if count >= param_num:
#                 pipe.terminate()
#                 pipe.wait()
#                 break
#         return inject_param_list
#     except Exception as e:
#         print(e)
#         return inject_param_list


def sqlmap_test(baseurl, api_url, api_method, header_dict, request_dict_list, test_params, log_file):
    # 定义sqlmap测试函数
    sqlmap_cmd = ["python", SQLMapPath]
    # 定义sqlmap命令
    if baseurl.endswith("/"):
        baseurl = baseurl[:-1]
    # 如果baseurl以/结尾，则去掉/
    api_path_dict, api_header_dict, api_query_dict, api_body_dict = request_dict_list
    # 解析request_dict_list，获取api_path_dict, api_header_dict, api_query_dict, api_body_dict
    if header_dict:
        api_header_dict.update(header_dict)
    # 如果header_dict不为空，则更新api_header_dict
    # format api_url
    path_params = re.findall(r'({.*?})', api_url)
    # 使用正则表达式匹配api_url中的参数
    if path_params and api_path_dict:
        for path_param in path_params:
            api_url = api_url.replace(path_param, str(api_path_dict[path_param[1:-1]]))
    # 如果path_params和api_path_dict都不为空，则替换api_url中的参数
    sqlmap_url = baseurl + api_url
    # 拼接baseurl和api_url，得到sqlmap_url
    if api_query_dict:
        sqlmap_url += "?"
        for api_query_key in api_query_dict:
            sqlmap_url += api_query_key + "=" + str(api_query_dict[api_query_key])
            sqlmap_url += "&"
        if sqlmap_url[-1] == "&":
            sqlmap_url = sqlmap_url[:-1]
    # 如果api_query_dict不为空，则拼接sqlmap_url
    sqlmap_cmd += ["-u", "\"" + sqlmap_url + "\""]
    sqlmap_cmd += ["--method=" + "\"" + api_method + "\""]
    # 添加sqlmap_url和api_method到sqlmap_cmd
    if api_header_dict:
        api_header_str = ""
        for api_header_key in api_header_dict:
            api_header_str += api_header_key + ":" + str(api_header_dict[api_header_key])
            api_header_str += "\\n"
        if api_header_str[-2:] == "\\n":
            api_header_str = api_header_str[:-2]
        sqlmap_cmd += ["--headers=" + "\"" + api_header_str + "\""]
    # 如果api_header_dict不为空，则添加到sqlmap_cmd
    if api_body_dict:
        api_body_str = ""
        for api_body_key in api_body_dict:
            api_body_str += api_body_key + "=" + str(api_body_dict[api_body_key])
            api_body_str += ";"
        if api_body_str[-1] == ";":
            api_body_str = api_body_str[:-1]
        sqlmap_cmd += ["--data=" + "\"" + api_body_str + "\"", "--param-del=\";\""]
    # 如果api_body_dict不为空，则添加到sqlmap_cmd
    test_param_str = "\""
    for test_param in test_params:
        test_param_str += test_param
        test_param_str += ","
    if test_param_str[-1] == ",":
        test_param_str = test_param_str[:-1]
    test_param_str += "\""
    sqlmap_cmd += ["-p", test_param_str, "--batch", "--smart"]
    # 添加test_params到sqlmap_cmd
    sqlmap_cmd_str = " ".join(sqlmap_cmd)
    inject_param_list = []
    try:
        log_str = "---------------------SQLMap Test: " + time.asctime() + "-------------------\n"
        log_str += "sqlmap_cmd: " + sqlmap_cmd_str + "\n"
        write_log(log_file, log_str)
        param_num = len(test_params)
        pipe = subprocess.Popen(sqlmap_cmd_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        inject_param_pattern = r"'(.+)' might be injectable"
        count = 0
        for info in iter(pipe.stdout.readline, b''):
            sql_info = info.decode()
            if "heuristic (basic) test" in sql_info:
                count += 1
                match = re.search(inject_param_pattern, sql_info)
                if match:
                    inject_param_list.append(match.group(1))
            if count >= param_num:
                pipe.terminate()
                pipe.wait()
                break
        return inject_param_list
    except Exception as e:
        print(e)
        return inject_param_list
import os, time, copy, json, argparse
from LLMGlobalData import *
from RESTlerCompileParser import *
from LLMTemplate import *
from LLMUtils import *
from urllib3 import encode_multipart_formdata
import os
import json

# 初始关键词列表
ApiParamKeywords = {
    "proxy_api": ["host", "link", "proxy", "fetch", "redirect", "callback", "hook", "img", "image", "connect"],
    "upload_api": ["upload", "import", "file", "pic", "image", "img", "content", "page", "avatar", "attach", "submit", "post"],
    "path_api": ["download", "export", "fetch", "file", "path", "category"],
    "command_api": ["set", "command", "cmd", "conf", "cfg", "rpc", "exec", "diagnose", "ping", "system", "ip", "nslookup"],
    "database_api": ["sql", "database", "db", "query", "list", "search", "order", "select", "table", "column", "row"],
    "display_api": ["name", "content", "edit", "desc", "title", "view", "html", "link", "display", "code", "text", "tab", "comment", "tag", "note"]
}

ApiPathKeywords = {
    "proxy_api": ["url", "uri", "host", "endpoint", "path", "href", "link", "proxy", "client", "remote", "fetch", "dest", "redirect", "site", "callback", "hook", "img", "image", "access", "domain", "agent", "ping"],
    "upload_api": ["upload", "file", "path", "category", "dir", "pic", "image", "img"],
    "path_api": ["file", "path", "category"],
    "command_api": ["set", "command", "cmd", "exec", "ping", "ip", "nslookup"],
    "database_api": ["sql", "query", "id", "select", "field"],
    "display_api": ["name", "content", "desc", "title", "view", "html", "code", "text", "tab", "comment", "tag", "note"]
}

def ask_chatgpt(api_url, request_params):
    """
    调用ChatGPT分析API URL和请求参数，返回关键词分类结果。
    """
   
    # 生成提示词
    role = (
    "你是一名专门分析 OpenAPI 规范并对 API 行为进行分类的 AI 助手。"
    "你的任务是根据 API 接口的语义和上下文描述，将每个 API 的 URL 路径及其请求参数划分到对应的功能类别中。"
    "你的最终目标是支持基于功能感知的漏洞检测，因此需要准确地将 API 元素映射到预定义的行为类型。"
)


    task = (
    f"API URL: {api_url}\n"
    f"请求参数: {', '.join(request_params)}\n\n"
    "请分析给定的 API URL 路径及其请求参数。\n\n"
    "请使用以下预定义的功能类别进行分类：\n"
    "- proxy_api：与代理或请求转发相关的 API\n"
    "- upload_api：与文件或数据上传相关的 API\n"
    "- database_api：涉及数据库操作或交互的 API\n"
    "- display_api：用于数据库内容展示或界面数据渲染的 API\n\n"
    "对于每个 API 接口：\n"
    "1. 分别对 URL 路径和请求参数进行分类。\n"
    "2. 返回的结果应符合以下 JSON 格式：\n\n"
    "{\n"
    "  \"ApiParamKeywords\": {\n"
    "    \"proxy_api\": [],\n"
    "    \"upload_api\": [],\n"
    "    \"database_api\": [],\n"
    "    \"display_api\": []\n"
    "  },\n"
    "  \"ApiPathKeywords\": {\n"
    "    \"proxy_api\": [],\n"
    "    \"upload_api\": [],\n"
    "    \"database_api\": [],\n"
    "    \"display_api\": []\n"
    "  }\n"
    "}\n\n"
    "⚠ 注意：返回的 JSON 结构必须严格符合以下格式，确保分类准确，避免错误分类或遗漏关键信息。"
)


    # 模拟调用ChatGPT（实际使用时替换为真实API调用）
    response = Aiclient.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": task},
        ],
        temperature=0.2,
    )
    print(response.choices[0].message.content.strip())
    content=response.choices[0].message.content
    if content.startswith("```json"):
        content = content[7:]  
    if content.endswith("```"):
        content = content[:-3]  
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # print(f"Error decoding enhanced schema: {enhanced_schema}")
        return None  # 返回原始 schema

def update_keywords(chatgpt_result):
    """
    根据ChatGPT返回的结果更新关键词列表。
    """
    global ApiParamKeywords, ApiPathKeywords

    # 更新ApiParamKeywords
    for api_type, keywords in chatgpt_result.get("ApiParamKeywords", {}).items():
        if api_type in ApiParamKeywords:
            for keyword in keywords:
                if keyword not in ApiParamKeywords[api_type]:
                    ApiParamKeywords[api_type].append(keyword)

    # 更新ApiPathKeywords
    for api_type, keywords in chatgpt_result.get("ApiPathKeywords", {}).items():
        if api_type in ApiPathKeywords:
            for keyword in keywords:
                if keyword not in ApiPathKeywords[api_type]:
                    ApiPathKeywords[api_type].append(keyword)

def api_extraction(api_template_list, openapi_spec,output_file="./gitea/api_extraction_output.json"):
    """
    提取API数据并使用ChatGPT分析，更新关键词列表。
    """
    # 遍历api_template_list中的每个api_template
    for api_template in api_template_list:
        # 获取小写的API URL
        api_url_lower = api_template.api_url.lower()
        print(api_url_lower)
        # 获取请求参数
        request_dict = copy.deepcopy(api_template.api_request)
        print(request_dict)
        del request_dict["path"]
        request_params = get_consumers_or_producers(request_dict)
        # request_param=fine_url_request(api_url_lower,openapi_spec)
        print(request_params)
        # 使用ChatGPT分析API
        chatgpt_result = ask_chatgpt(api_url_lower, request_params)

        # 更新关键词列表
        update_keywords(chatgpt_result)

    # 保存更新后的关键词列表到JSON文件
    result = {
        "ApiParamKeywords": ApiParamKeywords,
        "ApiPathKeywords": ApiPathKeywords
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"关键词列表已保存到 {output_file}")

def main():
    """主函数:解析命令行参数并执行API测试"""

    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--openapi', help='解析 OpenAPI 文件路径以支持 multipart/form-data 上传接口', type=str, default=None, required=False)
    parser.add_argument('--restler_compile', help='RESTler 编译文件路径', type=str, default="APIInfo.txt", required=False)
    parser.add_argument('--output_file', help='输出文件路径', type=str, default="api_extraction_output.json", required=False)
    # parser.add_argument('--api_template_file', help='API模板文件路径', type=str, default=None, required=False)

    args = parser.parse_args()
    

    # 加载API模板文件
    # if args.api_template_file:
    #     with open(args.api_template_file, "r", encoding="utf-8") as fd:
    #         add_api_templates_json = json.loads(fd.read().strip())
    #     add_api_templates_list, add_candidate_api_list = solve_add_api_templates_json(add_api_templates_json)
    # else:
    add_api_templates_list = None
    if args.openapi:
        with open(args.openapi, "r", encoding='utf-8') as f:
            openapi_spec = json.load(f)
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

    # 提取候选API列表
    api_extraction(api_template_list,openapi_spec)
    #print(candidate_api_list)
    # 处理上传API





if __name__ == "__main__":
    main()
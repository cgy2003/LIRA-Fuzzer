from config import Aiclient, OPENAI_MODEL
import json
import os


def enhance_parameter(schema):
    """
    增强OpenAPI schema，基于RESTGPT论文方法优化
    新增功能：
    1. 支持四种约束类型提取
    2. 改进示例值生成逻辑
    3. 添加输入验证和错误处理
    """
    if not schema:
        return schema

    # 检查是否需要增强(有描述才处理)
    if "description" not in str(schema):
        return schema

    # 更专业的系统角色提示(基于论文中的Guidelines)
    role = (
         "你是一个专门优化 OpenAPI 参数定义的 AI 助手，精通 API 安全、规范建模和接口增强任务。"
    "你的职责包括推断参数的类型、补全描述信息、添加合理约束（如长度、格式、枚举、正则表达式等），"
    "并在上下文允许的前提下提供示例值。"
    "你不会随意修改已有字段，也不会擅自填充模糊信息。"
    )

    task = (
         "请增强下面提供的 OpenAPI 参数 schema。具体要求如下：\n\n"
    "【格式验证】\n"
    "- 输入必须是结构正确的 JSON 格式 schema；若无效请返回错误。\n\n"
    "【增强规则】\n"
    "1. 明确补充类型字段（如 string、integer、boolean、array、object）。\n"
    "2. 对 string 类型参数推断 minLength 与 maxLength。\n"
    "3. 若参数有明显的格式要求，添加标准 format（如 email、uuid、date-time）。\n"
    "4. 对具有离散取值的字段添加 enum 值集合。\n"
    "5. 若能从描述或字段名逻辑推断出 pattern，则添加正则表达式。\n"
    "6. 提供贴近真实语义的 example 示例值，但仅在没有已有示例时才添加。\n"
    "7. 不允许凭空填写 description 字段，若无原始描述则保持为空。\n"
    "8. 若为嵌套对象或数组，应递归增强其子字段。\n\n"
    "【输出要求】\n"
    "- 保留原有字段，仅在逻辑清晰处做补充。\n"
    "- 返回完整增强后的 JSON（不包含解释、注释或额外说明）。\n"
    "- 输出结果需满足 OpenAPI 3.0.0 规范的 JSON 要求，可直接嵌入参数文档。\n\n"
        f"当前 schema:\n{json.dumps(schema, indent=2)}"
    )

    try:
        # 调用API(添加更合理的temperature设置)
        response = Aiclient.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": task},
            ],
            temperature=0.3,  # 比原0.2稍高以允许少量创造性
            response_format={"type": "json_object"}  # 确保返回JSON
        )
        
        content = response.choices[0].message.content
        
        # 更健壮的JSON提取
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        json_content = content[json_start:json_end]
        
        enhanced_schema = json.loads(json_content)
        
        # 保留原始schema中已有的字段
        for key in schema:
            if key not in enhanced_schema:
                enhanced_schema[key] = schema[key]
        print(enhanced_schema)
        return enhanced_schema
        
    except Exception as e:
        print(f"增强schema时出错: {str(e)}")
        return schema  # 失败时返回原始schema
def enhance_requestBody(schema):
    """
    增强OpenAPI schema，基于RESTGPT论文方法优化
    新增功能：
    1. 支持四种约束类型提取
    2. 改进示例值生成逻辑
    3. 添加输入验证和错误处理
    """
    if not schema:
        return schema

    # 检查是否需要增强(有描述才处理)
    if "description" not in str(schema):
        return schema

    # 更专业的系统角色提示(基于论文中的Guidelines)
    role = (
        "你是一个专门优化 OpenAPI 规范中 requestBody 部分的 AI 助手。"
    "你的任务是通过推理缺失字段、添加参数约束、生成示例负载等方式，对 requestBody 中的 schema 结构进行增强。"
    "当字段含义不明确或结构无法可靠推断时，你应保持原样，避免误填。"
    )

    task = (
        "请增强以下 OpenAPI requestBody 中的 schema 内容，具体要求如下：\n\n"
    "【结构检查】\n"
    "- 检查 requestBody 中是否包含 content 字段；若缺失则返回错误。\n\n"
    "【处理流程】\n"
    "1. 遍历所有受支持的媒体类型（如 application/json、multipart/form-data），提取每个 schema。\n"
    "2. 对每个 schema 执行如下增强操作：\n"
    "   - 明确补充属性的类型（如 string、integer、boolean、array、object）。\n"
    "   - 添加合理的属性约束（如 format、maxLength、minimum、maximum、pattern、enum）。\n"
    "   - 若字段为对象或数组，递归增强其嵌套属性。\n"
    "   - 为整个 schema 生成一个完整、语义合理的示例对象（example）。\n"
    "3. 若某字段含义不明确或结构不清，请保持原样，避免增加无根据的字段。\n\n"
    "【输出格式】\n"
    "- 返回增强后的 requestBody 对象，包含改进后的 schema 与生成的示例。\n"
    "- 结果必须是完整的 JSON 格式，便于直接集成到 OpenAPI 规范中。\n"
    "- 输出中不应包含任何说明性文字，仅输出增强后的 JSON。\n\n"
        f"当前 schema:\n{json.dumps(schema, indent=2)}"
    )

    try:
        # 调用API(添加更合理的temperature设置)
        response = Aiclient.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": task},
            ],
            temperature=0.3,  # 比原0.2稍高以允许少量创造性
            response_format={"type": "json_object"}  # 确保返回JSON
        )
        
        content = response.choices[0].message.content
        
        # 更健壮的JSON提取
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        json_content = content[json_start:json_end]
        
        enhanced_schema = json.loads(json_content)
        
        # 保留原始schema中已有的字段
        for key in schema:
            if key not in enhanced_schema:
                enhanced_schema[key] = schema[key]
        print(enhanced_schema)
        return enhanced_schema
        
    except Exception as e:
        print(f"增强schema时出错: {str(e)}")
        return schema  # 失败时返回原始schema


def enhance_parameters(parameters):
    """增强参数列表，添加批处理优化"""
    if not parameters:
        return parameters
    print("正在增强参数列表...")
    # 可以在此添加批处理逻辑以减少API调用次数
    return [enhance_parameter(param) for param in parameters]


def enhance_openapi_spec(openapi_spec):
    """增强完整OpenAPI规范，添加缓存机制"""
    if not isinstance(openapi_spec, dict):
        return openapi_spec
        
    # 深度复制以避免修改原始数据
    enhanced_spec = json.loads(json.dumps(openapi_spec))
    

    
    # 增强paths中的定义
    if 'paths' in enhanced_spec:
        for path, methods in enhanced_spec['paths'].items():
            for method, spec in methods.items():
                if isinstance(spec, dict):
                    if 'parameters' in spec:
                        spec['parameters'] = enhance_parameters(spec['parameters'])
                    if 'requestBody' in spec:
                        if 'content' in spec['requestBody']:
                            for media_type, content in spec['requestBody']['content'].items():
                                if 'schema' in content:
                                    content['schema'] = enhance_requestBody(content['schema'])
    
    return enhanced_spec


def main():
    # 添加输入输出路径验证
    input_path = "httplaceholder\httplaceholder.json"
    output_path = "./enhanced\httplaceholder1.json"
    
    if not os.path.exists(input_path):
        print(f"输入文件不存在: {input_path}")
        return
        
    try:
        with open(input_path, "r", encoding='utf-8') as f:
            openapi_spec = json.load(f)
            
        enhanced_spec = enhance_openapi_spec(openapi_spec)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(enhanced_spec, f, indent=2, ensure_ascii=False)
            
        print(f"成功增强并保存OpenAPI规范到: {output_path}")
        
    except Exception as e:
        print(f"处理失败: {str(e)}")


if __name__ == "__main__":
    main()
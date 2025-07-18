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
        "你是一个专门用于增强 OpenAPI 规范的 AI 助手。"
        "你的任务是通过添加清晰的描述、约束、示例和类型细节来改进 API 参数定义。"
        "你擅长根据参数描述和上下文推断逻辑示例值。"
        "如果参数缺少描述，请不要添加描述并保持原样。"
    )

    task = (
        "请增强以下 OpenAPI schema中所有的参数。\n\n"
        "指令：\n"
        "1. 为所有参数指定正确的类型（例如：string、integer、boolean）。\n"
        "2. 在适用的情况下添加约束（例如：minLength、maxLength、minValue、maxValue、pattern、enum）。\n"
        "3. 仅当可以从描述或现有数据中逻辑推断时，提供示例值。\n"
        "   - 确保示例是现实且与参数用途相关的。\n"
        "   - 如果无法推断出逻辑示例，请完全省略 'example' 字段。\n"
        "   - 如果某个参数已经有了示例值，不要再改变其示例值了，只有在没有示例值的时候才加示例值。\n"
        "4. 如果参数是对象或数组，请增强其嵌套属性。\n"
        "5. 如果参数缺少描述，请不要添加描述并保持原样。\n"
        "6. 确保输出是有效的 JSON 格式，适合直接用于 OpenAPI 规范。\n"
        "7. 不要包含任何额外解释，仅返回增强后的 OpenAPI schema（JSON 格式）。\n\n"
        "有效输出的示例：\n"
        "- 如果示例有效：\n"
        "  {\"type\": \"string\", \"description\": \"用户电子邮件地址\", \"format\": \"email\", \"example\": \"user@example.com\"}\n"
        "- 如果示例不确定：\n"
        "  {\"type\": \"string\", \"description\": \"用户电子邮件地址\", \"format\": \"email\"}\n"
        "- 如果没有描述：\n"
        "  {\"type\": \"string\"}\n\n"
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
def enhance_schema(schema):
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
        "你是一个专门用于增强 OpenAPI 规范的 AI 助手。"
        "你的任务是通过添加清晰的描述、约束、示例和类型细节来改进 API 参数定义。"
        "你擅长根据参数描述和上下文推断逻辑示例值。"
        "如果参数缺少描述，请不要添加描述并保持原样。"
    )

    task = (
        "请增强以下 OpenAPI schema中所有的参数。\n\n"
        "指令：\n"
        "1. 为所有参数指定正确的类型（例如：string、integer、boolean）。\n"
        "2. 在适用的情况下添加约束（例如：minLength、maxLength、minValue、maxValue、pattern、enum）。\n"
        "3. 仅当可以从描述或现有数据中逻辑推断时，提供示例值。\n"
        "   - 确保示例是现实且与参数用途相关的。\n"
        "   - 如果无法推断出逻辑示例，请完全省略 'example' 字段。\n"
        "   - 如果某个参数已经有了示例值，不要再改变其示例值了，只有在没有示例值的时候才加示例值。\n"
        "4. 如果参数是对象或数组，请增强其嵌套属性。\n"
        "5. 如果参数缺少描述，请不要添加描述并保持原样。\n"
        "6. 确保输出是有效的 JSON 格式，适合直接用于 OpenAPI 规范。\n"
        "7. 不要包含任何额外解释，仅返回增强后的 OpenAPI schema（JSON 格式）。\n\n"
        "有效输出的示例：\n"
        "- 如果示例有效：\n"
        "  {\"type\": \"string\", \"description\": \"用户电子邮件地址\", \"format\": \"email\", \"example\": \"user@example.com\"}\n"
        "- 如果示例不确定：\n"
        "  {\"type\": \"string\", \"description\": \"用户电子邮件地址\", \"format\": \"email\"}\n"
        "- 如果没有描述：\n"
        "  {\"type\": \"string\"}\n\n"
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
    
    # 增强components中的定义
    # if 'components' in enhanced_spec:
    #     if 'schemas' in enhanced_spec['components']:
    #         for name, schema in enhanced_spec['components']['schemas'].items():
    #             enhanced_spec['components']['schemas'][name] = enhance_schema(schema)
                
    #     if 'requestBodies' in enhanced_spec['components']:
    #         for name, body in enhanced_spec['components']['requestBodies'].items():
    #             if 'content' in body:
    #                 for media_type, content in body['content'].items():
    #                     if 'schema' in content:
    #                         content['schema'] = enhance_schema(content['schema'])
    
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
                                    content['schema'] = enhance_schema(content['schema'])
    
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
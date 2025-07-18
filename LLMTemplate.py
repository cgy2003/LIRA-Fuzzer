import copy, random
from LLMGlobalData import *
from LLMUtils import *
class ApiTemplate(object):
    def __init__(self, api_url, api_method, api_request, api_response):
        if api_url.startswith("/"):
            self.api_url = api_url
        else:
            self.api_url = "/" + api_url
        self.api_method = api_method
        if "__body__" in api_request["body"].keys():
            if type(api_request["body"]["__body__"]) == dict:
                api_request["body"] = api_request["body"]["__body__"]
        self.api_request = api_request
        if "headerResponse" not in api_response:
            api_response["headerResponse"] = {}
        self.api_response = api_response
        self.api_request_value = self.init_request_value()
        # print(api_method)
        if api_method == "Get":
            print(self.api_url, self.api_request_value)
        self.api_response_value = self.init_response_value()
    def init_request_value(self):
        def generate_random_value(param_type):
            return RandomValueDict[param_type][random.randint(0,43)]
            
        def get_param_format(param_name):
            for format_str in ApiParamFormat:
                if format_str in param_name:
                    return [ApiParamFormat[format_str][random.randint(0,43)], "LLM_FORMAT"]
            return []
        
        # 定义一个函数，用于将列表中的值转换为指定类型
        def value_type_conversion(value_list, type):
            # 创建一个空列表，用于存储转换后的值
            result_list = []
            # 判断要转换的类型
            if type == "Number":
                # 如果类型为Number，则将列表中的值转换为浮点数
                for value in value_list:
                    try:
                        result_list.append(float(value))
                    except:
                        # 如果转换失败，则跳过该值
                        continue
            elif type == "Int":
                # 如果类型为Int，则将列表中的值转换为整数
                for value in value_list:
                    try:
                        result_list.append(int(value))
                    except:
                        # 如果转换失败，则跳过该值
                        continue
            elif type == "Bool":
                # 如果类型为Bool，则将列表中的值转换为布尔值
                for value in value_list:
                    if value.lower() == 'true':
                        result_list.append(True)
                    elif value.lower() == 'false':
                        result_list.append(False)
                    else:
                        # 如果值既不是'true'也不是'false'，则跳过该值
                        continue
            else:
                # 如果类型不是Number、Int或Bool，则直接将列表中的值赋给result_list
                result_list = value_list
            return result_list
                
        def param_assignment(param_struct, param_name=""):
            # 获取参数类型
            # print(param_struct)
            param_type = param_struct[0]
            # 获取示例值列表
            example_value_list = param_struct[1]
            # 获取默认值列表
            default_value_list = param_struct[2]
            # ToDO: Support is_required
            # is_required = param_struct[3]
            # 初始化参数名值列表
            param_name_value = []
            # 如果有默认值列表
            if default_value_list:
                # 如果默认值列表的第一个元素不是"RESTler"
                if "RESTler" not in default_value_list[0]:
                    # 将默认值列表转换为参数类型
                    default_value_list = value_type_conversion(default_value_list, param_type)
                    # 将默认值列表的第一个元素和"LLM_SPECIFICATION"添加到参数名值列表中
                    param_name_value = [default_value_list[0], "LLM_SPECIFICATION"]
                    print("default request",param_name,param_name_value)
                else:
                    # 否则，将参数类型转换为随机值，并将"LLM_RANDOM"添加到参数名值列表中
                    param_name_value = [generate_random_value(param_type), "LLM_RANDOM"]
            # 如果有示例值列表
            if example_value_list:
                # example_value > default_value
                example_value_list = value_type_conversion(example_value_list, param_type)
                # print("example_value_list: ", example_value_list)
                param_name_value = [example_value_list[0], "LLM_SPECIFICATION"]
                print("example request",param_name,param_name_value)
            param_format_value = get_param_format(param_name)
            if param_format_value and param_name_value:
                if ParamValuePriority[param_format_value[1]] > ParamValuePriority[param_name_value[1]]:
                    param_name_value = param_format_value
            if param_name_value:
                return param_name_value
            else:
                return [generate_random_value(param_type, param_name), "LLM_RANDOM"]
        
        def traverse_and_assignment(param_dict, api_request_param_dict, param_name):
            # 获取param_dict中param_name对应的参数结构
            param_struct = param_dict[param_name]
            # print(param_struct,param_name)
            # 获取api_request_param_dict中param_name对应的参数结构
            api_request_param_struct = api_request_param_dict[param_name]
            # 如果参数结构是数组
            if param_struct[0] == "Array":
                # 遍历数组中的每个参数
                for array_param_index in range(1, len(param_struct)):
                    # 如果参数结构是字典
                    if type(param_struct[array_param_index]) == dict:
                        # 遍历字典中的每个参数
                        for array_param_name in param_struct[array_param_index]:
                            # 递归调用traverse_and_assignment函数
                            traverse_and_assignment(param_struct[array_param_index], api_request_param_struct[array_param_index], array_param_name)
                    # 如果参数结构是列表
                    elif type(param_struct[array_param_index]) == list:
                        # 调用param_assignment函数对参数进行赋值
                        param_struct[array_param_index] = param_assignment(param_struct[array_param_index],param_name)
                    # 如果参数结构是布尔值
                    elif type(param_struct[array_param_index]) == bool:
                        # ignore is_required
                        continue
                    else:
                        print("Not Supported param_struct in init_request_value: ", param_struct[array_param_index])
            # 如果参数结构是属性
            elif param_struct[0] == "Property":
                # 如果属性结构是列表
                if type(param_struct[1]) == list:
                    # fix api_resquest Struct
                    api_request_param_dict[param_name] = param_struct[1]
                    param_dict[param_name] = param_assignment(param_struct[1],param_name)
                # 如果属性结构是字典
                elif type(param_struct[1]) == dict:
                    # 遍历字典中的每个参数
                    for property_param_name in param_struct[1]:
                        # 递归调用traverse_and_assignment函数
                        traverse_and_assignment(param_struct[1], api_request_param_struct[1], property_param_name)
                else:
                    print("Not supported param_struct[1] in init_request_value: ", param_struct[1])
            else:
                # 调用param_assignment函数对参数进行赋值
                param_dict[param_name] = param_assignment(param_dict[param_name], param_name)
        api_request_value = copy.deepcopy(self.api_request)
        for api_request_part in api_request_value:
            if api_request_value[api_request_part]:
                if (len(api_request_value[api_request_part].keys()) == 1) and (type(api_request_value[api_request_part][list(api_request_value[api_request_part].keys())[0]]) == dict):
                    # Ignore meaningless first parameter names in OpenAPI V2 body parameters
                    api_request_value[api_request_part] = api_request_value[api_request_part][list(api_request_value[api_request_part].keys())[0]]
                    self.api_request[api_request_part] = self.api_request[api_request_part][list(self.api_request[api_request_part].keys())[0]]
                for param_name in api_request_value[api_request_part]:
                    traverse_and_assignment(api_request_value[api_request_part], self.api_request[api_request_part], param_name)    
        return api_request_value
    
    def init_response_value(self):
        def value_type_conversion(value_list, type):
            result_list = []
            if type == "Number":
                for value in value_list:
                    try:
                        result_list.append(float(value))
                    except:
                        continue
            elif type == "Int":
                for value in value_list:
                    try:
                        result_list.append(int(value))
                    except:
                        continue
            elif type == "Bool":
                for value in value_list:
                    if value.lower() == 'true':
                        result_list.append(True)
                    elif value.lower() == 'false':
                        result_list.append(False)
                    else:
                        continue
            else:
                result_list = value_list
            return result_list
        def param_assignment(param_struct):
            print(param_struct)
            param_type = param_struct[0]
            example_value_list = param_struct[1]
            default_value_list = param_struct[2]
            # is_required = param_struct[3]
            param_name_value = []
            # response_value only support LLM_SPECIFICATION, if not, response_value = []
            if default_value_list:
                if "RESTler" not in default_value_list[0]:
                    default_value_list = value_type_conversion(default_value_list, param_type)
                    param_name_value = [default_value_list[0], "LLM_SPECIFICATION"]
                    print("default response_value: ",param_name,param_name_value)
            if example_value_list:
                # example_value > default_value
                example_value_list = value_type_conversion(example_value_list, param_type)
                param_name_value = [example_value_list[0], "LLM_SPECIFICATION"]
                print("example response_value: ",param_name,param_name_value)
            return param_name_value
        
        def traverse_and_assignment(param_dict, api_response_param_dict, param_name):
            #print("param_dict: ", param_dict, param_name)
            param_struct = param_dict[param_name]
            api_response_param_struct = api_response_param_dict[param_name]
            #print("param_struct: ", param_struct)
            if param_struct[0] == "Array":
                for array_param_index in range(1, len(param_struct)):
                    if type(param_struct[array_param_index]) == dict:
                        for array_param_name in param_struct[array_param_index]:
                            traverse_and_assignment(param_struct[array_param_index], api_response_param_struct[array_param_index], array_param_name)
                    elif type(param_struct[array_param_index]) == list:
                        param_struct[array_param_index] = param_assignment(param_struct[array_param_index])
                    elif type(param_struct[array_param_index]) == bool:
                        # ignore is_required
                        continue
                    else:
                        print("Not Supported param_struct in init_response_value: ", param_struct[array_param_index])
            elif param_struct[0] == "Property":
                if type(param_struct[1]) == list:
                    # fix api_response Struct
                    api_response_param_dict[param_name] = param_struct[1]
                    param_dict[param_name] = param_assignment(param_struct[1])
                elif type(param_struct[1]) == dict:
                    for property_param_name in param_struct[1]:
                        traverse_and_assignment(param_struct[1], api_response_param_struct[1], property_param_name)
                else:
                    print("Not supported param_struct[1] in init_response_value: ", param_struct[1])
            else:
                param_dict[param_name] = param_assignment(param_dict[param_name])
                
        api_response_value = copy.deepcopy(self.api_response)
        for api_response_part in api_response_value:
            if api_response_value[api_response_part]:
                for param_name in api_response_value[api_response_part]:
                    traverse_and_assignment(api_response_value[api_response_part], self.api_response[api_response_part], param_name)
        return api_response_value

    def show(self):
        print("api_url: ", self.api_url)
        print("api_method: ", self.api_method)
        print("api_request: ", self.api_request)
        print("api_response: ", self.api_response)
        print("api_request_value: ", self.api_request_value)
        print("api_response_value: ", self.api_response_value)

    def show_txt(self):
        show_str = "api_url: " + self.api_url + "\n"
        show_str += "api_method: " + self.api_method + "\n"
        show_str += "api_request: " + str(self.api_request) + "\n"
        show_str += "api_response: " + str(self.api_response) + "\n"
        show_str += "api_request_value: " + str(self.api_request_value) + "\n"
        show_str += "api_response_value: "+ str(self.api_response_value) + "\n"
        show_str += "##################" + "\n"
        f = open("api_template.txt","a+")
        f.write(show_str)
        f.close()


# Example:
#     api_url = "/teams/{teamId}/memberships"
#     api_method = "Post"
#     api_request = {
#         "path": {
#             "teamId": ["String", [], ["RESTlerString"], False],
#         },
#         "header": {},
#         "query": {},
#         "body": {
#             "email": ["String", [], ["RESTlerString"], False],
#             "name": ["String", [], ["RESTlerString"], False],
#             "roles": ["Array",
#                 ["Int", [], ["0"], False],
#                 {
#                     "role1": ["String", ["my_role"], [], False],
#                     "role2": ["Array", {
#                         "role2-1": ["String", ["my_role2-1"], [], False]
#                     }, False]
#                 },
#                 ["String", [], ["RESTlerString"], False],
#                 False
#             ],
#             "url": ["String", [], ["RESTlerString"], False]
#         }
#     }
#     api_response = {
#         "bodyResponse": {
#             "$id": ["String", [], ["RESTlerString"], False],
#             "invited": ["Int", [], ["0"], False],
#             "name": ["String", [], ["RESTlerString"], False],
#             "teamId": ["String", [], ["RESTlerString"], False]
#         },
#         "headerResponse": {}
#     }
# -*- coding: UTF-8 -*-
import os, sys, json, argparse, subprocess

def replace_compiler_fs(LLM_compiler_dir, restler_compile_file_path):
    compiler_fs = LLM_compiler_dir + os.path.sep + "Restler.Compiler" + os.path.sep + "Compiler.fs"
    with open(compiler_fs, "r", encoding="utf-8") as f:
        compiler_fs_content = f.read()
    compiler_fs_replace_lindex = compiler_fs_content.find("// LLM Parser")
    compiler_fs_replace_rindex = compiler_fs_content.find("// LLM Parser End")
    compiler_fs_replace_temp = compiler_fs_content[compiler_fs_replace_lindex:compiler_fs_replace_rindex]
    compiler_fs_replace_rindex = compiler_fs_replace_lindex + compiler_fs_replace_temp.find("\", infoStr)")
    compiler_fs_replace_lindex += compiler_fs_replace_temp.find("File.AppendAllText(") + len("File.AppendAllText(\"")
    compiler_fs_new_content = compiler_fs_content[:compiler_fs_replace_lindex] + restler_compile_file_path + compiler_fs_content[compiler_fs_replace_rindex:]
    with open(compiler_fs, 'w', encoding='utf-8') as f:
        f.write(compiler_fs_new_content)

def set_global_json():
    # get dotnet version
    dotnet_version = None
    p = subprocess.Popen(["dotnet", "--list-sdks"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    if out:
        out = out.decode()
        for version_line in out.split("\n"):
            if "6.0." in version_line:
                dotnet_version = version_line[:version_line.find(" [")]
            if dotnet_version:
                break
    if not dotnet_version:
        print("Please Install .NET 6.0 First!")
        exit(0)
    global_json = {"sdk": {"version": dotnet_version}}
    with open("global.json", "w") as f:
        json.dump(global_json, f, indent=2)

def publish_restler_bin(LLM_compiler_dir, LLM_compiler_output_dir):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    if not os.path.exists("global.json"):
        set_global_json()
    fsproj = LLM_compiler_dir + os.path.sep + "Restler.CompilerExe" + os.path.sep + "Restler.CompilerExe.fsproj"
    #subprocess.run(["dotnet", "publish", fsproj, "--no-restore", "-o", LLM_compiler_output_dir, "-c", "release", "-f", "net6.0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 恢复依赖项
    # print("Restoring dependencies...")
    # restore_result = subprocess.run(
    #         ["dotnet", "restore", fsproj],
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         text=True
    #     )

    #     # 检查依赖项恢复结果
    # if restore_result.returncode != 0:
    #         print("Dependency restore failed!")
    #         print(restore_result.stderr)
    #         return  # 提前退出

    # print("Dependency restore succeeded!")
    result=subprocess.run(["dotnet", "publish", fsproj, "--no-restore", "-o", LLM_compiler_output_dir, "-c", "release", "-f", "net6.0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout)  # 输出标准输出
    print(result.stderr)  # 输出错误输出
def compile_api_spec(api_spec, LLM_compiler_output_dir):
    # set config.json
    config_json = {
        "SwaggerSpecFilePath": [api_spec],
        "GrammarOutputDirectoryPath": LLM_compiler_output_dir + os.path.sep + "Compile",
        "IncludeOptionalParameters": True,
        "UseHeaderExamples": False,
        "UsePathExamples": False,
        "UseQueryExamples": True,
        "UseBodyExamples": True,
        "UseAllExamplePayloads": True,
        "DiscoverExamples": False,
        "ExamplesDirectory": "",
        "DataFuzzing": True,
        "ReadOnlyFuzz": False,
        "ResolveQueryDependencies": True,
        "ResolveBodyDependencies": True,
        "ResolveHeaderDependencies": True,
        "UseRefreshableToken": True,
        "AllowGetProducers": True,
        "TrackFuzzedParameterNames": False
    }
    config_json_file = os.path.abspath('.') + os.path.sep + "config.json"
    with open(config_json_file, "w") as f:
        json.dump(config_json, f, indent=2)
    # parse api_spec to api_info
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    if not os.path.exists("global.json"):
        set_global_json()
    restler_dll = LLM_compiler_output_dir + os.path.sep + "Restler.CompilerExe.dll"
    subprocess.run(["dotnet", restler_dll, config_json_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--openapi', help='OpenAPI Specification File Path', type=str, default=None, required=True)
    parser.add_argument('--LLM_compiler_dir', help='LLMCompiler SourceCode Dir', type=str, default="./LLMCompiler", required=False)
    parser.add_argument('--LLM_compiler_output_dir', help='LLMCompiler Bin Dir', type=str, default="./LLMCompilerBin", required=False)
    parser.add_argument('--restler_compile_file_path', help='Restler Compile File Path', type=str, default="./APIInfo.txt", required=False)
    parser.add_argument('--recompile', action="store_true", help='Whether Need Recompile LLMCompiler, Default: False')
    args = parser.parse_args()
    if args.LLM_compiler_dir == "./LLMCompiler":
        LLM_compiler_dir = os.path.abspath('.') + os.path.sep + "LLMCompiler"
    else:
        LLM_compiler_dir = args.LLM_compiler_dir
    if args.LLM_compiler_output_dir == "./LLMCompilerBin":
        LLM_compiler_output_dir = os.path.abspath('.') + os.path.sep + "LLMCompilerBin"
    else:
        LLM_compiler_output_dir = args.LLM_compiler_output_dir
    if args.restler_compile_file_path == "./APIInfo.txt":
        restler_compile_file_path = os.path.abspath('.') + os.path.sep + "APIInfo.txt"
    else:
        restler_compile_file_path = os.path.normpath(os.path.abspath(args.restler_compile_file_path))
    if sys.platform.startswith("win"):
        restler_compile_file_path = restler_compile_file_path.replace("\\", "\\\\")
    if args.recompile:
        replace_compiler_fs(LLM_compiler_dir, restler_compile_file_path)
        publish_restler_bin(LLM_compiler_dir, LLM_compiler_output_dir)
    if os.path.exists(restler_compile_file_path):
        os.remove(restler_compile_file_path)
    
    compile_api_spec(args.openapi, LLM_compiler_output_dir)
    
if __name__ == "__main__":
    main()
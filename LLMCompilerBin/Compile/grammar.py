""" THIS IS AN AUTOMATICALLY GENERATED FILE!"""
from __future__ import print_function
import json
from engine import primitives
from engine.core import requests
from engine.errors import ResponseParsingException
from engine import dependencies

_ph_api_requests_get_0_correlationId = dependencies.DynamicVariable("_ph_api_requests_get_0_correlationId")

_ph_api_scenarios_get_0_scenario = dependencies.DynamicVariable("_ph_api_scenarios_get_0_scenario")

_ph_api_stubs_post_stub_id = dependencies.DynamicVariable("_ph_api_stubs_post_stub_id")

def parse_phapirequestsget(data, **kwargs):
    """ Automatically generated response parser """
    # Declare response variables
    temp_7262 = None

    if 'headers' in kwargs:
        headers = kwargs['headers']


    # Parse body if needed
    if data:

        try:
            data = json.loads(data)
        except Exception as error:
            raise ResponseParsingException("Exception parsing response, data was not valid json: {}".format(error))
        pass

    # Try to extract each dynamic object

        try:
            temp_7262 = str(data[0]["correlationId"])
            
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass



    # If no dynamic objects were extracted, throw.
    if not (temp_7262):
        raise ResponseParsingException("Error: all of the expected dynamic objects were not present in the response.")

    # Set dynamic variables
    if temp_7262:
        dependencies.set_variable("_ph_api_requests_get_0_correlationId", temp_7262)


def parse_phapiscenariosget(data, **kwargs):
    """ Automatically generated response parser """
    # Declare response variables
    temp_8173 = None

    if 'headers' in kwargs:
        headers = kwargs['headers']


    # Parse body if needed
    if data:

        try:
            data = json.loads(data)
        except Exception as error:
            raise ResponseParsingException("Exception parsing response, data was not valid json: {}".format(error))
        pass

    # Try to extract each dynamic object

        try:
            temp_8173 = str(data[0]["scenario"])
            
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass



    # If no dynamic objects were extracted, throw.
    if not (temp_8173):
        raise ResponseParsingException("Error: all of the expected dynamic objects were not present in the response.")

    # Set dynamic variables
    if temp_8173:
        dependencies.set_variable("_ph_api_scenarios_get_0_scenario", temp_8173)


def parse_phapistubspost(data, **kwargs):
    """ Automatically generated response parser """
    # Declare response variables
    temp_7680 = None

    if 'headers' in kwargs:
        headers = kwargs['headers']


    # Parse body if needed
    if data:

        try:
            data = json.loads(data)
        except Exception as error:
            raise ResponseParsingException("Exception parsing response, data was not valid json: {}".format(error))
        pass

    # Try to extract each dynamic object

        try:
            temp_7680 = str(data["stub"]["id"])
            
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass



    # If no dynamic objects were extracted, throw.
    if not (temp_7680):
        raise ResponseParsingException("Error: all of the expected dynamic objects were not present in the response.")

    # Set dynamic variables
    if temp_7680:
        dependencies.set_variable("_ph_api_stubs_post_stub_id", temp_7680)

req_collection = requests.RequestCollection([])
# Endpoint: /ph-api/configuration, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("configuration"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/configuration"
)
req_collection.add_request(request)

# Endpoint: /ph-api/configuration, method: Patch
request = requests.Request([
    primitives.restler_static_string("PATCH "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("configuration"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "configurationKey":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
    "newValue":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/configuration"
)
req_collection.add_request(request)

# Endpoint: /ph-api/export/requests/{requestId}, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("export"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("requests"),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_uuid4("RESTlerUuid", quoted=False, examples=["550e8400-e29b-41d4-a716-446655440000"]),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("type="),
    primitives.restler_fuzzable_group("type", ['NotSet','Curl','Hurl','Har']  ,quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/export/requests/{requestId}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/import/curl, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("import"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("curl"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("doNotCreateStub="),
    primitives.restler_fuzzable_bool("RESTlerBool", examples=["false"]),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("tenant="),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["finance"]),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("stubIdPrefix="),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["prefix_"]),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/import/curl"
)
req_collection.add_request(request)

# Endpoint: /ph-api/import/har, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("import"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("har"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("doNotCreateStub="),
    primitives.restler_fuzzable_bool("RESTlerBool", examples=["false"]),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("tenant="),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["finance"]),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("stubIdPrefix="),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["prefix_"]),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/import/har"
)
req_collection.add_request(request)

# Endpoint: /ph-api/import/openapi, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("import"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("openapi"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("doNotCreateStub="),
    primitives.restler_fuzzable_bool("RESTlerBool", examples=["false"]),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("tenant="),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["finance"]),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("stubIdPrefix="),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["prefix_"]),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/import/openapi"
)
req_collection.add_request(request)

# Endpoint: /ph-api/metadata, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("metadata"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/metadata"
)
req_collection.add_request(request)

# Endpoint: /ph-api/metadata/features/{featureFlag}, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("metadata"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("features"),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_group("featureFlag", ['Authentication']  ,quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/metadata/features/{featureFlag}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/requests, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("requests"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("x-from-identifier: "),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["12345"]),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("x-items-per-page: "),
    primitives.restler_fuzzable_int("RESTlerInt", examples=["10"]),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    
    {

        'post_send':
        {
            'parser': parse_phapirequestsget,
            'dependencies':
            [
                _ph_api_requests_get_0_correlationId.writer()
            ]
        }

    },

],
requestId="/ph-api/requests"
)
req_collection.add_request(request)

# Endpoint: /ph-api/requests, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("requests"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/requests"
)
req_collection.add_request(request)

# Endpoint: /ph-api/requests/overview, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("requests"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("overview"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("x-from-identifier: "),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["12345"]),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("x-items-per-page: "),
    primitives.restler_fuzzable_int("RESTlerInt", examples=["10"]),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/requests/overview"
)
req_collection.add_request(request)

# Endpoint: /ph-api/requests/{correlationId}, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("requests"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_requests_get_0_correlationId.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/requests/{correlationId}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/requests/{correlationId}, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("requests"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_requests_get_0_correlationId.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/requests/{correlationId}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/requests/{correlationId}/response, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("requests"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_requests_get_0_correlationId.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("response"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/requests/{correlationId}/response"
)
req_collection.add_request(request)

# Endpoint: /ph-api/requests/{correlationId}/stubs, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("requests"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_requests_get_0_correlationId.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "doNotCreateStub":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/requests/{correlationId}/stubs"
)
req_collection.add_request(request)

# Endpoint: /ph-api/scenarios, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("scenarios"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    
    {

        'post_send':
        {
            'parser': parse_phapiscenariosget,
            'dependencies':
            [
                _ph_api_scenarios_get_0_scenario.writer()
            ]
        }

    },

],
requestId="/ph-api/scenarios"
)
req_collection.add_request(request)

# Endpoint: /ph-api/scenarios, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("scenarios"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/scenarios"
)
req_collection.add_request(request)

# Endpoint: /ph-api/scenarios/{scenario}, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("scenarios"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_scenarios_get_0_scenario.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/scenarios/{scenario}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/scenarios/{scenario}, method: Put
request = requests.Request([
    primitives.restler_static_string("PUT "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("scenarios"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_scenarios_get_0_scenario.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "state":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
    "hitCount":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/scenarios/{scenario}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/scenarios/{scenario}, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("scenarios"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_scenarios_get_0_scenario.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/scenarios/{scenario}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/scheduledJob/{jobName}, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("scheduledJob"),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["backup_job"]),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/scheduledJob/{jobName}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/scheduledJob, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("scheduledJob"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/scheduledJob"
)
req_collection.add_request(request)

# Endpoint: /ph-api/stubs, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "id":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
    "conditions":
        {
            "method":
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ,
            "url":
                {
                    "path":
                        """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                    ,
                    "query":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string(""",
                    "fullPath":
                        """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                    ,
                    "isHttps":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                }
            ,
            "body":
            [
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ],
            "form":
            [
                {
                    "key":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "value":
                        """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                }
            ],
            "headers":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string(""",
            "xpath":
            [
                {
                    "queryString":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "namespaces":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                }
            ],
            "jsonPath":
            [
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ],
            "basicAuthentication":
                {
                    "username":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "password":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("""
                }
            ,
            "clientIp":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "host":
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ,
            "json":
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ,
            "scenario":
                {
                    "minHits":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "maxHits":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "exactHits":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "scenarioState":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("""
                }
        }
    ,
    "response":
        {
            "enableDynamicMode":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
            "statusCode":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
            "contentType":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "text":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "base64":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "file":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "textFile":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "headers":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string(""",
            "extraDuration":
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ,
            "json":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "xml":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "html":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "temporaryRedirect":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "permanentRedirect":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "movedPermanently":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "reverseProxy":
                {
                    "url":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "appendQueryString":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                    "appendPath":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                    "replaceRootUrl":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                }
            ,
            "lineEndings":
                """),
    primitives.restler_fuzzable_group("", ['NotSet','Windows','Unix']  ,quoted=True),
    primitives.restler_static_string("""
            ,
            "image":
                {
                    "type":
                        """),
    primitives.restler_fuzzable_group("", ['NotSet','Jpeg','Bmp','Png','Gif']  ,quoted=True),
    primitives.restler_static_string("""
                    ,
                    "width":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "height":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "backgroundColor":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "text":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "fontSize":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "fontColor":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "jpegQuality":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "wordWrap":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                }
            ,
            "scenario":
                {
                    "setScenarioState":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "clearState":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                }
            ,
            "abortConnection":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
            "replace":
            [
                {
                    "text":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "ignoreCase":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                    "regex":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "jsonPath":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "replaceWith":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("""
                }
            ]
        }
    ,
    "priority":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
    "enabled":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),
    
    {

        'post_send':
        {
            'parser': parse_phapistubspost,
            'dependencies':
            [
                _ph_api_stubs_post_stub_id.writer()
            ]
        }

    },

],
requestId="/ph-api/stubs"
)
req_collection.add_request(request)

# Endpoint: /ph-api/stubs, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/stubs"
)
req_collection.add_request(request)

# Endpoint: /ph-api/stubs, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/stubs"
)
req_collection.add_request(request)

# Endpoint: /ph-api/stubs/{stubId}, method: Put
request = requests.Request([
    primitives.restler_static_string("PUT "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_stubs_post_stub_id.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "id":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
    "conditions":
        {
            "method":
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ,
            "url":
                {
                    "path":
                        """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                    ,
                    "query":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string(""",
                    "fullPath":
                        """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                    ,
                    "isHttps":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                }
            ,
            "body":
            [
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ],
            "form":
            [
                {
                    "key":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "value":
                        """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                }
            ],
            "headers":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string(""",
            "xpath":
            [
                {
                    "queryString":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "namespaces":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                }
            ],
            "jsonPath":
            [
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ],
            "basicAuthentication":
                {
                    "username":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "password":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("""
                }
            ,
            "clientIp":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "host":
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ,
            "json":
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ,
            "scenario":
                {
                    "minHits":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "maxHits":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "exactHits":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "scenarioState":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("""
                }
        }
    ,
    "response":
        {
            "enableDynamicMode":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
            "statusCode":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
            "contentType":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "text":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "base64":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "file":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "textFile":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "headers":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string(""",
            "extraDuration":
                """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
            ,
            "json":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "xml":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "html":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "temporaryRedirect":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "permanentRedirect":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "movedPermanently":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
            "reverseProxy":
                {
                    "url":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "appendQueryString":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                    "appendPath":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                    "replaceRootUrl":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                }
            ,
            "lineEndings":
                """),
    primitives.restler_fuzzable_group("", ['NotSet','Windows','Unix']  ,quoted=True),
    primitives.restler_static_string("""
            ,
            "image":
                {
                    "type":
                        """),
    primitives.restler_fuzzable_group("", ['NotSet','Jpeg','Bmp','Png','Gif']  ,quoted=True),
    primitives.restler_static_string("""
                    ,
                    "width":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "height":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "backgroundColor":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "text":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "fontSize":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "fontColor":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "jpegQuality":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                    "wordWrap":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                }
            ,
            "scenario":
                {
                    "setScenarioState":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "clearState":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                }
            ,
            "abortConnection":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
            "replace":
            [
                {
                    "text":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "ignoreCase":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                    "regex":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "jsonPath":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                    "replaceWith":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("""
                }
            ]
        }
    ,
    "priority":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
    "enabled":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/stubs/{stubId}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/stubs/{stubId}, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_stubs_post_stub_id.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/stubs/{stubId}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/stubs/{stubId}, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_stubs_post_stub_id.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/stubs/{stubId}"
)
req_collection.add_request(request)

# Endpoint: /ph-api/stubs/overview, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("overview"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/stubs/overview"
)
req_collection.add_request(request)

# Endpoint: /ph-api/stubs/{stubId}/requests, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_ph_api_stubs_post_stub_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("requests"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/stubs/{stubId}/requests"
)
req_collection.add_request(request)

# Endpoint: /ph-api/tenants, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("tenants"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/tenants"
)
req_collection.add_request(request)

# Endpoint: /ph-api/tenants/{tenant}/stubs, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("tenants"),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["acme"]),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/tenants/{tenant}/stubs"
)
req_collection.add_request(request)

# Endpoint: /ph-api/tenants/{tenant}/stubs, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("tenants"),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["acme"]),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/tenants/{tenant}/stubs"
)
req_collection.add_request(request)

# Endpoint: /ph-api/tenants/{tenant}/stubs, method: Put
request = requests.Request([
    primitives.restler_static_string("PUT "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("tenants"),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["acme"]),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("stubs"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("["),
    primitives.restler_static_string("""
    {
        "id":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
        "conditions":
            {
                "method":
                    """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                ,
                "url":
                    {
                        "path":
                            """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                        ,
                        "query":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string(""",
                        "fullPath":
                            """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                        ,
                        "isHttps":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                    }
                ,
                "body":
                [
                    """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                ],
                "form":
                [
                    {
                        "key":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "value":
                            """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                    }
                ],
                "headers":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string(""",
                "xpath":
                [
                    {
                        "queryString":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "namespaces":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                    }
                ],
                "jsonPath":
                [
                    """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                ],
                "basicAuthentication":
                    {
                        "username":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "password":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("""
                    }
                ,
                "clientIp":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "host":
                    """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                ,
                "json":
                    """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                ,
                "scenario":
                    {
                        "minHits":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                        "maxHits":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                        "exactHits":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                        "scenarioState":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("""
                    }
            }
        ,
        "response":
            {
                "enableDynamicMode":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                "statusCode":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                "contentType":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "text":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "base64":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "file":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "textFile":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "headers":"""),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string(""",
                "extraDuration":
                    """),
    primitives.restler_fuzzable_object("RESTlerObject"),
    primitives.restler_static_string("""
                ,
                "json":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "xml":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "html":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "temporaryRedirect":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "permanentRedirect":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "movedPermanently":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                "reverseProxy":
                    {
                        "url":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "appendQueryString":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                        "appendPath":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                        "replaceRootUrl":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                    }
                ,
                "lineEndings":
                    """),
    primitives.restler_fuzzable_group("", ['NotSet','Windows','Unix']  ,quoted=True),
    primitives.restler_static_string("""
                ,
                "image":
                    {
                        "type":
                            """),
    primitives.restler_fuzzable_group("", ['NotSet','Jpeg','Bmp','Png','Gif']  ,quoted=True),
    primitives.restler_static_string("""
                        ,
                        "width":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                        "height":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                        "backgroundColor":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "text":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "fontSize":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                        "fontColor":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "jpegQuality":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
                        "wordWrap":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                    }
                ,
                "scenario":
                    {
                        "setScenarioState":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "clearState":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
                    }
                ,
                "abortConnection":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                "replace":
                [
                    {
                        "text":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "ignoreCase":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string(""",
                        "regex":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "jsonPath":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string(""",
                        "replaceWith":"""),
    primitives.restler_fuzzable_string("RESTlerString", quoted=True),
    primitives.restler_static_string("""
                    }
                ]
            }
        ,
        "priority":"""),
    primitives.restler_fuzzable_int("RESTlerInt"),
    primitives.restler_static_string(""",
        "enabled":"""),
    primitives.restler_fuzzable_bool("RESTlerBool"),
    primitives.restler_static_string("""
    }]"""),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/tenants/{tenant}/stubs"
)
req_collection.add_request(request)

# Endpoint: /ph-api/users/{username}, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_basepath(""),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ph-api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("users"),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_string("RESTlerString", quoted=False, examples=["john_doe"]),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: localhost\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/ph-api/users/{username}"
)
req_collection.add_request(request)

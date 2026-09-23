from time import sleep
from dab_tester import YesNoQuestion, Default_Validations
import jsons
import json
from schema import dab_response_validator

class ContentEntries:
    # Entries returned by the last content/search or content/recommendations,
    # so content/open can use an entryId that exists on the device.
    entries = []

def open_body():
    """Build a content/open body from an entry the device returned."""
    if not ContentEntries.entries:
        raise RuntimeError("No content entry available; content/search or content/recommendations must return entries first")
    return json.dumps({"entryId": ContentEntries.entries[0]["entryId"]})

def open(test_result, durationInMs=0,expectedLatencyMs=0):
    try:
        dab_response_validator.validate_content_open_response_schema(test_result.response)
    except Exception as error:
        print("Schema error:", error)
        return False
    response  = jsons.loads(test_result.response)
    if response['status'] != 200:
        return False
    sleep(0.1)
    return Default_Validations(test_result, durationInMs, expectedLatencyMs)

def search(test_result, durationInMs=0,expectedLatencyMs=0):
    try:
        dab_response_validator.validate_content_search_response_schema(test_result.response)
    except Exception as error:
        print("Schema error:", error)
        return False
    response = jsons.loads(test_result.response)
    if response['status'] != 200:
        return False
    if response['entries']:
        ContentEntries.entries = response['entries']
    sleep(0.1)
    return Default_Validations(test_result, durationInMs, expectedLatencyMs)

def recommendations(test_result, durationInMs=0,expectedLatencyMs=0):
    try:
        dab_response_validator.validate_content_recommendations_response_schema(test_result.response)
    except Exception as error:
        print("Schema error:", error)
        return False
    response  = jsons.loads(test_result.response)
    if response['status'] != 200:
        return False
    if response['entries']:
        ContentEntries.entries = response['entries']
    sleep(0.1)
    return Default_Validations(test_result, durationInMs, expectedLatencyMs)

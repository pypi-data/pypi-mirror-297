from typing import Optional, List, Any, Dict
import base64

# string

def get_encoded_string(plain_string:str) -> str:
    plain_string_bytes = plain_string.encode("ascii")
    base64_bytes = base64.b64encode(plain_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def get_decoded_string(base64_string:str) -> str:
    base64_bytes = base64_string.encode("ascii")
    plain_string_bytes = base64.b64decode(base64_bytes)
    plain_string = plain_string_bytes.decode("ascii")
    return plain_string

# list

def remove_duplicate_dicts(target_list:list, remove_from:list, keys:List[str]):
    for item in remove_from:
        for i in range(len(target_list)):
            real_i = len(target_list) - i - 1
            true_count = 0
            for key in keys:
                if key in item and key in target_list[real_i]:
                    if target_list[real_i][key] == item[key]:
                        true_count += 1
            if true_count == len(keys):
                del target_list[real_i]
    return target_list


def remove_empty_dicts(target_list:list, keys:list):
    for i in range(len(target_list)):
        real_i = len(target_list) - i - 1
        true_count = 0
        for key in keys:
            if key in target_list[real_i] and target_list[real_i][key] == '':
                true_count += 1
        if true_count == len(keys):
            del target_list[real_i]
    return target_list

def filter_keys(target_list:list, keys:list):
    results = []
    for target in target_list:
        result = {}
        for key in keys:
            if key in target:
                result[key] = target[key]
        if result:
            results.append(result)
    return results

def rename_keys(target_list:list, to_keys:list, from_keys:list):
    results = []
    for target in target_list:
        result = {}
        for from_key, to_key in zip(from_keys, to_keys):
            if from_key in target:
                result[to_key] = target[from_key]
        if result:
            results.append(result)
    return results

def sanitize_none_to_empty_string(target_list:list):
    for target in target_list:
        for key in target:
            if target[key] is None:
                target[key] = ''
    return target_list

def sanitize_int_to_string(target_list:list):
    for target in target_list:
        for key in target:
            if type(target[key]) == int:
                target[key] = str(target[key])
    return target_list

def combine_lists(list1:list, list2:list):
    return list(set(list1 + list2))

def remove_dicts_substring(target_list:List[Any], key:str,
        list_of_strings:List[str]) -> List[Any]:
    """
    Remove list of dicts based on the selected key and list of strings that is a substring of
        values
    Note: Case insensitive
    Empty string '' in list of strings will be ignored
    """
    return [d for d in target_list if not any(s.lower() in d[key].lower()
        for s in list_of_strings if s != '')]
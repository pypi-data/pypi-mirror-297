"""
    This file mainly contains three functions

    Functions without multi-threading capability：
    1. predict: Used in normal conversation，Fully interactive，Not multi-threaded

    Functions with multi-threading capability
    2. predict_no_ui_long_connection：Support multi-threading
"""

import json
import os
import re
import time
import traceback
import requests
import random

from loguru import logger

# Put your own secrets such as API and proxy address in config_private.py
# When reading, first check if there is a private config_private configuration file（Not controlled by git），If there is，Then overwrite the original config file
from void_terminal.toolbox import get_conf, update_ui, is_any_api_key, select_api_key, what_keys, clip_history
from void_terminal.toolbox import trimmed_format_exc, is_the_upload_folder, read_one_api_model_name, log_chat
from void_terminal.toolbox import ChatBotWithCookies, have_any_recent_upload_image_files, encode_image
proxies, TIMEOUT_SECONDS, MAX_RETRY, API_ORG, AZURE_CFG_ARRAY = \
    get_conf('proxies', 'TIMEOUT_SECONDS', 'MAX_RETRY', 'API_ORG', 'AZURE_CFG_ARRAY')

timeout_bot_msg = '[Local Message] Request timeout. Network error. Please check proxy settings in config.py.' + \
                  'Network error，Check if the proxy server is available，And if the format of the proxy settings is correct，The format must be[Protocol]://[Address]:[Port]，All parts are necessary。'

def get_full_error(chunk, stream_response):
    """
        Get the complete error message returned from OpenAI
    """
    while True:
        try:
            chunk += next(stream_response)
        except:
            break
    return chunk

def make_multimodal_input(inputs, image_paths):
    image_base64_array = []
    for image_path in image_paths:
        path = os.path.abspath(image_path)
        base64 = encode_image(path)
        inputs = inputs + f'<br/><br/><div align="center"><img src="file={path}" base64="{base64}"></div>'
        image_base64_array.append(base64)
    return inputs, image_base64_array

def reverse_base64_from_input(inputs):
    # Define a regular expression to match Base64 strings（假设Format为 base64="<Base64 encoding>"）
    # pattern = re.compile(r'base64="([^"]+)"></div>')
    pattern = re.compile(r'<br/><br/><div align="center"><img[^<>]+base64="([^"]+)"></div>')
    # Use findall method to find all matching Base64 strings
    base64_strings = pattern.findall(inputs)
    # Return a list of Base64 strings reversed
    return base64_strings

def contain_base64(inputs):
    base64_strings = reverse_base64_from_input(inputs)
    return len(base64_strings) > 0

def append_image_if_contain_base64(inputs):
    if not contain_base64(inputs):
        return inputs
    else:
        image_base64_array = reverse_base64_from_input(inputs)
        pattern = re.compile(r'<br/><br/><div align="center"><img[^><]+></div>')
        inputs = re.sub(pattern, '', inputs)
        res = []
        res.append({
            "type": "text",
            "text": inputs
        })
        for image_base64 in image_base64_array:
            res.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            })
        return res

def remove_image_if_contain_base64(inputs):
    if not contain_base64(inputs):
        return inputs
    else:
        pattern = re.compile(r'<br/><br/><div align="center"><img[^><]+></div>')
        inputs = re.sub(pattern, '', inputs)
        return inputs

def decode_chunk(chunk):
    # Read some information in advance （Used to judge exceptions）
    chunk_decoded = chunk.decode()
    chunkjson = None
    has_choices = False
    choice_valid = False
    has_content = False
    has_role = False
    try:
        chunkjson = json.loads(chunk_decoded[6:])
        has_choices = 'choices' in chunkjson
        if has_choices: choice_valid = (len(chunkjson['choices']) > 0)
        if has_choices and choice_valid: has_content = ("content" in chunkjson['choices'][0]["delta"])
        if has_content: has_content = (chunkjson['choices'][0]["delta"]["content"] is not None)
        if has_choices and choice_valid: has_role = "role" in chunkjson['choices'][0]["delta"]
    except:
        pass
    return chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role

from functools import lru_cache
@lru_cache(maxsize=32)
def verify_endpoint(endpoint):
    """
        Check if the endpoint is available
    """
    if "The API name you wrote yourself" in endpoint:
        raise ValueError("Endpoint is incorrect, Please check the configuration of AZURE_ENDPOINT! The current Endpoint is:" + endpoint)
    return endpoint

def predict_no_ui_long_connection(inputs:str, llm_kwargs:dict, history:list=[], sys_prompt:str="", observe_window:list=None, console_slience:bool=False):
    """
    Send to chatGPT，Waiting for reply，Completed in one go，Do not display intermediate processes。But internally use the stream method to avoid the network being cut off midway。
    inputs：
        This is the input of this inquiry
    sys_prompt:
        System silent prompt
    llm_kwargs：
        Internal tuning parameters of chatGPT
    history：
        history is the list of previous conversations
    observe_window = None：
        Used to transfer the already output part across threads，Most of the time it`s just for fancy visual effects，Leave it blank。observe_window[0]：Observation window。observe_window[1]：Watchdog
    """
    from void_terminal.request_llms.bridge_all import model_info

    watch_dog_patience = 5 # The patience of the watchdog, Set 5 seconds

    if model_info[llm_kwargs['llm_model']].get('openai_disable_stream', False): stream = False
    else: stream = True

    headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt=sys_prompt, stream=stream)
    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=False
            endpoint = verify_endpoint(model_info[llm_kwargs['llm_model']]['endpoint'])
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                    json=payload, stream=stream, timeout=TIMEOUT_SECONDS); break
        except requests.exceptions.ReadTimeout as e:
            retry += 1
            traceback.print_exc()
            if retry > MAX_RETRY: raise TimeoutError
            if MAX_RETRY!=0: logger.error(f'Request timed out，Retrying ({retry}/{MAX_RETRY}) ……')

    if not stream:
        # This branch is only applicable to the o1 model that does not support streams.，Other situations do not apply.
        chunkjson = json.loads(response.content.decode())
        gpt_replying_buffer = chunkjson['choices'][0]["message"]["content"]
        return gpt_replying_buffer

    stream_response = response.iter_lines()
    result = ''
    json_data = None
    while True:
        try: chunk = next(stream_response)
        except StopIteration:
            break
        except requests.exceptions.ConnectionError:
            chunk = next(stream_response) # Failed，Retry once？If it fails again, there is no way。
        chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role = decode_chunk(chunk)
        if len(chunk_decoded)==0: continue
        if not chunk_decoded.startswith('data:'):
            error_msg = get_full_error(chunk, stream_response).decode()
            if "reduce the length" in error_msg:
                raise ConnectionAbortedError("OpenAI rejected the request:" + error_msg)
            elif """type":"upstream_error","param":"307""" in error_msg:
                raise ConnectionAbortedError("Normal termination，But shows insufficient token，Resulting in incomplete output，Please reduce the amount of text input per request。")
            else:
                raise RuntimeError("OpenAI rejected the request：" + error_msg)
        if ('data: [DONE]' in chunk_decoded): break # api2d completed normally
        # Read some information in advance （Used to judge exceptions）
        if has_choices and not choice_valid:
            # Some errors caused by garbage third-party interfaces
            continue
        json_data = chunkjson['choices'][0]
        delta = json_data["delta"]
        if len(delta) == 0: break
        if (not has_content) and has_role: continue
        if (not has_content) and (not has_role): continue # raise RuntimeError("发现不标准The三方接口："+delta)
        if has_content: # has_role = True/False
            result += delta["content"]
            if not console_slience: print(delta["content"], end='')
            if observe_window is not None:
                # Observation window，Display the data already obtained
                if len(observe_window) >= 1:
                    observe_window[0] += delta["content"]
                # Watchdog，If the dog is not fed beyond the deadline，then terminate
                if len(observe_window) >= 2:
                    if (time.time()-observe_window[1]) > watch_dog_patience:
                        raise RuntimeError("User canceled the program。")
        else: raise RuntimeError("Unexpected JSON structure："+delta)
    if json_data and json_data['finish_reason'] == 'content_filter':
        raise RuntimeError("Due to Azure filtering out questions containing non-compliant content.。")
    if json_data and json_data['finish_reason'] == 'length':
        raise ConnectionAbortedError("Normal termination，But shows insufficient token，Resulting in incomplete output，Please reduce the amount of text input per request。")
    return result


def predict(inputs:str, llm_kwargs:dict, plugin_kwargs:dict, chatbot:ChatBotWithCookies,
            history:list=[], system_prompt:str='', stream:bool=True, additional_fn:str=None):
    """
    Send to chatGPT，Get output in a streaming way。
    Used for basic conversation functions。
    inputs are the inputs for this inquiry
    top_p, Temperature is an internal tuning parameter of chatGPT
    history is the list of previous conversations（Note that both inputs and history，An error of token overflow will be triggered if the content is too long）
    chatbot is the conversation list displayed in WebUI，Modify it，Then yield it out，You can directly modify the conversation interface content
    additional_fn represents which button is clicked，See functional.py for buttons
    """
    from void_terminal.request_llms.bridge_all import model_info
    if is_any_api_key(inputs):
        chatbot._cookies['api_key'] = inputs
        chatbot.append(("The input has been recognized as OpenAI`s api_key", what_keys(inputs)))
        yield from update_ui(chatbot=chatbot, history=history, msg="api_key has been imported") # Refresh the page
        return
    elif not is_any_api_key(chatbot._cookies['api_key']):
        chatbot.append((inputs, "Missing api_key。\n\n1. Temporary solution：Enter the api_key Directly in the Input Area，Submit after pressing Enter。2. Long-term Solution：Configure in config.py。"))
        yield from update_ui(chatbot=chatbot, history=history, msg="Missing api_key") # Refresh the page
        return

    user_input = inputs
    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    # Multimodal model
    has_multimodal_capacity = model_info[llm_kwargs['llm_model']].get('has_multimodal_capacity', False)
    if has_multimodal_capacity:
        has_recent_image_upload, image_paths = have_any_recent_upload_image_files(chatbot, pop=True)
    else:
        has_recent_image_upload, image_paths = False, []
    if has_recent_image_upload:
        _inputs, image_base64_array = make_multimodal_input(inputs, image_paths)
    else:
        _inputs, image_base64_array = inputs, []
    chatbot.append((_inputs, ""))
    yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page

    # Special model processing that prohibits the use of streams.
    if model_info[llm_kwargs['llm_model']].get('openai_disable_stream', False): stream = False
    else: stream = True

    # check mis-behavior
    if is_the_upload_folder(user_input):
        chatbot[-1] = (inputs, f"[Local Message] Operation error detected! After you upload the document，Click the `**Function Plugin Area**` button for processing，Do not click the `Submit` button or the `Basic Function Area` button。")
        yield from update_ui(chatbot=chatbot, history=history, msg="Normal") # Refresh the page
        time.sleep(2)

    try:
        headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt, image_base64_array, has_multimodal_capacity, stream)
    except RuntimeError as e:
        chatbot[-1] = (inputs, f"The api-key you provided does not meet the requirements，Does not contain any that can be used for{llm_kwargs['llm_model']}api-key。You may have selected the wrong model or request source。")
        yield from update_ui(chatbot=chatbot, history=history, msg="API key does not meet requirements") # Refresh the page
        return

    # Check if the endpoint is valid
    try:
        endpoint = verify_endpoint(model_info[llm_kwargs['llm_model']]['endpoint'])
    except:
        tb_str = '```\n' + trimmed_format_exc() + '```'
        chatbot[-1] = (inputs, tb_str)
        yield from update_ui(chatbot=chatbot, history=history, msg="Endpoint does not meet the requirements") # Refresh the page
        return

    # Add to history
    if has_recent_image_upload:
        history.extend([_inputs, ""])
    else:
        history.extend([inputs, ""])

    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=True
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                    json=payload, stream=stream, timeout=TIMEOUT_SECONDS);break
        except:
            retry += 1
            chatbot[-1] = ((chatbot[-1][0], timeout_bot_msg))
            retry_msg = f"，Retrying ({retry}/{MAX_RETRY}) ……" if MAX_RETRY > 0 else ""
            yield from update_ui(chatbot=chatbot, history=history, msg="Request timed out"+retry_msg) # Refresh the page
            if retry > MAX_RETRY: raise TimeoutError


    if not stream:
        # This branch is only applicable to the o1 model that does not support streams.，Other situations do not apply.
        yield from handle_o1_model_special(response, inputs, llm_kwargs, chatbot, history)
        return

    if stream:
        gpt_replying_buffer = ""
        is_head_of_the_stream = True
        stream_response =  response.iter_lines()
        while True:
            try:
                chunk = next(stream_response)
            except StopIteration:
                # such errors occur in non-OpenAI official interfaces，OpenAI and API2D will not go here
                chunk_decoded = chunk.decode()
                error_msg = chunk_decoded
                # First exclude a third-party bug where one-api does not have a done data package
                if len(gpt_replying_buffer.strip()) > 0 and len(error_msg) == 0:
                    yield from update_ui(chatbot=chatbot, history=history, msg="Detected defective non-OpenAI official interface，It is recommended to choose a more stable interface。")
                    break
                # Other situations，Direct return error
                chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg)
                yield from update_ui(chatbot=chatbot, history=history, msg="Non-OpenAI official interface returned an error:" + chunk.decode()) # Refresh the page
                return

            # Read some information in advance （Used to judge exceptions）
            chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role = decode_chunk(chunk)

            if is_head_of_the_stream and (r'"object":"error"' not in chunk_decoded) and (r"content" not in chunk_decoded):
                # The first frame of the data stream does not carry content
                is_head_of_the_stream = False; continue

            if chunk:
                try:
                    if has_choices and not choice_valid:
                        # Some errors caused by garbage third-party interfaces
                        continue
                    if ('data: [DONE]' not in chunk_decoded) and len(chunk_decoded) > 0 and (chunkjson is None):
                        # Passing in Some Weird Things
                        raise ValueError(f'Unable to read the following data，Please check the configuration。\n\n{chunk_decoded}')
                    # The former is the termination condition of API2D，The latter is the termination condition of OPENAI
                    if ('data: [DONE]' in chunk_decoded) or (len(chunkjson['choices'][0]["delta"]) == 0):
                        # Judged as the end of the data stream，gpt_replying_buffer is also written
                        log_chat(llm_model=llm_kwargs["llm_model"], input_str=inputs, output_str=gpt_replying_buffer)
                        break
                    # Processing the body of the data stream
                    status_text = f"finish_reason: {chunkjson['choices'][0].get('finish_reason', 'null')}"
                    # If an exception is thrown here，It is usually because the text is too long，See the output of get_full_error for details
                    if has_content:
                        # Normal situation
                        gpt_replying_buffer = gpt_replying_buffer + chunkjson['choices'][0]["delta"]["content"]
                    elif has_role:
                        # Some third-party interfaces encounter such errors，Let`s make it compatible
                        continue
                    else:
                        # This has exceeded the scope that a normal interface should enter，Some crappy third-party interfaces may produce such errors
                        if chunkjson['choices'][0]["delta"]["content"] is None: continue # Some crappy third-party interfaces have this error，Let`s make it compatible
                        gpt_replying_buffer = gpt_replying_buffer + chunkjson['choices'][0]["delta"]["content"]

                    history[-1] = gpt_replying_buffer
                    chatbot[-1] = (history[-2], history[-1])
                    yield from update_ui(chatbot=chatbot, history=history, msg=status_text) # Refresh the page
                except Exception as e:
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json parsing is not normal") # Refresh the page
                    chunk = get_full_error(chunk, stream_response)
                    chunk_decoded = chunk.decode()
                    error_msg = chunk_decoded
                    chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg)
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json parsing exception." + error_msg) # Refresh the page
                    logger.error(error_msg)
                    return
        return  # return from stream-branch

def handle_o1_model_special(response, inputs, llm_kwargs, chatbot, history):
    try:
        chunkjson = json.loads(response.content.decode())
        gpt_replying_buffer = chunkjson['choices'][0]["message"]["content"]
        log_chat(llm_model=llm_kwargs["llm_model"], input_str=inputs, output_str=gpt_replying_buffer)
        history[-1] = gpt_replying_buffer
        chatbot[-1] = (history[-2], history[-1])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    except Exception as e:
        yield from update_ui(chatbot=chatbot, history=history, msg="Json parsing exception." + response.text) # Refresh the page

def handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg):
    from void_terminal.request_llms.bridge_all import model_info
    openai_website = ' Please log in to OpenAI to view details at https://platform.openai.com/signup'
    if "reduce the length" in error_msg:
        if len(history) >= 2: history[-1] = ""; history[-2] = "" # Clear the current overflow input：history[-2] It is the input of this time, history[-1] It is the output of this time
        history = clip_history(inputs=inputs, history=history, tokenizer=model_info[llm_kwargs['llm_model']]['tokenizer'],
                                               max_token_limit=(model_info[llm_kwargs['llm_model']]['max_token'])) # Release at least half of the history
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Reduce the length. The input is too long this time, Or the historical data is too long. Historical cached data has been partially released, You can try again. (If it fails again, it is more likely due to input being too long.)")
    elif "does not exist" in error_msg:
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Model {llm_kwargs['llm_model']} Model does not exist, Or you do not have the qualification for experience.")
    elif "Incorrect API key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Incorrect API key. OpenAI claims that an incorrect API_KEY was provided, Service refused. " + openai_website)
    elif "exceeded your current quota" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You exceeded your current quota. OpenAI claims that the account balance is insufficient, Service refused." + openai_website)
    elif "account is not active" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Your account is not active. OpenAI states that it is due to account expiration, Service refused." + openai_website)
    elif "associated with a deactivated account" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You are associated with a deactivated account. OpenAI considers it as an account expiration, Service refused." + openai_website)
    elif "API key has been deactivated" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] API key has been deactivated. OpenAI considers it as an account failure, Service refused." + openai_website)
    elif "bad forward key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Bad forward key. API2D account balance is insufficient.")
    elif "Not enough point" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Not enough point. API2D account points are insufficient.")
    else:
        from void_terminal.toolbox import regular_txt_to_markdown
        tb_str = '```\n' + trimmed_format_exc() + '```'
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Exception \n\n{tb_str} \n\n{regular_txt_to_markdown(chunk_decoded)}")
    return chatbot, history

def generate_payload(inputs:str, llm_kwargs:dict, history:list, system_prompt:str, image_base64_array:list=[], has_multimodal_capacity:bool=False, stream:bool=True):
    """
    Integrate all information，Select LLM model，Generate http request，Prepare to send request
    """
    from void_terminal.request_llms.bridge_all import model_info

    if not is_any_api_key(llm_kwargs['api_key']):
        raise AssertionError("You provided an incorrect API_KEY。\n\n1. Temporary solution：Enter the api_key Directly in the Input Area，Submit after pressing Enter。2. Long-term Solution：Configure in config.py。")

    if llm_kwargs['llm_model'].startswith('vllm-'):
        api_key = 'no-api-key'
    else:
        api_key = select_api_key(llm_kwargs['api_key'], llm_kwargs['llm_model'])

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    if API_ORG.startswith('org-'): headers.update({"OpenAI-Organization": API_ORG})
    if llm_kwargs['llm_model'].startswith('azure-'):
        headers.update({"api-key": api_key})
        if llm_kwargs['llm_model'] in AZURE_CFG_ARRAY.keys():
            azure_api_key_unshared = AZURE_CFG_ARRAY[llm_kwargs['llm_model']]["AZURE_API_KEY"]
            headers.update({"api-key": azure_api_key_unshared})

    if has_multimodal_capacity:
        # When the following conditions are met，Enable multimodal capabilities：
        # 1. The model itself is multimodal（has_multimodal_capacity）
        # 2. Input contains images（len(image_base64_array) > 0）
        # 3. Historical input contains images（ any([contain_base64(h) for h in history]) ）
        enable_multimodal_capacity = (len(image_base64_array) > 0) or any([contain_base64(h) for h in history])
    else:
        enable_multimodal_capacity = False

    conversation_cnt = len(history) // 2
    openai_disable_system_prompt = model_info[llm_kwargs['llm_model']].get('openai_disable_system_prompt', False)

    if openai_disable_system_prompt:
        messages = [{"role": "user", "content": system_prompt}]
    else:
        messages = [{"role": "system", "content": system_prompt}]

    if not enable_multimodal_capacity:
        # Not using multimodal capabilities
        if conversation_cnt:
            for index in range(0, 2*conversation_cnt, 2):
                what_i_have_asked = {}
                what_i_have_asked["role"] = "user"
                what_i_have_asked["content"] = remove_image_if_contain_base64(history[index])
                what_gpt_answer = {}
                what_gpt_answer["role"] = "assistant"
                what_gpt_answer["content"] = remove_image_if_contain_base64(history[index+1])
                if what_i_have_asked["content"] != "":
                    if what_gpt_answer["content"] == "": continue
                    if what_gpt_answer["content"] == timeout_bot_msg: continue
                    messages.append(what_i_have_asked)
                    messages.append(what_gpt_answer)
                else:
                    messages[-1]['content'] = what_gpt_answer['content']
        what_i_ask_now = {}
        what_i_ask_now["role"] = "user"
        what_i_ask_now["content"] = inputs
        messages.append(what_i_ask_now)
    else:
        # Multimodal capabilities
        if conversation_cnt:
            for index in range(0, 2*conversation_cnt, 2):
                what_i_have_asked = {}
                what_i_have_asked["role"] = "user"
                what_i_have_asked["content"] = append_image_if_contain_base64(history[index])
                what_gpt_answer = {}
                what_gpt_answer["role"] = "assistant"
                what_gpt_answer["content"] = append_image_if_contain_base64(history[index+1])
                if what_i_have_asked["content"] != "":
                    if what_gpt_answer["content"] == "": continue
                    if what_gpt_answer["content"] == timeout_bot_msg: continue
                    messages.append(what_i_have_asked)
                    messages.append(what_gpt_answer)
                else:
                    messages[-1]['content'] = what_gpt_answer['content']
        what_i_ask_now = {}
        what_i_ask_now["role"] = "user"
        what_i_ask_now["content"] = []
        what_i_ask_now["content"].append({
            "type": "text",
            "text": inputs
        })
        for image_base64 in image_base64_array:
            what_i_ask_now["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            })
        messages.append(what_i_ask_now)


    model = llm_kwargs['llm_model']
    if llm_kwargs['llm_model'].startswith('api2d-'):
        model = llm_kwargs['llm_model'][len('api2d-'):]
    if llm_kwargs['llm_model'].startswith('one-api-'):
        model = llm_kwargs['llm_model'][len('one-api-'):]
        model, _ = read_one_api_model_name(model)
    if llm_kwargs['llm_model'].startswith('vllm-'):
        model = llm_kwargs['llm_model'][len('vllm-'):]
        model, _ = read_one_api_model_name(model)
    if model == "gpt-3.5-random": # Random selection, Bypass openai access frequency limit
        model = random.choice([
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-3.5-turbo-0301",
        ])

    payload = {
        "model": model,
        "messages": messages,
        "temperature": llm_kwargs['temperature'],  # 1.0,
        "top_p": llm_kwargs['top_p'],  # 1.0,
        "n": 1,
        "stream": stream,
    }

    return headers,payload



import os

"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Connecting to void-terminal:
    - set_conf:                     Dynamically modify configurations during runtime
    - set_multi_conf:               Dynamically modify multiple configurations during runtime
    - get_plugin_handle:            Get handle of plugin
    - get_plugin_default_kwargs:    Get default parameters of plugin
    - get_chat_handle:              Get handle of simple chat
    - get_chat_default_kwargs:      Get default parameters for simple chat
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


def get_plugin_handle(plugin_name):
    """
    e.g. plugin_name = 'crazy_functions.Markdown_Translate->TranslateMarkdownToSpecifiedLanguage'
    """
    import importlib

    assert (
        "->" in plugin_name
    ), "Example of plugin_name: crazy_functions.Markdown_Translate->TranslateMarkdownToSpecifiedLanguage"
    module, fn_name = plugin_name.split("->")
    f_hot_reload = getattr(importlib.import_module(module, fn_name), fn_name)
    return f_hot_reload


def get_chat_handle():
    """
    Get chat function
    """
    from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection

    return predict_no_ui_long_connection


def get_plugin_default_kwargs():
    """
    Get Plugin Default Arguments
    """
    from void_terminal.toolbox import ChatBotWithCookies, load_chat_cookies

    cookies = load_chat_cookies()
    llm_kwargs = {
        "api_key": cookies["api_key"],
        "llm_model": cookies["llm_model"],
        "top_p": 1.0,
        "max_length": None,
        "temperature": 1.0,
    }
    chatbot = ChatBotWithCookies(llm_kwargs)

    # txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request
    DEFAULT_FN_GROUPS_kwargs = {
        "main_input": "./README.md",
        "llm_kwargs": llm_kwargs,
        "plugin_kwargs": {},
        "chatbot_with_cookie": chatbot,
        "history": [],
        "system_prompt": "You are a good AI.",
        "user_request": None,
    }
    return DEFAULT_FN_GROUPS_kwargs


def get_chat_default_kwargs():
    """
    Get Chat Default Arguments
    """
    from void_terminal.toolbox import load_chat_cookies

    cookies = load_chat_cookies()
    llm_kwargs = {
        "api_key": cookies["api_key"],
        "llm_model": cookies["llm_model"],
        "top_p": 1.0,
        "max_length": None,
        "temperature": 1.0,
    }
    default_chat_kwargs = {
        "inputs": "Hello there, are you ready?",
        "llm_kwargs": llm_kwargs,
        "history": [],
        "sys_prompt": "You are AI assistant",
        "observe_window": None,
        "console_slience": False,
    }

    return default_chat_kwargs

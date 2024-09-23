
from void_terminal.toolbox import get_conf
from void_terminal.crazy_functions.Internet_GPT import ConnectToNetworkToAnswerQuestions
from void_terminal.crazy_functions.plugin_template.plugin_class_template import GptAcademicPluginTemplate, ArgProperty


class NetworkGPT_Wrap(GptAcademicPluginTemplate):
    def __init__(self):
        """
        Please note`execute`Will be executed in different threads，So when you define and use class variables，Should be extremely cautious!
        """
        pass

    def define_arg_selection_menu(self):
        """
        Define the secondary option menu of the plugin

        The first parameter，Name`main_input`，Parameters`type`Declare this as a text box，Displayed above the text box`title`，Text box internal display`description`，`default_value`For the default value;
        The second parameter，Name`advanced_arg`，Parameters`type`Declare this as a text box，Displayed above the text box`title`，Text box internal display`description`，`default_value`For the default value;
        The third parameter，Name`allow_cache`，Parameters`type`Declare that this is a dropdown menu，Display above the dropdown menu`title`+`description`，The options in the dropdown menu are`options`，`default_value`As the default value for the dropdown menu;

        """
        gui_definition = {
            "main_input":
                ArgProperty(title="Input question", description="Questions to be retrieved via the internet，Will automatically read the input box content", default_value="", type="string").model_dump_json(), # Primary input，Automatically sync from the input box
            "categories":
                ArgProperty(title="Search category", options=["Webpage", "Academic paper"], default_value="Webpage", description="None", type="dropdown").model_dump_json(),
            "engine":
                ArgProperty(title="Choose a search engine", options=["Mixed", "bing", "google", "duckduckgo"], default_value="google", description="None", type="dropdown").model_dump_json(),
            "optimizer":
                ArgProperty(title="Search optimization", options=["Close", "Turn on", "Turn on(Enhance)"], default_value="Close", description="Whether to use search enhancement。Note that this may consume more tokens", type="dropdown").model_dump_json(),
            "searxng_url":
                ArgProperty(title="Searxng service address", description="Enter the address of Searxng", default_value=get_conf("SEARXNG_URL"), type="string").model_dump_json(), # Primary input，Automatically sync from the input box

        }
        return gui_definition

    def execute(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
        """
        Execute the plugin
        """
        if plugin_kwargs["categories"] == "Webpage": plugin_kwargs["categories"] = "general"
        if plugin_kwargs["categories"] == "Academic paper": plugin_kwargs["categories"] = "science"
        yield from ConnectToNetworkToAnswerQuestions(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request)


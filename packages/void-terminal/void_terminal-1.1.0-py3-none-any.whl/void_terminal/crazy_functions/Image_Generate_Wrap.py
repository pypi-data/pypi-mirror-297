
from void_terminal.toolbox import get_conf, update_ui
from void_terminal.crazy_functions.Image_Generate import ImageGeneration_DALLE2, ImageGeneration_DALLE3, ImageModification_DALLE2
from void_terminal.crazy_functions.plugin_template.plugin_class_template import GptAcademicPluginTemplate, ArgProperty


class ImageGen_Wrap(GptAcademicPluginTemplate):
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

        """
        gui_definition = {
            "main_input":
                ArgProperty(title="Input image description", description="Text description for generating images，Use English as much as possible", default_value="", type="string").model_dump_json(), # Primary input，Automatically sync from the input box
            "model_name":
                ArgProperty(title="Model", options=["DALLE2", "DALLE3"], default_value="DALLE3", description="None", type="dropdown").model_dump_json(),
            "resolution":
                ArgProperty(title="Resolution", options=["256x256(Limited to DALLE2)", "512x512(Limited to DALLE2)", "1024x1024", "1792x1024(Limited to DALLE3)", "1024x1792(Limited to DALLE3)"], default_value="1024x1024", description="None", type="dropdown").model_dump_json(),
            "quality (Only DALLE3 takes effect)":
                ArgProperty(title="Quality", options=["standard", "hd"], default_value="standard", description="None", type="dropdown").model_dump_json(),
            "style (Only DALLE3 takes effect)":
                ArgProperty(title="Style", options=["vivid", "natural"], default_value="vivid", description="None", type="dropdown").model_dump_json(),

        }
        return gui_definition

    def execute(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
        """
        Execute the plugin
        """
        # Resolution
        resolution = plugin_kwargs["resolution"].replace("(Limited to DALLE2)", "").replace("(Limited to DALLE3)", "")

        if plugin_kwargs["model_name"] == "DALLE2":
            plugin_kwargs["advanced_arg"] = resolution
            yield from ImageGeneration_DALLE2(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request)

        elif plugin_kwargs["model_name"] == "DALLE3":
            quality = plugin_kwargs["quality (Only DALLE3 takes effect)"]
            style = plugin_kwargs["style (Only DALLE3 takes effect)"]
            plugin_kwargs["advanced_arg"] = f"{resolution}-{quality}-{style}"
            yield from ImageGeneration_DALLE3(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request)

        else:
            chatbot.append([None, "Sorry，Model not found"])
            yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

from void_terminal.toolbox import CatchException, update_ui, promote_file_to_downloadzone, get_log_folder, get_user
from void_terminal.crazy_functions.plugin_template.plugin_class_template import GptAcademicPluginTemplate, ArgProperty
import re

f_prefix = 'TranslatedText'

def write_chat_to_file(chatbot, history=None, file_name=None):
    """
    Write the conversation record history to a file in Markdown format。If no file name is specified，Generate a file name using the current time。
    """
    import os
    import time
    from void_terminal.themes.theme import advanced_css

    if file_name is None:
        file_name = f_prefix + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.html'
    fp = os.path.join(get_log_folder(get_user(chatbot), plugin_name='chat_history'), file_name)

    with open(fp, 'w', encoding='utf8') as f:
        from textwrap import dedent
        form = dedent("""
        <!DOCTYPE html><head><meta charset="utf-8"><title>Conversation archive</title><style>{CSS}</style></head>
        <body>
        <div class="test_temp1" style="width:10%; height: 500px; float:left;"></div>
        <div class="test_temp2" style="width:80%;padding: 40px;float:left;padding-left: 20px;padding-right: 20px;box-shadow: rgba(0, 0, 0, 0.2) 0px 0px 8px 8px;border-radius: 10px;">
            <div class="chat-body" style="display: flex;justify-content: center;flex-direction: column;align-items: center;flex-wrap: nowrap;">
                {CHAT_PREVIEW}
                <div></div>
                <div></div>
                <div style="text-align: center;width:80%;padding: 0px;float:left;padding-left:20px;padding-right:20px;box-shadow: rgba(0, 0, 0, 0.05) 0px 0px 1px 2px;border-radius: 1px;">Conversation（Original data）</div>
                {HISTORY_PREVIEW}
            </div>
        </div>
        <div class="test_temp3" style="width:10%; height: 500px; float:left;"></div>
        </body>
        """)

        qa_from = dedent("""
        <div class="QaBox" style="width:80%;padding: 20px;margin-bottom: 20px;box-shadow: rgb(0 255 159 / 50%) 0px 0px 1px 2px;border-radius: 4px;">
            <div class="Question" style="border-radius: 2px;">{QUESTION}</div>
            <hr color="blue" style="border-top: dotted 2px #ccc;">
            <div class="Answer" style="border-radius: 2px;">{ANSWER}</div>
        </div>
        """)

        history_from = dedent("""
        <div class="historyBox" style="width:80%;padding: 0px;float:left;padding-left:20px;padding-right:20px;box-shadow: rgba(0, 0, 0, 0.05) 0px 0px 1px 2px;border-radius: 1px;">
            <div class="entry" style="border-radius: 2px;">{ENTRY}</div>
        </div>
        """)
        CHAT_PREVIEW_BUF = ""
        for i, contents in enumerate(chatbot):
            question, answer = contents[0], contents[1]
            if question is None: question = ""
            try: question = str(question)
            except: question = ""
            if answer is None: answer = ""
            try: answer = str(answer)
            except: answer = ""
            CHAT_PREVIEW_BUF += qa_from.format(QUESTION=question, ANSWER=answer)

        HISTORY_PREVIEW_BUF = ""
        for h in history:
            HISTORY_PREVIEW_BUF += history_from.format(ENTRY=h)
        html_content = form.format(CHAT_PREVIEW=CHAT_PREVIEW_BUF, HISTORY_PREVIEW=HISTORY_PREVIEW_BUF, CSS=advanced_css)
        f.write(html_content)

    promote_file_to_downloadzone(fp, rename_file=file_name, chatbot=chatbot)
    return 'Conversation history written：' + fp

def gen_file_preview(file_name):
    try:
        with open(file_name, 'r', encoding='utf8') as f:
            file_content = f.read()
        # pattern to match the text between <head> and </head>
        pattern = re.compile(r'<head>.*?</head>', flags=re.DOTALL)
        file_content = re.sub(pattern, '', file_content)
        html, history = file_content.split('<hr color="blue"> \n\n Conversation data (No rendering):\n')
        history = history.strip('<code>')
        history = history.strip('</code>')
        history = history.split("\n>>>")
        return list(filter(lambda x:x!="", history))[0][:100]
    except:
        return ""

def read_file_to_chat(chatbot, history, file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        file_content = f.read()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(file_content, 'lxml')
    # Extract QaBox information
    chatbot.clear()
    qa_box_list = []
    qa_boxes = soup.find_all("div", class_="QaBox")
    for box in qa_boxes:
        question = box.find("div", class_="Question").get_text(strip=False)
        answer = box.find("div", class_="Answer").get_text(strip=False)
        qa_box_list.append({"Question": question, "Answer": answer})
        chatbot.append([question, answer])
    # Extract historyBox information
    history_box_list = []
    history_boxes = soup.find_all("div", class_="historyBox")
    for box in history_boxes:
        entry = box.find("div", class_="entry").get_text(strip=False)
        history_box_list.append(entry)
    history = history_box_list
    chatbot.append([None, f"[Local Message] Load conversation{len(qa_box_list)}条，Context{len(history)}条。"])
    return chatbot, history

@CatchException
def ChatHistoryArchive(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    user_request    Current user`s request information（IP addresses, etc.）
    """
    file_name = plugin_kwargs.get("file_name", None)
    if (file_name is not None) and (file_name != "") and (not file_name.endswith('.html')): file_name += '.html'
    else: file_name = None

    chatbot.append((None, f"[Local Message] {write_chat_to_file(chatbot, history, file_name)}，You can use the `LoadChatHistoryArchive` in the drop-down menu to restore the current conversation。"))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time


class Conversation_To_File_Wrap(GptAcademicPluginTemplate):
    def __init__(self):
        """
        Please note`execute`Will be executed in different threads，So when you define and use class variables，Should be extremely cautious!
        """
        pass

    def define_arg_selection_menu(self):
        """
        Define the secondary option menu of the plugin

        The first parameter，Name`file_name`，Parameters`type`Declare this as a text box，Displayed above the text box`title`，Text box internal display`description`，`default_value`For the default value;
        """
        gui_definition = {
            "file_name": ArgProperty(title="Save file name", description="Enter the dialogue archive file name，Leave blank to use time as the file name", default_value="", type="string").model_dump_json(), # Primary input，Automatically sync from the input box
        }
        return gui_definition

    def execute(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
        """
        Execute the plugin
        """
        yield from ChatHistoryArchive(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request)





def hide_cwd(str):
    import os
    current_path = os.getcwd()
    replace_path = "."
    return str.replace(current_path, replace_path)

@CatchException
def LoadChatHistoryArchive(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    user_request    Current user`s request information（IP addresses, etc.）
    """
    from void_terminal.crazy_functions.crazy_utils import get_files_from_everything
    success, file_manifest, _ = get_files_from_everything(txt, type='.html')

    if not success:
        if txt == "": txt = 'Empty input field'
        import glob
        local_history = "<br/>".join([
            "`"+hide_cwd(f)+f" ({gen_file_preview(f)})"+"`"
            for f in glob.glob(
                f'{get_log_folder(get_user(chatbot), plugin_name="chat_history")}/**/{f_prefix}*.html',
                recursive=True
            )])
        chatbot.append([f"Looking for conversation history file（HTML format）: {txt}", f"No HTML files found: {txt}。But the following history files are stored locally，You can paste any file path into the input area，and try again：<br/>{local_history}"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    try:
        chatbot, history = read_file_to_chat(chatbot, history, file_manifest[0])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    except:
        chatbot.append([f"Load conversation history file", f"Conversation history file is corrupted!"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

@CatchException
def DeleteAllLocalConversationHistoryRecords(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    user_request    Current user`s request information（IP addresses, etc.）
    """

    import glob, os
    local_history = "<br/>".join([
        "`"+hide_cwd(f)+"`"
        for f in glob.glob(
            f'{get_log_folder(get_user(chatbot), plugin_name="chat_history")}/**/{f_prefix}*.html', recursive=True
        )])
    for f in glob.glob(f'{get_log_folder(get_user(chatbot), plugin_name="chat_history")}/**/{f_prefix}*.html', recursive=True):
        os.remove(f)
    chatbot.append([f"Delete all history conversation files", f"Deleted<br/>{local_history}"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    return
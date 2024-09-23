from void_terminal.toolbox import CatchException, report_exception, get_log_folder, gen_time_str
from void_terminal.toolbox import update_ui, promote_file_to_downloadzone, update_ui_lastest_msg, disable_auto_promotion
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency
from void_terminal.crazy_functions.crazy_utils import read_and_clean_pdf_text
from void_terminal.crazy_functions.pdf_fns.parse_pdf import parse_pdf, get_avail_grobid_url, translate_pdf
from void_terminal.shared_utils.colorful import *
import copy
import os
import math
import logging

def markdown_to_dict(article_content):
    import markdown
    from bs4 import BeautifulSoup
    cur_t = ""
    cur_c = ""
    results = {}
    for line in article_content:
        if line.startswith('#'):
            if cur_t!="":
                if cur_t not in results:
                    results.update({cur_t:cur_c.lstrip('\n')})
                else:
                    # Handling duplicate chapter names
                    results.update({cur_t + " " + gen_time_str():cur_c.lstrip('\n')})
            cur_t = line.rstrip('\n')
            cur_c = ""
        else:
            cur_c += line
    results_final = {}
    for k in list(results.keys()):
        if k.startswith('# '):
            results_final['title'] = k.split('# ')[-1]
            results_final['authors'] = results.pop(k).lstrip('\n')
        if k.startswith('###### Abstract'):
            results_final['abstract'] = results.pop(k).lstrip('\n')

    results_final_sections = []
    for k,v in results.items():
        results_final_sections.append({
            'heading':k.lstrip("# "),
            'text':v if len(v) > 0 else f"The beginning of {k.lstrip('# ')} section."
        })
    results_final['sections'] = results_final_sections
    return results_final


@CatchException
def BatchTranslatePDFDocuments(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):

    disable_auto_promotion(chatbot)
    # Basic information：Function, contributor
    chatbot.append([
        "Function plugin feature？",
        "BatchTranslatePDFDocuments。Function plugin contributor: Binary-Husky"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Clear history，To avoid input overflow
    history = []

    from void_terminal.crazy_functions.crazy_utils import get_files_from_everything
    success, file_manifest, project_folder = get_files_from_everything(txt, type='.pdf')
    if len(file_manifest) > 0:
        # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
        try:
            import nougat
            import tiktoken
        except:
            report_exception(chatbot, history,
                             a=f"Parsing project: {txt}",
                             b=f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade nougat-ocr tiktoken```。")
            yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
            return
    success_mmd, file_manifest_mmd, _ = get_files_from_everything(txt, type='.mmd')
    success = success or success_mmd
    file_manifest += file_manifest_mmd
    chatbot.append(["File list：", ", ".join([e.split('/')[-1] for e in file_manifest])]);
    yield from update_ui(      chatbot=chatbot, history=history)
    # Checking input parameters，If no input parameters are given，Exit directly
    if not success:
        if txt == "": txt = 'Empty input field'

    # If no files are found
    if len(file_manifest) == 0:
        report_exception(chatbot, history,
                         a=f"Parsing project: {txt}", b=f"Cannot find any file with .pdf extension: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Start executing the task formally
    yield from ParsePDF_NOUGAT(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)




def ParsePDF_NOUGAT(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import copy
    import tiktoken
    TOKEN_LIMIT_PER_FRAGMENT = 1024
    generated_conclusion_files = []
    generated_html_files = []
    DST_LANG = "Chinese"
    from void_terminal.crazy_functions.crazy_utils import nougat_interface
    from void_terminal.crazy_functions.pdf_fns.report_gen_html import construct_html
    nougat_handle = nougat_interface()
    for index, fp in enumerate(file_manifest):
        if fp.endswith('pdf'):
            chatbot.append(["Current progress：", f"Analyzing the paper，Please wait。（When running for the first time，It takes a long time to download NOUGAT parameters）"]); yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
            fpp = yield from nougat_handle.NOUGAT_parse_pdf(fp, chatbot, history)
            promote_file_to_downloadzone(fpp, rename_file=os.path.basename(fpp)+'.nougat.mmd', chatbot=chatbot)
        else:
            chatbot.append(["The current paper does not need to be parsed：", fp]); yield from update_ui(      chatbot=chatbot, history=history)
            fpp = fp
        with open(fpp, 'r', encoding='utf8') as f:
            article_content = f.readlines()
        article_dict = markdown_to_dict(article_content)
        logging.info(article_dict)
        yield from translate_pdf(article_dict, llm_kwargs, chatbot, fp, generated_conclusion_files, TOKEN_LIMIT_PER_FRAGMENT, DST_LANG)

    chatbot.append(("Provide a list of output files", str(generated_conclusion_files + generated_html_files)))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page



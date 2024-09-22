"""
Test each plugin in the project。Running method：Run python tests/test_plugins.py directly
"""

import init_test
import os, sys


if __name__ == "__main__":
    from test_utils import plugin_test

    plugin_test(plugin='crazy_functions.SourceCode_Comment->CommentPythonProject', main_input="build/test/python_comment")

    # plugin_test(plugin='crazy_functions.Internet_GPT->ConnectToNetworkToAnswerQuestions', main_input="谁是应急食品？")

    # plugin_test(plugin='crazy_functions.DynamicFunctionGeneration->DynamicFunctionGeneration', main_input='Swap blue channel and red channel of the image', advanced_arg={"file_path_arg": "./build/ants.jpg"})

    # plugin_test(plugin='crazy_functions.Latex_Function->TranslateChineseToEnglishInLatexAndRecompilePDF', main_input="2307.07522")

    # plugin_test(plugin='crazy_functions.PDF_Translate->BatchTranslatePDFDocuments', main_input='build/pdf/t1.pdf')

    # plugin_test(
    #     plugin="crazy_functions.Latex_Function->TranslateChineseToEnglishInLatexAndRecompilePDF",
    #     main_input="G:/SEAFILE_LOCAL/50503047/My Library/Degree/paperlatex/aaai/Fu_8368_with_appendix",
    # )

    # plugin_test(plugin='crazy_functions.VoidTerminal->VoidTerminal', main_input='修改api-key为sk-jhoejriotherjep')

    # plugin_test(plugin='crazy_functions.BatchTranslatePDFDocuments_NOUGAT->BatchTranslatePDFDocuments', main_input='crazy_functions/test_project/pdf_and_word/aaai.pdf')

    # plugin_test(plugin='crazy_functions.VoidTerminal->VoidTerminal', main_input='Invoke plugin，To C:Parse the python file in /Users/fuqingxu/Desktop/旧File/gpt/chatgpt_academic/crazy_functions/latex_fns')

    # plugin_test(plugin='crazy_functions.命令line助手->命令line助手', main_input='查看当前的docker容器List')

    # plugin_test(plugin='crazy_functions.SourceCode_Analyse->ParsePythonProject', main_input="crazy_functions/test_project/python/dqn")

    # plugin_test(plugin='crazy_functions.SourceCode_Analyse->ParseCProject', main_input="crazy_functions/test_project/cpp/cppipc")

    # plugin_test(plugin='crazy_functions.FullTextProofreadingForLatex->EnglishProofreadingForLatex', main_input="crazy_functions/test_project/latex/attention")

    # plugin_test(plugin='crazy_functions.Markdown_Translate->MarkdownChineseToEnglish', main_input="README.md")

    # plugin_test(plugin='crazy_functions.PDF_Translate->BatchTranslatePDFDocuments', main_input='crazy_functions/test_project/pdf_and_word/aaai.pdf')

    # plugin_test(plugin='crazy_functions.GoogleSearchAssistant->GoogleSearchAssistant', main_input="https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=auto+reinforcement+learning&btnG=")

    # plugin_test(plugin='crazy_functions.SummarizingWordDocuments->SummarizingWordDocuments', main_input="crazy_functions/test_project/pdf_and_word")

    # plugin_test(plugin='crazy_functions.DownloadArxivPaperTranslateAbstract->DownloadArxivPaperAndTranslateAbstract', main_input="1812.10695")

    # plugin_test(plugin='crazy_functions.ChatGPTConnectedToNetwork->ConnectToNetworkToAnswerQuestions', main_input="谁是应急食品？")

    # plugin_test(plugin='crazy_functions.ParsingJupyterNotebook->ParsingIpynbFiles', main_input="crazy_functions/test_samples")

    # plugin_test(plugin='crazy_functions.MathematicalAnimationGenerationManim->AnimationGeneration', main_input="A ball split into 2, and then split into 4, and finally split into 8.")

    # for lang in ["English", "French", "Japanese", "Korean", "Russian", "Italian", "German", "Portuguese", "Arabic"]:
    #     plugin_test(plugin='crazy_functions.Markdown_Translate->TranslateMarkdownToSpecifiedLanguage', main_input="README.md", advanced_arg={"advanced_arg": lang})

    # plugin_test(plugin='crazy_functions.InjectKnowledgeBaseFiles->InjectKnowledgeBaseFiles', main_input="./")

    # plugin_test(plugin='crazy_functions.InjectKnowledgeBaseFiles->ReadKnowledgeArchiveAnswerQuestions', main_input="What is the installation method？")

    # plugin_test(plugin='crazy_functions.InjectKnowledgeBaseFiles->ReadKnowledgeArchiveAnswerQuestions', main_input="Deploy to remote cloud server？")

    # plugin_test(plugin='crazy_functions.Latex_Function->TranslateChineseToEnglishInLatexAndRecompilePDF', main_input="2210.03629")

    # advanced_arg = {"advanced_arg":"--llm_to_learn=gpt-3.5-turbo --prompt_prefix='根据下面的服装类型prompt，Imagine a wearer，Describe the appearance, environment, inner world, and character of this person.。Requirement：Within 100 words，Use the second person。' --system_prompt=''" }
    # plugin_test(plugin='crazy_functions.ChatGLMFineTuningTool->FineTuneDatasetGeneration', main_input='build/dev.json', advanced_arg=advanced_arg)

    # advanced_arg = {"advanced_arg":"--pre_seq_len=128 --learning_rate=2e-2 --num_gpus=1 --json_dataset='t_code.json' --ptuning_directory='/home/hmp/ChatGLM2-6B/ptuning'     " }
    # plugin_test(plugin='crazy_functions.ChatGLMFineTuningTool->StartFineTuning', main_input='build/dev.json', advanced_arg=advanced_arg)

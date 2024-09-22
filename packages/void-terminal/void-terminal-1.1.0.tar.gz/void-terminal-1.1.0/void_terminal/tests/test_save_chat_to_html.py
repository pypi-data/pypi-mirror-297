def validate_path():
    import os, sys
    os.path.dirname(__file__)
    root_dir_assume = os.path.abspath(os.path.dirname(__file__) + "/..")
    os.chdir(root_dir_assume)
    sys.path.append(root_dir_assume)
validate_path()  # validate path so you can run from base directory

def write_chat_to_file(chatbot, history=None, file_name=None):
    """
    Write the conversation record history to a file in Markdown format。If no file name is specified，Generate a file name using the current time。
    """
    import os
    import time
    from void_terminal.themes.theme import advanced_css
    # debug
    import pickle
    # def objdump(obj, file="objdump.tmp"):
    #     with open(file, "wb+") as f:
    #         pickle.dump(obj, f)
    #     return

    def objload(file="objdump.tmp"):
        import os
        if not os.path.exists(file):
            return
        with open(file, "rb") as f:
            return pickle.load(f)
    # objdump((chatbot, history))
    chatbot, history = objload()

    with open("test.html", 'w', encoding='utf8') as f:
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


    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')

    # Extract QaBox information
    qa_box_list = []
    qa_boxes = soup.find_all("div", class_="QaBox")
    for box in qa_boxes:
        question = box.find("div", class_="Question").get_text(strip=False)
        answer = box.find("div", class_="Answer").get_text(strip=False)
        qa_box_list.append({"Question": question, "Answer": answer})

    # Extract historyBox information
    history_box_list = []
    history_boxes = soup.find_all("div", class_="historyBox")
    for box in history_boxes:
        entry = box.find("div", class_="entry").get_text(strip=False)
        history_box_list.append(entry)

    print('')


write_chat_to_file(None, None, None)
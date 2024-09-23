import requests
import random
import time
import re
import json
from bs4 import BeautifulSoup
from functools import lru_cache
from itertools import zip_longest
from void_terminal.check_proxy import check_proxy
from void_terminal.toolbox import CatchException, update_ui, get_conf
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive, input_clipping
from void_terminal.request_llms.bridge_all import model_info
from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection
from void_terminal.crazy_functions.prompts.internet import SearchOptimizerPrompt, SearchAcademicOptimizerPrompt

def search_optimizer(
    query,
    proxies,
    history,
    llm_kwargs,
    optimizer=1,
    categories="general",
    searxng_url=None,
    engines=None,
):
    # ------------- < Step 1：Try to optimize the search > -------------
    # Enhanced optimization，Will try to optimize the search by combining historical records
    if optimizer == 2:
        his = " "
        if len(history) == 0:
            pass
        else:
            for i, h in enumerate(history):
                if i % 2 == 0:
                    his += f"Q: {h}\n"
                else:
                    his += f"A: {h}\n"
        if categories == "general":
            sys_prompt = SearchOptimizerPrompt.format(query=query, history=his, num=4)
        elif categories == "science":
            sys_prompt = SearchAcademicOptimizerPrompt.format(query=query, history=his, num=4)
    else:
        his = " "
        if categories == "general":
            sys_prompt = SearchOptimizerPrompt.format(query=query, history=his, num=3)
        elif categories == "science":
            sys_prompt = SearchAcademicOptimizerPrompt.format(query=query, history=his, num=3)
    
    mutable = ["", time.time(), ""]
    llm_kwargs["temperature"] = 0.8
    try:
        querys_json = predict_no_ui_long_connection(
            inputs=query,
            llm_kwargs=llm_kwargs,
            history=[],
            sys_prompt=sys_prompt,
            observe_window=mutable,
        )
    except Exception:
        querys_json = "1234"
    #* Try to decode the optimized search results
    querys_json = re.sub(r"```json|```", "", querys_json)
    try:
        querys = json.loads(querys_json)
    except Exception:
        #* If decoding fails,Lower the temperature and try again
        try:
            llm_kwargs["temperature"] = 0.4
            querys_json = predict_no_ui_long_connection(
                inputs=query,
                llm_kwargs=llm_kwargs,
                history=[],
                sys_prompt=sys_prompt,
                observe_window=mutable,
            )
            querys_json = re.sub(r"```json|```", "", querys_json)
            querys = json.loads(querys_json)
        except Exception:
            #If failed again，Directly return the original question
            querys = [query]
    links = []
    success = 0
    Exceptions = ""
    for q in querys:
        try:
            link = searxng_request(q, proxies, categories, searxng_url, engines=engines)
            if len(link) > 0:
                links.append(link[:-5])
                success += 1
        except Exception:
            Exceptions = Exception
            pass
    if success == 0:
        raise ValueError(f"Online search failed!\n{Exceptions}")
    # Cleaning search results，Put each group`s first one by one，Second search result，Clean and remove duplicate search results
    seen_links = set()
    result = []
    for tuple in zip_longest(*links, fillvalue=None):
        for item in tuple:
            if item is not None:
                link = item["link"]
                if link not in seen_links:
                    seen_links.add(link)
                    result.append(item)
    return result


@lru_cache
def get_auth_ip():
    ip = check_proxy(None, return_ip=True)
    if ip is None:
        return '114.114.114.' + str(random.randint(1, 10))
    return ip


def searxng_request(query, proxies, categories='general', searxng_url=None, engines=None):
    if searxng_url is None:
        url = get_conf("SEARXNG_URL")
    else:
        url = searxng_url

    if engines == "Mixed":
        engines = None

    if categories == 'general':
        params = {
            'q': query,         # Search query
            'format': 'json',   # Output format is JSON
            'language': 'zh',   # Search language
            'engines': engines,
        }
    elif categories == 'science':
        params = {
            'q': query,         # Search query
            'format': 'json',   # Output format is JSON
            'language': 'zh',   # Search language
            'categories': 'science'
        }
    else:
        raise ValueError('Unsupported retrieval type')

    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'X-Forwarded-For': get_auth_ip(),
        'X-Real-IP': get_auth_ip()
    }
    results = []
    response = requests.post(url, params=params, headers=headers, proxies=proxies, timeout=30)
    if response.status_code == 200:
        json_result = response.json()
        for result in json_result['results']:
            item = {
                "title": result.get("title", ""),
                "source": result.get("engines", "unknown"),
                "content": result.get("content", ""),
                "link": result["url"],
            }
            results.append(item)
        return results
    else:
        if response.status_code == 429:
            raise ValueError("Searxng（Online search service）Current user count is too high，Please wait。")
        else:
            raise ValueError("Online search failed，Status code: " + str(response.status_code) + '\t' + response.content.decode('utf-8'))


def scrape_text(url, proxies) -> str:
    """Scrape text from a webpage

    Args:
        url (str): The URL to scrape text from

    Returns:
        str: The scraped text
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Content-Type': 'text/plain',
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=8)
        if response.encoding == "ISO-8859-1": response.encoding = response.apparent_encoding
    except:
        return "Cannot connect to the webpage"
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text


@CatchException
def ConnectToNetworkToAnswerQuestions(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    optimizer_history = history[:-8]
    history = []    # Clear history，To avoid input overflow
    chatbot.append((f"Please answer the following questions based on internet information：{txt}", "Searching..."))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # ------------- < Step 1：Crawl the results of search engines > -------------
    from void_terminal.toolbox import get_conf
    proxies = get_conf('proxies')
    categories = plugin_kwargs.get('categories', 'general')
    searxng_url = plugin_kwargs.get('searxng_url', None)
    engines = plugin_kwargs.get('engine', None)
    optimizer = plugin_kwargs.get('optimizer', "Close")
    if optimizer == "Close":
        urls = searxng_request(txt, proxies, categories, searxng_url, engines=engines)
    else:
        urls = search_optimizer(txt, proxies, optimizer_history, llm_kwargs, optimizer, categories, searxng_url, engines)
    history = []
    if len(urls) == 0:
        chatbot.append((f"Conclusion：{txt}",
                        "[Local Message] Restricted，Unable to retrieve information from searxng! Please try changing the search engine。"))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # ------------- < Step 2：Visit web pages in order > -------------
    max_search_result = 5   # Include results from how many web pages at most
    if optimizer == "Turn on(Enhance)":
        max_search_result = 8
    chatbot.append(["In network retrieval ...", None])
    for index, url in enumerate(urls[:max_search_result]):
        res = scrape_text(url['link'], proxies)
        prefix = f"The{index}search results [From{url['source'][0]}Search] （{url['title'][:25]}）："
        history.extend([prefix, res])
        res_squeeze = res.replace('\n', '...')
        chatbot[-1] = [prefix + "\n\n" + res_squeeze[:500] + "......", None]
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # ------------- < Step 3：ChatGPT synthesis > -------------
    if (optimizer != "Turn on(Enhance)"):
        i_say = f"Extract information from the above search results，Then answer the question：{txt}"
        i_say, history = input_clipping(    # Trim the input，Start trimming from the longest entry，Prevent token explosion
            inputs=i_say,
            history=history,
            max_token_limit=min(model_info[llm_kwargs['llm_model']]['max_token']*3//4, 8192)
        )
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say,
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=history,
            sys_prompt="Please extract information from the given search results，Summarize the two most relevant search results，Then answer the question。"
        )
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update

    #* Or use a search optimizer，This ensures that subsequent questions and answers can read valid historical records
    else:
        i_say = f"Extract from the above search results related to the question：{txt} Related information:"
        i_say, history = input_clipping(    # Trim the input，Start trimming from the longest entry，Prevent token explosion
            inputs=i_say,
            history=history,
            max_token_limit=min(model_info[llm_kwargs['llm_model']]['max_token']*3//4, 8192)
        )
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say,
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=history,
            sys_prompt="Please extract information from the given search results，Summarize the top three most relevant search results"
        )
        chatbot[-1] = (i_say, gpt_say)
        history = []
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update

        # ------------- < Step 4：Answer questions comprehensively > -------------
        i_say = f"Please answer the question based on the above search results：{txt}"
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say,
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=history,
            sys_prompt="Answer the question based on the given search results"
        )
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history)
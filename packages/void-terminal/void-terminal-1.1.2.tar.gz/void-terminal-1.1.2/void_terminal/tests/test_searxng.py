def validate_path():
    import os, sys
    os.path.dirname(__file__)
    root_dir_assume = os.path.abspath(os.path.dirname(__file__) + "/..")
    os.chdir(root_dir_assume)
    sys.path.append(root_dir_assume)
validate_path()  # validate path so you can run from base directory

from void_terminal.toolbox import get_conf
import requests

def searxng_request(query, proxies, categories='general', searxng_url=None, engines=None):
    url = 'http://localhost:50001/'

    if engines is None:
        engine = 'bing,'
    if categories == 'general':
        params = {
            'q': query,         # Search query
            'format': 'json',   # Output format is JSON
            'language': 'zh',   # Search language
            'engines': engine,
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
        'X-Forwarded-For': '112.112.112.112',
        'X-Real-IP': '112.112.112.112'
    }
    results = []
    response = requests.post(url, params=params, headers=headers, proxies=proxies, timeout=30)
    if response.status_code == 200:
        json_result = response.json()
        for result in json_result['results']:
            item = {
                "title": result.get("title", ""),
                "content": result.get("content", ""),
                "link": result["url"],
            }
            print(result['engines'])
            results.append(item)
        return results
    else:
        if response.status_code == 429:
            raise ValueError("Searxng（Online search service）Current user count is too high，Please wait。")
        else:
            raise ValueError("Online search failed，Status code: " + str(response.status_code) + '\t' + response.content.decode('utf-8'))
res = searxng_request("vr environment", None, categories='science', searxng_url=None, engines=None)
print(res)
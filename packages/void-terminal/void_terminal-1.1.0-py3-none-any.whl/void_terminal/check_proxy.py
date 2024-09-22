from loguru import logger

def check_proxy(proxies, return_ip=False):
    import requests
    proxies_https = proxies['https'] if proxies is not None else 'None'
    ip = None
    try:
        response = requests.get("https://ipapi.co/json/", proxies=proxies, timeout=4)
        data = response.json()
        if 'country_name' in data:
            country = data['country_name']
            result = f"Proxy configuration {proxies_https}, Location of the proxy：{country}"
            if 'ip' in data: ip = data['ip']
        elif 'error' in data:
            alternative, ip = _check_with_backup_source(proxies)
            if alternative is None:
                result = f"Proxy configuration {proxies_https}, Location of the proxy：Unknown，IP query frequency is limited"
            else:
                result = f"Proxy configuration {proxies_https}, Location of the proxy：{alternative}"
        else:
            result = f"Proxy configuration {proxies_https}, Proxy data parsing failed：{data}"
        if not return_ip:
            logger.warning(result)
            return result
        else:
            return ip
    except:
        result = f"Proxy configuration {proxies_https}, Timeout when querying the location of the proxy，Proxy may be invalid"
        if not return_ip:
            logger.warning(result)
            return result
        else:
            return ip

def _check_with_backup_source(proxies):
    import random, string, requests
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    try:
        res_json = requests.get(f"http://{random_string}.edns.ip-api.com/json", proxies=proxies, timeout=4).json()
        return res_json['dns']['geo'], res_json['dns']['ip']
    except:
        return None, None

def backup_and_download(current_version, remote_version):
    """
    One-click protocol update：Backup and download
    """
    from void_terminal.toolbox import get_conf
    import shutil
    import os
    import requests
    import zipfile
    os.makedirs(f'./history', exist_ok=True)
    backup_dir = f'./history/backup-{current_version}/'
    new_version_dir = f'./history/new-version-{remote_version}/'
    if os.path.exists(new_version_dir):
        return new_version_dir
    os.makedirs(new_version_dir)
    shutil.copytree('./', backup_dir, ignore=lambda x, y: ['history'])
    proxies = get_conf('proxies')
    try:    r = requests.get('https://github.com/binary-husky/chatgpt_academic/archive/refs/heads/master.zip', proxies=proxies, stream=True)
    except: r = requests.get('https://public.agent-matrix.com/publish/master.zip', proxies=proxies, stream=True)
    zip_file_path = backup_dir+'/master.zip'
    with open(zip_file_path, 'wb+') as f:
        f.write(r.content)
    dst_path = new_version_dir
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        for zip_info in zip_ref.infolist():
            dst_file_path = os.path.join(dst_path, zip_info.filename)
            if os.path.exists(dst_file_path):
                os.remove(dst_file_path)
            zip_ref.extract(zip_info, dst_path)
    return new_version_dir


def patch_and_restart(path):
    """
    One-click protocol update：Overwrite and restart
    """
    from distutils import dir_util
    import shutil
    import os
    import sys
    import time
    import glob
    from void_terminal.shared_utils.colorful import log_yellow, log_green, log_red
    # if not using config_private, move origin config.py as config_private.py
    if not os.path.exists('config_private.py'):
        log_yellow('Since you have not set the config_private.py private configuration，Now move your existing configuration to config_private.py to prevent configuration loss，',
              'In addition, you can always retrieve the old version of the program in the history subfolder。')
        shutil.copyfile('config.py', 'config_private.py')
    path_new_version = glob.glob(path + '/*-master')[0]
    dir_util.copy_tree(path_new_version, './')
    log_green('Code has been updated，Will update pip package dependencies soon...')
    for i in reversed(range(5)): time.sleep(1); log_green(i)
    try:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except:
        log_red('Problem occurred during installation of pip package dependencies，Need to manually install the newly added dependency library `python -m pip install -r requirements.txt`，Then use the regular`python main.py`way to start。')
    log_green('Update completed，You can always retrieve the old version of the program in the history subfolder，Restart after 5 seconds')
    log_red('If restart fails，You may need to manually install new dependencies `python -m pip install -r requirements.txt`，Then use the regular`python main.py`way to start。')
    log_green(' ------------------------------ -----------------------------------')
    for i in reversed(range(8)): time.sleep(1); log_green(i)
    os.execl(sys.executable, sys.executable, *sys.argv)


def get_current_version():
    import json
    try:
        with open('./version', 'r', encoding='utf8') as f:
            current_version = json.loads(f.read())['version']
    except:
        current_version = ""
    return current_version


def auto_update(raise_error=False):
    """
    One-click protocol update：Check version and user feedback
    """
    try:
        from void_terminal.toolbox import get_conf
        import requests
        import json
        proxies = get_conf('proxies')
        try:    response = requests.get("https://raw.githubusercontent.com/binary-husky/chatgpt_academic/master/version", proxies=proxies, timeout=5)
        except: response = requests.get("https://public.agent-matrix.com/publish/version", proxies=proxies, timeout=5)
        remote_json_data = json.loads(response.text)
        remote_version = remote_json_data['version']
        if remote_json_data["show_feature"]:
            new_feature = "New features：" + remote_json_data["new_feature"]
        else:
            new_feature = ""
        with open('./version', 'r', encoding='utf8') as f:
            current_version = f.read()
            current_version = json.loads(current_version)['version']
        if (remote_version - current_version) >= 0.01-1e-5:
            from void_terminal.shared_utils.colorful import log_yellow
            log_yellow(f'\nNew version available。New version:{remote_version}，Current version:{current_version}。{new_feature}')
            logger.info('（1）Github update address:\nhttps://github.com/binary-husky/chatgpt_academic\n')
            user_instruction = input('（2）Update code with one click?（Y+Enter=Confirm，Enter other/No input+Enter=No update）？')
            if user_instruction in ['Y', 'y']:
                path = backup_and_download(current_version, remote_version)
                try:
                    patch_and_restart(path)
                except:
                    msg = 'Update failed。'
                    if raise_error:
                        from void_terminal.toolbox import trimmed_format_exc
                        msg += trimmed_format_exc()
                    logger.warning(msg)
            else:
                logger.info('Automatic update program：Disabled')
                return
        else:
            return
    except:
        msg = 'Automatic update program：Disabled。Suggested troubleshooting：Proxy network configuration。'
        if raise_error:
            from void_terminal.toolbox import trimmed_format_exc
            msg += trimmed_format_exc()
        logger.info(msg)

def warm_up_modules():
    logger.info('Some modules are being preheated ...')
    from void_terminal.toolbox import ProxyNetworkActivate
    from void_terminal.request_llms.bridge_all import model_info
    with ProxyNetworkActivate("Warmup_Modules"):
        enc = model_info["gpt-3.5-turbo"]['tokenizer']
        enc.encode("Module preheating", disallowed_special=())
        enc = model_info["gpt-4"]['tokenizer']
        enc.encode("Module preheating", disallowed_special=())

def warm_up_vectordb():
    logger.info('Some modules are being preheated ...')
    from void_terminal.toolbox import ProxyNetworkActivate
    with ProxyNetworkActivate("Warmup_Modules"):
        import nltk
        with ProxyNetworkActivate("Warmup_Modules"): nltk.download("punkt")


if __name__ == '__main__':
    import os
    os.environ['no_proxy'] = '*'  # Avoid unexpected pollution caused by proxy networks
    from void_terminal.toolbox import get_conf
    proxies = get_conf('proxies')
    check_proxy(proxies)

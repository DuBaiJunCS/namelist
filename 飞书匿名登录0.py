import requests
import requests

def get_anonymous_session():
    url = 'https://ncnjv3qw5wjd.feishu.cn/share/base/view/shrcn0T0NcS3UyFsOAMJqZ9GoeS'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    with requests.Session() as session:
        try:
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # 自动抛出错误请求
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return ""

        # 查找名为 "session" 的 Cookie
        session_cookie = session.cookies.get("session", "")
        return session_cookie or ""

# 示例调用
print(get_anonymous_session())

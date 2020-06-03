import requests
from typing import List

need_fields = 'archived created_at description forks forks_count language name private pushed_at size stargazers_count  updated_at  '.split()


def get_repos(github_token: str) -> List[dict]:
    """
    github的页码是从1开始的

    :param github_token: github的token
    :return: repo列表，list[dict]
    """
    sess = requests.Session()
    # auth的方式已经不鼓励使用了
    sess.headers['Authorization'] = f"token {github_token}"
    sess.headers['Accept'] = 'application/vnd.github.v3+json'
    sess.headers['User-Agent'] = 'Awesome-Octocat-App'
    current_user_url = 'https://api.github.com/user'
    repos_url = 'https://api.github.com/user/repos'
    user = sess.get(current_user_url).json()
    repo_count = user['total_private_repos'] + user['public_repos']
    a = []
    page_size = 100
    for i in range(0, repo_count, page_size):
        response = sess.get(repos_url, params={
            'page': i // page_size + 1,
            'per_page': page_size,
        })
        resp = response.json()
        for repo in resp:
            now = {}
            for k in need_fields:
                now[k] = repo[k]
            a.append(now)
    return a


if __name__ == '__main__':
    res = get_repos()
    print(len(res))

import requests


class Github:
    def __init__(self, github_token):
        self.github_token = github_token
        self.sess = requests.session()
        self.sess.headers['Authorization'] = f"token {self.github_token}"
        self.sess.headers['Accept'] = 'application/vnd.github.v3+json'
        self.sess.headers['User-Agent'] = 'Awesome-Octocat-App'

    def get_user_info(self):
        current_user_url = 'https://api.github.com/user'
        return self.get(current_user_url)

    def get(self, url):
        resp = self.sess.get(url)
        return resp.json()

    def get_list(self, url: str):
        # auth的方式已经不鼓励使用了
        a = []
        page_size = 100
        pageRemaining = True
        current_page = 1
        while pageRemaining:
            response = self.sess.get(url, params={
                'page': current_page,
                'per_page': page_size,
            })
            current_page += 1
            resp = response.json()
            if resp is dict and resp.get('message') == 'Not Found':
                return []
            for repo in resp:
                a.append(repo)
            if len(resp) == 0:
                break
        return a

    def get_repos(self):
        repos_url = 'https://api.github.com/user/repos'
        return self.get_list(repos_url)

    def get_my_repos(self):
        repos = self.get_repos()
        u = self.get_user_info()
        return [i for i in repos if i['full_name'].startswith(u['name'])]

    def get_user_repos(self, username: str):
        repos_url = f"https://api.github.com/users/{username}/repos"
        return self.get_list(repos_url)

import os

from fu import github_api

github_token = os.environ['GITHUB_TOKEN']


def test_user():
    g = github_api.Github(github_token)
    print(g.get_user_info())


def get_my_repos():
    g = github_api.Github(github_token)
    repos = g.get_my_repos()
    print(len(repos))
    print(repos)


def test_repo():
    g = github_api.Github(github_token)
    # repos = g.get_repos()
    repos = g.get_user_repos("jhump")
    print(len(repos))
    print(repos)


get_my_repos()

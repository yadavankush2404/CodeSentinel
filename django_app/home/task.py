from celery import Celery
from celery import shared_task
# from ..django_app.celery import app
from home.utils.github import analyze_pr

@shared_task
def analyse_repo_task(repo_url,pr_num,git_token=None):
    result = analyze_pr(repo_url,pr_num, git_token)
    return result
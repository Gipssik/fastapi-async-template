# Cookiecutter FastAPI Async

This project template was copied from [this repo](https://github.com/anancarv/cookiecutter-fastapi-async/). I just 
changed it a bit.

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for creating a backend using [FastAPI](https://github.com/tiangolo/fastapi) and SQLAlchemy Async ORM.


## Install
First, you need to Install cookiecutter
```bash
pip install cookiecutter
```

Generate a Python package project:
```bash
cookiecutter https://github.com/anancarv/cookiecutter-fastapi-async.git
full_name [Your Name]:
email [you@example.com]:
github_username [your-username]:
...
```

## Create a GitHub Repo
Go to your GitHub account and create a new repo (e.g  test-fastapi) that matches the `project_slug` from your previous answers.
Back to your CLI, you can do the following in the root of your generated project:
```bash
git add .
git commit -m "Initial skeleton."
git remote add origin git@github.com:<MY_USERNAME>/<MY-REPO-SLUG>.git
git push -u origin master
```

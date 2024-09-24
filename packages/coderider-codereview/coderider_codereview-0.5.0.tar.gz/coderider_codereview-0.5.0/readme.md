# CodeRider CodeReview

## How to set up

Copy `.env.example` to `.env`, and set ENV:

```.env
CR_AI_BOT_TOKEN=""
CR_MR_PROJECT_PATH=""
CR_MR_IID=""
```

Install dependencies:

```shell
poetry install
```

## Publish

Update versions of `pyproject.toml` and `coderider_codereview/__init__.py`.

https://pypi.org/project/coderider-codereview/

```shell
poetry build
poetry config pypi-token.pypi <pypi-token>
poetry publish
```

## Use it in local

```shell
pip install coderider_codereview
CR_AI_BOT_TOKEN="" CR_MR_PROJECT_PATH="" CR_MR_IID="" crcr
```

## GitLab CI Template File

https://jihulab.com/-/snippets/6198

```yml
include:
  - remote: 'https://jihulab.com/-/snippets/6198/raw/main/coderider-codereview-0.1.0.yml'
```

## Dependencies

- Vulnerability comments in diff:  GitLab >= 16.5
- Customize analyzer settings: Premium Plan
- Project Access Token: Premium Plan

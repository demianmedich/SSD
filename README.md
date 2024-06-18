# SSD Project

CRA 과정 Final project

## How to use
### 1. venv setup
PyCharm에서 virtualenv 셋업을 별도로 진행할 경우 스킵
```bash
$ pip install virtualenv
$ python -m virtualenv <venv dir>
$ source <venv dir>/bin/activate
```

### 2. 패키지 설치하기
```bash
$ pip install --upgrade pip
$ pip install setuptools  # build backend로 setuptools 사용
$ pip install -e .[dev]  # editable 모드로 설치
```
zsh 사용자의 경우 `.[dev]`를 `".[dev]"`로 수정

### 3. pre-commit 설정하기
통일된 코드 포매터 사용을 강제하기 위해 Commit(또는 push) 전에 black, isort (, pytest)를 강제로 수행하도록 하는 hook을 설정합니다.
```bash
$ pre-commit run --all-files  # 문제없이 실행되는지 확인
$ pre-commit install  # pre-commit 단계 hook 설치 (black, isort)
$ pre-commit -t pre-push  # pre-push 단계 hook 설치 (black, isort, pytest)
```

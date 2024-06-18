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
$ pre-commit install -t pre-push  # pre-push 단계 hook 설치 (black, isort, pytest)
```

## Coding Convention
### PEP8 사용
- 해당 프로젝트에서는 가장 common하게 사용되는 PEP8을 코딩 스타일로 사용합니다.
- 코딩 스타일을 적용하기 위해 pre-commit, black, isort를 사용합니다.
- 커밋을 할 때마다 black, isort가 자동적으로 실행됩니다. 코딩 스타일이 맞지 않다면 자동적으로 해당 툴이 포매팅을 맞춰줍니다. 이 때는 새로 stage 단계로 올리고 다시 커밋을 해주셔야 합니다.
- push 할 때는 tests/unittest 아래에 추가한 TC들을 같이 수행합니다.

### Branch Policy
- main이 기본 브랜치이며 모든 토픽 브랜치들은 아래와 prefix
- 기능 개발용인 경우: feature/ssd
- 버그 수정용인 경우: bugfix/ssd-raise-exception

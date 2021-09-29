# django swagger 테스트 코드

`django rest framework`의 APIView와 `drf-yasg`를 이용한 swagger API 구현

# Setting

## 1. 가상환경 생성 및 접속

```
> python -m venv venv
> venv\Scripts\activate
```

## 2. 라이브러리 설치

```
(venv)> pip install django
(venv)> pip install djangorestframework
(venv)> pip install drf-yasg
```

## 3. DB 생성

```
(venv)> py manage.py makemigrations
(venv)> py manage.py migrate
```


# 실행

## 1. 서버 실행

```
(venv)> py manage.py runserver
```

## 2. 접속

웹브라우저에서 `http://localhost:8000/swagger/` 주소로 접속

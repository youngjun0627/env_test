## 1. challenge 디렉토리
challenge 디렉토리는 유저에게 보여줘야 할 데이터 및 지문을 넣습니다.

#### 디렉토리 구조

```
challenge
ㄴ data 디렉토리
	ㄴ 유저에게 주어질 디렉토리
	ㄴ train.csv
	ㄴ test.csv(테스트 할 과제)
ㄴ ipynb 파일
```

#### 디렉토리 구조 설명

* data 디렉토리: 
	* 유저에게 줄 trian, test input 파일을 넣음
	* **주의** 정답 파일은 여기 넣으면 안 됨
* 문제.ipynb


## 2. evaluate 디렉토리
evaluate 디렉토리에는 정답 파일과 채점 python 파일을 넣습니다.

#### 디렉토리 구조

```
evaluate
ㄴ 정답 csv 파일
ㄴ evaluator.py
ㄴ sample.py(evaluator를 위한 클래스, 메소드 제공) - 
```

#### 디렉토리 구조 설명

* 정답 csv 파일
	* submission.csv 등의 정답 csv 파일
* evaluator.py
	* 유저가 제작한 csv 파일과 정답 csv 파일을 비교하여 채점하는 python 파일
	* 문제에 따라 파일 이름이나 채점 방식이 달라지므로 `evaluator.py`의 내용은 문제별로 수정되어야 합니다.
	* 파일을 어떻게 수정해야하는지는 파일 상단의 주석을 참고하세요.

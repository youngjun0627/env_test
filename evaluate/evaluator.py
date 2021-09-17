# -*- coding: utf-8 -*-

"""
파일의 다음 부분을 바꾸어주세요

1. FILE_NAME을 정답 파일 이름으로 수정해주세요. 이때 '/submission.csv' 와 같이 / 를 앞에 꼭 넣어주세요.
2. INDEX_COLUMNS를 수정해주세요. INDEX_COLUMN이 없는 경우는 []으로 설정하면 됩니다.
"""

FILE_NAME = '/submission.csv'
INDEX_COLUMNS = []

from sample import File_Evaluator

def validate(file_evaluator=None):
    """이 함수는 사용자의 output file의 형식을 체크합니다.
    응시자의 output file을 읽어 파일의 존재여부, column 수, row 수를 확인하세요.
    Returns:
        bool: 형식이 정확하면 True, 아니면 False
        str: 형식이 정확하지 않은 이유
    """
    if not file_evaluator:
        file_evaluator = File_Evaluator(FILE_NAME, INDEX_COLUMNS)
    return file_evaluator.validate()


def evaluate():
    """이 함수는 사용자의 output file을 채점합니다.
    응시자의 output file을 읽어 정답 데이터와 비교하고 정확도(%)를 반환하세요.
    Returns:
        float: 정확도(%)는 0.0부터 100.0 사이의 값을 반환하세요.
    """
    file_evaluator = File_Evaluator(FILE_NAME, INDEX_COLUMNS)
    return file_evaluator.evaluate()

if __name__ == '__main__':
    print('validate:', validate())
    print('evaluate:', evaluate())

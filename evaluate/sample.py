# -*- coding: utf-8 -*-

"""
파일의 다음 부분을 바꾸어주세요
1. evaluate 메소드의 마지막 리턴부분을 적절하게 선택해주세요(아래 설명 참고)
    * return self.calc_accuracy() - 주로 전처리 문제에서 사용(채점기준=완전 일치)
    * return self.calc_r2_score() - 주로 numeric prediction 문제에서 사용(채점기준=r2 score)
    * return self.calc_roc_auc_score() - 주로 binary classification 문제에서 사용(채점기준=roc auc)
"""

import os
import pandas as pd
import glob
import sys
from sklearn.metrics import r2_score, roc_auc_score

class File_Evaluator():
    def __init__(self, file_name, index_columns=[]):
        NOTEBOOK_DIR = os.environ['HOME']
        OUTPUT_DIR = NOTEBOOK_DIR + "/work"

        self.file_name = file_name
        self.file_path = OUTPUT_DIR + file_name
        self.file_got = None
        self.file_expected = None
        self.index_columns = index_columns

    def validate_check_file_exists(self):
        if not os.path.exists(self.file_path):
            return False, f"파일 {self.file_name}가 존재하지 않습니다."
        return True, None

    def validate_read_files(self):
        try:
            self.file_got = pd.read_csv(self.file_path)
            self.file_expected = pd.read_csv('.' + self.file_name)
        except:
            return False, f"파일 {self.file_name}을 읽지 못했습니다. 이유: \n{sys.exc_info()[0]}"
        return True, None

    def validate_check_columns_count(self):
        cols_got = list(map(str.strip, list(self.file_got.columns)))
        cols_expected = list(map(str.strip, list(self.file_expected.columns)))

        if len(cols_expected) <= len(cols_got) <= len(cols_expected) + 1:
            return True, None

        MESSAGE_COLUM_DIFFERENT = f"""파일 {self.file_name}의 컬럼이 예상과 다릅니다.
예상한 컬럼: {', '.join(cols_expected)}
제출한 파일의 컬럼: {', '.join(cols_got)[:64]}"""
        return cols_got == cols_expected, MESSAGE_COLUM_DIFFERENT

    def validate_check_rows_count(self):
        rows_count_got = self.file_got.shape[0]
        rows_count_expected = self.file_expected.shape[0]

        if rows_count_got == rows_count_expected:
            return True, None

        MESSAGE_ROW_DIFFERENT = f"""파일 {self.file_name}의 row 수가 예상과 다릅니다.
예상한 row 수: {rows_count_expected+1}
제출한 파일의 row 수: {rows_count_got+1}"""
        return False, MESSAGE_ROW_DIFFERENT

    def validate(self):
        VALIDATION_FUNCTIONS = [
            self.validate_check_file_exists,
            self.validate_read_files, 
            self.validate_check_columns_count, 
            self.validate_check_rows_count
        ]
        messages = []
        for check_function in VALIDATION_FUNCTIONS:
            valid, message = check_function()
            if not valid:
                messages.append(message)
                break

        return not messages, '\n'.join(messages)

    def refine_dataframe_got(self):
        # column 갯수, 이름, 타입 일치 시키기, 필요없는 컬럼 제거하기
        if len(self.file_got.columns) == len(self.file_expected.columns) + 1:
            self.file_got = self.file_got[self.file_got.columns[1:]].copy()
        self.file_got.columns = list(self.file_expected.columns)
        self.file_got = self.file_got.head(self.file_expected.shape[0])

        for col in self.file_expected.columns:
            try:
                self.file_got[col] = self.file_got[col].astype(self.file_expected[col].dtype.name)
            except:
                pass

    def calc_accuracy(self):
        n_row, n_col = self.file_expected.shape
        total = n_row * (n_col - len(self.index_columns))
        correct = 0
        scoring_columns = self.file_expected.columns.difference(self.index_columns)
        for col in scoring_columns:
            correct += (self.file_expected[col] == self.file_got[col]).sum()
        return 100 * correct / total

    def calc_r2_score(self):
        scoring_columns = self.file_expected.columns.difference(self.index_columns)
        score = 0
        for col in scoring_columns:
            score += r2_score(self.file_expected[col], self.file_got[col]) * 100

        score = score / len(scoring_columns)
        score = min(score, 100)
        score = max(score, 0)
        return score

    def calc_roc_auc_score(self):
        scoring_columns = self.file_expected.columns.difference(self.index_columns)
        score = 0
        for col in scoring_columns:
            score += roc_auc_score(self.file_expected[col], self.file_got[col]) * 100
        return score / len(scoring_columns)

    def evaluate(self):
        valid, message = self.validate()
        if not valid or self.file_expected.shape[0] > self.file_got.shape[0]:
            return 0.0
        try:
            self.refine_dataframe_got()
        except:
            return 0.0

        for col in self.index_columns:
            if (self.file_expected[col] != self.file_got[col]).sum():
                return 0.0

        return self.calc_accuracy() 

# -*- coding: utf-8 -*-

import os
import pandas as pd
import glob
import sys

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

    def validate(self):
        VALIDATION_FUNCTIONS = [
            self.validate_check_file_exists,
            self.validate_read_files, 
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

    def evaluate(self):
        '''
        파일을 검증합니다
        '''
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
        '''
        파일을 채점합니다
        '''
        return self.calc_accuracy() 

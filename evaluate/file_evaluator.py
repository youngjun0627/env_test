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

    '''
    검증 메소드들을 통해 검증합니다
    '''
    def validate(self):
        VALIDATION_FUNCTIONS = []
        messages = []
        for check_function in VALIDATION_FUNCTIONS:
            valid, message = check_function()
            if not valid:
                messages.append(message)
                break

        return not messages, '\n'.join(messages)


    '''
    채점방식에 필요한 메소드입니다
    '''
    def calc_accuracy(self):
        n_row, n_col = self.file_expected.shape
        total = n_row * (n_col - len(self.index_columns))
        correct = 0
        scoring_columns = self.file_expected.columns.difference(self.index_columns)
        for col in scoring_columns:
            correct += (self.file_expected[col] == self.file_got[col]).sum()
        return 100 * correct / total

    '''
    채점 메소드를 사용하여 파일을 채점합니다.
    '''
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

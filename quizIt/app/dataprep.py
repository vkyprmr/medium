"""
Preparing data in the required format
"""
# Imports
import random
import pandas as pd


"""
Developer: vkyprmr
Filename: dataprep.py
Created on: 2020-07-12 at 15:11:30

Modified by: vkyprmr
Modified on: 2023-05-28, Sun, 14:17:00
"""


# Class for generating data in the required format
class GenerateData:
    """ 
        Generate lists of random questions, their choices and answers.
        
        Parameters
        ----------
        df: pd.DataFrame
            DataFrame containing vocabulary
        num_ques: int
            Number of questions to be generated
        form: str
            "German to English" or "English to German"
    """
    def __init__(self, df: pd.DataFrame, num_ques: int, form: str):
        self.df = df
        self.num_ques = num_ques
        self.form = form

    def generate_eng2ger(self):
        """ 
        Generates a list containing question, multiple-choices and 
        answer for English to German.
        
        Returns
        -------
        tuple: tuple
            question, options, answer (in that order)
         """
        question = []
        data_len = len(self.df)+1
        n = random.randint(0, data_len)
        lst = []
        options = []
        for _ in range(3):
            no = random.randint(0, data_len)
            lst.append(no)
        lst.append(n)
        lst = random.sample(lst, len(lst))
        # Creating a question
        question.append(f"German for '{self.df.iloc[n, 1]}' is _______")
        # Creating options/choices
        for l in lst:
            options.append(f"{self.df.iloc[l, 0]}")
        # Allocating the answer
        answer = self.df.iloc[n, 0]

        return question, options, answer

    def generate_ger2eng(self):
        """ 
        Generates a list containing question, multiple-choices and 
        answer for German to English.
        
        Returns
        -------
        tuple: tuple
            question, options, answer (in that order)
         """
        question = []
        data_len = len(self.df)+1
        n = random.randint(0, data_len)
        lst = []
        options = []
        for _ in range(3):
            no = random.randint(0, data_len)
            lst.append(no)
        lst.append(n)
        lst = random.sample(lst, len(lst))
        # Creating the question
        question.append(f"'{self.df.iloc[n, 0]}' heißt _______ auf Englisch.")
        # Creating options/choices
        for l in lst:
            options.append(f"{self.df.iloc[l, 1]}")
        # Allocating the answer
        answer = self.df.iloc[n, 1]

        return question, options, answer

    def collection(self):
        """ 
        Generates a list containing question, multiple-choices and 
        answer based on the given form.
        
        Returns
        -------
        tuple: tuple
            question, options, answer (in that order)
         """
        questions = []
        choice_list = []
        answers = []

        if self.form=="English to German":
            for _ in range(self.num_ques):
                question, options, answer = self.generate_eng2ger()
                questions.append(question)
                choice_list.append(options)
                answers.append(answer)
        else:
            for _ in range(self.num_ques):
                question, options, answer = self.generate_ger2eng()
                questions.append(question)
                choice_list.append(options)
                answers.append(answer)

        return questions, choice_list, answers

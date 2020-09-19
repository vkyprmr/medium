'''
Developer: vkyprmr
Filename: dataprep.py
Created on: 2020-07-12 at 15:11:30
'''
'''
Modified by: vkyprmr
Last modified on: 2020-09-14 at 08:21:51
'''

# Imports
import random

# Class for generating data in the required format


class GenerateData:
    """ 
        Generate lists of random questions, their choices and answers.
         Arguments:
            df: DataFrame containing vocab
            num_ques: Number of questions to be generated
            form: Choose:
                  'The Correct German word' or 'The Correct English word'
    """
    def __init__(self, df, num_ques, form):
        self.df = df
        self.num_ques = num_ques
        self.form = form

    def generate_eng2ger(self):
        """ 
        Generates a list containing question, multiple-choices and answer for English to German.
         Returns:
            question, options, answer (in that order)
         """
        question = []
        data_len = len(self.df)+1
        n = random.randint(0, data_len)
        lst = []
        options = []
        for i in range(3):
            no = random.randint(0, data_len)
            lst.append(no)
        lst.append(n)
        lst = random.sample(lst, len(lst))
        ### Creating the question
        question.append(f'Select a german word for "{self.df.iloc[n, 1]}":')
        ### Creating options/choices
        for l in lst:
            options.append(f'{self.df.iloc[l, 0]}')
        ### Allocating the answer
        answer = self.df.iloc[n, 0]

        return question, options, answer

    def generate_ger2eng(self):
        """ 
        Generates a list containing question, multiple-choices and answer for German to English.
         Returns:
            question, options, answer (in that order)
         """
        question = []
        data_len = len(self.df)+1
        n = random.randint(0, data_len)
        lst = []
        options = []
        for i in range(3):
            no = random.randint(0, data_len)
            lst.append(no)
        lst.append(n)
        lst = random.sample(lst, len(lst))
        ### Creating the question
        question.append(f'Ein Englisches Wort für "{self.df.iloc[n, 0]}" auswählen:')
        ### Creating options/choices
        for l in lst:
            options.append(f'{self.df.iloc[l, 1]}')
        ### Allocating the answer
        answer = self.df.iloc[n, 1]

        return question, options, answer

    def collection(self):
        """ 
        Generates a collection of questions, respective multiple-choices and answers for German to English.
         Returns:
            questions, options, answers (in that order)
         """
        questions = []
        choice_list = []
        answers = []

        if self.form=='The correct German word':
            for i in range(self.num_ques):
                question, options, answer = self.generate_eng2ger()
                questions.append(question)
                choice_list.append(options)
                answers.append(answer)
        else:
            for i in range(self.num_ques):
                question, options, answer = self.generate_ger2eng()
                questions.append(question)
                choice_list.append(options)
                answers.append(answer)

        return questions, choice_list, answers

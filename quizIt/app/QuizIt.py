'''
Developer: vkyprmr
Filename: QuizIt.py
Created on: 2020-07-29 at 13:41:15
'''
'''
Modified by: vkyprmr
Last modified on: 2020-09-14 at 09:02:41
'''

# Imports
import os
import pickle
import PIL
from PIL import ImageTk
import pandas as pd
from datetime import datetime
from dataprep import GenerateData
from tkinter import *
from tkinter import messagebox

# GUI Application

### Preparing the dataframe
df = pd.read_excel('vocab_reduced.xlsm')    # Reading the vocab from an Excel file
df.dropna(inplace=True)     # Droping NaN (empty cells/values)
df.drop_duplicates(subset=['German', 'English'], keep='last', inplace=True)     # Dropping words if they repeat
df.reset_index(inplace=True, drop=True)


### Application Class


class QuizIt:
    """ 
    GUI-based quiz application for learning German/English.
     Arguments:
        master: Requires a tkinter master window
        df: Dataframe containing the vocabulary
     """
    def __init__(self, master, df):
        ### Try to load the score if available else create an empty dictionary
        try:
            with open('scores.pickle', 'rb') as file_scores:
                self.scores_users = pickle.load(file_scores)
        except:
            self.scores_users = {}

        self.score_list = list(self.scores_users)
        self.df = df

        ### Initializing some values
        self.ques_num = 0       # current question number, keeps on incrementing during the quiz
        self.score = 0          # current score, keeps on incrementing(decrements if wrong) during the quiz
        self.ques_opts = [5,10,25,50,100]
        self.form_opts = ['The correct German word', 'The correct English word']

        self.master = master
        self.master.configure(background='white')
        self.masterFrame = Frame(self.master, background='white')
        self.masterFrame.pack(expand=1, fill='both')
        self.home()

    def home(self):
        """ 
        Displaying the home page of the app
         """
        self.img = PIL.Image.open('quizit.png')     # tkinter requires a PhotoImage object
        self.img = ImageTk.PhotoImage(self.img)
        self.img_label = Label(self.masterFrame, image = self.img, background='white')      # Displaying the German Flag at the top of the Application
        self.img_label.pack()
        o = Label(self.masterFrame, background='white')     # Empty space, just for aesthetic reasons
        o.pack()
        self.mot_text = Label(self.masterFrame, text='Good luck learning the language.', background='white', font='Helvetica 12 bold')
        self.mot_text.pack()
        o = Label(self.masterFrame, background='white')     # Empty space, just for aesthetic reasons
        o.pack()
        self.input_frame = Frame(self.masterFrame, background='white')
        self.input_frame.pack()
        self.usr_txt = Label(self.input_frame, text='Username:        ', background='white', font='Helvetica 10')
        self.usr_txt.grid(row=0, column=0)
        self.usr_name = Entry(self.input_frame, background='white')
        self.usr_name.grid(row=0, column=1)
        o = Label(self.input_frame, background='white')     # Empty space, just for aesthetic reasons
        o.grid(row=1, column=0)
        self.what_form = Label(self.input_frame, text='How would you like to learn?     ',  background='white', font='Helvetica 10')
        self.what_form.grid(row=2, column=0)
        self.form_var = StringVar(self.input_frame)
        self.form_var.set(self.form_opts[0])
        self.form_sel = OptionMenu(self.input_frame, self.form_var, *self.form_opts)
        self.form_sel.grid(row=2, column=1)
        self.form_sel.configure(background='white', foreground='black')
        o = Label(self.input_frame, background='white')     # Empty space, just for aesthetic reasons
        o.grid(row=3, column=0)
        self.how_many = Label(self.input_frame, text = 'How many questions would you like to answer?', background ='white')
        self.how_many.grid(row=4, column=0)
        self.num_var = IntVar(self.input_frame)
        self.num_var.set(self.ques_opts[0])
        self.num_ques = OptionMenu(self.input_frame, self.num_var, *self.ques_opts)
        self.num_ques.grid(row=4, column=1)
        self.num_ques.configure(background='white', foreground='black')
        o = Label(self.input_frame, background='white')     # Empty space, just for aesthetic reasons
        o.grid(row=5, column=0)
        self.start_btn = Button(self.input_frame, text='Start', background='white', command=self.start)
        self.start_btn.grid(row=6, column=0)
        self.learn_btn = Button(self.input_frame, text='Learn', background='white', command=self.learn)
        self.learn_btn.grid(row=6, column=1)
        o = Label(self.input_frame, background='white')     # Empty space, just for aesthetic reasons
        o.grid(row=7, column=0)
        self.score_frame = Frame(self.masterFrame, background='white')
        self.score_frame.pack()
        self.error = Label(self.score_frame, text='', background='white')
        self.error.pack()
        self.score_title = Label(self.score_frame, text='Scores', background='white', font='Helvetica 12 bold')
        self.score_title.pack()
        o = Label(self.masterFrame, background='white')        # Empty space, just for aesthetic reasons
        o.pack()
        self.score_lst_frame = Frame(self.masterFrame, background='white')
        self.score_lst_frame.pack()
        self.usr0 = Label(self.score_lst_frame, text='...\t', background='white', font='Helvetica 10')
        self.usr0.grid(row=0, column=0)
        self.score0 = Label(self.score_lst_frame, text='...', background='white', font='Helvetica 10 bold')
        self.score0.grid(row=0, column=1)
        self.usr1 = Label(self.score_lst_frame, text='...\t', background='white', font='Helvetica 10')
        self.usr1.grid(row=1, column=0)
        self.score1 = Label(self.score_lst_frame, text='...', background='white', font='Helvetica 10 bold')
        self.score1.grid(row=1, column=1)
        self.usr2 = Label(self.score_lst_frame, text='...\t', background='white', font='Helvetica 10')
        self.usr2.grid(row=2, column=0)
        self.score2 = Label(self.score_lst_frame, text='...', background='white', font='Helvetica 10 bold')
        self.score2.grid(row=2, column=1)
        self.usr3 = Label(self.score_lst_frame, text='...\t', background='white', font='Helvetica 10')
        self.usr3.grid(row=3, column=0)
        self.score3 = Label(self.score_lst_frame, text='...', background='white', font='Helvetica 10 bold')
        self.score3.grid(row=3, column=1)
        self.usr4 = Label(self.score_lst_frame, text='...\t', background='white', font='Helvetica 10')
        self.usr4.grid(row=4, column=0)
        self.score4 = Label(self.score_lst_frame, text='...', background='white', font='Helvetica 10 bold')
        self.score4.grid(row=4, column=1)
        o = Label(self.masterFrame, background='white')     # Empty space, just for aesthetic reasons
        o.pack()
        self.reset_btn = Button(self.masterFrame, background='white', text='Reset', command=self.reset)
        self.reset_btn.pack()
        o = Label(self.masterFrame, background='white')     # Empty space, just for aesthetic reasons
        o.pack()
        ### Try and load the scores if available. *The scores are stored as a pickle file locallcy
        try:
            self.usr0['text'] = f'{self.scores_list[-1]}'
            self.score0['text'] = f'{self.scores_users[self.scores_list[-1]]}'
        except:
            pass
        try:
            self.usr1['text'] = f'{self.scores_list[-2]}'
            self.score1['text'] = f'{self.scores_users[self.scores_list[-2]]}'
        except:
            pass
        try:
            self.usr2['text'] = f'{self.scores_list[-3]}'
            self.score2['text'] = f'{self.scores_users[self.scores_list[-3]]}'
        except:
            pass
        try:
            self.usr3['text'] = f'{self.scores_list[-4]}'
            self.score3['text'] = f'{self.scores_users[self.scores_list[-4]]}'
        except:
            pass
        try:
            self.usr4['text'] = f'{self.scores_list[-5]}'
            self.score4['text'] = f'{self.scores_users[self.scores_list[-5]]}'
        except:
            pass
        
    def start(self):
        """ 
        Contains the quiz section.
         """
        self.num_quess = self.num_var.get()
        self.form = self.form_var.get()
        self.usr = self.usr_name.get()
        self.end = False
        if self.usr=='' or self.usr.isspace():
            self.error['text'] = 'Please enter a valid username'
            self.error.configure(foreground='red', font='Helvetica 9')
        else:
            self.checked = 0
            self.error['text'] = f''
            self.new_window = Tk()
            self.new_window.geometry('750x250')
            self.new_window.wm_iconbitmap('quizit.ico')
            self.new_window.wm_title('Quiz')
            self.new_window.configure(background='white')
            self.opt_selected = IntVar(self.new_window)
            self.ques = self.create_ques(self.ques_num)
            self.opts =self.create_opts(4)
            self.display_ques(self.ques_num)
            self.f = Frame(self.new_window, background='white')
            self.f.pack(side='bottom')
            o = Label(self.f, text='', background='white')
            o.pack(side='bottom')
            self.frame_btn = Frame(self.new_window, background='white')
            self.frame_btn.pack()
            self.check_btn = Button(self.frame_btn, text="Check all meanings", command=self.check, background = 'white')
            self.check_btn.grid(row=0, column=0)
            o = Label(self.frame_btn, background='white')
            o.grid(row=0, column=1)
            self.next_btn = Button(self.frame_btn, text="Next", command=self.nxt, background = 'white')
            self.next_btn.grid(row=0, column=2)
            o = Label(self.frame_btn, background='white')
            o.grid(row=0, column=3)
            self.quit_btn = Button(self.frame_btn, text="Quit", command=self.quitt, background = 'white')
            self.quit_btn.grid(row=0, column=4)
            self.checked = 0
            self.new_window.protocol("WM_DELETE_WINDOW", self.quitt)

    def create_ques(self, ques_num):
        """ 
        Prepares the question string.
         """
        gd = GenerateData(self.df, self.num_quess, self.form)
        self.questions, self.list_of_options, self.answers = gd.collection()
        self.frame_ques = Frame(self.new_window, background = 'white')
        self.frame_ques.pack()
        self.w = Label(self.frame_ques, text=str(self.questions[ques_num][0]), background = 'white')
        self.w.pack(side='top')
        return self.w

    def create_opts(self, n):
        """ 
        Prepares the options from the collected list of options.
         """
        b_val = 0
        self.b = []
        self.frame_frame = Frame(self.new_window, background='white')
        self.frame_frame.pack()
        self.frame_opt = Frame(self.frame_frame, background = 'white')
        self.frame_opt.pack(side='left')
        self.frame_meaning = Frame(self.frame_frame, background = 'white')
        self.frame_meaning.pack(side='right')
        while b_val < n:
            self.btn = Radiobutton(self.frame_opt, text="foo", variable=self.opt_selected, value=b_val+1, background = 'white')
            self.b.append(self.btn)
            self.btn.grid(row=b_val, column=0, sticky='w', ipadx=100)
            b_val = b_val + 1
        return self.b

    def display_ques(self, ques_num):
        """ 
        Displays the question and the options.
         """
        b_val = 0
        self.opt_selected.set(0)
        self.ques['text'] = str(self.ques_num+1) + '.)  ' + str(self.questions[ques_num][0])
        for op in self.list_of_options[ques_num]:
            self.opts[b_val]['text'] = op
            b_val = b_val + 1

    def actual_meanings(self):
        """ 
        Prepares the meanings of each and every option displayed for that particular question.
         """
        self.opts_new = self.list_of_options[self.ques_num]
        self.meanings = []
        
        if self.form=='The correct German word':
            meaning1 = self.df[self.df['German']==self.opts_new[0]]
            meaning1.reset_index(drop=True,inplace=True)

            meaning2 = self.df[self.df['German']==self.opts_new[1]]
            meaning2.reset_index(drop=True,inplace=True)

            meaning3 = self.df[self.df['German']==self.opts_new[2]]
            meaning3.reset_index(drop=True,inplace=True)

            meaning4 = self.df[self.df['German']==self.opts_new[3]]
            meaning4.reset_index(drop=True,inplace=True)
                
            self.meanings.append(meaning1)
            self.meanings.append(meaning2)
            self.meanings.append(meaning3)
            self.meanings.append(meaning4)
        else:
            meaning1 = self.df[self.df['English']==self.opts_new[0]]
            meaning1.reset_index(drop=True,inplace=True)

            meaning2 = self.df[self.df['English']==self.opts_new[1]]
            meaning2.reset_index(drop=True,inplace=True)

            meaning3 = self.df[self.df['English']==self.opts_new[2]]
            meaning3.reset_index(drop=True,inplace=True)

            meaning4 = self.df[self.df['English']==self.opts_new[3]]
            meaning4.reset_index(drop=True,inplace=True)
                
            self.meanings.append(meaning1)
            self.meanings.append(meaning2)
            self.meanings.append(meaning3)
            self.meanings.append(meaning4)
            print(self.meanings)

    def display_meanings(self):
        """ 
        Displays individual meanings to all the displayed options.
         """
        if self.form=='The correct German word':
            for i in range(0,4):
                self.meanings_text = Label(self.frame_meaning, background='white')
                self.meanings_text['text'] = self.meanings[i].iloc[0,1]
                self.meanings_text.grid(row=i, column=1, sticky='w')
                self.meanings_text.config(font=('Helvetica 10 bold'))
        else:
            for i in range(0,4):
                self.meanings_text = Label(self.frame_meaning, background='white')
                self.meanings_text['text'] = self.meanings[i].iloc[0,0]
                self.meanings_text.grid(row=i, column=1, sticky='w')
                self.meanings_text.config(font=('Helvetica 10 bold'))

    def check_q(self):
        """ 
        Checks wheter the selected option is right or wrong.
         """
        self.opt_sel = self.opt_selected.get()
        self.opt_this = self.list_of_options[self.ques_num]
        self.ans = self.opt_this[self.opt_sel-1]
        if self.opt_sel!=0:
            if self.ans==self.answers[self.ques_num]:
                self.a = 1
            else:
                self.a = 0
            return self.a
        else:
            self.a = 2
            return self.a

    def check(self):
        """ 
        Uses *check_q* and adds to the current score if the answer is right else passes on the current score as it is.
         """
        self.check_q()
        self.actual_meanings()
        if self.a==2:
            self.checked = 0
            self.frame_score = Frame(self.frame_btn, background='white')
            self.frame_score.grid(row=1, columnspan=5)
            self.score_ans = Label(self.frame_score, text = 'Please select an option first', foreground='red', background='white', font='Helvetica 10')
            self.score_ans.pack()
        else:
            try:
                self.frame_score.destroy()
                self.score_ans.destroy()
            except:
                pass
            if self.a==0:
                self.checked = 1
                self.frame_score = Frame(self.frame_btn, background='white')
                self.frame_score.grid(row=1, columnspan=5)
                self.score_ans = Label(self.frame_score, text = 'Wrong', foreground='red', background='white', font='Helvetica 10 bold')
                self.score_ans.pack()
            elif self.a==1:
                self.frame_score = Frame(self.frame_btn, background='white')
                self.frame_score.grid(row=1, columnspan=5)
                self.score_ans = Label(self.frame_score, text = 'Score', foreground='green', background='white', font='Helvetica 10 bold')
                self.score_ans.pack()
                if self.checked==0:
                    self.score+=1
                self.checked = 1

            try:
                self.display_meanings()
            except:
                self.frame_meaning = Frame(self.frame_frame, background = 'white')
                self.frame_meaning.pack(side='right')
                self.display_meanings()

    def nxt(self):
        """ 
        Displays the next Question with options.
         """
        try:
            self.frame_score.destroy()
            self.score_ans.destroy()
            self.frame_meaning.destroy()
        except:
            pass
        self.check_q()
        if self.a==2:
            self.frame_score = Frame(self.frame_btn, background='white')
            self.frame_score.grid(row=1, columnspan=5)
            self.score_ans = Label(self.frame_score, text = 'Please select an option first', foreground='red', background='white', font='Helvetica 10')
            self.score_ans.pack()
        else:
            if self.checked!=1:
                if self.a==1:
                    self.score+=1
                elif self.a==0:
                    self.score = self.score
            else:
                self.score = self.score

            self.ques_num+=1
            if self.ques_num >= len(self.questions):
                self.print_results()
                self.end = True
                self.quitt()
                self.ques_num = 0
                self.score = 0
            else:
                self.end = False
                try:
                    self.frame_score.destroy()
                    self.score_ans.destroy()
                    self.meanings_text.destroy()
                except:
                    pass
                self.display_ques(self.ques_num)

        self.checked = 0
               
    def quitt(self):
        """ 
        Destroys the Quiz window with the entire progress.
         """
        if self.end:
            self.new_window.destroy()
            self.score = 0
            self.ques_num = 0
        else:
            sure = messagebox.askyesno("askyesno", "Your score won't be considered if you quit. Are you sure you want to quit?", parent=self.new_window)
            if sure:
                self.new_window.destroy()
                self.score = 0
                self.ques_num = 0
        
    def print_results(self):
        self.scores_users[f'{self.usr} on {datetime.now().strftime("%m/%d/%Y at %H:%M:%S")} scored'] = f'{self.score} out of {self.num_quess} in the form of {self.form}'
        with open('scores.pickle', 'wb') as file_scores:
            pickle.dump(self.scores_users, file_scores)
        with open('scores.pickle', 'rb') as file_scores:
            self.scores_users = pickle.load(file_scores)
            self.scores_list = list(self.scores_users)
            try:
                self.usr0['text'] = f'{self.scores_list[-1]}'
                self.score0['text'] = f'{self.scores_users[self.scores_list[-1]]}'
            except:
                pass
            try:
                self.usr1['text'] = f'{self.scores_list[-2]}'
                self.score1['text'] = f'{self.scores_users[self.scores_list[-2]]}'
            except:
                pass
            try:
                self.usr2['text'] = f'{self.scores_list[-3]}'
                self.score2['text'] = f'{self.scores_users[self.scores_list[-3]]}'
            except:
                pass
            try:
                self.usr3['text'] = f'{self.scores_list[-4]}'
                self.score3['text'] = f'{self.scores_users[self.scores_list[-4]]}'
            except:
                pass
            try:
                self.usr4['text'] = f'{self.scores_list[-5]}'
                self.score4['text'] = f'{self.scores_users[self.scores_list[-5]]}'
            except:
                pass

    def reset(self):
        sure = messagebox.askyesno("askyesno", "Are you sure you want to reset the scores?")
        if sure==True:
            self.scores_users = {}
            with open('scores.pickle', 'wb') as file_scores:
                pickle.dump(self.scores_users, file_scores)
            self.usr0['text'] = '...'
            self.score0['text']= '...'
            self.usr1['text'] = '...'
            self.score1['text']= '...'
            self.usr2['text'] = '...'
            self.score2['text']= '...'
            self.usr3['text'] = '...'
            self.score3['text']= '...'
            self.usr4['text'] = '...'
            self.score4['text']= '...'

    def learn(self):
        os.startfile('vocab_reduced.pdf')



# Run
root = Tk()
app = QuizIt(root, df)
root.wm_iconbitmap('quizit.ico')
root.wm_title('QuizIt')
root.mainloop()

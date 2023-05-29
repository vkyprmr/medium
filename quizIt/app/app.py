"""
A Tkinter based GUI for a Quiz App.
"""

# Imports
import subprocess
import pickle
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import pandas as pd
from dataprep import GenerateData


"""
Developer: vkyprmr
Filename: app.py
Created on: 2020-07-29 at 13:41:15

Modified by: vkyprmr
Modified on: 2023-05-28, Sun, 16:54:00
"""


# class GermanQuest
class GermanQuest:
    """ 
    GUI-based quiz application for learning German/English.
    
    Parameters
    ----------
        master: Tk
            A tkinter master window
        df: pd.DataFrame
            Dataframe containing the vocabulary
    """

    def __init__(self, master: Tk, df: pd.DataFrame):
        # Try to load the score if available else create an empty dictionary
        try:
            with open("scores.pickle", "rb") as file_scores:
                self.scores_users = pickle.load(file_scores)
        except FileNotFoundError:
            self.scores_users = {
                "times": [],
                "users": [],
                "scores": [],
                "forms": []
            }

        self.score_list = list(self.scores_users)
        self.df = df

        # Initializing some values
        self.ques_num = 0  # current question number, keeps on incrementing
        self.score = 0  # current score, keeps on incrementing/decrementing
        self.ques_opts = [5, 10, 25, 50, 100]
        self.form_opts = ["English to German", "German to English"]

        self.master = master
        self.master.configure(background="#323232")
        self.masterFrame = Frame(self.master, background="#323232")
        self.masterFrame.pack(expand=1, fill="both")
        self.home()

    # Home
    def home(self):
        """
        Home
        """
        self.ip_part()
        self.display_scores()

    # Input part of the app
    def ip_part(self):
        """ 
        Displaying the home page of the app
        """
        o = Label(self.masterFrame, background="#323232")  # Empty space
        o.pack()
        text = "Welcome to self. Good luck learning the language."
        self.mot_text = Label(self.masterFrame, 
                                     text=text, 
                                     background="#323232",
                                     font="Helvetica 14")
        self.mot_text.pack()
        o = Label(self.masterFrame, background="#323232")  # Empty space
        o.pack()
        self.input_frame = Frame(self.masterFrame, background="#323232")
        self.input_frame.pack()
        self.usr_txt = Label(self.input_frame, text="Username:        ", 
                             background="#323232", font="Helvetica 12")
        self.usr_txt.grid(row=0, column=0)
        self.usr_name = Entry(self.input_frame, background="white",
                              foreground="black")
        self.usr_name.grid(row=0, column=1)
        o = Label(self.input_frame, background="#323232")  # Empty space
        o.grid(row=1, column=0)
        self.what_form = Label(self.input_frame, 
                               text="How would you like to learn?     ", 
                               background="#323232",
                               font="Helvetica 12")
        self.what_form.grid(row=2, column=0)
        self.form_var = StringVar(self.input_frame)
        self.form_var.set(self.form_opts[0])
        self.form_sel = OptionMenu(self.input_frame, self.form_var, 
                                   *self.form_opts)
        self.form_sel.grid(row=2, column=1)
        self.form_sel.configure(background="#323232", foreground="#323232")
        o = Label(self.input_frame, background="#323232")  # Empty space
        o.grid(row=3, column=0)
        self.how_many = Label(self.input_frame, 
                              text="How many questions would you like to answer?", 
                              background="#323232")
        self.how_many.grid(row=4, column=0)
        self.num_var = IntVar(self.input_frame)
        self.num_var.set(self.ques_opts[0])
        self.num_ques = OptionMenu(self.input_frame, self.num_var, 
                                   *self.ques_opts)
        self.num_ques.grid(row=4, column=1)
        self.num_ques.configure(background="#323232", foreground="#323232")
        o = Label(self.input_frame, background="#323232")  # Empty space
        o.grid(row=5, column=0)
        self.start_btn = Button(self.input_frame, text="Start", 
                                background="#323232", command=self.start)
        self.start_btn.grid(row=6, column=0)
        self.learn_btn = Button(self.input_frame, text="Learn", 
                                background="#323232", command=self.learn)
        self.learn_btn.grid(row=6, column=1)
        o = Label(self.input_frame, background="#323232")  # Empty space
        o.grid(row=7, column=0)
        self.score_frame = Frame(self.masterFrame, background="#323232")
        self.score_frame.pack()
        self.error = Label(self.score_frame, text="", background="#323232")
        self.error.pack()
        self.score_title = Label(self.score_frame, text="LEADERBOARD", 
                                 background="#323232", font="Helvetica 12 bold")
        self.score_title.pack()

    # Scores
    def display_scores(self):
        o = Label(self.masterFrame, background="#323232")  # Empty space
        o.pack()
        self.score_lst_frame = Frame(self.masterFrame, background="#323232")
        self.score_lst_frame.pack()

        self.time_title = Label(self.score_lst_frame, text="TIME", 
                                background="#323232", font="Helvetica 12 bold")
        self.time_title.grid(row=0, column=3)

        self.user_title = Label(self.score_lst_frame, text="USER", 
                                background="#323232", font="Helvetica 12 bold")
        self.user_title.grid(row=0, column=1)

        self.score_title = Label(self.score_lst_frame, text="SCORE", 
                            background="#323232", font="Helvetica 12 bold")
        self.score_title.grid(row=0, column=2)

        self.form_title = Label(self.score_lst_frame, text="FORM", 
                            background="#323232", font="Helvetica 12 bold")
        self.form_title.grid(row=0, column=0)

        self.time0 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.usr0 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.score0 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.form0 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.time0.grid(row=1, column=3)
        self.usr0.grid(row=1, column=1)
        self.score0.grid(row=1, column=2)
        self.form0.grid(row=1, column=0)
        
        self.time1 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.usr1 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.score1 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.form1 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.time1.grid(row=2, column=3)
        self.usr1.grid(row=2, column=1)
        self.score1.grid(row=2, column=2)
        self.form1.grid(row=2, column=0)

        self.time2 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.usr2 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.score2 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.form2 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.time2.grid(row=3, column=3)
        self.usr2.grid(row=3, column=1)
        self.score2.grid(row=3, column=2)
        self.form2.grid(row=3, column=0)

        self.time3 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.usr3 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.score3 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.form3 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.time3.grid(row=4, column=3)
        self.usr3.grid(row=4, column=1)
        self.score3.grid(row=4, column=2)
        self.form3.grid(row=4, column=0)

        self.time4 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.usr4 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.score4 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.form4 = Label(self.score_lst_frame, text="", 
                          background="#323232", font="Helvetica 12")
        self.time4.grid(row=4, column=3)
        self.usr4.grid(row=4, column=1)
        self.score4.grid(row=4, column=2)
        self.form4.grid(row=4, column=0)

        o = Label(self.masterFrame, background="#323232")  # Empty space
        o.pack()
        self.reset_btn = Button(self.masterFrame, background="#323232", 
                                text="Reset", command=self.reset)
        self.reset_btn.pack()
        o = Label(self.masterFrame, background="#323232")  # Empty space
        o.pack()
        # Try and load the scores if available. The scores are stored as a pickle file locallcy
        try:
            self.time0["text"] = f"{self.scores_users['times'][-1]}"
            self.usr0["text"] = f"{self.scores_users['users'][-1]}"
            self.score0["text"] = f"{self.scores_users['scores'][-1]}"
            self.form0["text"] = f"{self.scores_users['forms'][-1]}"
        except (IndexError, AttributeError):
            pass
        try:
            self.time1["text"] = f"{self.scores_users['times'][-2]}"
            self.usr1["text"] = f"{self.scores_users['users'][-2]}"
            self.score1["text"] = f"{self.scores_users['scores'][-2]}"
            self.form1["text"] = f"{self.scores_users['forms'][-2]}"
        except (IndexError, AttributeError):
            pass
        try:
            self.time2["text"] = f"{self.scores_users['times'][-3]}"
            self.usr2["text"] = f"{self.scores_users['users'][-3]}"
            self.score2["text"] = f"{self.scores_users['scores'][-3]}"
            self.form2["text"] = f"{self.scores_users['forms'][-3]}"
        except (IndexError, AttributeError):
            pass
        try:
            self.time3["text"] = f"{self.scores_users['times'][-4]}"
            self.usr3["text"] = f"{self.scores_users['users'][-4]}"
            self.score3["text"] = f"{self.scores_users['scores'][-4]}"
            self.form3["text"] = f"{self.scores_users['forms'][-4]}"
        except (IndexError, AttributeError):
            pass
        try:
            self.time4["text"] = f"{self.scores_users['times'][-5]}"
            self.usr4["text"] = f"{self.scores_users['users'][-5]}"
            self.score4["text"] = f"{self.scores_users['scores'][-5]}"
            self.form4["text"] = f"{self.scores_users['forms'][-5]}"
        except (IndexError, AttributeError):
            pass

    # Start Quiz
    def start(self):
        """ 
        Start the quiz.
        """
        self.num_quess = self.num_var.get()
        self.form = self.form_var.get()
        self.usr = self.usr_name.get()
        self.end = False
        if self.usr == "" or self.usr.isspace():
            self.error["text"] = "Please enter a valid username"
            self.error.configure(foreground="red", font="Helvetica 9")
        else:
            self.checked = 0
            self.error["text"] = ""
            self.new_window = Tk()
            self.new_window.geometry("750x250")
            self.new_window.wm_iconbitmap("self.ico")
            self.new_window.wm_title("Quiz")
            self.new_window.configure(background="#323232")
            self.opt_selected = IntVar(self.new_window)
            self.ques = self.create_ques(self.ques_num)
            self.opts = self.create_opts(4)
            self.display_ques(self.ques_num)
            self.f = Frame(self.new_window, background="#323232")
            self.f.pack(side="bottom")
            o = Label(self.f, text="", background="#323232")
            o.pack(side="bottom")
            self.frame_btn = Frame(self.new_window, background="#323232")
            self.frame_btn.pack()
            self.check_btn = Button(self.frame_btn, text="Check all meanings", 
                                    command=self.check, background="#323232")
            self.check_btn.grid(row=0, column=0)
            o = Label(self.frame_btn, background="#323232")
            o.grid(row=0, column=1)
            self.next_btn = Button(self.frame_btn, text="Next", 
                                   command=self.nxt, background="#323232")
            self.next_btn.grid(row=0, column=2)
            o = Label(self.frame_btn, background="#323232")
            o.grid(row=0, column=3)
            self.quit_btn = Button(self.frame_btn, text="Quit", 
                                   command=self.quitt, background="#323232")
            self.quit_btn.grid(row=0, column=4)
            self.checked = 0
            self.new_window.protocol("WM_DELETE_WINDOW", self.quitt)

    # Creating questions
    def create_ques(self, ques_num):
        """ 
        Prepares the question.
        """
        gd = GenerateData(self.df, self.num_quess, self.form)
        self.questions, self.list_of_options, self.answers = gd.collection()
        self.frame_ques = Frame(self.new_window, background="#323232")
        self.frame_ques.pack()
        w = Label(self.frame_ques, text=str(self.questions[ques_num][0]), background="#323232")
        w.pack(side="top")
        return w

    # Create options
    def create_opts(self, n):
        """ 
        Prepares the options from the collected list of options.
        """
        b_val = 0
        b = []
        self.frame_frame = Frame(self.new_window, background="#323232")
        self.frame_frame.pack()
        self.frame_opt = Frame(self.frame_frame, background="#323232")
        self.frame_opt.pack(side="left")
        self.frame_meaning = Frame(self.frame_frame, background="#323232")
        self.frame_meaning.pack(side="right")
        while b_val < n:
            btn = Radiobutton(self.frame_opt, text="foo", 
                              variable=self.opt_selected, value=b_val + 1,
                              background="#323232")
            b.append(btn)
            btn.grid(row=b_val, column=0, sticky="w", ipadx=10)
            b_val = b_val + 1
        return b

    # Display questions
    def display_ques(self, ques_num):
        """ 
        Displays the question and the options.
        """
        b_val = 0
        self.opt_selected.set(0)
        self.ques["text"] = f"{self.ques_num + 1}. {self.questions[ques_num][0]}"
        for op in self.list_of_options[ques_num]:
            self.opts[b_val]["text"] = op
            b_val = b_val + 1

    # Actual Meanings
    def actual_meanings(self):
        """ 
        Prepares the meanings of each and every option displayed for 
        that particular question.
        """
        self.opts_new = self.list_of_options[self.ques_num]
        self.meanings = []

        if self.form == "English to German":
            meaning1 = self.df[self.df["German"] == self.opts_new[0]]
            meaning1.reset_index(drop=True, inplace=True)

            meaning2 = self.df[self.df["German"] == self.opts_new[1]]
            meaning2.reset_index(drop=True, inplace=True)

            meaning3 = self.df[self.df["German"] == self.opts_new[2]]
            meaning3.reset_index(drop=True, inplace=True)

            meaning4 = self.df[self.df["German"] == self.opts_new[3]]
            meaning4.reset_index(drop=True, inplace=True)

            self.meanings.append(meaning1)
            self.meanings.append(meaning2)
            self.meanings.append(meaning3)
            self.meanings.append(meaning4)
        else:
            meaning1 = self.df[self.df["English"] == self.opts_new[0]]
            meaning1.reset_index(drop=True, inplace=True)

            meaning2 = self.df[self.df["English"] == self.opts_new[1]]
            meaning2.reset_index(drop=True, inplace=True)

            meaning3 = self.df[self.df["English"] == self.opts_new[2]]
            meaning3.reset_index(drop=True, inplace=True)

            meaning4 = self.df[self.df["English"] == self.opts_new[3]]
            meaning4.reset_index(drop=True, inplace=True)

            self.meanings.append(meaning1)
            self.meanings.append(meaning2)
            self.meanings.append(meaning3)
            self.meanings.append(meaning4)

    # Display meaning
    def display_meanings(self):
        """ 
        Displays individual meanings to all the displayed options.
        """
        if self.form == "English to German":
            for i in range(0, 4):
                new_opt = f"{self.opts[i]['text']}: {self.meanings[i].iloc[0, 1]}"
                self.opts[i]["text"] = new_opt
        else:
            for i in range(0, 4):
                new_opt = f"{self.opts[i]['text']}: {self.meanings[i].iloc[0, 0]}"
                self.opts[i]["text"] = new_opt

    # Check answer
    def check_q(self):
        """ 
        Checks wheter the selected option is right or wrong.
        """
        self.opt_sel = self.opt_selected.get()
        self.opt_this = self.list_of_options[self.ques_num]
        self.ans = self.opt_this[self.opt_sel - 1]
        if self.opt_sel != 0:
            if self.ans == self.answers[self.ques_num]:
                return 1
            return 0
        return 2

    # Check answer and display meanings
    def check(self):
        """ 
        Uses `check_q` and adds to the current score if the answer is 
        right else passes on the current score as it is.
        """
        a = self.check_q()
        self.actual_meanings()
        if a == 2:
            self.checked = 0
            self.frame_score = Frame(self.frame_btn, background="#323232")
            self.frame_score.grid(row=1, columnspan=5)
            self.score_ans = Label(self.frame_score, 
                                   text="Please select an option first", 
                                   foreground="red",
                                   background="#323232", font="Helvetica 12")
            self.score_ans.pack()
        else:
            try:
                self.frame_score.destroy()
                self.score_ans.destroy()
            except Exception:
                pass
            if a == 0:
                self.checked = 1
                self.frame_score = Frame(self.frame_btn, background="#323232")
                self.frame_score.grid(row=1, columnspan=5)
                self.score_ans = Label(self.frame_score, text="WRONG", 
                                       foreground="red", background="#323232",
                                       font="Helvetica 12 bold")
                self.score_ans.pack()
            elif a == 1:
                self.frame_score = Frame(self.frame_btn, background="#323232")
                self.frame_score.grid(row=1, columnspan=5)
                self.score_ans = Label(self.frame_score, text="SCORE", 
                                       foreground="green", background="#323232",
                                       font="Helvetica 12 bold")
                self.score_ans.pack()
                if self.checked == 0:
                    self.score += 1
                self.checked = 1

            try:
                self.display_meanings()
            except Exception:
                self.frame_meaning = Frame(self.frame_frame, background="#323232")
                self.frame_meaning.pack(side="right")
                self.display_meanings()

    # Next question
    def nxt(self):
        """ 
        Displays the next Question with options.
        """
        try:
            self.frame_score.destroy()
            self.score_ans.destroy()
            self.frame_meaning.destroy()
        except Exception:
            pass

        a = self.check_q()
        if a == 2:
            self.frame_score = Frame(self.frame_btn, background="#323232")
            self.frame_score.grid(row=1, columnspan=5)
            self.score_ans = Label(self.frame_score, 
                                   text="Please select an option first", foreground="red",
                                   background="#323232", font="Helvetica 12")
            self.score_ans.pack()
        else:
            if self.checked != 1:
                if a == 1:
                    self.score += 1
                elif a == 0:
                    self.score = self.score
            else:
                self.score = self.score

            self.ques_num += 1
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
                except Exception:
                    pass
                self.display_ques(self.ques_num)

        self.checked = 0

    # Quit
    def quitt(self):
        """ 
        Destroys the Quiz window with the entire progress.
         """
        if self.end:
            self.new_window.destroy()
            self.score = 0
            self.ques_num = 0
        else:
            txt = "Your score won't be considered if you quit. Are you sure you want to quit?"
            sure = messagebox.askyesno("askyesno", txt, parent=self.new_window)
            if sure:
                self.new_window.destroy()
                self.score = 0
                self.ques_num = 0

    # Print the results
    def print_results(self):
        self.scores_users["times"].append(f"{datetime.now().strftime('%m/%d/%Y (%H:%M:%S)')}")
        self.scores_users["users"].append(self.usr)
        self.scores_users["scores"].append(f"{self.score}/{self.num_quess}")
        self.scores_users["forms"].append(self.form)
        
        with open("scores.pickle", "wb") as file_scores:
            pickle.dump(self.scores_users, file_scores)

        try:
            self.time0["text"] = f"{self.scores_users['times'][-1]}"
            self.usr0["text"] = f"{self.scores_users['users'][-1]}"
            self.score0["text"] = f"{self.scores_users['scores'][-1]}"
            self.form0["text"] = f"{self.scores_users['forms'][-1]}"
        except (IndexError, AttributeError):
            pass
        try:
            self.time1["text"] = f"{self.scores_users['times'][-2]}"
            self.usr1["text"] = f"{self.scores_users['users'][-2]}"
            self.score1["text"] = f"{self.scores_users['scores'][-2]}"
            self.form1["text"] = f"{self.scores_users['forms'][-2]}"
        except (IndexError, AttributeError):
            pass
        try:
            self.time2["text"] = f"{self.scores_users['times'][-3]}"
            self.usr2["text"] = f"{self.scores_users['users'][-3]}"
            self.score2["text"] = f"{self.scores_users['scores'][-3]}"
            self.form2["text"] = f"{self.scores_users['forms'][-3]}"
        except (IndexError, AttributeError):
            pass
        try:
            self.time3["text"] = f"{self.scores_users['times'][-4]}"
            self.usr3["text"] = f"{self.scores_users['users'][-4]}"
            self.score3["text"] = f"{self.scores_users['scores'][-4]}"
            self.form3["text"] = f"{self.scores_users['forms'][-4]}"
        except (IndexError, AttributeError):
            pass
        try:
            self.time4["text"] = f"{self.scores_users['times'][-5]}"
            self.usr4["text"] = f"{self.scores_users['users'][-5]}"
            self.score4["text"] = f"{self.scores_users['scores'][-5]}"
            self.form4["text"] = f"{self.scores_users['forms'][-5]}"
        except (IndexError, AttributeError):
            pass

    # Reset Scores
    def reset(self):
        sure = messagebox.askyesno("askyesno", "Are you sure you want to reset the scores?")
        if sure == True:
            self.scores_users = {
                "times": [],
                "users": [],
                "scores": [],
                "forms": []
            }
            with open("scores.pickle", "wb") as file_scores:
                pickle.dump(self.scores_users, file_scores)

            self.time0["text"] = ""
            self.usr0["text"] = ""
            self.score0["text"] = ""
            self.form0["text"] = ""
            self.time1["text"] = ""
            self.usr1["text"] = ""
            self.score1["text"] = ""
            self.form1["text"] = ""
            self.time2["text"] = ""
            self.usr2["text"] = ""
            self.score2["text"] = ""
            self.form2["text"] = ""
            self.time3["text"] = ""
            self.usr3["text"] = ""
            self.score3["text"] = ""
            self.form3["text"] = ""
            self.time4["text"] = ""
            self.usr4["text"] = ""
            self.score4["text"] = ""
            self.form4["text"] = ""

    def learn(self):
        subprocess.call(["open", "vocab_reduced.pdf"])


# Run
if __name__ == "__main__":
    # Preparing the dataframe
    dataframe = pd.read_excel('vocab_reduced.xlsm')  # Reading the vocab from an Excel file
    dataframe.dropna(inplace=True)  # Droping NaN (empty cells/values)
    dataframe.drop_duplicates(subset=['German', 'English'], keep='last', inplace=True)  # Dropping words if they repeat
    dataframe.reset_index(inplace=True, drop=True)

    root = Tk()
    app = GermanQuest(root, dataframe)
    root.wm_iconbitmap("self.ico")
    root.wm_title("GermanQuest")
    root.mainloop()

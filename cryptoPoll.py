#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
#os.system('pip install --upgrade pip')
#os.system('pip install mysql.connector')
#os.system('pip install pycryptodome')
#os.system('pip install simple-crypt --no-dependencies')


# In[2]:


import tkinter as tk
from tkinter import ttk
import mysql.connector
from simplecrypt import encrypt, decrypt
#import os
import secrets


# In[3]:



mydb = mysql.connector.connect(
    host="snf-16955.ok-kno.grnetcloud.net",
    user="root",
    port='3306',
    password="crypto2021",
    database="cryptoPollDb"
)

mycursor = mydb.cursor()

print(mycursor)


# In[31]:


#___FUNCTIONS___________________________________________________________________

#___SHOW PAGE FUNCTION__________________________________________________________
def showPage(currentPage, targetPage):
    currentPage.pack_forget()
    targetPage.pack()
#_______________________________________________________________________________

#___LOGIN FUNCTION______________________________________________________________
def login():
    try:
        mydb = mysql.connector.connect(
            host="snf-16955.ok-kno.grnetcloud.net",
            user="root",
            port='3306',
            password="crypto2021",
            database="cryptoPollDb"
        )
        mycursor = mydb.cursor()
    except mysql.connector.Error as error:
        connectionError()

    username = usernameEntry.get()
    password = passwordEntry.get()

    try:
        sql = "SELECT *FROM user WHERE username=%s AND password=%s"
        val = (username,password)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        if myresult == []:
            loginError()
        else:
            showPage(loginPage, mainPage)
            #print(username, globalUsername)
    except mysql.connector.Error as error:
        connectionError()
    #print(username, password)

#_______________________________________________________________________________

#___SIGN UP FUNCTION____________________________________________________________
def signUp():
    try:
        mydb = mysql.connector.connect(
            host="snf-16955.ok-kno.grnetcloud.net",
            user="root",
            port='3306',
            password="crypto2021",
            database="cryptoPollDb"
        )
        mycursor = mydb.cursor()
    except mysql.connector.Error as error:
        connectionError()

    username = usernameEntryReg.get()
    password = passwordEntryReg.get()
    confirmPassword = confirmPasswordEntryReg.get()

    if password != confirmPassword:
        openWrongPass()
    #print(username, password)
    elif password == confirmPassword:
        try:
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            val = (username, password)
            mycursor.execute(sql, val)
            mydb.commit()
            #connectionSuccess()
            secretWindow(username)
        except mysql.connector.Error as error:
            connectionError()

#_______________________________________________________________________________

#_______________________________________________________________________________
def logout():
    mycursor.close()
    globalUsername = None
    showPage(mainPage, loginPage)
#_______________________________________________________________________________

#___WRONG PASSWORD OPEN WINDOW FUNCTION_________________________________________
def openWrongPass():
    newWindow = tk.Toplevel(root)
    newWindow.title("Password Error")
    newWindow.geometry("200x50")
    tk.Label(newWindow, text ="Passwords do not match").pack()
    okButton = tk.Button(newWindow, text="OK", command=lambda: newWindow.destroy()).pack()
#_______________________________________________________________________________

#___CONNECTION ERROR OPEN WINDOW FUNCTION_______________________________________
def connectionError():
    newWindow = tk.Toplevel(root)
    newWindow.title("Connection Error")
    newWindow.geometry("200x60")
    tk.Label(newWindow, text ="Cannot connect to database\nor do what you asked").pack()
    okButton = tk.Button(newWindow, text="OK", command=lambda: newWindow.destroy()).pack()
#_______________________________________________________________________________

#___DATABASE SUCCESS WINDOW FUNCTION____________________________________________
def connectionSuccess():
    newWindow = tk.Toplevel(root)
    newWindow.title("Connection Success")
    newWindow.geometry("200x50")
    tk.Label(newWindow, text ="Changes were successfully done!").pack()
    okButton = tk.Button(newWindow, text="OK", command=lambda: newWindow.destroy()).pack()
#_______________________________________________________________________________

#___LOGIN ERROR WINDOW FUNCTION_________________________________________________
def loginError():
    newWindow = tk.Toplevel(root)
    newWindow.title("Login error")
    newWindow.geometry("200x50")
    tk.Label(newWindow, text ="Invalid Credentials").pack()
    okButton = tk.Button(newWindow, text="OK", command=lambda: newWindow.destroy()).pack()
#_______________________________________________________________________________

#___GENERATE SECRET KEY AND STRING WINDOW_______________________________________
def secretWindow(user):
    secWindow = tk.Toplevel(root)
    secWindow.title("Secret Window")
    secWindow.geometry("200x80")
    tk.Label(secWindow, text ="Changes were successfully done!").pack()
    tk.Label(secWindow, text ="Give a secret string").pack()
    e = tk.Entry(secWindow, width=30)
    e.pack()
    secretKey = secrets.token_urlsafe(16)
    f = open("cipherKey.txt", "w")
    f.write(secretKey)
    f.close()
    #f = open("cipherString.txt", "w")
    #myString = e.get()
    #f.write(e.get())
    #f.close()
    #___ENCRYPT_________________________________
    #ciphertext = encrypt(secretKey, myString)

    okButton = tk.Button(secWindow, text="OK", command=lambda: stringAndDestroy(e, secWindow, user, secretKey)).pack()
#_______________________________________________________________________________

#___STRING AND DESTROY__________________________________________________________
def stringAndDestroy(entry, window, user, secretKey):
    f = open("cipherString.txt", "w")
    InputString = entry.get()
    f.write(InputString)
    f.close()
    ciphertext = encrypt(secretKey, InputString)
    #ciphertext = ciphertext.decode("utf-8")
    print(ciphertext)
    print(user)
    try:
        mydb = mysql.connector.connect(
            host="snf-16955.ok-kno.grnetcloud.net",
            user="root",
            port='3306',
            password="crypto2021",
            database="cryptoPollDb"
        )
        mycursor = mydb.cursor()
        sql = "UPDATE user SET cipherKey=%s WHERE username=%s"
        val = (ciphertext,user)
        print(val)
        mycursor.execute(sql, val)
        mydb.commit()
        connectionSuccess()
    except mysql.connector.Error as error:
        connectionError()
    window.destroy()
#______________________________________________________________________________________

#___CREATE QUESTION FUNCTION___________________________________________________________
def createPollQuestion():
    try:
        mydb = mysql.connector.connect(
            host="snf-16955.ok-kno.grnetcloud.net",
            user="root",
            port='3306',
            password="crypto2021",
            database="cryptoPollDb"
        )
        mycursor = mydb.cursor()
    except mysql.connector.Error as error:
        connectionError()

    question = questionEntry.get()
    print(question)

    try:
        sql = "SELECT *FROM poll"
        val = question
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        print(myresult)
    except mysql.connector.Error as error:
        connectionError()

    if myresult == []:
        try:
            sql = "INSERT INTO poll (IDpoll, question) VALUES (%s, %s)"
            val = (1, question)
            mycursor.execute(sql, val)
            mydb.commit()
            #___INSERT ANSWERS__________________
            answers = answersEntry.get()
            answers = answers.split(',', 10)
            for i in range(0, len(answers), 1):
                answers[i] = answers[i].strip(' ')
            print(answers)

            nextIDans = 0
            for i in range(0, len(answers), 1):
                sql = "INSERT INTO answer (idanswer, answerText, poll_IDpoll) VALUES (%s,%s,%s)"
                nextIDans = nextIDans + 1
                val = (nextIDans, answers[i], 1)
                print(val)
                mycursor.execute(sql, val)
                mydb.commit()
            connectionSuccess()
        except mysql.connector.Error as error:
            connectionError()
    else:
        try:
            #___INSERT POLL_____________________
            sql = "SELECT * FROM poll ORDER BY IDpoll DESC LIMIT 1"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            (lastID, lastQuestion) = myresult[0]
            print(myresult[0])
            print(lastID, lastQuestion)
            sql = "INSERT INTO poll (IDpoll,question) VALUES (%s,%s)"
            nextID = lastID + 1
            val = (nextID, question)
            print(val)
            mycursor.execute(sql, val)
            mydb.commit()
            #___INSERT ANSWERS__________________
            answers = answersEntry.get()
            answers = answers.split(',', 10)
            for i in range(0, len(answers), 1):
                answers[i] = answers[i].strip(' ')
            print(answers)

            nextIDans = 0
            for i in range(0, len(answers), 1):
                sql = "INSERT INTO answer (idanswer, answerText, poll_IDpoll) VALUES (%s,%s,%s)"
                nextIDans = nextIDans + 1
                val = (nextIDans, answers[i], nextID)
                print(val)
                mycursor.execute(sql, val)
                mydb.commit()
            connectionSuccess()
        except mysql.connector.Error as error:
            connectionError()


#___SEE POLLS FUNCTIONS________________________________________________________________
def seePolls(mainPage, votePage):
    showPage(mainPage, votePage)
    try:
        mydb = mysql.connector.connect(
            host="snf-16955.ok-kno.grnetcloud.net",
            user="root",
            port='3306',
            password="crypto2021",
            database="cryptoPollDb"
        )
        mycursor = mydb.cursor()
        sql = "SELECT question FROM poll"

        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        print(myresult)
        polls = []
        for i in range(0, len(myresult), 1):
            polls.append(myresult[i][0])
        print(polls)
        buttons = []
        for i in range(0, len(polls), 1):
            button = tk.Button(votePage, width=35, height=2, text=polls[i], command=lambda j=i: voteForPoll(polls[j])).pack(side='top', pady=10, padx=10)
            buttons.append(button)
    except mysql.connector.Error as error:
        connectionError()
#______________________________________________________________________________________
#___VOTE FOR POLL FUNCTION_____________________________________________________________
def voteForPoll(q):
    try:
        mydb = mysql.connector.connect(
            host="snf-16955.ok-kno.grnetcloud.net",
            user="root",
            port='3306',
            password="crypto2021",
            database="cryptoPollDb"
        )
        mycursor = mydb.cursor()
        sql = "SELECT *FROM poll WHERE question=%s"
        val = q
        mycursor.execute(sql, (val,))
        myresult = mycursor.fetchall()
        print(myresult)
        (IDpoll, question) = myresult[0]
        askForName(IDpoll)
    except mysql.connector.Error as error:
        connectionError()
#______________________________________________________________________________________

def askForName(IDpoll):
    nameWindow = tk.Toplevel(root)
    nameWindow.title("Name Window")
    nameWindow.geometry("200x80")
    tk.Label(nameWindow, text ="Give your username").pack()
    e = tk.Entry(nameWindow, width=30)
    e.pack()
    okButton = tk.Button(nameWindow, text="OK", command=lambda: pollOrDecline(IDpoll, e, nameWindow)).pack()
#______________________________________________________________________________________

def pollOrDecline(IDpoll, entry, window):
    username = entry.get()
    try:
        mydb = mysql.connector.connect(
            host="snf-16955.ok-kno.grnetcloud.net",
            user="root",
            port='3306',
            password="crypto2021",
            database="cryptoPollDb"
        )
        mycursor = mydb.cursor()
        sql = "SELECT *FROM pollUserList WHERE poll_IDpoll=%s AND user_username=%s"
        val = (IDpoll, username)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        print(myresult)
    except mysql.connector.Error as error:
        connectionError()

    if myresult == []:
        print(IDpoll, username)
        window.destroy()
        specificPoll(IDpoll, username)
    else:
        print('DECLINED')
        window.destroy()
#______________________________________________________________________________________

def specificPoll(IDpoll, username):
    showPage(votePage, specificPage)
    tk.Label(specificPage, text='Access Granted').pack()
    try:
        mydb = mysql.connector.connect(
            host="snf-16955.ok-kno.grnetcloud.net",
            user="root",
            port='3306',
            password="crypto2021",
            database="cryptoPollDb"
        )
        mycursor = mydb.cursor()
        sql = "SELECT question FROM poll WHERE IDpoll=%s"
        val = (IDpoll,)
        mycursor.execute(sql, val)
        pollResult = mycursor.fetchall()
        pollResult = pollResult[0][0]
        print(pollResult)
        tk.Label(specificPage, text=pollResult).pack()
        sql = "SELECT idanswer, answerText FROM answer WHERE poll_IDpoll=%s"
        val = (IDpoll,)
        mycursor.execute(sql, val)
        answerResult = mycursor.fetchall()
        #answerResult = answerResult
        print(answerResult)
        buttons = []
        for i in range(0, len(answerResult), 1):
            button = tk.Button(specificPage, width=35, height=2, text=answerResult[i][1], command=lambda j=i: chooseAnswer(answerResult[j][0], username, IDpoll)).pack(side='top', pady=10, padx=10)
            buttons.append(button)
    except mysql.connector.Error as error:
        connectionError()

#______________________________________________________________________________________
def chooseAnswer(answerID, username, IDpoll):
    print(answerID, username, IDpoll)
    try:
        mydb = mysql.connector.connect(
            host="snf-16955.ok-kno.grnetcloud.net",
            user="root",
            port='3306',
            password="crypto2021",
            database="cryptoPollDb"
        )
        mycursor = mydb.cursor()
        sql = "SELECT cipherKey FROM user WHERE username=%s"
        val = (username,)
        mycursor.execute(sql, val)
        cipherResult = mycursor.fetchall()
        cipherResult = cipherResult[0][0]
        f = open("cipherString.txt", "r")
        myString = f.read()
        f.close()
        f = open("cipherKey.txt", "r")
        cipherKey = f.read()
        f.close()
        print(myString, cipherKey)
        print(username, IDpoll)
        decryptedString = decrypt(cipherKey, cipherResult)
        decryptedString = decryptedString.decode("utf-8")
        print(decryptedString)
        if decryptedString == myString:
            sql = "INSERT INTO pollUserList (user_username, poll_IDpoll) VALUES(%s, %s)"
            val = (username, IDpoll)
            mycursor.execute(sql, val)
            mydb.commit()
            token = secrets.token_urlsafe(16)
            f = open("token.txt", "w")
            f.write(token+'\n'+str(answerID)+'\n'+str(IDpoll))
            f.close()
            sql = "INSERT INTO votes (tokenID, answer_idanswer, poll_IDpoll) VALUES(%s, %s, %s)"
            val = (token, answerID, IDpoll)
            mycursor.execute(sql, val)
            mydb.commit()
            showPage(specificPage, mainPage)
            connectionSuccess()
    except mysql.connector.Error as error:
        connectionError()


# In[30]:


root = tk.Tk()


root.title('cryptoPoll')
root.geometry('500x330')
root.iconbitmap('hacker.ico')

bg = tk.PhotoImage(file='background2.png')
bgLabel = tk.Label(root, image=bg)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

#__LOGIN PAGE_____________________________________________________
loginPage = tk.Frame(root)
loginPage.pack()
#___BUTTONS_______________________________________________________
regButton = tk.Button(loginPage, width=10, height=2, text="Register", command=lambda: showPage(loginPage, registerPage))
regButton.pack(side='bottom', pady=30)

loginButton = tk.Button(loginPage,width=10, height=2, text="Login", command=lambda: login())
loginButton.pack(side='bottom', pady=20)
#_________________________________________________________________

#___ENTRIES AND LABELS____________________________________________
passwordEntry = tk.Entry(loginPage, width=25)
passwordEntry.pack(side='bottom', pady=0)
passwordLabel = tk.Label(loginPage, text='Password', anchor='center')
passwordLabel.pack(side='bottom')

usernameEntry = tk.Entry(loginPage, width=25)
usernameEntry.pack(side='bottom', pady=0)
usernameLabel = tk.Label(loginPage, text='Username', anchor='center')
usernameLabel.pack(side='bottom')

welcomeLabel = tk.Label(loginPage, text='Welcome to cryptoPoll\n the Anonymous Voting Platform', pady=30)
welcomeLabel.pack(side='bottom')
#_________________________________________________________________



#__REGISTER PAGE__________________________________________________
registerPage = tk.Frame(root)
#___BUTTONS_______________________________________________________
backButtonReg = tk.Button(registerPage, width=10, height=2, text="<< Back", command=lambda: showPage(registerPage, loginPage))
backButtonReg.pack(side='bottom', pady=30)

signupButton = tk.Button(registerPage, width=10, height=2, text="Sign up", command=lambda: signUp())
signupButton.pack(side='bottom', pady=5)
#_________________________________________________________________

#___ENTRIES AND LABELS____________________________________________
confirmPasswordEntryReg = tk.Entry(registerPage, width=25)
confirmPasswordEntryReg.pack(side='bottom', pady=0)
confirmPasswordLabelReg = tk.Label(registerPage, text='Confirm Password', anchor='center')
confirmPasswordLabelReg.pack(side='bottom')

passwordEntryReg = tk.Entry(registerPage, width=25)
passwordEntryReg.pack(side='bottom', pady=0, padx=14)
passwordLabelReg = tk.Label(registerPage, text='Password', anchor='center')
passwordLabelReg.pack(side='bottom')

usernameEntryReg = tk.Entry(registerPage, width=25)
usernameEntryReg.pack(side='bottom', pady=0)
usernameLabelReg = tk.Label(registerPage, text='Username', anchor='center')
usernameLabelReg.pack(side='bottom')

welcomeLabelReg = tk.Label(registerPage, text='Be a part of the change', pady=30)
welcomeLabelReg.pack(side='bottom')
#_________________________________________________________________




#__MAIN PAGE______________________________________________________
mainPage = tk.Frame(root)
#___BUTTONS_______________________________________________________
logoutButtonMain = tk.Button(mainPage, width=10, height=2, text="Logout", command=lambda: logout())
logoutButtonMain.pack(side='bottom', pady=40, padx=40)

voteButton = tk.Button(mainPage, width=13, height=2, text="Vote for a poll", command=lambda:seePolls(mainPage, votePage))
voteButton.pack(side='bottom', pady=10)

createButton = tk.Button(mainPage, width=13, height=2, text="Create a poll", command=lambda:showPage(mainPage, createPage))
createButton.pack(side='bottom', pady=10)
#_________________________________________________________________
#___ENTRIES AND LABELS____________________________________________
welcomeLabelMain = tk.Label(mainPage, text='Determine public opinion', pady=60)
welcomeLabelMain.pack(side='bottom')
#_________________________________________________________________


#___CREATE PAGE___________________________________________________
createPage = tk.Frame(root)
#___BUTTONS_______________________________________________________
backButtonCreate = tk.Button(createPage, width=10, height=2, text="<< Back", command=lambda:showPage(createPage, mainPage))
backButtonCreate.pack(side='bottom', pady=20)

createQuestionButton = tk.Button(createPage, width=15, height=2, text="Create Poll", command=lambda:createPollQuestion())
createQuestionButton.pack(side='bottom', pady=20)
#_________________________________________________________________
#___ENTRIES AND LABELS____________________________________________
answersEntry = tk.Entry(createPage, width=40)
answersEntry.pack(side='bottom', pady=10)

answersLabel = tk.Label(createPage, text="Add poll answers\nseperated with comma(,)")
answersLabel.pack(side='bottom', pady=10)


questionEntry = tk.Entry(createPage, width=40)
questionEntry.pack(side='bottom', pady=10)

questionLabel = tk.Label(createPage, text="Add poll question")
questionLabel.pack(side='bottom', pady=10)
#_________________________________________________________________


#___VOTE PAGE_____________________________________________________
votePage = tk.Frame(root)

#___SPECIFIC PAGE_________________________________________________
specificPage = tk.Frame(root)



root.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:

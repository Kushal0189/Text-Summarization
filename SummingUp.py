import heapq
import nltk
from nltk.corpus import stopwords

def nltk_summarizer(raw_text):
    stopWords = set(stopwords.words("english"))
    word_frequencies = {}
    for word in nltk.word_tokenize(raw_text):
        if word not in stopWords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    sentence_list = nltk.sent_tokenize(raw_text)
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary


# NLP Pkgs
import spacy

nlp = spacy.load('en_core_web_sm')
# Pkgs for Normalizing Text
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
# Import Heapq for Finding the Top N Sentences
from heapq import nlargest


def spacy_summarization(raw_docx):
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    # Build Word Frequency # word.text is tokenization in spacy
    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)
    # Sentence Tokens
    sentence_list = [sentence for sentence in docx.sents]

    # Sentence Scores
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)
    return summary

# Core Packages
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog

# NLP Pkg
from gensim.summarization import summarize

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Structure and Layout
window = Tk()
window.title("SummingUp")
window.geometry("2000x2000")
window.config(background='black')

style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='wn', )

# TAB LAYOUT
tab_control = ttk.Notebook(window, style='lefttab.TNotebook')

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)

# ADD TABS TO NOTEBOOK
tab_control.add(tab1, text=f'{"Home":^20s}')
tab_control.add(tab2, text=f'{"File":^24s}')
tab_control.add(tab3, text=f'{"URL":^22s}')
tab_control.add(tab4, text=f'{"Compare ":^15s}')
tab_control.add(tab5, text=f'{"About ":^20s}')

label1 = Label(tab1, text='Summaryzer', font = ("Times New Roman", 16), padx=0, pady=5)
label1.grid(row=0, column=0)

label2 = Label(tab2, text='File Processing', font = ("Times New Roman", 16), padx=5, pady=5)
label2.grid(column=0, row=0)

label3 = Label(tab3, text='URL', font = ("Times New Roman", 16), padx=5, pady=5)
label3.grid(column=0, row=0)

label3 = Label(tab4, text='Compare Summarizers', font = ("Times New Roman", 16), padx=5, pady=5)
label3.grid(column=0, row=0)

label4 = Label(tab5, text='About', font = ("Times New Roman", 16), padx=5, pady=5)
label4.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')

# Functions
def get_summary():
    tab1_display.configure(state="normal")
    raw_text = str(entry.get('1.0', tk.END))
    final_text = spacy_summarization(raw_text)
    print(final_text)
    result = '\nSummary:{}'.format(final_text)
    tab1_display.insert(tk.END, result)
    tab1_display.configure(state="disabled")

# Clear entry widget
def clear_display_result():
    tab1_display.configure(state="normal")
    tab1_display.delete('1.0', END)
    tab1_display.configure(state="disabled")

def clear_text():
    entry.delete('1.0', END)
    clear_display_result()

# Clear Result of Functions
def clear_text_result():
    tab2_display_text.configure(state="normal")
    tab2_display_text.delete('1.0', END)
    tab2_display_text.configure(state="disabled")

# Clear Text  with position 1.0
def clear_text_file():
    displayed_file.configure(state="normal")
    displayed_file.delete('1.0', END)
    displayed_file.configure(state="disabled")
    clear_text_result()
    
# Clear For URL
def clear_url_display():
    tab3_display_text.configure(state="normal")
    tab3_display_text.delete('1.0', END)
    tab3_display_text.configure(state="disabled")

def clear_url_entry():
    url_entry.delete(0, END)
    url_display.configure(state="normal")
    url_display.delete('1.0',END)
    url_display.configure(state="disabled")
    clear_url_display()

# Clear entry widget
def clear_compare_display_result():
    tab4_display.configure(state="normal")
    tab4_display.delete('1.0', END)
    tab4_display.configure(state="disabled")

def clear_compare_text():
    entry1.delete('1.0', END)
    clear_compare_display_result()

# Functions for TAB 2 FILE PROCESSER
# Open File to Read and Process
def openfiles():
    displayed_file.configure(state="normal")
    file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files", ".txt"), ("All files", "*")))
    read_text = open(file1).read()
    displayed_file.insert(tk.END, read_text)
    displayed_file.configure(state="disabled")

def get_file_summary():
    tab2_display_text.configure(state="normal")
    raw_text = displayed_file.get('1.0', tk.END)
    final_text = spacy_summarization(raw_text)
    result = '\nSummary:{}'.format(final_text)
    tab2_display_text.insert(tk.END, result)
    tab2_display_text.configure(state="disabled")

# Fetch Text From Url
def get_text():
    url_display.configure(state="normal")
    raw_text = str(url_entry.get())
    page = urlopen(raw_text)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    url_display.insert(tk.END, fetched_text)
    url_display.configure(state="disabled")

def get_url_summary():
    tab3_display_text.configure(state="normal")
    raw_text = url_display.get('1.0', tk.END)
    final_text = spacy_summarization(raw_text)
    result = '\nSummary:{}'.format(final_text)
    tab3_display_text.insert(tk.END, result)
    tab3_display_text.configure(state="disabled")

# COMPARER FUNCTIONS
def use_spacy():
    tab4_display.configure(state="normal")
    raw_text = str(entry1.get('1.0', tk.END))
    final_text = spacy_summarization(raw_text)
    print(final_text)
    result = '\nSpacy Summary:{}\n'.format(final_text)
    tab4_display.insert(tk.END, result)
    tab4_display.configure(state="disabled")

def use_nltk():
    tab4_display.configure(state="normal")
    raw_text = str(entry1.get('1.0', tk.END))
    final_text = nltk_summarizer(raw_text)
    print(final_text)
    result = '\nNLTK Summary:{}\n'.format(final_text)
    tab4_display.insert(tk.END, result)
    tab4_display.configure(state="disabled")

def use_gensim():
    tab4_display.configure(state="normal")
    raw_text = str(entry1.get('1.0', tk.END))
    final_text = summarize(raw_text)
    print(final_text)
    result = '\nGensim Summary:{}\n'.format(final_text)
    tab4_display.insert(tk.END, result)
    tab4_display.configure(state="disabled")

def use_sumy():
    tab4_display.configure(state="normal")
    raw_text = str(entry1.get('1.0', tk.END))
    final_text = spacy_summarization(raw_text)
    print(final_text)
    result = '\nSumy Summary:{}\n'.format(final_text)
    tab4_display.insert(tk.END, result)
    tab4_display.configure(state="disabled")

# MAIN NLP TAB
l1 = Label(tab1, text="Enter Text To Summarize:", font = ("Times New Roman", 14))
l1.grid(row=1, column=1)

entry = Text(tab1, height=15, width=155)
entry.grid(row=2, column=0, columnspan=3, padx=13, pady=5)

# BUTTONS
button1 = Button(tab1, text="Reset", command=clear_text, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button1.grid(row=5, column=0, pady=7)

button2 = Button(tab1, text="Summarize", command=get_summary, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button2.grid(row=5, column=2, pady=7)

button3 = Button(tab1, text="Clear Result", command=clear_display_result, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button3.grid(row=6, column=0, pady=5)

button4 = Button(tab1, text="Close", width=12,command=window.destroy, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button4.grid(row=6, column=2, pady=5)

# Display Screen For Result
tab1_display = Text(tab1, height=15, width=155)
tab1_display.configure(state="disabled")
tab1_display.grid(row=8, column=0, columnspan=3, padx=13, pady=7)

# FILE PROCESSING TAB
l1 = Label(tab2, text="Open File To Summarize", font = ("Times New Roman", 12))
l1.grid(row=1, column=1)

displayed_file = ScrolledText(tab2, height=15, width=155)  # Initial was Text(tab2)
displayed_file.configure(state="disabled")
displayed_file.grid(row=2, column=0, columnspan=3, padx= 13, pady=5)

# BUTTONS FOR SECOND TAB/FILE READING TAB
b0 = Button(tab2, text="Open File", width=12, command=openfiles, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
b0.grid(row=5, column=0, pady=7)

b1 = Button(tab2, text="Reset ", width=12, command=clear_text_file, bg="#0000b3", fg='#fff', font = ("Times New Roman", 12))
b1.grid(row=5, column=2, pady=5)

b2 = Button(tab2, text="Summarize", width=12, command=get_file_summary, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
b2.grid(row=6, column=0, pady=5)

b3 = Button(tab2, text="Clear Result", width=12, command=clear_text_result, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
b3.grid(row=6, column=2, pady=5)

# Display Screen
tab2_display_text = ScrolledText(tab2, height=15, width=155)
tab2_display_text.configure(state="disabled")
tab2_display_text.grid(row=8, column=0, columnspan=3, padx=13, pady=7)

# URL TAB
l1 = Label(tab3, text="Enter URL To Summarize:", font = ("Times New Roman", 12))
l1.grid(row=1, column=0)

raw_entry = StringVar()
url_entry = Entry(tab3, textvariable=raw_entry, width=50)
url_entry.grid(row=1, column=1)

# BUTTONS
button1 = Button(tab3, text="Reset", command=clear_url_entry, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button1.grid(row=4, column=0, pady=7)

button2 = Button(tab3, text="Get Text", command=get_text, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button2.grid(row=4, column=2, pady=5)

button3 = Button(tab3, text="Clear Result", command=clear_url_display, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button3.grid(row=5, column=0, pady=7)

button4 = Button(tab3, text="Summarize", command=get_url_summary, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button4.grid(row=5, column=2, pady=5)

# Display Screen For Result
url_display = ScrolledText(tab3, height=15, width = 155)
url_display.configure(state="disabled")
url_display.grid(row=7, column=0, columnspan=3, padx=13, pady=7)
tab3_display_text = ScrolledText(tab3, height=15, width = 155)
tab3_display_text.configure(state="disabled")
tab3_display_text.grid(row=10, column=0, columnspan=3, padx=13, pady=5)

# COMPARER TAB
l1 = Label(tab4, text="Enter Text To Summarize", font = ("Times New Roman", 12))
l1.grid(row=1, column=1)

entry1 = ScrolledText(tab4, height=15, width=155)
entry1.grid(row=2, column=0, columnspan=3, padx=13, pady=5)

# BUTTONS
button1 = Button(tab4, text="Reset", command=clear_compare_text, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button1.grid(row=4, column=0, pady=7)

button2 = Button(tab4, text="SpaCy", command=use_spacy, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button2.grid(row=4, column=1, pady=7)

button3 = Button(tab4, text="Clear Result", command=clear_compare_display_result, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button3.grid(row=5, column=0, pady=5)

button4 = Button(tab4, text="NLTK", command=use_nltk, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button4.grid(row=4, column=2, pady=7)

button5 = Button(tab4, text="Gensim", command=use_gensim, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button5.grid(row=5, column=1, pady=5)

button6 = Button(tab4, text="Summarize", command=use_sumy, width=12, bg='#0000b3', fg='#fff', font = ("Times New Roman", 12))
button6.grid(row=5, column=2, pady=5)

# Display Screen For Result
tab4_display = ScrolledText(tab4, height=15, width=155)
tab4_display.configure(state="disabled")
tab4_display.grid(row=7, column=0, columnspan=3, padx=13, pady=7)
 
# About TAB
about_label = Label(tab5, text="Kushal Master \n Sharad Dobariya \n Harsh Shah", pady=15, padx=5, font = ("Times New Roman", 20))
about_label.grid(column=2, row=10)

window.mainloop()

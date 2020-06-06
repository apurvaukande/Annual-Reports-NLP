import spacy
import os
from collections import Counter

nlp = spacy.load('en_core_web_lg')

def filter_lines(sentence, ent_type):
    text = []
    for line in sentence:
        nlp_str = nlp(line)
        sents = [x for x in nlp_str.sents]
        for sent in sents:
            flag = 0
            for word in sent.ents:
                if word.label_ == ent_type:
                    s = word.text
                    if s[0].isupper():
                        text.append(line)
                        flag = 1
                        break
            if flag == 1:
                break
    return text
                        
def remove_stop_words(sentences): # list of strings
    text = []
    stopwords = nlp.Defaults.stop_words
    for sent in sentences:
        sent = nlp(sent)
        tokens = [token.text for token in sent if not token.is_stop]
        tokens = [word for word in tokens if not word in stopwords]
        tokens = [x for x in tokens]
        line = " ".join(tokens)
        text.append(line)

    return text

def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])

def n_grams(lines, n):
    count = {}
    all_ngram = []
    for line in lines:
        words = line.split()
        n_gram = find_ngrams(words, n)

        for item in n_gram:
            all_ngram.append(item)

    count = Counter(all_ngram)
    most_freq = count.most_common(1)
    print(most_freq)
    return most_freq



# To open and read a file
f = open('./text_report/eurotech-2018.txt', 'r', encoding='utf-16')
text = f.read()
f.close()

#To remove all punctuation except '.' and numbers
string = ['"', '%', '&', '(', ')', '*', '+', ',', '-', '/', ':', ';', '@', '[', ']', '^', '–', '_', '`', '{', '|', '}', '~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

#string2 = ['!', '#', '?', '$']

for i in text:
    for j in string:
        if i == j:
            text = text.replace( i, ' ')

# To remove empty lines
text = os.linesep.join([s for s in text.splitlines() if s])
text_new = ""
for x in text:
    if x != '\n':
        text_new += x
    else:
        text_new += ' '


#Split the lines and make a list of sentences.
text = text_new.split('.')

# All punctuation, numbers, white spaces are removed. Now we have list of strings.

#code to access sentence
# We want list of lines, individually seperated by "."
# We will feed each line, i.e item of this list made above to the functions, 
# which will recognise if this lines contains mention of an org/person

text_org = filter_lines(text, 'ORG')			
text_person = filter_lines(text, 'PERSON')

#Remove extra spaces in all lines
text_new = []
for x in text_org:
    l = x.split()
    l = " ".join(l)
    text_new.append(l)

text_org = text_new


text_new = []
for x in text_person:
    l = x.split()
    l = " ".join(l)
    text_new.append(x)

text_person = text_new

#Remove Stop Words

text_org = remove_stop_words(text_org)
text_person = remove_stop_words(text_person)


# Now both above are list of lines with stopwords 
#removed to reduce extra noise while taking n_grams
print("Comany name is probably:")
most_freq1 = n_grams(text_org, 1)
most_freq2 = n_grams(text_org, 2)
most_freq3 = n_grams(text_org, 3)
most_freq4 = n_grams(text_org, 4)


# ORG = (Take most_freq of above 3)
print("CEO name is probably:")
most_freq1 = n_grams(text_person, 1)
most_freq2 = n_grams(text_person, 2)
most_freq3 = n_grams(text_person, 3)
most_freq4 = n_grams(text_person, 4)


# PERSON = (Most freq of 3)

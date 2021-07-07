import re, math, nltk, numpy
from collections import defaultdict
from nltk.stem import PorterStemmer


def isStop(word):
    stop_list= ['a','the','an','and','or','but','about','above','after','along','amid','among','as','at','by',\
    'for','from','in','into','like','minus','near','of','off','on','onto','out','over','past','per','plus','since',\
    'till','to','under','until','up','via','vs','with','that','can','cannot','could','may','might','must',\
    'need','ought','shall','should','will','would','have','had','has','having','be','is','am','are','was','were',\
    'being','been','get','gets','got','gotten','getting','seem','seeming','seems','seemed','enough', 'both', 'all', \
    'your' 'those', 'this', 'these', 'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my','its', 'his' 'her',\
     'every', 'either', 'each', 'any', 'another','an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
    'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more','most', 'less' 'least', 'so', 'enough', 'too', 'pretty',\
     'quite','rather', 'somewhat', 'sufficiently' 'same', 'different', 'such','when', 'why', 'where', 'how', 'what', 'who',\
    'whom', 'which','whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', 'anything', 'anytime' 'anywhere',\
     'everybody', 'everyday','everyone', 'everyplace', 'everything' 'everywhere', 'whatever','whenever', 'whereever', \
    'whichever', 'whoever', 'whomever' 'he','him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
      'you','your','yours','me','my','mine','I','we','us','much','and/or']
    if word in stop_list: 
        return True
    else: 
        return False
    

# 1. Read cran.qry file
cran_qry_words = {}
count = 0
stemmer = PorterStemmer() #stem related words to one group
cran_q_file = open('cran.qry', "r")
# read each line and populate the list of queries
for l in cran_q_file:
    if '.I' in l:
        count += 1
    elif '.W' not in l:
        clear_regex=re.split('([^a-zA-Z0-9_])', l.strip())
        if count in cran_qry_words:
            cran_qry_words[count] += list(filter(None, clear_regex))
        else:
            cran_qry_words[count]  = list(filter(None, clear_regex))                     
cran_q_file.close()

#update the list of queries to not include
#any stop words and group stems together
for i in cran_qry_words:
    current_l=cran_qry_words[i]
    words_l=[]
    for word in current_l:
        if not(isStop(word)):
            words_l.append(stemmer.stem(word))
    cran_qry_words[i] = words_l

# 2. Read cran.all.1400 file
count = 0
cran_abs_words = {}
cran_abs_file = open('cran.all.1400', "r")
# read each line and populate the list of abstracts
for l in cran_abs_file:
    if '.I' in l:
        count += 1
    elif '.W' not in l:
        #clear_regex=re.split('([^a-zA-Z0-9_])|([0-9])', l.strip())
        clear_regex=re.split('([^a-zA-Z0-9_])', l.strip())
        if count in cran_abs_words:
            cran_abs_words[count] += list(filter(None, clear_regex))
        else:
            cran_abs_words[count]  = list(filter(None, clear_regex)) 
                    
cran_abs_file.close()
for i in cran_abs_words:
    current_l=cran_abs_words[i]
    words_l=[]
    for word in current_l:
        if not(isStop(word)):
            words_l.append(stemmer.stem(word))
    cran_abs_words[i] = words_l


# 3. Calculate tfidf scores for the cran queries

query_tfidf= defaultdict(lambda: defaultdict(float))
#separate query sentences
qry_sentences = list(cran_qry_words.values())
query_idf = {}
i = 1
#calculate idf, tfidf for every word in a query sentence 
for sentence in qry_sentences:
    for word in sentence:
        if word not in query_idf.keys():
            count = 0 #word has not appeared before
            for query in qry_sentences:
                if word in query:
                    count += 1
            query_idf[word] = math.log(225 / count) #idf score
        query_tfidf[i][word] = (sentence.count(word) / len(sentence)) * query_idf[word]
    i += 1


# 4. Calculate tfidf scores for the cran abstracts
abstracts_tfidf= defaultdict(lambda: defaultdict(float))
#separate abstract sentences
abs_sentences = list(cran_abs_words.values())
abstracts_idf = {}
i = 1
#calculate idf, tfidf for every word in an abstract sentence 
for sentence in abs_sentences:
    for word in sentence:
        if word not in abstracts_idf.keys():
            count = 0 #word has not appeared before
            for query in abs_sentences:
                if word in query:
                    count += 1
            abstracts_idf[word] = math.log(1400 / count) #idf score
        abstracts_tfidf[i][word] = (sentence.count(word) / len(sentence)) * abstracts_idf[word]
    i += 1

# 5. Calculate cosine similarity scores and populate the scores array
total_query_score = 0
total_abs_score = 0
temp_query_words = []
temp_query_tfidf = []
temp_abs_tfidf = []
cosine_sim_scores = defaultdict(lambda: defaultdict(float))
#calculate cosine similarity scores for each query and each abstract
for q in query_tfidf.keys():
    temp_query_tfidf = list(query_tfidf[q].values())
    temp_query_words = list(query_tfidf[q].keys())
    for abst in abstracts_tfidf.keys(): #process abstract
        for word in temp_query_words:
            if word not in list(abstracts_tfidf[abst].keys()):
                temp_abs_tfidf.append(0) #word appears first time
            else: #record the tfidf score of the word from abstract
                temp_abs_tfidf.append(abstracts_tfidf[abst][word])
        for k in temp_abs_tfidf:
            total_abs_score += k**2
        for i in temp_query_tfidf:
            total_query_score += i**2
        #finally calculate the cosine similarity score and store it
        a = numpy.dot(temp_query_tfidf, temp_abs_tfidf) #nominator
        temp_abs_tfidf = []
        b = numpy.sqrt(total_query_score * total_abs_score) #denominator
        final = 0
        if b != 0:
            final = a / b
        cosine_sim_scores[q][abst] = final

#sort the cosine similarity scores
for score in cosine_sim_scores.keys():
    cosine_sim_scores[score] = {a: s for a, s in sorted(cosine_sim_scores[score].items(), key=lambda item: item[1], reverse=True)} 

# 6. Write the results to the output file
out_file= open("output.txt", "w")
for query in cosine_sim_scores.keys():
    for abstract in cosine_sim_scores[query].keys():
        out_file.write(str(query)+' '+str(abstract)+' '+str('{:f}'.format(cosine_sim_scores[query][abstract]))+'\n')
out_file.close()


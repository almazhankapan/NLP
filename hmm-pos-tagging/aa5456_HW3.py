# Almazhan Abdukhat
# Assignment 3, CSCI-UA 480 Natural Language Processing
# I have discussed this homework with Betty Kao

import sys

all_sentences = [] #list of all frequencies
pos_tags = []      #list of all tags
pr_likelihood = {} #dict of likelihood probabilities
trans_count = {}  #dict of transition frequencies
pr_trans = {}   #dict of transition probabilities
pr_emis = {}     #dict of emission probabilities
input_file = ""  #training input file
test_corpus = "" #test file

#read the input training file and set up tables based on the processed data
def setup(train_corpus):

    input_file = open(train_corpus, 'r')
    prior_state = "sentence_start" #set start state

    #find probabilities based on frequencies for each line
    for l in input_file:
        if not l.isspace(): #if line is non-empty
            token,tag = l.strip().split("\t") 
            #check if tag has appeared before
            #if not, record it in the dict of likelihood probabilities 
            if tag not in pr_likelihood: 
                pr_likelihood[tag] = {}           
            #increment the count for the token
            if token in pr_likelihood[tag]:
                pr_likelihood[tag][token] += 1
            else:
                pr_likelihood[tag][token] = 1
            #check if transition has appeared before
            #if not, record it in the trans_count
            if prior_state not in trans_count:
                trans_count[prior_state] = {}   
            #increment the count for the transition
            if tag in trans_count[prior_state]:
                trans_count[prior_state][tag] += 1
            else: 
                trans_count[prior_state][tag] = 1

            prior_state = tag
            
        elif l.isspace(): #if line is empty
            #check if state has appeared before and record if needed
            if prior_state not in trans_count:
                trans_count[prior_state] = {}
            #increment frequency for 'sentence end' state    
            if "sentence_end" in trans_count[prior_state]:
                trans_count[prior_state]["sentence_end"] += 1
            else: 
                trans_count[prior_state]["sentence_end"] = 1
            prior_state = "sentence_start"

    input_file.close()

# auxiliary function to find probabilities for items in the frequency matrix
# and store the results in the prob_matrix
def find_prob(freq_matrix, prob_matrix):
    for key, matrix in freq_matrix.items():
        total = 0
        for target, count in matrix.items():
            total += count
            if target not in prob_matrix:
                prob_matrix[target] = {}
            prob_matrix[target][key] = count / total


# process test corpus and create a matrix of sentences
def process_test(test_corpus):
    test_corpus = open(test_corpus, 'r')
    matrix = []
    # for each line append the tokens to all_sentences
    for l in test_corpus:
        if l in ['\n', '\r\n']:
            all_sentences.append(matrix)
            matrix = []
        if l.strip():
            word = l.strip()
            matrix.append(word)       
    test_corpus.close()

#process the out of vocabulary words if they appear
def process_oov(v_table):
    end="sentence_end"
    start="sentence_start"
    for s in range(2, len(v_table)):
        #if emission probability is calculated
        if v_table[0][2] in pr_emis.keys():
            if v_table[s][0] != end:   #if state is not end of sentence   
                can_calculate= (v_table[s][0] in pr_emis[v_table[0][2]].keys() and v_table[s][0] in trans_count[start].keys())
                if not can_calculate :
                    v_table[s][2] = None
                else:
                    v_table[s][2] = pr_emis[v_table[0][2]][v_table[s][0]] * pr_trans[v_table[s][0]][start] 
        else:
            if v_table[s][0] != end:   #if state is not end of sentence           
                if not (v_table[s][0] in trans_count[start].keys()):
                    v_table[s][2] = None       
                else: #assume the tag has probability 0.001
                    v_table[s][2] = pr_trans[v_table[s][0]][start] * 0.001
                    
# auxiliary function to compute the viterbi scores and fill in the backpointer, viterbi tables      
def compute_scores(cur_tokens, backpointer, v_table):
    for j in range(3, len(v_table[0])): 
        #oov if the word does not appear in the training corpus
        oov=not (v_table[0][j] in pr_emis.keys())
        if oov: #the word is oov
            for i in range(2, len(v_table)-1):
                for state, value in cur_tokens.items():
                    if state in pr_trans[v_table[i][0]].keys():
                        result = value * 0.001 * pr_trans[v_table[i][0]][state]  
                        update_score=((v_table[i][j] == None) or result > v_table[i][j]) 
                        if update_score:
                            v_table[i][j] = result
                    else:
                            v_table[i][j] = value * 0.001 * 0.001
        else: 
            for i in range(2, len(v_table) - 1):
                if v_table[i][0] in pr_emis[v_table[0][j]].keys():
                    for state, value in cur_tokens.items(): 
                        if not (state in pr_trans[v_table[i][0]].keys()):
                            #set score for a tag for which transition prob is not known
                            v_table[i][j] = value * 0.001 * pr_emis[ v_table[0][j] ][ v_table[i][0] ]
                        else: # otherwise set score as max previous score * transition prob * likelihood/emissio
                            result = value * pr_trans[ v_table[i][0] ][state] * pr_emis[ v_table[0][j] ][ v_table[i][0] ]
                            update_score=((v_table[i][j] == None) or result > v_table[i][j] ) 
                            if update_score:
                                v_table[i][j] = result
            
        cur_tokens= {} #clean the current tokens dict

        for n in range(2, len(v_table) - 1):
            if v_table[n][j] != None:
                cur_tokens[v_table[n][0]] = v_table[n][j]
            
        temp = sorted(cur_tokens.items(), key = lambda d:d[1], reverse = True) 
        #set backpointer as the max of previous scores
        backpointer.append(temp[0][0])       
        for i, j in temp:
            cur_tokens[i] = j
    return backpointer 
    
                    

# run viterbi algorithm, create viterbi array and fill in the scores
def run_viterbi(temp_states):
    #create the viterbi array
    for sentence in all_sentences:
        v_table = [] #viterbi table         
        
        #set up the viterbi table and fill in the viterbi table
        for i in range(len(temp_states) + 1):
            v_table.append([])
            for j in range(len(sentence) + 3):
                v_table[i].append(None)
        v_table[0][0] = "nil"  
        v_table[0][1] = 0
        v_table[1][1] = 1  
        v_table[0][-1] = len(v_table[0]) - 2 
        
        for i in range(1, len(v_table)):
            v_table[i][0] = temp_states[i - 1]   

        for j in range(2, len(v_table[0]) - 1):
            v_table[0][j] = sentence[j - 2]

        #process any out of vocabulary words
        process_oov(v_table)

        cur_tokens = {} #store current tokens
        backpointer = []  #store max viterbi scores    
         
        for n in range(2, len(v_table)):
            if v_table[n][2] != None:
                cur_tokens[v_table[n][0]] = v_table[n][2]
        
        temp = sorted(cur_tokens.items(), key = lambda d:d[1], reverse = True)      # Sort previous cell scores so max is at [0][0]
        backpointer.append(temp[0][0])          # backpointer = maximum previous
        
        for key, val in temp:
            cur_tokens[key] = val

        # using viterbi algorithm, compute the scores and fill-in the table
        backpointer=compute_scores(cur_tokens,backpointer, v_table)
        #store the backpointer
        pos_tags.append(backpointer) 
    
    

if __name__ == '__main__':
    #read input files
    train_corpus = sys.argv[1] #use WSJ_02-21.pos
    test_corpus = sys.argv[2] #use WSJ_23.words
    #read the input training file and set up tables based on the processed data
    setup(train_corpus)
    #find transition probabilities by processing transition frequencies in the training corpus
    find_prob(trans_count, pr_trans)
    #find emission probabilities by processing likelihood probabilities in the training corpus
    find_prob(pr_likelihood, pr_emis)
    # process test corpus and create a matrix of sentences
    process_test(test_corpus)
    # set up the temp_states array by adding tags, start and end states
    temp_states = []
    temp_states.append("sentence_start")
    for states in pr_likelihood.keys():
        temp_states.append(states)
    temp_states.append("sentence_end")
    # run viterbi algorithm, create viterbi array and fill in the scores
    run_viterbi(temp_states)   
    #write resulting tokens - tag pairs to the output file
    out_file = open("submission.pos","w")
    for i in range(len(all_sentences)):
        for j in range(len(all_sentences[i])):
            out_file.write(all_sentences[i][j] + "\t" + pos_tags[i][j] + "\n")
        out_file.write("\n")
        
    out_file.close()
       
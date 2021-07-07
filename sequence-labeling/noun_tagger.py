import sys

#create features for a training corpus 
#or apply them depending on the corpus and feature type                                                                                                  
def setFeatures(corpus, c_type, feature):
    with open(corpus, 'r') as corpus_file:
        with open(feature, 'w') as feature_file:
            train_words = corpus_file.readlines()
            for k, line in enumerate(train_words):
                line = line.strip()
                if len(line) == 0:
                    feature_file.write('\n')
                else:
                    if c_type==1: #training file
                        #current word, its POS and bio tag are used as features
                        current_word, current_POS, current_tag = line.split()
                        current_word, current_POS, current_tag = line.split()
                    else:  #testing file
                        current_word, current_POS = line.split()
                        current_tag = 'current_tag=#'
                    #feature denotes if the current word starts with uppercase letter
                    is_upper = ''
                    word = train_words[k].strip().split()[0]
                    if word[0].isupper():
                        is_upper = 'is_upper=1'
                    else:
                        is_upper = 'is_upper=0'

                    #Beginning 
                    if k < 1:
                        previous_word = 'previous_word=0'
                        previous_POS = 'previous_POS=0'
                        is_prev_upper = 'is_prev_upper=0'
                        before_prev_word = 'before_prev_word=0'
                        before_prev_POS = 'before_prev_POS=0'
                        is_before_prev_upper = 'is_before_prev_upper=0'
                    else:  #if previous token is null
                        if (len(train_words[k - 1].strip()) == 0):
                            #previous word as a feature
                            previous_word = 'previous_word=0'
                            #previous word's POS as a feature
                            previous_POS = 'previous_POS=0'
                            #feature denotes if previous word is uppercase
                            is_prev_upper = 'is_prev_upper=0'
                        else: #otherwise set features to their actual values
                            previous_word = 'previous_word=' + train_words[k - 1].strip().split()[0]
                            previous_POS = 'previous_POS=' + train_words[k - 1].strip().split()[1]
                            #check if previous word is uppercase
                            token = train_words[k - 1].strip().split()[0]
                            if token[0].isupper():  
                                is_prev_upper = 'is_prev_upper=1'
                            else:
                                is_prev_upper = 'is_prev_upper=0'
                        #if the token before the previous token is null
                        if (k < 2 or len(train_words[k - 2].strip()) == 0):
                            #word before previous word as a feature
                            before_prev_word = 'before_prev_word=0'
                            #POS of the word before the previous word as a feature
                            before_prev_POS = 'before_prev_POS=0'
                            #feature denotes if the word before the previous word is uppercase
                            is_before_prev_upper = 'is_before_prev_upper=0'
                        else:
                            before_prev_word = 'before_prev_word=' + train_words[k - 2].strip().split()[0]
                            before_prev_POS  = 'before_prev_POS=' + train_words[k - 2].strip().split()[1]
                            token = train_words[k - 2].strip().split()[0]
                            #check if the word before previous word is uppercase
                            if token[0].isupper():
                                is_before_prev_upper = 'is_before_prev_upper=1'
                            else:
                                is_before_prev_upper = 'is_before_prev_upper=0'
                    #Beginning
                    if (k > len(train_words) - 2):
                        #the word following current word as a feature
                        following_word = 'following_word=</s>'
                        #the following word's POS as a feature
                        following_POS = 'following_POS=</s>'
                        #feature denotes if the following word is uppercase
                        is_follow_upper = 'is_follow_upper=0'
                        #the next next word as a feature
                        next_follow_word = 'next_follow_word=</s>'
                        #POS of the next next word as a feature
                        next_follow_POS = 'next_follow_POS=</s>'
                        #feature denotes if the next next word is uppercase
                        is_next_follow_upper = 'is_next_follow_upper=0'
                    else:  #if the next token is null
                        if (len(train_words[k + 1].strip()) == 0):
                            following_word = 'following_word=</s>'
                            following_POS = 'following_POS=</s>'
                            is_follow_upper = 'is_follow_upper=0'
                        else:  # otherwise set features to their actual values
                            following_word = 'following_word=' + train_words[k + 1].strip().split()[0]
                            following_POS = 'following_POS=' + train_words[k + 1].strip().split()[1]
                            word = train_words[k + 1].strip().split()[0]
                            #check if the next word is uppercase
                            if word[0].isupper():
                                is_follow_upper = 'is_follow_upper=1'
                            else:
                                is_follow_upper = 'is_follow_upper=0'
                        #if the next next token is null
                        if ((k > len(train_words) - 3) or len(train_words[k + 2].strip()) == 0):
                            next_follow_word = 'next_follow_word=</s>'
                            next_follow_POS = 'next_follow_POS=</s>'
                        else:  # otherwise set features to their actual values
                            next_follow_word='next_follow_word=' + train_words[k + 2].strip().split()[0]
                            next_follow_POS = 'next_follow_POS=' + train_words[k + 2].strip().split()[1]
                            word = train_words[k + 2].strip().split()[0]
                            #check if the next word is uppercase
                            if word[0].isupper():
                                is_next_follow_upper = 'is_next_follow_upper=1'
                            else:
                                is_next_follow_upper = 'is_next_follow_upper=0'

                    line = '\t'.join([current_word, current_POS, is_upper, previous_word,
                                      previous_POS, is_prev_upper, following_word, following_POS,
                                      is_follow_upper, before_prev_word, before_prev_POS, is_before_prev_upper, next_follow_word,
                                      next_follow_POS, is_next_follow_upper, current_tag])
                    feature_file.write(line + '\n')

def main():
    #process command line arguments
    train_corpus = sys.argv[1]
    test_corpus = sys.argv[2]
    #create features and train the data
    setFeatures(train_corpus,1,'training.feature')
    #produce system output
    setFeatures(test_corpus, 2, 'test.feature')

if __name__ == "__main__":
    main()





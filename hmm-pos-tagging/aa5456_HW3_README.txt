To run the program, use the following command: 
    
    python3 aa5456_HW3.py WSJ_02-21.pos WSJ_23.words

WSJ_02-21.pos is a training file and WSJ_23.words is the testing file. 
WSJ_24.pos was used for development purposes. 

To address the out of vocabulary words (not in the training corpus), 
set likelihood value as 1/1000 for all OOV words and parts of speech. 

Description of the viterbi algorithm implemented in the program is given in the lecture 3 slides
and chapter 5 in the 'Speech and Language Processing' by Jurafsky and Martin. 

I have discussed the homework with Betty Kao. 
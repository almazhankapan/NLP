Natural Language Processing HW 5

1. Run the program with the following command: 

python3 noun_tagger.py WSJ_02-21.pos-chunk WSJ_24.pos

WSJ_02-21.pos-chunk is a train file
WSJ_24.pos is a test file

The system outputs training.feature and test.feature files

2. To create models, run the following commands: 
	
	For Linux, Apple and other Posix systems, do:
		javac -cp maxent-3.0.0.jar:trove.jar *.java ### compiling
		java -cp .:maxent-3.0.0.jar:trove.jar MEtrain training.feature model.chunk ### creating the model of the training data
		java -cp .:maxent-3.0.0.jar:trove.jar MEtag test.feature model.chunk response.chunk ### creating the system output

	For Windows, do: 
	
		javac -cp maxent-3.0.0.jar;trove.jar *.java ### compiling
		java -cp .:maxent-3.0.0.jar;trove.jar MEtrain training.feature model.chunk ### creating the model of the training data
		java -cp .:maxent-3.0.0.jar;trove.jar MEtag test.feature model.chunk response.chunk ### creating the system output

3. To score the system, run the following command: 

python score.chunk.py WSJ_24.pos-chunk response.chunk

4. Analysis. 

The following features were used for the system: 
- current word
- current word's Part of Speech tag
- feature that denotes if the current word has an uppercase letter
- previous word
- previous word's Part of Speech tag
- previous word's tag
- feature that denotes if the previous word has an uppercase letter
- following word
- Part of Speech tag of the following word
- feature that denotes if the following word has an uppercase letter
- next word after the following word (next next word)
- next next word's Part of Speech tag
- feature that denotes if the next next word has an uppercase letter
- the word before the previous word 
- feature that denotes if the word before the previous word has an uppercase letter
- Part of Speech tag of the woword before the previous word previous word 

Some observations: 
- Using the word's POS as a feature significantly improved the overall performance of the system. 
- Using subsequent words as a feature also contributes positively to the performance. 
- Using subsequent POS tags also contributes positively to the performance. 
- Using uppercase letter as a feature didn't improve the system significantly
- Stemming affets the performance negatively


The system was tested on the file WSJ_24.chunk and received the following score: 

  accuracy: 96.49
  precision: 90.3
  recall:    92.1
  F1:        91.2













































































#Data Cleaning
For this exercise, I will address most of the data cleaning within the SQL database, posting the queries below with explanations

##Dropping impossible values
In very few cases (~20 out of 150,000), there exists values which are impossible. For sake of completeness, we will delete these values. 

~~~~sql
DELETE FROM TwitterWordle
WHERE Score > 6;
~~~~

##Replacing score values of 0 with 7
In my design of the Twitter Scraper, I made the decision to classify a loss as 0. When a person "loses" they have not correctly guessed the word in 6 tries. Not only would including 0 as a value throw off averages, it also does not accurately represent that person's score or game. So, I've decided to give the benefit of the doubt to these poor Wordle players and predict they would guess correctly on their 7th try, givin them a score of 7 for that day. 

~~~~sql
UPDATE TwitterWordle
SET Score = 7
WHERE Score = 0;
~~~~
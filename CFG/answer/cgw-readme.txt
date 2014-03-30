#This is my readme file. Hope it is a good one. It should smell of elderberries.

This readme file is rather a note when I took during this two weeks of study and development. So the early 
part of it may look "immature", however, I decide to keep it this way :)

At the very beginning, I spent some time looking into the provided files, the problem specifications.  

And I made some observations: 
(1) In Vocab.gr, many words are tagged Misc.
(2) In Vocab.gr, the tag set used is not the same as the one used atis3.treebank.
(3) "The NLTK data package includes a 10% sample of the Penn Treebank".
(4) Atis3.treebank uses the same tag set as the Penn Treebank (also contains some phrase level tags).
(5) Many words in the allowed word list do not have tagged corpus, (e.g. 'sixty' is not in either brown or treebank)
(6) In the given Vocab.gr, words are well-categorized.
(7) There is a corpus in nltk.corpus.webtext.sents('grail.txt'), which is the target text

Step 1, improve the Vocab.gr:

- Given (2) I decided NOT to use the brown tag set but the nltk.corpus.treebank to re-tag the Vocab.gr
- Given (3),(5),(6) I decided to hand-tag and hand-re-tag the Vocab.gr according to penn tree band tag set
- Use Penn Treebank pos tag set representations (https://www.comp.leeds.ac.uk/ccalas/tagsets/upenn.html)
- *Given (7), I used the nltk pos tagger to tag the sentences, given it is trained from a tree bank, similar to penn treebank
- Add some new tags for the words to model the ambiguity.
- Tune the weights of each tag-word pair, using treebank data.
- Finally, I generated a file called "Vocab_grail.gr", providing the terminal words with tags and weights.
- Hand-tag those pairs still with Misc tag, all Misc are get rid of, results are in Vocab_grail_tuned.gr 
  (Notice #1, the "Vocab.gr" ipv_vocab.py reads in has been modified to fit the penn tree tag set)
  (Notice #2, we cannot tag , . ! etc.. to the original tags, since it causes cycle. I add $ to the tag, namely (,)->($,)
  (Notice #3, NLTK and Penn Treebank Official Tag for "--" seems to be inconsistent)

Step 2, generate the S2.gr, based on Vocab.gr

- In this step, basically I permute the combinations of tags, to generate the S2.gr, with weights, however. So it is a HMM.
- Run the program on the dev set, compared the cases having weights on vocab or not,and I found out that for S2.gr, 
  with weights we have a slightly better result (-9.21 -> -9.17)with the *no weights* one, which is a little bit surprising to me. 
  So the most part of Step 1 *seemingly* becomes useless.
- Then, I tried to add weights to this S2.gr, and I tried it using two ways. One is touse the text of "grail.txt", 
  to generate the HMM and then generate the weights for each rule. It increase the -entropy to -9.13; 
  The other is to use penn treebank, which increase the -entropy to -8.62, and with some hand tuning, 
  especially for the start symbol rules and rules for ".", it improved to -8.0002.
  Further tuning on S2.gr makes this S2-only result to -7.66 on dev set.
  
  (Notice #1, I found keeping the Misc tags for words like 'm and 're, instead of replacing them all, gives a better result. 
  I think it is because those ones are rather unique then just being "am" and "are". That's why use Misc to tag them is a good option.)

Step 3, generate the S1.gr

- I have to make a decision whether or not to hand-write it by looking into the provided data or generated the grammar from a treebank.
- I decided to chose the latter one, generating the grammar from atis.treebank. 
  This is because:
  1. You can always hand-tuned the grammar after generating it, but hardly do the opposite.
  2. I believe the grammar generated from the treebank will be more reasonable than what I, as a non-native speaker, hand-write.
  3. It is scalable. It has less chance to over fit the data.
  4. It is much easier for me as a programmer.
  5. It is much more interesting for me as a programmer.

- To generate my primary tagger, I used the nltk.Tree module, transforming the trees in atis3.treebank into eCNF, with a little bit more 
  code, especially on transforming the output into a Chomsky-normal-form. Also I sort the rules when write them into the file, 
  so that I can tune them easily after.

- Removed some tags/rules that does not appear in the Vocab.gr (find a tag and remove all others contains it). 
  
Step 4, tuning by generating some sentences using S1.gr, Vocab.gr

- I generate some sentences, and found there are some irreasonable ones. For example, "we" appears as a verb, so I look into the Vocab.gr, 
  it turns out when I modelled the ambiguity of the words and its pos-tags using nltk.treebank, I modelled this one, which is very unlikely,
  and the weights of it is unreasonably high. So I tuned again on the weights of the vocabularies. This time, I actually referred to the 
  frequency of words in nltk.corpus.webtext.sents('grail.txt'), but I did not use the original weight to avoid over fitting.

- Now the -entropy is around -7.4, using only S1.gr, and -7.3 using both S2.gr and S1.gr.

Step 5, how to make my grammar "competitive"

- What I thought was, if I want lower other's performance, I should find some ways to lower mine first. In the meantime,
  I can improve my own grammar. Kill two birds in one stone.
- It turns out, My grammar has a lot of "weakness" on itself, for example, it did not accept a comma as the beginning of a sentence.
  Then I found out there was a bug in my HMM, (use two different symbols for punctuations). But S1.gr still does not support it anyway.
  So I designated another "TRAP" rule to generate a sentence starts with a comma.
- Likewise I added sentences start with punctuations or end without period
- My S1.gr did not include possessive pronouns, now it does.
- I tuned the weight so that my own grammar can remain a -7.2 performance while generating this trap at the same time.
- My S2.gr based on HMM is quite strong, so that I thought can "defend" well.
  (Notice#1 : Trap I set is also a defence, since others may play the same trick.)

Step 6, check if Vocab.gr stays consistent with allow-words.txt

- Compare two files: allow-words.txt and Vocab.gr, in ipv_check.py  
- And I did find a not-allowed-word, so I removed it immediately
  
Finally, with a conservative tuning strategy, I obtained the final result on dev set:

FINAL ENTROPY ON DEV SET: -6.79 
  
Some thoughts:

- Even a model is presumed to be good after training, with some tuning, its performance can still improve a lot.
- There has always been a trade-off between tuning and over-fitting. An interesting thing is, when you try to
  generate some corner cases, it actually makes your grammar less over-fitting, and it also helps you "defend"
  others' unexpected grammar.

Finally, let me finish this note by a "poem" generated from my grammar in a single run: 
(there were many longer and reasonable ones, but I found this one most interesting)

********************
Title: Snake on You!
********************

'''
Arthur !
that snakes on you !
which snakes ?
one just !
'''

The End.


























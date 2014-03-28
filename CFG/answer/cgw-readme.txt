
#This is your readme file. Make it a good one. It should smell of elderberries.

The first glance at this problem made me decide to obtain the weighted context free grammar by inferring from the data set.

I spent some time looking into the provided files, including the *.gr, as well as the atis3.treebank. 

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

So in ipv_vocab.py:
- *Given (7), I used the nltk pos tagger to tag the sentences, given it is trained from a tree bank, similar to penn treebank
- Add some new tags for the words to model the ambiguity.
- Tune the weights of each tag-word pair, using treebank data
- Finally, I generated a file called "Vocab_grail.gr", providing the terminal words with tags and weights
- Rename Vocab_grail.gr to Vocab.gr as the part in the answer (having two names simply makes the programs look neat)
- Hand-tag those pairs still with Misc tag, all Misc are get rid of, results are in Vocab_grail_tuned.gr 
  (Notice #1, the "Vocab.gr" ipv_vocab.py reads in has been modified to fit the penn tree tag set)
  (Notice #2, we cannot tag , . ! etc.. to the original tags, since it causes cycle. I add $ to the tag, namely (,)->($,)
 
(NLTK and Penn Treebank Official Tag for "--" seems to be inconsistent)

Step 2, generate the S2.gr, based on Vocab.gr

- In this step, basically I permute the combinations of tags, to generate the S2.gr
- Run the program on the examples, compared the cases having weights on vocab or not,
  and I found out that for S2.gr, with weights we have a slightly better result (-9.21 -> -9.17)with the *no weights* one, which is a little bit surprising to me
- Then, I tried to add weights to this S2.gr, and I tried it using two ways. One is to
  use the text of "grail.txt", to generate the bigrams and then generate the weights for each rule. It increase the -entropy to -9.13; The other is to use penn treebank, which increase the -entropy to -8.62, and with some hand tuning, especially for the start symbol rules and rules for ".". It improved to -8.0002.
  Further tuning makes this S2-only result to -7.66 on dev set and -7.70 example text.
  (Notice #1, I found keeping the Misc tags for words like 'm and 're, instead of replacing them all, gives a better result. I think it is because those ones are rather unique then just being "am" and "are". That's why use Misc to tag them is a good option.)

Step 3, generate the S1.gr

Using nltk.Tree, we can transform the trees in atis3.treebank into eCNF.





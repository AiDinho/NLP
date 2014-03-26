
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
- Add some new tags for the words to model the ambiguity.
- Add some tages by hand.
- Tune the weights of each tag-word pair, using treebank data
- *Given (7), I used the nltk pos tagger to tag the sentences, given it is trained from a tree bank, similar to penn treebank
  - Generate a file called "Vocab_grail.gr", providing the tags (with weights) additional words part of Vocab.gr, hand tag some untagged Misc tags, 
    add/replace the content of the file to the Vocab.gr  
  
(NLTK and Penn Treebank Official Tag for "--" seems to be inconsistent)

Step 2, 



   
   



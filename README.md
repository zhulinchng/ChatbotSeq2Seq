# ChatBotSeq2Seq

CSCK507 NLP Group Project to implement a seq-2-seq model with and without attention mechanism for developing a generative chatbot.

## Datasets

### Microsoft Research WikiQA Corpus

Original paper: <https://aclanthology.org/D15-1237/>

[Description]( http://aka.ms/WikiQA)

- The WikiQA corpus is a new publicly available set of question and sentence pairs, collected and annotated for research on open-domain question answering.
- In order to reflect the true information need of general users, we used Bing query logs as the question source.
- Each question is linked to a Wikipedia page that potentially has the answer. Because the summary section of a Wikipedia page provides the basic and usually most important information about the topic, we used sentences in this section as the candidate answers.
- With the help of crowdsourcing, we included 3,047 questions and 29,258 sentences in the dataset, where 1,473 sentences were labeled as answer sentences to their corresponding questions.
- More detail of this corpus can be found in our EMNLP-2015 paper, "WikiQA: A Challenge Dataset for Open-Domain Question Answering" [Yang et al. 2015]. In addition, this download also includes the experimental results in the paper, an evaluation script for judging the "answer triggering" task, as well as the answer phrases labeled by the authors of the paper.

Other researches using this dataset:

- <https://paperswithcode.com/sota/question-answering-on-wikiqa>

### CMU Question-Answer Dataset

Original paper: <https://www.cs.cmu.edu/~nasmith/papers/smith+heilman+hwa.nsf08.pdf>

Wikipedia articles alongside manually-generated factoid questions

### Ubuntu Dialogue Corpus

Original paper: <https://arxiv.org/pdf/1506.08909.pdf>

Sample of one million two-person conversations extracted from the Ubuntu chat logs, used to train a “chatbot” to hold conversations with humans.

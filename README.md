# Sentiment Analysis of NetizenBuzz

**Table of Contents**

- [Sentiment Analysis](#sentiment-analysis)
- [NLTK and Vader Analysis](#nltk-and-vader-analysis)
- [Methods](#methods)
- [Results](#results)
  - [Word Counting](word-counting)
  - [Gender Classification](gender-classification)
  - [Validation](validation)
  - [Future Steps](future-steps)

Netizenbuzz has routinely been accused of bias, both by commenters on the site as well as elsewhere. To determine if Netizenbuzz is truly biased, we employed sentiment analysis to determine the overall positivity of articles translated by NetizenBuzz. The overall sentiment should generally reflect the positivity or negativity of a given post, and contrasting different groups along with known events (scandals, debuts, positive vents) should elucidate whether Netizenbuzz is biased.

Each article is ranked by its newsworthiness (based on the total interest by Netizens), its overall sentiment, and grouped by tags, for analysis by various combinations of these factors. This article is written for a well-educated layperson, and may not be comprehensible to the average Korean Pop, or K-Pop fan.

## Sentiment Analysis

To gage the overall tone of a body of text, we classify the utilization of various words to score the sentence by its overall tone. Specific words can add a positive, negative, or neutral sentiment to the sentence. The overall sentiment is then derived from a factor of these three: if the sentence is overwhelmingly neutral, with very little positive or negative content, the resulting score will be near 0, while positive sentences will be closer to 1 and negative sentences closer to -1.

## NLTK and Vader Analysis

The Natural Language Toolkit is a Python library to analyze natural speech, for the classification of human speech. [Vader analysis](http://www.nltk.org/api/nltk.sentiment.html#module-nltk.sentiment.vader) is a subset of natural language processing specialized for social media content, making it ideal for analyzing the nature of content on Netizenbuzz. We can also use naive Bayesian classifiers, which are then specialized for a given dataset, to enhance our dataset.

## Methods

The overall workflow, and source files are included throughout the repository. The general steps are as follows:

- Download (scrape) all content from Netizenbuzz
- Process the raw HTML into content (tags, comments, upvotes, downvotes).
- Count words by the most frequent, and add Korean and K-Pop slang (such as "ㅋ" and "iljin") to the sentiment dictionary.
- Calculate the sentiment of each comment, and rank the overall article.
- Analyze the data by different components (group, source).

## Results

### Word Counting

While analyzing Netizenbuzz posts for Korean slang, the following words the most frequently in the top 150 words. These words were then mapped to existing phrases in the Vader lexicon, to avoid introducing untested words into our reference set. The following words were added, as is shown in [kpop_lexicon.txt](/kpop_lexicon.txt).

| Slang    | Count  | Equivalent |
|:--------:|:------:|:----------:|
|  ㅋ      | 118564 |    lol     |
|  ㅠ      |  19546 |    :'(     |
| daebak   |   1814 |   great    |
| ㅜㅜ     |   1299 |   :'(      |
| ㅜ       |   453  |   :'(      |
| oppa    |   402  |            |
| ㅎ       |   392  |  giggle    |
| nuna    |   268  |            |
| Ilbe    |   265  |            |
| sajaegi |   243  | cheating   |

### Gender Classification

For classifying genders, foreign celebrities and CEOs were not included, with the exception of JYP, since he is still an active idol. Songs were associated with the group they correspond to, so for example, "4 walls" would correspond to "f(x)" and therefore be classified under female idols.

### Validation

To verify the validity of my methods, I selected a subset of the 10 most popular male and female idols/groups. Among the top 10, girl groups had more coverage, summing to nearly 60% of all articles in this subset.

In this subset, I selected 20 random articles from male or female idols (40 total), as well as 20 random articles from AOA or Block B as a control set. I manually analyzed the overalls sentiment of the comments and gave it a 0 score for neutral, +1 for positive, or -1 for negative, to contrast our control set to the Vader analysis.

**Scatter Plot**

To determine if our Vader analysis matched our control set, we plotted scores from [AOA posts](/validation/aoa.csv) against the compound scores from the Vader analysis.

![AOA Manual vs. Automatic Scatter Plot](/images/scatter_aoa.png)

However, we found no correlation between the manually assigned scores and the Vader scores, suggesting our Vader analysis is inaccurate or generally insufficient. If there was a correlation, we would expect manually-determined negative posts to produce negative Vader scores, with little overlap with positive posts. Instead, we see nearly the opposite: a large section of overlap between positive and negative posts, and on average higher Vader rankings for manually-assigned negative posts. Even without running a linear regression, we can tell we are looking primarily at noise.

**Sentiment over Time**

Since our Vader classifier does not seem to properly determine the general tone of Netizenbuzz-translated articles, we sought to determine whether the overall sentiment is neutral over time. Since a neutral sentiment could be attributed to an unbiased translator, two groups (Block B and AOA) were selected that had major scandals since Netizenbuzz started. If the Vader analysis is accurate, we would predict increases in negativity during their scandals, with as subsequent regression to the mean. For a control group, we plotted the time series of all posts, as well as subdivded into the top male and female idols, since the overall sentiment should be more stable relative to individual idols or groups.

| Male vs. Female Idols | AOA vs. Block B |
|:---------------------:|:---------------:|
| ![Male-vs-Female](/images/sentiment_time.png) | ![AOA-vs-BlockB](/images/aoa_blockb.png) |

The overall Vader sentiment plotted over time is mostly neutral and fairly stable, while for individual groups the sentiment is much noisier. However, we see no corresponding decrease in the Vader sentiment during idol scandals. For example, we see no major decrease in sentiment for Block B or AOA in May-August 2016, despite numerous negative articles published during AOA's "History Scandal" (May 2016) and during Seolhyun and Zico's dating scandal (August 2016). We can therefore concluded that our Vader model does not accurately reflect Netizen sentiment.

### Future Steps

Although Vader excels with emojis and instant-messaging, it seems to have particular difficulty with K-Pop vernacular. For example, the word "disband" carries a negative sentiment in K-Pop but does not change the compound sentiment in Vader Analysis. One possible step would be to train the Vader classifier to become aware of K-Pop vernacular, another would be to create a new classifier from naive Bayes' classifiers. Both of these steps would take substantial amounts of time, something I simply do not have.

## Credits

T-Ara, for their determination.
AOA, for being the constant brunt of my jokes.
Hwayoung, for not being her sister.

## License

The code here is freely released into the Public Domain, with the exception of `kpop_lexicon.txt`, which is under an MIT license. There are absolutely no restrictions on what you may do with these files.

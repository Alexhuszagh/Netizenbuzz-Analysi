# Sentiment Analysis of NetizenBuzz

**Table of Contents**

- [NLTK and Vader Analysis](#nltk-and-vader-analysis)

The following describes a sentiment analysis of the overall sentiment of the translated articles on NetizenBuzz grouped by artist tags. The overall sentiment is derived from the sentiment of the comments weighted by their popularity, in order to accurately reflect the overall sentiment of the comments posted on NetizenBuzz.

Each article is ranked by its newsworthiness (based on the total interest by Netizens), its overall sentiment, and grouped by tags, for analysis by various combinations of these factors. This article is written for a well-educated layperson, and may not be comprehensible to the average Korean Pop, or K-Pop fan.

## Sentiment Analysis

To gage the overall tone of a body of text, we classify the utilization of various words to score the sentence by its overall tone. Specific words can add a positive, negative, or neutral sentiment to the sentence. The overall sentiment is then derived from a factor of these three: if the sentence is overwhelmingly neutral, with very little positive or negative content, the resulting score will be near 0, while positive sentences will be closer to 1 and negative sentences closer to -1.

## NLTK and Vader Analysis

The Natural Language Toolkit is a Python library to analyze natural speech, for the classification of human speech. [Vader analysis](http://www.nltk.org/api/nltk.sentiment.html#module-nltk.sentiment.vader) is a subset of natural language processing specialized for social media content, making it ideal for analyzing the nature of content on Netizenbuzz.

## Methods

The overall workflow, and source files are included throughout the repository. The general steps are as follows:

- Download (scrape) all content from Netizenbuzz
- Process the raw HTML into content (tags, comments, upvotes, downvotes).
- Count words by the most frequent, and add Korean and K-Pop slang (such as "ㅋ" and "iljin") to the sentiment dictionary.
- Calculate the sentiment of each comment, and rank the overall article.
- Analyze the data by different components (group, source).

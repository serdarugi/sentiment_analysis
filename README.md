# sentiment_analysis
Using social media data, especially Reddit’s posts, this report explores applying sentiment
analysis to derive public opinion on climate change. Python’s PRAW library was leveraged to
fetch data from Reddit ‘climatechange’ subreddit, running queries such as ‘global warming’,
‘greenhouse gases’ and ‘carbon footprint.’ Posts were classified as positive, neutral or negative
sentiments with the help of VADER Sentiment Analyzer. To support dynamic sentiment
monitoring, the project used a hybrid Lambda architecture where both historical (batch) and real
time (streaming) data could be processed. Foundational insights came from batch processing, and
real time trends were captured using the streaming. Sentiment distributions and how they varied
were visualized using histograms and pie charts and finally presented in tables. Results showed
that positive sentiments (60%) were preceded by progress in climate action, while negative
sentiments (25 – 28%) pointed at policy failure and crisis.
Typically the neutral sentiments (12-15%) related to factual or informational content. The
analysis emphasized the polarization of climate discourse and its implications for developing
targeted awareness campaigns as well as for corporate sustainability strategies. Results of this
work show that sentiment study can provide input for strategies aimed at improving public
engagement and aligning organizational activities with public perceptions.

from wordcloud import WordCloud
import matplotlib.pyplot as plt


def generate_wordcloud(text, stopwords, filename):
    wordcloud = WordCloud(stopwords=stopwords).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(filename, bbox_inches='tight')
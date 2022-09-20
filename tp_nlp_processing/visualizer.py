from wordcloud import WordCloud
import matplotlib.pyplot as plt


def generate_wordcloud(text, filename):
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(filename)
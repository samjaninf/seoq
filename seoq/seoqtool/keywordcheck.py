# 18 July 2016, Jessie Shen
# Strips down a given phrase, removing google stopwords.


class KeywordChecker(object):

    def checkKeyword(self, keyword):
        query = keyword
        stopwords = []
        with open("seoq/seoqtool/stop_words.txt", "r") as ins:
            for line in ins:
                stopwords.append(line)
        querywords = query.split()
        resultwords = []
        for word in querywords:
            if word + '\n' not in stopwords:
                resultwords.append(word)
        result = ' '.join(resultwords)

        print result

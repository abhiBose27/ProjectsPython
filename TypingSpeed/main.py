from essential_generators import DocumentGenerator
import time

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def findSimilarity(x_sen, y_sen):
    x_list = word_tokenize(x_sen)
    y_list = word_tokenize(y_sen)

    sw = stopwords.words('english')
    l1 = []
    l2 = []

    x_set = {w for w in x_list if not w in sw}
    y_set = {w for w in y_list if not w in sw}

    rvector = x_set.union(y_set)
    for w in rvector:
        if w in x_set:
            l1.append(1)
        else:
            l1.append(0)
        if w in y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2))**0.5)
    return round(cosine * 100, 2)


def getText():
    gen = DocumentGenerator()
    return gen.paragraph(2, 3)


def main():
    inputStr = getText()
    print(inputStr)
    time.sleep(3)
    print("\nAfter you are done, press enter to know your time and speed")
    input("Press any key to Start: ")

    try:
        print("Timer started\n")
        start = time.time()
        t = input()
        end = time.time()
        total = round(end - start, 2)
        wpm = len(t) * 60 / (5 * total)
        print("Accuracy: ", str(findSimilarity(inputStr, t)) + "%")
        print("WPM: ", str(round(wpm)))
        print("Time: ", str(total) + "seconds")
    except KeyboardInterrupt:
        print("")


if __name__ == '__main__':
    main()

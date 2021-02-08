import spacy
from collections import Counter
nlp = spacy.load("ro_core_news_lg")

filename = "turist1.txt"
doc = str(open(filename, encoding="utf8").read())
doc = nlp(doc)


# for token in doc:
#     print(token.text, token.has_vector, token.vector_norm, token.is_oov)
#define some parameters
noisy_pos_tags = ["PROP"]
min_token_length = 2

#Function to check if the token is a noise or not
def isNoise(token):
    is_noise = False
    if token.pos_ in noisy_pos_tags:
        is_noise = True
    elif token.is_stop == True:
        is_noise = True
    elif len(token.text) <= min_token_length:
        is_noise = True
    return is_noise

def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()

# check all adjectives used with a word
def pos_words (sentence, token, ptag):
    sentences = [sent for sent in sentence.sents if token in sent.text]
    pwrds = []
    for sent in sentences:
        for word in sent:
            if token in word.text:
                pwrds.extend([child.text.strip()
                for child in word.children
                    if child.pos_ == ptag] )
    return Counter(pwrds).most_common(10)


cleaned_list = [cleanup(word.text) for word in doc if not isNoise(word)]
print(Counter(cleaned_list).most_common(7))

labels = set([w.label_ for w in doc.ents])
for label in labels:
    entities = [cleanup(e.text, lower=False) for e in doc.ents if label==e.label_]
    entities = list(set(entities))
    print (label,entities)

vulcan = [sent for sent in doc.sents if 'vulcan' in sent.text.lower()]

sentence = vulcan[3]
for word in sentence:
	print (word, ': ', str(list(word.children)))


found_adjective = pos_words(doc, 'vulcan', "ADJ")

print(found_adjective)
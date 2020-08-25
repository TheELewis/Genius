import nltk
import random
from nltk.corpus import masc_tagged as m_t
from syllabler import count # simple syl counter for now since nltks is too slow
import re
#consider importing pronouncing to do rhyme checks. It's simpler than nltk


def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word,
                   pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)

def nsyl(word):
    local_cmu_dict = nltk.corpus.cmudict.dict()
    return [len(list(y for y in x if y[-1].isdigit())) for x in local_cmu_dict[word.lower()]]


if __name__ == '__main__':
    fname = "ToyData.txt"
    fp = open(fname)
    lines = [line.strip('\n').lower() for line in fp]
    fp.close()
    tokenized_lines = []
    simpler_tokens = []
    for line in lines:
        #initialy removing punctuation for simplicity
        line = re.sub(r'[^\w\s]','',line)
        tokenized_line = nltk.word_tokenize(line)
        tokenized_lines.append(nltk.pos_tag(tokenized_line))
    #this only worked ok, maybe there is another model for me to use
    #rhymes = rhyme("hat", 10)
    #For each line, replace word with part of speech of same syllable count
    general_lines = []
    for line in tokenized_lines:
        new_line = []
        r = line[-1][0]
        for word in line:
            new_line.append([word[1],count(word[0]),0])
        new_line[-1][2] = (1, r)
        general_lines.append(new_line)
    
    madlib_lines = []
    ref_corpo = m_t.tagged_words()
    ceil = len(m_t.tagged_words())-1
    for line in general_lines:
        new_line = []
        for (word_pos, sylc, rhyme_flag) in line:
            #random selection to avoid repeated words and bias
            match_flag = 0
            if rhyme_flag != 0:
                rhyme_set = rhyme(rhyme_flag[1],1)
            while(not match_flag):
                #Find an equivalent POS with the same syllable count
                selection = random.randrange(ceil)
                print("Trying for {}".format(ref_corpo[selection]))
                if rhyme_flag != 0 and ref_corpo[selection][0] not in rhyme_set:
                    continue

                if (ref_corpo[selection][1] == word_pos): #Don't bother with slow syl count if POS doesn't match
                    match_flag = (count(ref_corpo[selection][0]) == sylc)
                    if not match_flag:
                        print("No Match")
            new_line.append(ref_corpo[selection][0])
        madlib_lines.append(new_line)
    with open('output.txt', 'a') as op_fd:
        for line in [' '.join(i) for i in madlib_lines]:
            op_fd.write(line + '\n')        
import re
from nltk.corpus import words
from itertools import product

mapping = {"1": ["1"],
           "2": ["A","B","C","2"],
           "3": ["D","E","F","3"],
           "4": ["G","H","I","4"],
           "5": ["J","K","L","5"],
           "6": ["M","N","O","6"],
           "7": ["P","Q","R","S","7"],
           "8": ["T","U","V", "8"],
           "9": ["W","X","Y","Z", "9"],
           "0": ["0"]}

def get_english_vocabulary(min_vocab_word_len):
    """ Use nltk.words word list,  words shorter than min_vocab_word_len will be excluded."""
    try:
        vocab = set([word.upper() for word in words.words() if len(word) >= min_vocab_word_len])
    except:
        print("NLTK 'words' corpus not found. Downloading...")
        import nltk
        nltk.download('words')
        vocab = set([word.upper() for word in words.words() if len(word) >= min_vocab_word_len])
            
    return vocab

def find_valid_word(regexp, vocab, get_all_words = False):
     """  Output either a single valid English word or a set of all English words matching input regex string. """
    all_words = set()
    for word in vocab: 
        hit = re.match(regexp, word.upper())
        if hit is not None:
            if not get_all_words: return word.upper()
            all_words.add(word.upper())
    return all_words

def number_to_words(num, vocab, mapping, min_word_len = 1):
    """ Convert str representing phone number to wordified str. If no valid wordifications exist - return original digits. """
    def find_usable_substrings(num_str, min_len = 1):
        """ Find substr of num_str and furter split them on chars that can't be converted to letters('1' and '0'). """   
        num_len, subs = len(num_str), set()
        
        for i in range(num_len):
            subs = subs.union([num_str[i:j + 1] for j in range(i + min_len - 1, num_len)])
        
        for el in subs.copy():
            if ("1" in el) or ("0" in el):
                subs.remove(el)
                subs.union(el.replace("1", "0").split("0"))
            return subs

    wordified = num.replace("-","")
    subs = find_usable_substrings(wordified, min_len = min_word_len)
    
    while len(subs)>0:
        substr = subs.pop()
        reg = "^" + "".join(["[" + "".join(mapping[ch]) + "]" for ch in substr]).replace("[-]","") + "$"
        word = find_valid_word(reg, vocab)
        if word == set(): word = None
        if word is not None: 
            wordified = wordified.replace(substr, word) #will replace all copies of substr if >1 present. Spec didn't specify desired behavior so leaving this as-is
            #print(substr.rjust(12),'<->', reg.rjust(50), '<->', str(word).rjust(12),'<->', wordified.rjust(12)) #uncomment to see intermediate steps
            break

    return wordified


def words_to_number(wordified, mapping):
    """ Reverse of number_to_words(). """
    reversed_num = ""
    for ch in wordified.replace("-","").upper():
        reversed_num +=  next(key for key, val in mapping.items() if ch in val)
            
    return reversed_num[0] + '-' + reversed_num[1:4] + "-" + reversed_num[4:7] + "-" + reversed_num[7:]

def all_wordifications(num, vocab, mapping):
    """ Output all possible combinations of numbers and English words in a phone number. """
    
    def gen_partitions(num_str):
        """ Generate all possible partitions of a string into constituent substrings. """
        for i in range(len(num_str)):
            if i == len(num_str) - 1:
                yield num_str

            first, rest = num_str[0:i+1], num_str[i+1:]

            for j in gen_partitions(rest):
                yield '~'.join([first, j])
                
    num = num.replace("-","")

    subs_dict, ans = dict(), set()
    for partition in gen_partitions(num):
        subs = partition.split('~')

        for sub in subs:
            #adding dict entries for previously not encountered substrings
            if sub not in subs_dict:
                if ("1" in sub) or ("0" in sub):
                    subs_dict[sub] = set()
                else:
                    reg = "^" + "".join(["[" + "".join(mapping[ch]) + "]" for ch in sub]) + "$" 
                    subs_dict[sub] = find_valid_word(reg, vocab, get_all_words = True)
                subs_dict[sub].add(sub)

        combos = product(*[subs_dict[el] for el in subs])
        
        for c in combos:
            ans.add("".join(c))
            
    return ans

if __name__ == '__main__':

    vocabulary = get_english_vocabulary(min_vocab_word_len = 3)
    
    print("\nWORDS TO NUMBER:")
    test_str = "1-800-PAINTER"
    print(test_str,' <-> ', words_to_number(test_str, mapping))

    print("\nNUMBER TO WORDS (one possible 'wordification'):")
    test_str = "1-800-724-6837"
    print(test_str,' <-> ', number_to_words(test_str, vocabulary, mapping, min_word_len = 4))
          
    print("\nALL WORDIFICAITONS:")
    test_str = "1-800-724-6837"
    all_words = all_wordifications(test_str, vocabulary, mapping)
    print("Done! Printing output (if minimal word size was set to 1 it may take some time):\n")
    print(all_words)



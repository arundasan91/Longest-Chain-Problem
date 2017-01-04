import time
import random

#Start timing the code
start_time=time.time()

#Open the textfile
testdata=open('dictionary.txt')

# value count for each key
count=0

# max length of any word
max_wLen=0

# dictionary for storing tokens
token_dict={}

# save lengths of token_dict
wLen_array=[]

# save number of values in each key
count_array=[]
test_data=[]
data_array=[]

# strip and tokenize words
for testword in testdata:
    testword=testword.strip()
    data_array.append(testword)
    wLen=len(testword)
    #wLen_array.append(str(wLen))
    if(wLen>max_wLen):
        max_wLen=wLen
    #change inside these-------------
    
    # If the key is not in the dictionary, add it; 
    # else append the new value (with same length) to the same key.
    # if not wLen in token_dict:
    #    token_dict_tuple[wLen]=[tuple(testword)]
    # else:
    #    token_dict_tuple.setdefault(wLen, []).append(tuple(testword))
    
    if not wLen in token_dict:
        token_dict[wLen]=[testword]
        wLen_array.append(int(wLen))
    else:
        token_dict.setdefault(wLen, []).append(testword) 

data_array.sort(key = lambda s: len(s))

# save number of values in each key to count_array[]
while count<len(wLen_array):
    count_array.append(int(len(token_dict[wLen_array[count]])))
    count+=1
    
#### 

def findWordsInList(word,wordList):
    listOfStrings=[]
    for i in range(len(wordList)):
        if isSubStr(wordList[i],word):
            listOfStrings.append(wordList[i])
    return listOfStrings

####


####

def isSubStr(bigstring,smallstring):
    ngram=False
    total=0
    sslen=len(smallstring)
    for letter in smallstring:
        if letter not in bigstring:
            ngram=False
        else:
            total=total+1
            bigstring=bigstring.replace(letter,"",1)
            #print(letter,bigstring)
    if total==len(smallstring):
        ngram=True
    return(ngram)

####
def splice(List, start, numdel):
    outList= List[:start] + List[start+numdel:]
    return outList
####

def findAllChains(data,token_dict):
    used_words={}
    def getChainsForWord(word):
        chains_for_word=[]
        def getNextWordsInChain(word):
            if (int(len(word)+1) in token_dict):
                next_words=findWordsInList(word, token_dict[int(len(word)+1)])
                #random.shuffle(next_words)
                #print(word, len(word)+1,token_dict[int(len(word)+1)],next_words,"\n")
                #next_words.sort(reverse=True)
                for j in range(len(next_words)):
                    if next_words[j] not in used_words:
                        used_words[next_words[j]] = 1
                        #if chains_for_word == []:
                            #used_words[next_words[j]] = 1
                        chains_for_word.append(next_words[j])
                        getNextWordsInChain(next_words[j])
                        #elif (len(chains_for_word[-1]) == len(next_words[j])-1) & (isSubStr(next_words[j],chains_for_word[-1])):
                            #if(len(chains_for_word)>4):
                        #    used_words[next_words[j]] = 1
                        #    chains_for_word.append(next_words[j])
                        #    getNextWordsInChain(next_words[j])
                    #else:
                        #print("not any chain",chains_for_word)
                    #    continue
        
        getNextWordsInChain(word)
        
        return chains_for_word
    
    chains={}
    #chains['to'] = getChainsForWord('to')
    for i in range(len(data)):
        if data[i] not in used_words:
            chains[data[i]] = getChainsForWord(data[i])
            #print(getChainsForWord(dataarray[i]))
    return chains

def findLongestChain(chains):
    longest_chain={'words':[],'chainLength':0}
    for word in chains:
        longest_chain_for_word= [word]
        test_chain= [word]
        chain_array= chains[word]
        #print("test_chain: ",test_chain)
        for i in range(len(chain_array)):
            if len(chain_array[i]) > len(test_chain[len(test_chain)-1]):
                test_chain.append(chain_array[i])
                #print("test_chain: ",test_chain)
            else:
                if len(test_chain) > len(longest_chain_for_word):
                    longest_chain_for_word = test_chain
                elems_to_splice = len(test_chain[len(test_chain)-1])-len(chain_array[i])+1
                test_chain=splice(test_chain, len(test_chain)-elems_to_splice, elems_to_splice)
                test_chain.append(chain_array[i])
            #print("test_chain: ",test_chain)
            if len(test_chain) > len(longest_chain_for_word):
                longest_chain_for_word = test_chain
            if len(longest_chain_for_word) > longest_chain['chainLength']:
                longest_chain['words'] = longest_chain_for_word
                longest_chain['chainLength']=len(longest_chain_for_word)
    return longest_chain

def getLongestChain(data, token_dict):
    start_time=time.time()
    longest_Chain = findLongestChain(findAllChains(data, token_dict))
    end_time=time.time()
    print("longest_Chain: ",longest_Chain,"TIME:",(end_time-start_time))
    return longest_Chain,(end_time-start_time)
####

getLongestChain(data_array, token_dict)

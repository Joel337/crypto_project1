import random

#constants
IN_LENGTH = 500
KEY_LENGTH = 25
UPPER = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = " abcdefghijklmnopqrstuvwxyz"
kp1 = ("cabooses meltdowns bigmouth makework flippest neutralizers gipped mule antithetical imperials carom masochism stair retsina dullness adeste corsage "
"saraband promenaders gestational mansuetude fig redress pregame borshts pardoner reforges refutations calendal moaning doggerel dendrology governs "
"ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepenults blacksmith constance furores chroniclers overlie hoers "
"jabbing resigner quartics polishers mallow hovelling ch")
kp2 = ("biorhythmic personalizing abjure greets rewashed thruput kashmir chores fiendishly combatting alliums lolly milder postpaid larry annuli codgers apostatizing "
"scrim carillon rust grimly lignifying lycanthrope samisen founds millimeters pentagon humidification checkup hilts agonise crumbs rejected kangaroo forenoons grazable acidy "
"duellist potent recyclability capture memorized psalmed meters decline deduced after oversolicitousness demoralizers ologist conscript cronyisms melodized girdles nonago")
kp3 = ("hermitage rejoices oxgall bloodstone fisticuff huguenot janitress assailed eggcup jerseyites fetas leipzig copiers pushiness fesse precociously modules navigates "
"gaiters caldrons lisp humbly datum recite haphazardly dispassion calculability circularization intangibles impressionist jaggy ascribable overseen copses devolvement "
"permutationists potations linesmen hematic fowler pridefully inversive malthus remainders multiplex petty hymnaries cubby donne ohioans avenues reverts glide photos antiaci")
kp4 = ("leonardo oxygenate cascade fashion fortifiers annelids co intimates cads expanse rusting quashing julienne hydrothermal defunctive permeation sabines hurries "
"precalculates discourteously fooling pestles pellucid circlers hampshirites punchiest extremist cottonwood dadoes identifiers retail gyrations dusked opportunities ictus "
"misjudge neighborly aulder larges predestinate bandstand angling billet drawbridge pantomimes propelled leaned gerontologists candying ingestive museum chlorites maryland s")
kp5 = ("undercurrents laryngeal elevate betokened chronologist ghostwrites ombres dollying airship probates music debouching countermanded rivalling linky wheedled heydey sours "
"nitrates bewares rideable woven rerecorded currie vasectomize mousings rootstocks langley propaganda numismatics foetor subduers babcock jauntily ascots nested notifying "
"mountainside dirk chancellors disassociating eleganter radiant convexity appositeness axonic trainful nestlers applicably correctional stovers organdy bdrm insis")

dictionary = ["awesomeness", "hearkened", "aloneness", "beheld", "courtship", "swoops", "memphis", "attentional", "pintsized", "rustics", "hermeneutics", "dismissive",
              "delimiting", "proposes", "between", "postilion", "repress", "racecourse", "matures", "directions", "pressed", "miserabilia", "indelicacy", "faultlessly",
              "chuted", "shorelines", "irony", "intuitiveness", "cadgy", "ferries", "catcher", "wobbly", "protruded", "combusting", "unconvertible", "successors", "footfalls",
              "bursary", "myrtle", "photocompose"]

#This function can be used to encrypt a plain-text with a random non-repeating key based on an input key
def encrypt(string, key):
    index_done = []
    index_cipher = []
    string_ciphered = ""
    i = 0

    print("Your key is " + key + " of length " + str(len(key)))

    # generate a randon keystream based on shifts from the given key and save into an array (index_cipher)
    while len(index_cipher) < len(string):
        key_index = key[random.randint(0, len(key)-1)]
        #print("Key index " + str(key_index))

        rand_fromKey = UPPER.find(key_index)
        #print("rand_fromKey: " + str(rand_fromKey))
        index_cipher.append(rand_fromKey)

    #print("The keystream, based on \'" + key + "\' is: \n")
    #print(index_cipher)
    
    # turn the input string into an array of numerical values. Using all caps ("UPPER") 
    while i < len(string):
        index = UPPER.find(string[i])
        index_done.append((index + index_cipher[i]) % len(UPPER))
        i=i+1
    
    for character in index_done:
        string_ciphered+=UPPER[character]

    return string_ciphered

#given a known plaintext and a ciphered string, find the key for 'length' chars
def forceKey(kp, c_string, length):
    index_kp = []
    index_c = []
    index_key = []

    if length > len(kp) or length > len(c_string):
        print("breaking, text is smaller than key length")
    else:
        i = 0
        while i  < length:
            index_kp.append(UPPER.find(kp[i]))
            index_c.append(UPPER.find(c_string[i]))
            index_key.append((((26 + index_c[i]) - index_kp[i]) % 27) + 1)
            i+=1
    #print("cipher text was " + c_string + " looking for " + kp + ". Returning:")
    #print(index_key)
    return index_key

#Checks all plaintexts to look for something that resembles a key. return the index of the KP and update the confidence value to the delta between the index sizes.
def iterateKPs(c_string, confidence):
    list = [kp1, kp2, kp3, kp4, kp5]
    counts =[]

    #go through each known plaintext and get the first part of the key (3x the max key length, assuming that plaintext
    for item in list:
        result_key = forceKey(item.upper(), c_string.upper(), KEY_LENGTH*3)
        values = []
        counter = 0
        #count the number of unique values in the resulting key.  If the count is > the keylength, we know it cannot be the key
        #(but for the random values).  For the test code, I don't use this though.
        for value in result_key:
            if value not in values:
                counter+=1
                values.append(value)
        counts.append(counter)
    

    #Find the comparative index lengths to determine confidence.  A large gap indicates higher confidence.
    counts_copy = counts
    m1 = sorted(counts_copy)[0]
    m2 = sorted(counts_copy)[1]
    confidence = int(m2)-int(m1)
    #The ciphertext is most likely from the plaintext where the key has the least entropy. e.g. if the key is "MARY", each shift can only be by one of 4 values.  
    #The minimum count finds this reliably until the key is the length of the alphabet.  At that point we would need to add some features. 
    return counts.index(min(counts)), confidence

#find the minimum number of characters needed to create a key for the word.  Return that value and the key.
def findPossibileWords(word, ciphertext):
    keyspace = 99
    keySequence = []
    cipher_copy = ciphertext

    while len(cipher_copy) >= len(word):
        key_index = forceKey(word, cipher_copy, len(word))
        if len(set((key_index))) < keyspace:
            keyspace = len(set(key_index))
            keySequence = key_index
        cipher_copy = cipher_copy[1:]
        #print(cipher_copy)
        #print("keyspace: " + str(keyspace))

    return keySequence, keyspace

# we can fine tune this, but I assume that for 500 chars over 40 words in the dictionary, we will have at least 3/5 of the words I picked. (**I haven't mathed this**)
def getCommonality(word_index_info):
    threeIndex = []
    jointIndex = []
    ordered = []
    #right now I am just taking the three words with the smallest keyspace. alternatively we could look for overlap.
    for item in word_index_info:
        ordered.append(item[1])
    ordered.sort()
    
    i = 0
    while i < 3:
        for item in word_index_info:
            if item[1] == ordered[i]:
                threeIndex.append(item[0])
        i+=1

    jointIndex = threeIndex[0] + threeIndex[1] + threeIndex[2]
    jointIndex = list(set(jointIndex))

    print("my key guess is ")
    print(jointIndex)
    return jointIndex

def forceDict(cipher_text, key_guess):
    found_counter = 0
    i = 0
    decrypted = ""
    while i < len(cipher_text):
        flow_control = 0
        for word in dictionary:
            if testWord(word, cipher_text[i:(i+len(word)+1)], key_guess): 
                decrypted+=(word + " ")
                found_counter += 1
                i+=(len(word)+1)
                flow_control = 1
        if flow_control == 0:
            decrypted+=cipher_text[i]
            i+=1
 
    return decrypted, found_counter

#This does a character by character analyis to see if the word can be formed from the probable key
def testWord(word, cipher_text, key_guess):
    validity_array = []
    i = 0
    word=word.upper()+" "
    if len(word) > len(cipher_text):
       #word=word[0:len(cipher_text)] #this doesn't appear to be working, instead we will just give up on partial words for now
       return False
    while i < (len(word)-1):
        reqValue = ((UPPER.find(cipher_text[i]) - UPPER.find(word[i])) % 27) 
        #print("cipher " + cipher_text[i]+ "and the word character " + word[i] + " looking for " + str(reqValue))
        #the best case is that the chars line up directly with a possible key value (no random injected characters. If they line up, add a 1 to the array.
        if reqValue in key_guess:
            validity_array.append(1)
        #This is a test case for dealing with randomness. Right now it doesn't work, as it lets way too many words in.
        #elif (i+1 < len(word)) and (((UPPER.find(cipher_text[i+1]) - UPPER.find(word[i])) % 27) in key_guess):
        #    validity_array.append(1)
        else:
            validity_array.append(0)
        i+=1
    
    #We can look at how many valid chars we have and how many invalid chars we have. Not clear to me what the right number is here.
    if (len(word) - sum(validity_array)) > 1:
        return False
    else:
        return True

#Here's our driver code
kp = input("Input your plaintext or enter 1-5 for a known plaintext: ")
if kp == "1":
   kp = kp1
if kp == "2":
   kp = kp2
if kp == "3":
   kp = kp3
if kp == "4":
   kp = kp4
if kp == "5":
   kp = kp5

confidence = 0
x = str(input("Insert key: "))
ret = encrypt(kp.upper(), x.upper())
#print ("returned ciphertext is: \n" + ret)
prob_KP = iterateKPs(ret.upper(), confidence)
answer = ""
if prob_KP[0] == 0:
   answer = kp1
if prob_KP[0] == 1:
   answer = kp2
if prob_KP[0] == 2:
   answer = kp3
if prob_KP[0] == 3:
   answer = kp4
if prob_KP[0] == 4:
   answer = kp5

confidence = prob_KP[1]




#Start looking at the dictionary/begin case 2 analysis. Right now it has a few large words. I think a better approach may be to pick words with as many different chars as possible
bigwords = ["intuitiveness", "faultlessly", "hermeneutics", "unconvertible", "photocompose"]

minWordKeys = []
for word in bigwords:
    minWordKeys.append(findPossibileWords(word.upper(), ret.upper()))

keyGuess = getCommonality(minWordKeys)

decryption = forceDict(ret, keyGuess)

#we should test to set these at accurate measures. these are just guesses.
#if the confidence is higher than 5, we have likely found a known plaintext. We can also return that answer and break before processing the case 2 stuff.  
if confidence > 5:
    print("Probable known plaintext is case " + str(prob_KP[0]+1) + ". The confidence level is " + str(prob_KP[1]))
    print("That plaintext is: " + answer)

elif decryption[1] > 40:
    print("We are guessing this is a case two text, and our decryption guess is: \n")
    print(decryption[0])
elif (decryption[1] < 25 and confidence > 2 ):
    print("We aren't really sure on this one, we are guessing a known plaintext, " + str(prob_KP[0]+1))
    print(answer)
else:
    print("You won this round, we don't know. In an attempt to salvage some credit, here are our guesses:")
    print("maybe known plaintext " + str(prob_KP[0]+1) + "or a case two text decrypted as follows: ")
    print(decryption[0])



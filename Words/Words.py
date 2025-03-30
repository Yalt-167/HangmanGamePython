from random import choice 

def Pick(length : int) -> str:
    return choice(Read()[length])

def Read() -> dict[int,list[str]]:
    with open("Words/Words.txt","r") as words:
        wordsDict : dict[int,list[str]] = dict()
        for word in words:
            word = word.strip().lower()
            if len(word) in wordsDict:
                wordsDict[len(word)].append(word)
            else:
                wordsDict[len(word)] = [word]
    return wordsDict

def RemoveInvalidWords() -> None:
    with open("Words/InitialWords.txt","r") as words:
        with open("Words/Words.txt","w+") as txt:
            for word in words:
                word = word.strip().lower()
                if 2 < len(word) < 10:
                    txt.write(word + "\n")


if __name__ == "__main__":
    RemoveInvalidWords()
    wholeDict = Read()
    for length in range (1,20):
        try:
            cur = wholeDict[length]
            print(len(cur)," words for length : ",length)
        except KeyError:
            print(f"No word for the length {length}")



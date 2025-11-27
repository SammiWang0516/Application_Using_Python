import music_search
# for detecting the encoded type of the file
import chardet

fileName = "music.csv"

with open(fileName, 'rb') as f:
    rawdata = f.read()
result = chardet.detect(rawdata)
print(result)

music = music_search.MusicLibrary()
music.readFile(fileName)
music.printData()

print()

print(music.binarySearch("Taylor Swift", 0))

print(music.seqSearch("Taylor Swift", 0))

music.shuffleData()

music.quickSort(0)

music.printData()
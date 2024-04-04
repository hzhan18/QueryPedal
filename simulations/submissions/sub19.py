story=open("story.txt")
words=open("words.txt")
x=story.read()
for lin in words:
    #x=x.replace(lin,"____")
print(x)
story.close()
words.close()
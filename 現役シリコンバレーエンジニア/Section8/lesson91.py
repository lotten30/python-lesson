f = open("test.txt", "w")
f.write("Test\n")
print("My","name", "is", "Mike", sep="--", file=f)
f.close()
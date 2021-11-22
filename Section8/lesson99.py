import zipfile
import glob

with zipfile.ZipFile("test.zip", "w") as z:
    #z.write("test_dir")
    #z.write("test_dir.test.txt")
    for  f in glob.glob("Section8/test_dir/**", recursive=True):
        #print(f)
        z.write(f)

with zipfile.ZipFile("test.zip", "r") as z:
    z.extractall("zzz")
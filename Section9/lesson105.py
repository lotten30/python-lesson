import csv
import os

from tools.tools import read_template, ranking_sort

if not os.path.exists("Section9/ranking.csv"):
    with open("Section9/ranking.csv", "w", newline="") as csv_file:
        fieldnames = ["NAME", "COUNT"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

text_ask_name = read_template()[0]
text_ask_restaurant = read_template()[1]
text_recommend_restaurant = read_template()[2]
text_bye = read_template()[3]

text1 = text_ask_name.substitute(name="Roboko")
print(text1)

while True:
    input_name = input()
    if input_name != "":
        break

with open("Section9/ranking.csv", "r+") as csv_file:
    reader = csv.DictReader(csv_file)
    d={}
    for row in reader:
        d[row["NAME"]] = int(row["COUNT"])
    print(d)

    ### ranking.csv が空でなければ実行
    if d:
        rank_sorted = ranking_sort(d)

        for idx in range(len(rank_sorted)):
            text2 = text_recommend_restaurant.substitute(
                recommend_restaurant=rank_sorted[idx][0])
            print(text2)

            while True:
                input_yn = input()
                if (input_yn == "y") or (input_yn == "n"):
                    break
            
            if input_yn == "n":
                continue
            
            if input_yn == "y":
                #print(d)
                d[rank_sorted[idx][0]] += 1
                #print(d)
                break


    if input_yn == "n":
        text3 = text_ask_restaurant.substitute(input_name=input_name)
        print(text3)

        while True:
            input_shop = input()
            if input_shop != "":
                break
        
        if input_shop not in d:
            d[input_shop] = 0
        d[input_shop] += 1
        #print(d)


with open("Section9/ranking.csv", "w", newline="") as csv_file:
    fieldnames = ["NAME", "COUNT"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in d:
        writer.writerow({"NAME":row, "COUNT":d[row]})

#print(d)

text4 = text_bye.substitute(input_name=input_name)
print(text4)

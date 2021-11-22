import string

def read_template():

    with open("Section9/text_dir/ask_name.txt", "r") as f:
        text_ask_name = string.Template(f.read())

    with open("Section9/text_dir/ask_restaurant.txt", "r") as f:
        text_ask_restaurant = string.Template(f.read())

    with open("Section9/text_dir/recommend_restaurant.txt", "r") as f:
        text_recommend_restaurant = string.Template(f.read())

    with open("Section9/text_dir/bye.txt", "r") as f:
        text_bye = string.Template(f.read())

    return text_ask_name, text_ask_restaurant, text_recommend_restaurant, text_bye

def ranking_sort(dict):
    rank_sorted = sorted(dict.items(), key=lambda x:x[1], reverse=True)
    print(rank_sorted)
    return rank_sorted


#def ranking_get(dict):
#    return dict[0]

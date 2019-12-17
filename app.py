import requests
import urllib.parse
#
# deco = 'Antidote Jewel+'
# if (deco.find("Jewel") >=0) or (deco.find("Jewel+")>=0): #jewel word exists
#     if deco[-1].isdigit():
#         print("search detailed with jewel")
#     else:
#         deco = deco + " 1"
#         print(deco)
#     # digit_exists = False
#     # for d in deco.split():
#     #     if d.isdigit(): #if there is number in the string
#     #         if (int(deco[-1])) > 0: #positive number
#     #             digit_exists = True
#     #         else:
#     #             digit_exists = False
#     #     else:
#     #         digit_exists = False
#     # if digit_exists:
#     #     print('search detailed')
#     # else:
#     #     print('search generally')
# else: #no jewel keyword
#     if deco[-1].isdigit():
#         print("search detailed with no jewel")
#     else:
#         print("searched generally with no jewel")


# text = "Antidote Res 2"
# new_text = text.split()
# test_text = new_text[:-1]
# if new_text[-1].isdigit():
#     new_text.insert(-1,'Jewel')
# else:
#     new_text.append("Jewel")
#     new_text.append("1")
# print(" ".join(new_text))
name = 'monster bone+'
# new_encode = '{"name":"' + name + '"}'
# encode = urllib.parse.quote(new_encode, safe='"')
# print(encode)
# query = 'https://mhw-db.com/items/?q=' + encode
name = urllib.parse.quote(name)
query = 'https://mhw-db.com/items/?q={"name":"' + name + '"}'
print(query)
r = requests.get(query)
result = r.json()
print(result)
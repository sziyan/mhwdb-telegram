import requests

# r = requests.get('https://mhw-db.com/weapons/497')
# #r = requests.get('https://mhw-db.com/monsters/?q={"name":"nergigante"}')
# reply = r.json()
# slot = []
# listOfSlots = reply.get('slots')
# # for i in range(0,len(listOfSlots)):
# #     slot.append(str(listOfSlots[i].get('rank')))
# #
# # slot_msg = ', '.join(slot)
# # print(slot_msg)
# print(len(listOfSlots))

# image = "https:\/\/assets.mhw-db.com\/weapons\/great-sword\/76e6584da87cdfb534ef27e7cc8a851b2ab24f08.9267944286ff359b6d24cdda11a748be.png"
# link = image.replace("\/","/")
# print(link)

branches = [2,3]
for weapon_id in branches:
    print(weapon_id)
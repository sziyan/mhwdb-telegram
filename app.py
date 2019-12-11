import requests

r = requests.get('https://mhw-db.com/monsters?q={"name":"nergigante"}')
reply = r.json()[0]
#reply = r.text
print(reply)



# events_name=[]
# for e in reply:
#     #events.append(e.get('name'))
#     events.append(e.get('name'))
# print('\n'.join(events))

# weakness = []
# all_weakness = reply.get("weaknesses")
# for w in all_weakness:
#     weakness.append(w.get('element'))
# print(','.join(weakness))
# print(reply.get("species"))
# print(reply.get("description"))
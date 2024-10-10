# create an empty dictionary
d = {}
# d = {'key1' : 'value1', 'key2' : 'value2'}

# add entry inside the dictionary
d['serpent'] = 'it is a snake'
d['peroquet'] = 'it is a parrot'

# view value of the a key
print(f"The value at serpent key is: {d['serpent']}")

# view all entries of a dictionary
print(f"Here all the current entries: \n{d}")

# modifies or replace value a given key
d['peroquet'] += ' bird'
print(f"Updated dictionary: \n{d}")

# delete entry of a dictionary
del d['serpent']
print(f"the new dictionary entry are: \n{d}")

# loop over dictionary keys
for x in d:
    print(d[x])
    print(x)

# Same: loop over dictionary using a key method
for x in d.keys():
    print(x)

# loop over dictionary values
for y in d.values():
    print(y)
    
# loop over dictionary entries
for z in d.items():
    print(z)

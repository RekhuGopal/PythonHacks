from event import data

print(data['bucket'])
print(data['name'])
print(data['timeCreated'])

from main import streaming

streaming(data, 'context')
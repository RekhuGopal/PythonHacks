import xml
import requests

input_region = "EU" # programatic

#https://my.pingdom.com/probes/feed

response = requests.get("https://my.pingdom.com/probes/feed")
raw_xml = response.content
print(response.content)

#method -1
Ips =  []
for each_line in raw_xml:
    if "<pingdom:ip>" in  each_line and "</pingdom:ip>" in  each_line:
        if input_region in each_line:
            Ips.append(each_line.split())

#method - 2
xml_read_form = response.content
# List down the all #item block as array.
'''
[<item>
                <pingdom:ip>178.162.206.244</pingdom:ip>
                <pingdom:region>EU</pingdom:region>
</item>]
'''



     


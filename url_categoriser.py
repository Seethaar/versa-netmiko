#!/usr/bin/env python3
import os,re
from netmiko import ConnectHandler
import pandas as pd
filename = input('Enter the filename : ')
with open(filename,'r') as fh:
    urls = fh.read().splitlines()
pp = os.environ.get('pp')
dfs = pd.DataFrame(columns=['URL','Reputation','Reputation_Score','Category_ID','Category_Confidence','Category'])
remote_device = {
    'device_type': 'flexvnf_ssh',
    'ip': "10.156.67.151",
    'username': "admin",
#    'password': "versa123",
    'use_keys': True,
#    'allow_agent': true,
    'key_file': '/mnt/c/Users/RNNAN2/OneDrive - AMP Services Ltd/Documents/openssh_key',
    'passphrase': pp
}
#outputs = []
row_iter = 0
org = 'AMP-Dev'
#cmds = ['request orgs org-services AMP-Dev url-filtering cloud-lookup lookup url webshar.es', 'request orgs org-services AMP-Dev url-filtering cloud-lookup lookup url webshar.us']
# global_delay_factor IS THE KEY :p
net_connect = ConnectHandler(**remote_device, global_delay_factor=2)
for url in urls:
    cmd = f'request orgs org-services {org} url-filtering cloud-lookup lookup url {url}'
    output = net_connect.send_command(cmd)
    xe = re.search(r"(?<=Reputation)\s*:\s(\d*)\s\((.*)\)", output)
    print(xe.groups())
    dfs.at[row_iter,'URL'] = url
    dfs.at[row_iter,'Reputation_Score'] = xe.groups()[0]
    dfs.at[row_iter,'Reputation'] = xe.groups()[1] 
    if 'Categories' in output:
        #print('categorised')
        xe2 = re.search(r".*\s*ID\s:\s*(\d*),\sConfidence:\s*(\d*),\sName\s:\s(\w*)",output)
        #print(xe2.groups())
        dfs.at[row_iter,'Category_ID'] = xe2.groups()[0]
        dfs.at[row_iter,'Category_Confidence'] = xe2.groups()[1]
        dfs.at[row_iter,'Category'] = xe2.groups()[2]
    else:
        print('this URL is uncategorised')
        dfs.at[row_iter,'Category_ID'] = "N/A"
        dfs.at[row_iter,'Category_Confidence'] = "N/A"
        dfs.at[row_iter,'Category'] = "Uncategorised"
    row_iter+= 1
#    print(output)
    #outputs.append(output)

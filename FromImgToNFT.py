#############
## MODULES ##
#############

import os
import json
import requests
import http.client
import time
from distutils.command.upload import upload

###############
## FUNCTIONS ##
###############

def selec_data(listNFT):
    celebrities = []
    tweets = []
    styles = []
    for nft in listNFT:
        celebrities.append(nft.split("_")[0])
        tweets.append(nft.split("_")[1])
        styles.append(nft.split("_")[2])
    return celebrities, tweets, styles

def upload_file(NFTfile,api):
    print("\nTry to upload the file:\n")
    file = open(NFTfile, "rb")
    response = requests.post(
        "https://api.nftport.xyz/v0/files",
        headers={"authorization": api},
        files={"file": file}
    )
    ipfsurl = response.json()["ipfs_url"]
    print("ipfsurl:", ipfsurl)
    return ipfsurl

def create_smart_contract(api):
    print("Create the smart contract:\n")
    url = "https://api.nftport.xyz/v0/contracts"
    payload = "{\n  \"chain\": \"polygon\",\n  \"name\": \"AI generate image from Tweets of celebrities\",\n  \"symbol\": \"AIMGT\",\n  \"owner_address\": \"0xd1ed4C17f17E447577315B857A6F80e9A43eeD6E\",\n  \"metadata_updatable\": false\n}"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "%s"%api
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    #print(response.text)   
    trxhash = response.json()["transaction_hash"]
    print("trx hash:",trxhash)
    return  trxhash

def get_contract_addres(trxhash,api):
    print("\nTry to get the contract adress:")
    conn = http.client.HTTPSConnection("api.nftport.xyz")
    headers = {
        'Content-Type': "application/json",
        'Authorization': "%s"%api
        }
    url = "/v0/contracts/%s?chain=polygon"%trxhash
    conn.request("GET",url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    NFTcontract = json.loads(data)["contract_address"]
    print("NFT contract:",NFTcontract)
    return NFTcontract

def upload_metadata(api, celebrity, tweet, style, ipfsurl):
    print("\nTry to upload the metadata file:")
    conn = http.client.HTTPSConnection("api.nftport.xyz")
    payload = "{\n  \"name\": \" %s\",\n  \"description\": \"Images generated with VQGAN+CLIP algorithm based on %s 's tweet\",\n  \"file_url\": \"%s\",\n  \"attributes\": [\n  {\n  \"trait_type\": \"Style\",\n  \"value\": \"%s\"\n }\n  ]\n}"%(tweet,celebrity, ipfsurl, style)
    headers = {
        'Content-Type': "application/json",
        'Authorization': "%s"%api
        }
    conn.request("POST", "/v0/metadata", payload, headers)
    res = conn.getresponse()
    data = res.read() 
    data = data.decode("utf-8")
    metadatauri  = json.loads(data)["metadata_uri"] 
    print("metadata url:",metadatauri) 
    return metadatauri

def mint_the_nft(api,NFTcontract,metadatauri):
    print("\n\Try to mint the nft:")
    conn = http.client.HTTPSConnection("api.nftport.xyz")
    payload = "{\n  \"chain\": \"polygon\",\n  \"contract_address\": \"%s\",\n  \"metadata_uri\": \"%s\",\n  \"mint_to_address\": \"0xd1ed4C17f17E447577315B857A6F80e9A43eeD6E\"\n}"%(NFTcontract,metadatauri)
    headers = {
        'Content-Type': "application/json",
        'Authorization': "%s"%api
        }
    conn.request("POST", "/v0/mints/customizable", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    print(data)
    return 

def main():
    apifile = open('nftportaut.txt',"r")
    api = apifile.read()[4:]
    apifile.close()
    listNFT = os.listdir(r"NFTweets/") 
    os.chdir(r"NFTweets/") 
    ipfsurls = []
    for nft in listNFT:
      ipfsurls.append(upload_file(nft,api))
    #ipfsurl = upload_file(listNFT[0],api)
    listNFT = [nft[:-4] for nft in listNFT]
    celebrities, tweets, styles = selec_data(listNFT) 
    #trxhash = create_smart_contract(api)
    trxhash = "0x5a9afcb5b1e23314db4169fef94a22253a0ebfd63ec08d90b2f913e60e1054c3" #This is a trxHash from a smart contract already created
    NFTcontract = get_contract_addres(trxhash,api)
    #metadatauri = upload_metadata(api, celebrities[0], tweets[0], styles[0], ipfsurl)
    #mint_the_nft(api,NFTcontract,metadatauri)
    # for i in range(len(listNFT)):
    #     metadatauri = upload_metadata(api, celebrities[i], tweets[i], styles[i], ipfsurls[i])
    #     mint_the_nft(api,NFTcontract,metadatauri)
if __name__ == "__main__":
    main()

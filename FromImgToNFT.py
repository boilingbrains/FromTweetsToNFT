from distutils.command.upload import upload
import os
import json
import requests
import http.client

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
    url = "https://api.nftport.xyz/v0/contracts"
    payload = "{\n  \"chain\": \"polygon\",\n  \"name\": \"AI generate image from Tweets of celebrities\",\n  \"symbol\": \"AIMGT\",\n  \"owner_address\": \"0xd1ed4C17f17E447577315B857A6F80e9A43eeD6E\",\n  \"metadata_updatable\": false\n}"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "%s"%api
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)   
    trxhash = response.text["transaction_hash"]
    return  trxhash

def get_contract_addres(trxhash,api):
    conn = http.client.HTTPSConnection("api.nftport.xyz")
    headers = {
        'Content-Type': "application/json",
        'Authorization': "%s"%api
        }
    conn.request("GET", "/v0/contracts/{}?chain=polygon".format(trxhash), headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    NFTcontract = data["contract_address"]
    return NFTcontract



def upload_metadata(api, celebrity, tweet, style, ipfsurl):
    conn = http.client.HTTPSConnection("api.nftport.xyz")
    payload = "{\n  \"name\": \" %s\",\n  \"description\": \"Images generated with VQGAN+CLIP algorithm based on %s 's tweet\",\n  \"file_url\": \"%s\",\n  \"attributes\": [\n  {\n  \"trait_type\": \"Style\",\n  \"value\": \"%s\"\n  }  }\n  ]\n}"%(tweet,celebrity, ipfsurl, style)
    headers = {
        'Content-Type': "application/json",
        'Authorization': "%s"%api
        }
    conn.request("POST", "/v0/metadata", payload, headers)
    res = conn.getresponse()
    data = res.read() 
    print(data.decode("utf-8"))
    metadatauri  = data["metadata_uri"]  
    return metadatauri

def mint_the_nft(api):
    conn = http.client.HTTPSConnection("api.nftport.xyz")
    payload = "{\n  \"chain\": \"polygon\",\n  \"contract_address\": \"0x8E187F7b8D62f3F9f1490A3B8659ac03ca34C540\",\n  \"metadata_uri\": \"ipfs://bafkreiepfwroxy47wzvllrfyu5dwecz6blkiztzmc3r3frryasdve74zii\",\n  \"mint_to_address\": \"0xF62735d60151852dAFACfF270a926a7911b6705e\"\n}"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "<api-key>"
        }

    conn.request("POST", "/v0/mints/customizable", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

    return 


def main():
    apifile = open('nftportaut.txt',"r")
    api = apifile.read()[4:]
    apifile.close()
    # network = 'https://rpc-mumbai.maticvigil.com'
    listNFT = os.listdir(r"NFTweets/") 
    os.chdir(r"NFTweets/") 
    ipfsurls = []
    for nft in listNFT:
       ipfsurls.append(upload_file(nft,api))
    listNFT = [nft[:-4] for nft in listNFT]
    celebrities, tweets, styles = selec_data(listNFT) 
    metadatauri = upload_metadata()
    trxhash = create_smart_contract(api)
    NFTcontract = get_contract_addres(trxhash,api)

if __name__ == "__main__":
    main()

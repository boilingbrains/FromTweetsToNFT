import os
import json
#from thirdweb import ThirdwebSdk, SdkOptions

# nft_smart_contract_address = "0x5BF9a35287F5d0f0FF2b1Ace4d0aDD0E47824ae2"
# sdk = ThirdwebSdk(SdkOptions(), 'https://rpc-mumbai.maticvigil.com')
# sdk.set_private_key(os.environ['PRIVATE_KEY'])
# nft_module = sdk.get_nft_module(nft_smart_contract_address)

list_nft = os.listdir(r"NFTweets/") 
print(list_nft)

#TODO: list nft inside output, choose a rondom one, copy/move to NFTtweets if minted to avoid double 

# name_nft = "new nft!"
# description_nft = "NFT EXAMPLE"
# image_nft = "ipfs://QmdFeKxt6FJUNvaGgzYuYNRbpNWyHxP2PFzjsgPf1eD2Jf"
# prop = {}

# nft_module.mint(MintArg(name=name_nft,
# description=description_nft,
# image_uri=image_nft,
# properties=prop))
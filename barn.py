#!/usr/bin/env python3

import asyncio
import sys
import argparse
import json
import urllib.request
import subprocess

'''
Available APIs to pull CAT data from:
    
    natsabari in Keybase:
    https://api2.spacescan.io/1/xch/tokens/summary?page=1&count=25
    
    
    https://xchtoken.org/token_api.php
    
'''
CAT_API_URL='https://xchtoken.org/token_api.php'

async def update_with_new_cats(chia_path, chia_wallet_fingerprint):
    print('----------UPDATE CATS ---------')
    
    # get a list of current cats
    all_cats = await get_available_cats()
    # print(json.dumps(all_cats, indent=4, sort_keys=True))
    
    print('Looking for stray CATs...\n')
    # get CATs from chia light wallet which don't have names in chia wallet
    chia_local_wallet_cat_list=chia_path + " wallet show -f " + chia_wallet_fingerprint
    process = subprocess.Popen(chia_local_wallet_cat_list, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output,stderr = process.communicate()
    status = process.poll()
    # print(output)
    untamed_cats_list = []
    for line in output.decode('ascii').splitlines():
        # print(line)
        
        if "type COLOURED_COIN CAT WALLET" in line:
            line_as_list = line.split()
            asset_id_location = line_as_list.index('ID:')
            if (asset_id_location != -1):
                unnamed_asset_id = line_as_list[asset_id_location+1]
                
                unnamed_asset_id = unnamed_asset_id.replace(')', '')
                wallet_id = line_as_list[2]
                print("FOUND unnamed CAT: walletID: " + wallet_id + " assetID: " + unnamed_asset_id)
                untamed_cats_list.append(unnamed_asset_id)
    
    
    if (len(untamed_cats_list) == 0):
        print ("All cats are tamed...err...named [^._.^]ﾉ彡")
        sys.exit(1)
    
    # print(json.dumps(all_cats, indent=4, sort_keys=True))
    
    # rename cats without names
    for untamed_cat in untamed_cats_list:
        
        await rename_cat(chia_path, chia_wallet_fingerprint, untamed_cat, all_cats)
    
    print("All cats are tamed...err...named [^._.^]ﾉ彡")
    
#chia wallet add_token -id <asset_id> -n <asset_name>
async def rename_cat(chia_path, chia_wallet_fingerprint, asset_id, known_cats_list):
    
    known_cats_list = known_cats_list['data']
    
    for known_cat in known_cats_list:
        # print(known_cat)
        # print('-------------------------------------------')
        
        if not 'ASSET_ID' in known_cat:
            continue
        
        if (known_cat['ASSET_ID'] == asset_id):
            
            if not 'Symbol' in known_cat and not 'Name' in known_cat:
                print('ERROR: Found ASSET_ID but neither Symbol nor Name...skipping...')
                continue
            
            new_wallet_name = ''
            symbol = ''
            name = ''
            
            if 'Symbol' in known_cat:
                symbol = known_cat['Symbol']
                new_wallet_name = symbol
            
            if 'Name' in known_cat:
                name = known_cat['Name']
                
                if len(new_wallet_name) > 0:
                    new_wallet_name += " (" + name + ")"
                else:
                    new_wallet_name = name
            
            # print("Adopting CAT: " + new_wallet_name)
            
            chia_local_wallet_cat_list=chia_path + " wallet add_token -f " + chia_wallet_fingerprint + " -id " + asset_id + ' -n \"' + new_wallet_name + '\"'
            process = subprocess.Popen(chia_local_wallet_cat_list, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output,stderr = process.communicate()
            status = process.poll()

            for line in output.decode('ascii').splitlines():
                print(line)
            
            print('----------------------------------------')
    

async def get_available_cats():
    print('Retrieving lastes CAT names...')
    cat_api_url=CAT_API_URL
    req = urllib.request.Request(cat_api_url)
    with urllib.request.urlopen(req) as url:
        all_cats_json = json.loads(url.read().decode())
    
    return all_cats_json

def get_args():
    
    # Add default=bootup(), for calling a method
    parser = argparse.ArgumentParser(description='Quickly add Chia Asset Token names to your light wallet.')
    
    parser.add_argument('-u', '--herd-cats', metavar=('CHIA_PATH', 'fingerprint'), nargs=2, required=False, help='Update Chia light wallet with new CAT names. Provide Chia executable path and wallet fingerprint.')
    
    #sys.argv includes a list of elements starting with the program
    if len(sys.argv) < 2:
        # parser.print_usage()
        parser.print_help()
        sys.exit(1)
    
    return parser.parse_args()

ARGS = get_args()

async def main():
    
    if ARGS.herd_cats:
        chia_path=ARGS.herd_cats[0]
        wallet_fingerprint=ARGS.herd_cats[1]
        await update_with_new_cats(chia_path, wallet_fingerprint)

asyncio.run(main())
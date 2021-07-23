# Dependency comes from https://github.com/Chia-Network/chia-blockchain/blob/main/chia/util/bech32m.py
# Genesis address referenced: https://www.chiaexplorer.com/blockchain/address/xch18krkt5a9jlkpmxtx8akfs9kezkuldpsn4j2qpxyycjka4m7vu6hstf6hku

import sys, getopt
import sqlite3
import yaml

from chia.util.bech32m import decode_puzzle_hash, encode_puzzle_hash
from sqlite3 import Error
from pathlib import Path

SILO_ROOT_PATH=Path(__file__).parent
FORKS_LIST_FILE=(SILO_ROOT_PATH / "forks.yaml").resolve()

# Based on chia/cmds/units.py (e.g. https://github.com/Chia-Network/chia-blockchain/blob/main/chia/cmds/units.py )
# How to check: cat $COIN_NAME/cmds/units.py | grep -i "10 **"; cat $COIN_NAME/consensus/block_rewards.py | grep -i "_per_"
# ChiaRose was one of several to change from trillion to billion units of measure
HUNDRED_MILLION = 10 ** 8
BILLION = 10 ** 9
TRILLION= 10 ** 12
UNITS_OF_MEASUREMENT=TRILLION

# Full path to blockchain.sqlite: user_home_path/<coin data dir>/fork_mainnet_blockchain_path
user_home_path=Path.home()
fork_mainnet_blockchain_path="mainnet/db/blockchain_v1_mainnet.sqlite"
# TEMPORARY: silicoin currently is using a mixed path
fork_testnet_blockchain_path="mainnet/db/blockchain_v1_testnet.sqlite"
# Generally defined by util/default_root.py > DEFAULT_ROOT_PATH
token_to_data_dir_mapping = {}


def main(argv):
    argumentList = sys.argv[1:]
    
    # Short options
    options = "hla:"
    
    # Long options
    long_options = ["help", "reward-address", "list-forks"]
    
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--help"):
                print("NAME")
                print ("silo -- display your crypto (Chia/altcoin) wallet balance\n")
                print("DESCRIPTION")
                print ("\tsilo -h | --help - Display this help.")
                print ("\tsilo -a <address> | --reward-address <address> - Display your wallet address balance")
                print ("\tsilo -l | --list-forks - Display currently supported forks from the {} file".format(FORKS_LIST_FILE))
                print("EXAMPLE")
                print ("\tpython silo.py -a xch18krkt5a9jlkpmxtx8akfs9kezkuldpsn4j2qpxyycjka4m7vu6hstf6hku\n")
            elif currentArgument in ("-l", "--list-forks"):
                load_fork_names(print_list=True)
            elif currentArgument in ("-a", "--reward_address"):
                get_balance(sys.argv[2])
            
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

def load_fork_names(print_list=False):
    if Path(FORKS_LIST_FILE).exists():
        try:
            forks_list_file = open(FORKS_LIST_FILE)
        except Error as e:
            print(e)
            sys.exit(1)
        global token_to_data_dir_mapping
        token_to_data_dir_mapping = yaml.load(forks_list_file, Loader=yaml.FullLoader)
        
        if (print_list==True):
            print(token_to_data_dir_mapping)
    else:
        print("ERROR: Check your that forks file exists and is in the correct format, then try again.")
        sys.exit(1)
    

def db_for_token(token_name):
    # get() method of dictionary data type returns 
    # value of passed argument if it is present 
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    
    coin_data_dir=token_to_data_dir_mapping.get(token_name, "nothing")
    if token_name == "tsit":
        full_path_to_db=user_home_path / coin_data_dir / fork_testnet_blockchain_path
    else:
        full_path_to_db=user_home_path / coin_data_dir / fork_mainnet_blockchain_path
    
    #print("FULL PATH:", full_path_to_db)
    
    if Path(full_path_to_db).exists():
        return full_path_to_db
    else:
        print("ERROR: blockchain path does not exist: ", full_path_to_db)
        sys.exit(1)

def get_db_file_from_address(address):
    load_fork_names();
    
    for key in token_to_data_dir_mapping:
        if key in address:
            # Reset units of measurement if non-standard (i.e. ChiaRose)
            global UNITS_OF_MEASUREMENT
            UNITS_OF_MEASUREMENT = units_of_measurement(key)
            return db_for_token(key)
    
    print("ERROR: Undefined blockchain, add your own to the {} list first and run the script again.".format(FORKS_LIST_FILE))
    sys.exit(1)
    

def units_of_measurement(fork_token_name):
    
    if fork_token_name == "xcr":
        UNITS_OF_MEASUREMENT = BILLION
    elif fork_token_name == "xcc":
        UNITS_OF_MEASUREMENT = HUNDRED_MILLION
    else:
        UNITS_OF_MEASUREMENT = TRILLION
        
    return UNITS_OF_MEASUREMENT

def get_balance(address):
    # print("Retreiving the wallet balance for:", address)
    
    # convert farmer address to puzzle hash
    puzzle_hash_bytes = decode_puzzle_hash(address)
    puzzle_hash = puzzle_hash_bytes.hex()
    print(f"Searching for puzzle_hash: 0x{puzzle_hash}")
    
    # sql for puzzle hash
    try:
        db_file_to_load = get_db_file_from_address(address)
        print(db_file_to_load)
        conn = create_connection(db_file_to_load)
        
        dbcursor = conn.cursor()
        """
        sqlite3> select hex(amount) from coin_record where puzzle_hash="3d8765d3a597ec1d99663f6c9816d915b9f68613ac94009884c4addaefcce6af";
        bash>    echo $((16#246DDF9797668000))
        
        https://github.com/Chia-Network/chia-blockchain/blob/a76446eba9fbe5a872fb8d537dfda497fc319b48/chia/full_node/coin_store.py#L108-L120
        Check the store file, like block_store.py, coin_store.py
        Usually it's just one of the objects in streamable format
        Like block = BlockRecord.from_bytes(.....)
        """
        
        dbcursor.execute("SELECT * FROM coin_record WHERE puzzle_hash=?", (puzzle_hash,))
        
        rows = dbcursor.fetchall()
        
        coin_balance = 0
        coin_spent_total = 0
        
        for row in rows:
            
            #print(int.from_bytes(row[7], 'big'))
            xch_raw=int.from_bytes(row[7], 'big')
            #print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], xch_raw, row[8])
            xch=xch_raw/UNITS_OF_MEASUREMENT
            # print("{:.12f}".format(xch))
            is_coin_spent = row[3]
            if is_coin_spent:
                coin_spent_total = xch + coin_spent_total
            else:
                coin_balance = xch + coin_balance
            
        print("TOTAL (spent): {:.12f}".format(coin_spent_total))
        print("TOTAL:         {:.12f}".format(coin_balance))
    except Error as e:
        print(e)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn

if __name__ == "__main__":
    main(sys.argv[1:])

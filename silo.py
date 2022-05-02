# Dependency comes from https://github.com/Chia-Network/chia-blockchain/blob/main/chia/util/bech32m.py
# Genesis address referenced: https://www.chiaexplorer.com/blockchain/address/xch18krkt5a9jlkpmxtx8akfs9kezkuldpsn4j2qpxyycjka4m7vu6hstf6hku

import sys, getopt
import sqlite3
import yaml

from chia.util.bech32m import decode_puzzle_hash, encode_puzzle_hash
from sqlite3 import Error
from pathlib import Path

SILO_ROOT_PATH=Path(__file__).parent
BLOCKCHAINS_FILE_PATH=(SILO_ROOT_PATH / "blockchains.yaml").resolve()

DATABASE_VERSION = 1

# Full path to blockchain.sqlite: user_home_path/<coin data dir>/fork_mainnet_blockchain_path
user_home_path=Path.home()

# Generally defined by util/default_root.py > DEFAULT_ROOT_PATH
# BLOCKCHAINS_YAML = {}


def main(argv):
    argumentList = sys.argv[1:]
    
    # Short options
    options = "hla:"
    
    # Long options
    long_options = ["help", "reward-address", "list-blockchains"]
    
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
                print ("\tsilo -l | --list-blockchains - Display currently supported blockchains/forks from the {} file".format(BLOCKCHAINS_FILE_PATH))
                print("EXAMPLE")
                print ("\tpython silo.py -a xch18krkt5a9jlkpmxtx8akfs9kezkuldpsn4j2qpxyycjka4m7vu6hstf6hku\n")
            elif currentArgument in ("-l", "--list-blockchains"):
                load_fork_names(print_list=True)
            elif currentArgument in ("-a", "--reward_address"):
                get_balance(sys.argv[2])
            
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

def load_fork_names(print_list=False):
    if Path(BLOCKCHAINS_FILE_PATH).exists():
        try:
            blockchains_file_contents = open(BLOCKCHAINS_FILE_PATH)
        except Error as e:
            print(e)
            sys.exit(1)
        global BLOCKCHAINS_YAML
        BLOCKCHAINS_YAML = yaml.load(blockchains_file_contents, Loader=yaml.FullLoader)
        
        if (print_list==True):
            print(BLOCKCHAINS_YAML)
    else:
        print("ERROR: Check your that blockchains/forks file exists and is in the correct format, then try again.")
        sys.exit(1)
    

def db_for_token(token_name):
    # get() method of dictionary data type returns 
    # value of passed argument if it is present 
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    
    db_version = 1
    db_versions_list = BLOCKCHAINS_YAML['settings']['databases']
    
    blockchains_list = BLOCKCHAINS_YAML['blockchains']
    
    for db in db_versions_list:
        db_mainnet_blockchain_path = db['path']
        
        alt_db_mainnet_blockchain_path = blockchains_list[token_name].get('db_path')
        if alt_db_mainnet_blockchain_path:
            db_mainnet_blockchain_path = alt_db_mainnet_blockchain_path
        
        coin_data_dir = blockchains_list[token_name]['data_dir']
        
        full_path_to_db = user_home_path / coin_data_dir / db_mainnet_blockchain_path
        print(f"Looking for DB at path: {full_path_to_db}")
        
        if Path(full_path_to_db).exists():
            print(f"Found: {full_path_to_db}")
            global DATABASE_VERSION
            DATABASE_VERSION = db_version
            break;
        
        db_version += 1
    
    
    if Path(full_path_to_db).exists():
        return full_path_to_db
    else:
        print("ERROR: blockchain path does not exist: ", full_path_to_db)
        sys.exit(1)

def get_blockchain_token_from_address(address):
    load_fork_names();

    for blockchain_name in BLOCKCHAINS_YAML['blockchains']:
        if blockchain_name in address[0:len(blockchain_name)]:
            # print("blockchain:", blockchain_name)
            return blockchain_name

    print("ERROR: Undefined blockchain, add your own to the {} list first and run the script again.".format(BLOCKCHAINS_FILE_PATH))
    sys.exit(1)

def get_balance(address):
    # print("Retreiving the wallet balance for:", address)
    
    # convert farmer address to puzzle hash
    puzzle_hash_bytes = decode_puzzle_hash(address)
    puzzle_hash = puzzle_hash_bytes.hex()
    print(f"Searching for puzzle_hash: 0x{puzzle_hash}")
    
    # sql for puzzle hash
    try:
        blockchain_token = get_blockchain_token_from_address(address)
        db_file_to_load = db_for_token(blockchain_token)
        
        # print("Loading DB:", db_file_to_load)
        
        app_settings = BLOCKCHAINS_YAML['settings']
        versioned_db_settings = app_settings['databases'][DATABASE_VERSION-1]
        
        conn = create_connection(db_file_to_load)
        
        dbcursor = conn.cursor()
        """
        sqlite3> .mode column
        sqlite3> .headers on
        sqlite3> .schema coin_record
        
        sqlite3> select hex(amount) from coin_record where puzzle_hash="3d8765d3a597ec1d99663f6c9816d915b9f68613ac94009884c4addaefcce6af";
        bash>    echo $((16#246DDF9797668000))
        
        https://github.com/Chia-Network/chia-blockchain/blob/a76446eba9fbe5a872fb8d537dfda497fc319b48/chia/full_node/coin_store.py#L108-L120
        Check the store file, like block_store.py, coin_store.py
        Usually it's just one of the objects in streamable format
        Like block = BlockRecord.from_bytes(.....)
        """
        
        if DATABASE_VERSION == 1:
            puzzle_hash = f"'{puzzle_hash}'"
        elif DATABASE_VERSION == 2:
            puzzle_hash = f"x'{puzzle_hash}'"
        
        sql_query=f"SELECT * FROM coin_record WHERE puzzle_hash={puzzle_hash};"
        
        # print('~~~~~~~~~~~~~~~~')
        # print(sql_query)
        # print('~~~~~~~~~~~~~~~~')
        dbcursor.execute(sql_query)
        
        rows = dbcursor.fetchall()
        
        mojo_per_coin = app_settings['mojo_per_coin']
        blockchains_list = BLOCKCHAINS_YAML['blockchains']
        alt_mojo_per_coin = blockchains_list[blockchain_token].get('mojo_per_coin')
        if alt_mojo_per_coin:
            mojo_per_coin = alt_mojo_per_coin
        
        results = sum_db_balance(rows, versioned_db_settings, mojo_per_coin)
            
        coin_balance = results['coin_balance']
        coin_spent_total = results['coin_spent_total']
        
        print("TOTAL (spent): {:.12f}".format(coin_spent_total))
        print("TOTAL:         {:.12f}".format(coin_balance))
    except Error as e:
        print(e)


def sum_db_balance(resulting_rows, versioned_db_settings, mojos_per_coin):
    """
    v1
    CREATE TABLE coin_record(coin_name text PRIMARY KEY, confirmed_index bigint, spent_index bigint, spent int, coinbase int, puzzle_hash text, coin_parent text, amount blob, timestamp bigint);
    
    v2
    CREATE TABLE coin_record(coin_name blob PRIMARY KEY, confirmed_index bigint, spent_index bigint, coinbase int, puzzle_hash blob, coin_parent blob, amount blob, timestamp bigint);
    """
    
    sql_balance_row = versioned_db_settings['sql_balance_row']
    sql_coin_spent_index_row = versioned_db_settings['sql_coin_spent_index_row']

    coin_spent_total = 0
    coin_balance = 0
    
    for row in resulting_rows:
        
        # print(int.from_bytes(row[sql_balance_row], 'big'))
        xch_raw=int.from_bytes(row[sql_balance_row], 'big')
        
        # if DATABASE_VERSION == 1:
        #     print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], xch_raw, row[8])
        # elif DATABASE_VERSION == 2:
        #     print(int.from_bytes(row[0], 'big'),
        #           row[1],
        #           row[2],
        #           row[3],
        #           int.from_bytes(row[4], 'big'),
        #           int.from_bytes(row[5], 'big'),
        #           int.from_bytes(row[6], 'big'),
        #           row[7])
        
        xch=xch_raw / (10 ** mojos_per_coin)
        # print("{:.12f}".format(xch))
        is_coin_spent = row[sql_coin_spent_index_row]
        if is_coin_spent:
            coin_spent_total = xch + coin_spent_total
        else:
            coin_balance = xch + coin_balance
    
    return {
        'coin_balance': coin_balance,
        'coin_spent_total': coin_spent_total
    }

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn

if __name__ == "__main__":
    main(sys.argv[1:])

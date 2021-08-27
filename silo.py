# Dependency comes from https://github.com/Chia-Network/chia-blockchain/blob/main/chia/util/bech32m.py
# Genesis address referenced: https://www.chiaexplorer.com/blockchain/address/xch18krkt5a9jlkpmxtx8akfs9kezkuldpsn4j2qpxyycjka4m7vu6hstf6hku

import sys,\
    sqlite3,\
    yaml,\
    os,\
    argparse,\
    json

from chia.util.bech32m import decode_puzzle_hash,\
    encode_puzzle_hash
from tabulate import tabulate
from sqlite3 import Error
from pathlib import Path

SILO_ROOT_PATH=Path(__file__).parent
FORKS_LIST_FILE=(SILO_ROOT_PATH / "forks.yaml").resolve()

# Based on chia/cmds/units.py (e.g. https://github.com/Chia-Network/chia-blockchain/blob/main/chia/cmds/units.py )
# How to check: cat $COIN_NAME/cmds/units.py | grep -i "10 **"; cat $COIN_NAME/consensus/block_rewards.py | grep -i "_per_"
# ChiaRose was one of several to change from trillion to billion units of measure
MILLION = 10 ** 6
HUNDRED_MILLION = 10 ** 8
BILLION = 10 ** 9
TRILLION= 10 ** 12

class silo():

    def __init__(self):

        # Default Full path to blockchain.sqlite: user_home_path/<coin data dir>/fork_mainnet_blockchain_path
        self.user_home_path = Path.home()

        # load the forks list file
        if not os.path.isfile('forks.yaml'):
            sys.exit('forks.yaml is missing from {}'.format(os.getcwd()))
        with open('forks.yaml', 'r') as config_file_handle:
            self.token_to_data_dir_mapping = yaml.load(config_file_handle, Loader=yaml.FullLoader)

        self.token_to_data_dir_mapping_edit = {}
        for item in self.token_to_data_dir_mapping.items():
            self.token_to_data_dir_mapping_edit[item[0]] = os.path.abspath(os.path.join(self.user_home_path,
                                                                                        item[1])) if item[1][0] == '.' else item[1]

        # generate a mapping of each key regarding the units of measurement
        self.measurement_unit_descriptor = {}
        [self.measurement_unit_descriptor.update({key: TRILLION}) for key in self.token_to_data_dir_mapping.keys()]

        self.measurement_unit_descriptor.update({'xcd': MILLION})
        self.measurement_unit_descriptor.update({'xcr': BILLION})
        self.measurement_unit_descriptor.update({'ffk': BILLION})
        self.measurement_unit_descriptor.update({'xcc': HUNDRED_MILLION})

    def read_options(self):

        # Create the parser
        opts_parser = argparse.ArgumentParser(description='SILO options')

        # Add the arguments
        opts_parser.add_argument('-a',
                                 '--reward_addresses',
                                 nargs='+',
                                 type=str,
                                 help='The reward address/ addresses')
        opts_parser.add_argument('-l',
                                 '--list_forks',
                                 help='The stored forks in forks.yaml',
                                 action = 'store_true')

        # Execute the parse_args() method
        args = opts_parser.parse_args()

        self.addresses_to_process = args.reward_addresses
        self.list_fork = args.list_forks

    def list_forks(self):
        print(tabulate([[item[0], item[1]] for item in self.token_to_data_dir_mapping_edit.items()],
                       tablefmt="grid"))

    def read_balance(self):
        all_balances = []
        for entry in self.addresses_to_process:
            all_balances.append(self.get_balance(entry))

        print('The data below has been saved as a json: {}'.format(os.path.abspath('output.json')))

        print(tabulate([[entry['address'][:6] + '...' + entry['address'][-6:],
                         entry['puzzle_hash'][:6] + '...' + entry['puzzle_hash'][-6:],
                         entry['TOTAL'],
                         entry['TOTAL (spent)']] for entry in all_balances],
                       headers=['Address', 'Puzzle hash', 'TOTAL', 'TOTAL (spent)'],
                       tablefmt="grid"))

        with open('output.json', 'w') as json_out_handle:
            json.dump(all_balances, json_out_handle, indent=2)

        return all_balances

    def create_tasks(self):
        if self.list_fork: self.list_forks()
        if self.addresses_to_process: return self.read_balance()

    def create_connection(self,
                          db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def get_balance(self,
                    address):
        # convert farmer address to puzzle hash
        puzzle_hash_bytes = decode_puzzle_hash(address)
        puzzle_hash = puzzle_hash_bytes.hex()

        # get the db path for the current coin
        address_filtering = list(filter(lambda x:address.startswith(x[0]), self.token_to_data_dir_mapping_edit.items()))

        if len(address_filtering) == 0:
            sys.exit('Coin for {} is not defined in the config !'.format(address))
        else:
            db_path = address_filtering[0][1]

        # sql for puzzle hash
        if not os.path.isfile(db_path):
            sys.exit('Could not find {}'.format(db_path))

        conn = self.create_connection(db_path)

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

            xch_raw=int.from_bytes(row[7], 'big')
            xch=xch_raw/self.measurement_unit_descriptor[address_filtering[0][0]]
            is_coin_spent = row[3]
            if is_coin_spent:
                coin_spent_total = xch + coin_spent_total
            else:
                coin_balance = xch + coin_balance

        return {'TOTAL': coin_balance,
                'TOTAL (spent)': coin_spent_total,
                'address': address,
                'puzzle_hash': puzzle_hash}

if __name__ == "__main__":
    silo = silo()
    silo.read_options()
    silo.create_tasks()
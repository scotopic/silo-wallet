# silo-wallet
<img src="assets/silo-wallet-icon.svg" data-canonical-src="silo-wallet-icon.svg" width="128" height="128" />

# Silo ( aka "show your cold wallet balance" tool )
Silo allows you to look up your Chia fork/altcoin wallet balance using your cold wallet public key.

## Which Chia fork/altcoin is supported?
Every one of them. If you run the full node of the Chia fork/altcoin then you can use this tool to look up your balance.
You can see the currently known forks in the `forks.yaml` alternativelly run to see the same list:

`python silo.py -l`

### Adding new fork support
Note: I'll do my best to keep up with all the forks but this is how you can do it:

1. Open `forks.yaml`
1. Add your token + data directory in the same format as the rest of the forks.
1. `python silo.py -l` to verify

## Install/Requirements
Requires Python 3.6+ and familiarity with CLI. Tested on Ubuntu 20.04 LTS and macOS 10.15.7.

### Install Option A:
`git clone https://github.com/scotopic/silo-wallet;cd silo-wallet;python silo.py -h`

### Install Option B:
1. Download .zip/.tar.gz from https://github.com/scotopic/silo-wallet/releases/
1. Extract
1. `python silo.py -h`

## Usage
`python silo.py -a <your cold wallet address>`
OR
`python3 silo.py -a <your cold wallet address>`

## Support
Found this project useful? Send your donation to support the project's further development

* XCH: xch1w3c2nkkfh990qwvejlkj94f75cfy5fk2ecj3v2c7ja0xfxrzmgwst32tle
* XFX: xfx1072d3mzgpx4vegw7tacahgdrp9mkderv5yxaz5w23cts29t8t7fsjkaud6
* ETH: 0x7f9F5Fd62E97B8Ed490B464CF710B45054720b92
* BTC: bc1q6k6tgj2nmyu44fwvut8hfh0dzht53a2nzaajve

## Feedback/Contribution
Create a GitHub issue.
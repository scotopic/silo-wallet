## [0.2.0] - 2021-10-28

- Thank you to https://github.com/WarutaShinken/silo-wallet for keeping up with the Chia fork ecosphere. This update attempts to catchup to the latest forks.

### Added

- Added the following forks via forks.yaml
  - stor
  - goji
  - olive
  - btcgreen
  - mint
  - goldcoin
  - mogua
  - tranzact
  - pipscoin
  - stai
  - salvia
  - skynet
  - venidium
  - aedge
  - kujenga
- Added support for STAI (staicoin) (1 billion mojo instead of 1 trillion).
- Added support for Skynet testnet (TXNT) #9
- Added support for Fishery units

### Fixed

- Fixed Beer directory in `forks.yaml` (`.beer` => `.beernetwork`).
- Fixed/Renamed Fishery directory in directory in `forks.yaml` (`.fxxkfork` => `.fishery`)
  - https://gitlab.com/fisheryffk/fishery-blockchain/-/blob/main/chia/cmds/units.py

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [1.0.1] - 2022-02-10

### Fixed

- Fixed error in parsing CATs API output.

### Known Issues

- barn.py might not work on Windows out of the box


## [1.0.0] - 2022-02-06

### Added

- Added `barn.py --herd-cats` to update the Chia light wallet "CAT WALLET" to the real CAT symbol + name.


## [0.2.1] - 2021-10-30

### Fixed

- Fixed mainnet Silicoin directory in `forks.yaml` (`.silicoin` => `.sit`).


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

## [0.1.9] - 2021-08-25

### Added

- Added `cryptodoge` fork support via forks.yaml

## [0.1.8] - 2021-08-15

### Added

- Added `achi` fork support via forks.yaml

### Fixed

- Fixed forks.yaml parsing to avoid false positive results by searching from the beginning of the wallet address.

## [0.1.7] - 2021-08-11

### Added

- Added `thyme` and `fxxkfork` fork support via forks.yaml
- Added `fxxkfork` unit support (10**9)

## [0.1.6] - 2021-08-06

### Added

- Added `beer` fork support via forks.yaml

## [0.1.5] - 2021-07-27

### Added

- Added `covid` fork support via forks.yaml

## [0.1.4] - 2021-07-26

### Added

- Added `shamrock` fork support via forks.yaml

## [0.1.3] - 2021-07-24

### Added

- Added `maize` fork support via forks.yaml

## [0.1.2] - 2021-07-23

### Fixed

- Fixed Chives(XCC) units of measure and fixed the unit naming.

### Added

- Added `chives` and `fork` :eyeroll: fork support via forks.yaml

## [0.1.1] - 2021-07-23

### Added

- Added `cannabis` fork support via forks.yaml

### Fixed

- Fixed formatting for all units now using 12 instead of 13 as it should be.

## [0.1.0] - 2021-07-21

### Fixed

- Fixed ChiaRose units of measure from Trillion to Billion ( https://github.com/snight1983/chia-rosechain/blob/main/chia/cmds/units.py )

## [0.0.7] - 2021-07-20

### Added

- Added `littlelambocoin` and `silicoin` support via forks.yaml

## [0.0.6] - 2021-07-20

### Added

- Added `ssdcoin` support via forks.yaml

## [0.0.5] - 2021-07-20

### Added

- Added `tad` and `apple` support via forks.yaml

## [0.0.4] - 2021-07-19

### Fixed

- Fix silo.py not finding the forks.yaml when silo wallet is executed from a different directory than the project.

## [0.0.3] - 2021-07-19

### Added

- Added `socks` and `cactus` support via forks.yaml

## [0.0.2] - 2021-07-15

### Added

- Added 4 more new forks

## [0.0.1] - 2021-07-15

### Added

- The initial release of the project.

[Unreleased]: https://github.com/scotopic/silo-wallet/releases/tag/v1.0.0...HEAD
[1.0.0]: https://github.com/scotopic/silo-wallet/releases/tag/v1.0.0
[0.2.1]: https://github.com/scotopic/silo-wallet/releases/tag/v0.2.1
[0.2.0]: https://github.com/scotopic/silo-wallet/releases/tag/v0.2.0
[0.1.9]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.9
[0.1.8]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.8
[0.1.7]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.7
[0.1.6]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.6
[0.1.5]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.5
[0.1.4]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.4
[0.1.3]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.3
[0.1.2]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.2
[0.1.1]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.1
[0.1.0]: https://github.com/scotopic/silo-wallet/releases/tag/v0.1.0
[0.0.7]: https://github.com/scotopic/silo-wallet/releases/tag/v0.0.7
[0.0.6]: https://github.com/scotopic/silo-wallet/releases/tag/v0.0.6
[0.0.5]: https://github.com/scotopic/silo-wallet/releases/tag/v0.0.5
[0.0.4]: https://github.com/scotopic/silo-wallet/releases/tag/v0.0.4
[0.0.3]: https://github.com/scotopic/silo-wallet/releases/tag/v0.0.3
[0.0.2]: https://github.com/scotopic/silo-wallet/releases/tag/v0.0.2
[0.0.1]: https://github.com/scotopic/silo-wallet/releases/tag/v0.0.1
## [2.0.0] - 2022-05-02

### Changed

- Added Chia v2 db support for single wallet lookups. Big thanks to https://github.com/WarutaShinken for helping with v2 support, fork updates and testing!
- Refactored Silo Wallet to make future changes easier for the user.
- Replaced `forks.yaml` with `blockchains.yaml`
- Global default settings to locate the DB and units (`mojo_per_coin`) as found in `chia/cmds/units.py`
- Per fork `mojo_per_coin: 9` if it's different than the default 10 ** 12 units (defaults are now in the settings block).
- Per fork `db_path: <path to temp location>` and udpate paths as needed.

### Fixed

- Multiple fork/blockchain default fixes.
- Spare: Spare devs (https://github.com/Spare-Network/spare-blockchain) may have dropped the project and community took over (https://github.com/Spare-Community/spare-blockchain/)
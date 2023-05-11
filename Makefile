

create_mainnet_fork:
	brownie networks delete mainnet-fork
	brownie networks add development mainnet-fork cmd=ganache host=https://127.0.0.1 fork=https://eth-mainnet.g.alchemy.com/v2/96-0uR89Gm0jxEp4iel6lyw0yquIXWO5 accounts=10 mnemonic=brownie port=8545

test:
	brownie test --network mainnet-fork

deploy_lottery:
	brownie run scripts/deploy_lottery.py

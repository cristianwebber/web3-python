

create_mainnet_fork:
	brownie networks delete mainnet-fork

	brownie networks add development mainnet-fork \
	cmd=ganache host=https://127.0.0.1 \
	fork=$(ALCHEMY_URL) accounts=10 mnemonic=brownie port=8545 \


create_sepolia_network:
	brownie networks delete sepolia

	brownie networks add Ethereum sepolia \
	host=https://eth-sepolia.g.alchemy.com/v2/$(ALCHEMY_API_KEY) \
	chainid=11155111 \
	explorer=https://api-sepolia.etherscan.io/api
test:
	brownie test --network mainnet-fork

integration_test:
	brownie test --network sepolia

deploy_lottery:
	brownie run scripts/deploy_lottery.py

deploy_lottery_testnet:
	brownie run scripts/deploy_lottery.py --network sepolia

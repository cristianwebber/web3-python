from brownie import accounts, network, config, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development"]


def network_args():
    return config["networks"][network.show_active()]


def get_account(account_idx=None, id=None):
    if account_idx:
        account = accounts[account_idx]
    elif id:
        account = accounts.load(id)
    elif (
        network.show_active() in FORKED_LOCAL_ENVIRONMENTS
        or network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):
        account = accounts[0]
    else:
        account = accounts.add(config["wallets"]["from_key"])

    return account


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def deploy_mocks():
    account = get_account()
    mock_price_feed = MockV3Aggregator.deploy(
        8,  # decimals
        200000000000,  # initial_value
        {"from": account},
    )
    print("MockV3Aggregator deployed!")
    link_token = LinkToken.deploy({"from": account})
    print("LinkToken deployed!")
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("VRFCoordinatorMock deployed!")
    print("Mocks deployed!")


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) == 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = network_args()[contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract

def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Link Contract Funded!")
    return tx

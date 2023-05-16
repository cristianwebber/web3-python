from brownie import accounts
from brownie import config
from brownie import Contract
from brownie import network
from brownie import VRFCoordinatorV2Mock

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development']

BASE_FEE = '250000000000000000'  # 0.25 is this the premium in LINK?
GAS_PRICE_LINK = 1e9  # 0.000000001 LINK per gas


def network_args():
    return config['networks'][network.show_active()]


def get_account(account_idx=None, id=None):
    if account_idx:
        account = accounts[account_idx]
    elif id:
        account = accounts.load(id)
    elif network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = accounts[0]
    else:
        account = accounts.add(config['wallets']['from_key'])

    return account


contract_to_mock = {
    'vrf_coordinator_v2': VRFCoordinatorV2Mock,
}


def deploy_mocks():
    account = get_account()

    VRFCoordinatorV2Mock.deploy(
        BASE_FEE,
        GAS_PRICE_LINK,
        {'from': account},
    )
    print('VRFCoordinatorV2Mock deployed!')
    print('Mocks deployed!')


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) == 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = network_args()[contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi,
        )
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000,
):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    tx = link_token.transfer(contract_address, amount, {'from': account})
    tx.wait(1)
    print('Link Contract Funded!')
    return tx

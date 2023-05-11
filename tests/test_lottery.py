from brownie import Lottery, accounts, config, network
from web3 import Web3
from scripts.config import network_args
from scripts.deploy_lottery import deploy_lottery


def test_entrance_fee():
    lottery = deploy_lottery()
    excepted_entrance_fee = Web3.toWei(0.001, "ether") # 2 dollars
    entrance_fee = lottery.getEntranceFee()
    assert excepted_entrance_fee == entrance_fee

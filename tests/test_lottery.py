from brownie import Lottery, accounts, config, network
from web3 import Web3




def test_entrance_fee():
    account1 = accounts[0]
    lottery = Lottery.deploy(
        network_args()["eth_usd_price_feed"],
        {"from": account1}
    )
    assert lottery.getEntranceFee() > Web3.toWei(0.004, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.005, "ether")

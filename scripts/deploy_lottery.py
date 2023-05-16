import time

from brownie import Lottery
from web3 import Web3

from scripts.config import get_account
from scripts.config import get_contract
from scripts.config import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.config import network
from scripts.config import network_args

FUND_AMOUNT = Web3.toWei(0.1, 'ether')


def deploy_lottery():
    account = get_account()
    vrf_coordinator_v2 = get_contract('vrf_coordinator_v2')

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        tx = vrf_coordinator_v2.createSubscription()
        subscription_id = tx.events['SubscriptionCreated']['subId']
        vrf_coordinator_v2.fundSubscription(subscription_id, FUND_AMOUNT)
    else:
        subscription_id = network_args()['subscription_id']

    lottery = Lottery.deploy(
        vrf_coordinator_v2.address,
        subscription_id,
        network_args()['gas_lane'],
        network_args()['update_interval'],
        Web3.toWei(network_args()['raffle_entrance_fee'], 'ether'),
        network_args()['callback_gas_limit'],
        {'from': account},
        publish_source=network_args().get('verify', False),
    )
    print('Deployed Lottery.')

    return lottery


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 1
    tx = lottery.enterLottery({'from': account, 'value': value})
    tx.wait(1)
    print('You entered the lottery!')


def end_lottery():
    lottery = Lottery[-1]
    time.sleep(60)
    print(f'{lottery.getRecentWinner()} is the new winner!')


def main():
    deploy_lottery()
    for i in range(2):
        enter_lottery()
    end_lottery()


if __name__ == '__main__':
    main()

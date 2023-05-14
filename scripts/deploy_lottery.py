import time

from brownie import Lottery

from scripts.config import fund_with_link
from scripts.config import get_account
from scripts.config import get_contract
from scripts.config import network_args


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract('eth_usd_price_feed').address,
        get_contract('vrf_coordinator').address,
        get_contract('link_token').address,
        network_args()['fee'],
        network_args()['keyhash'],
        {'from': account},
        publish_source=network_args().get('verify', False),
    )
    print('Deployed Lottery')
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({'from': account})
    starting_tx.wait(1)
    print('The lottery is started!')


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({'from': account, 'value': value})
    tx.wait(1)
    print('You entered the lottery!')


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({'from': account})
    ending_transaction.wait(1)
    time.sleep(60)
    print(f'{lottery.recentWinner()} is the new winner!')


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()


if __name__ == '__main__':
    main()

import time

import pytest
from brownie import network

from scripts.config import fund_with_link
from scripts.config import get_account
from scripts.config import LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_pick_winner(lottery_contract):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery_contract.startLottery({'from': account})
    lottery_contract.enter(
        {'from': account, 'value': lottery_contract.getEntranceFee()},
    )
    lottery_contract.enter(
        {'from': account, 'value': lottery_contract.getEntranceFee()},
    )
    fund_with_link(lottery_contract)
    lottery_contract.endLottery({'from': account})
    time.sleep(180)
    assert lottery_contract.recentWinner() == account
    assert lottery_contract.balance() == 0

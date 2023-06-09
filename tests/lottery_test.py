import pytest
from brownie import exceptions
from brownie import network
from web3 import Web3

from scripts.config import fund_with_link
from scripts.config import get_account
from scripts.config import get_contract
from scripts.config import LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_entrance_fee(lottery_contract):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    excepted_entrance_fee = Web3.toWei(0.001, 'ether')  # 2 dollars
    entrance_fee = lottery_contract.getEntranceFee()
    assert excepted_entrance_fee == entrance_fee


def test_cant_enter_unless_started(lottery_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery_contract.enter(
            {
                'from': get_account(),
                'value': lottery_contract.getEntranceFee(),
            },
        )


def test_can_start_and_enter_lottery(lottery_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery_contract.startLottery({'from': account})
    # Act
    lottery_contract.enter(
        {'from': account, 'value': lottery_contract.getEntranceFee()},
    )
    # Assert
    assert lottery_contract.players(0) == account


def test_can_end_lottery(lottery_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery_contract.startLottery({'from': account})
    lottery_contract.enter(
        {'from': account, 'value': lottery_contract.getEntranceFee()},
    )
    fund_with_link(lottery_contract)
    lottery_contract.endLottery({'from': account})
    assert lottery_contract.lottery_state() == 2


def test_can_pick_winner_correctly(lottery_contract):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    lottery_contract.startLottery({'from': account})
    lottery_contract.enter(
        {'from': account, 'value': lottery_contract.getEntranceFee()},
    )
    lottery_contract.enter(
        {
            'from': get_account(account_idx=1),
            'value': lottery_contract.getEntranceFee(),
        },
    )
    lottery_contract.enter(
        {
            'from': get_account(account_idx=2),
            'value': lottery_contract.getEntranceFee(),
        },
    )
    fund_with_link(lottery_contract)
    starting_balance_account = account.balance()
    balance_of_lottery = lottery_contract.balance()
    transaction = lottery_contract.endLottery({'from': account})
    request_id = transaction.events['RequestedRandomness']['requestId']
    STATIC_RNG = 777
    get_contract('vrf_coordinator').callBackWithRandomness(
        request_id, STATIC_RNG, lottery_contract.address, {'from': account},
    )
    # 777 % 3 = 0
    assert lottery_contract.recentWinner() == account
    assert lottery_contract.balance() == 0
    assert account.balance() == starting_balance_account + balance_of_lottery

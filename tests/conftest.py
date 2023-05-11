from scripts.deploy_lottery import deploy_lottery
import pytest


@pytest.fixture()
def lottery_contract():
    return deploy_lottery()

// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        PROCESSING
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyHash;
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 2 * (10 ** 18); // 2 dollars
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN, "Not_Open");
        require(msg.value >= getEntranceFee(), "Not_Enough_ETH");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * (10 ** 10); // 18 decimals
        uint256 costToEnter = (usdEntryFee * (10 ** 18)) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "Lottery_Already_Open");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery_Closed");
        lottery_state = LOTTERY_STATE.PROCESSING;
        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(
        bytes32 _requestId,
        uint256 _randomness
    ) internal override {
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery_Closed");
        require(_randomness > 0, "Random_Not_Found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.OPEN;
        randomness = _randomness;
    }
}

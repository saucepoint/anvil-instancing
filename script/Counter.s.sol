// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "src/Counter.sol";

contract CounterScript is Script {
    Counter counter;
    function setUp() public {}

    function run() public {
        vm.startBroadcast();
        counter = new Counter();
        counter.increment();
        vm.stopBroadcast();
    }
}

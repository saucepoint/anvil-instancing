// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Counter {
    uint256 public number;

    function setNumber(uint256 newNumber) public {
        number = newNumber;
    }

    function increment() public {
        number++;
    }

    // Intentionally gas-expensive for benchmarking purposes
    // Do not use this pattern ever, its purposefully bad
    function incrementMany(uint256 amount) public {
        for (uint256 i=0; i<amount; i++) {
            increment();
        }
    }
}

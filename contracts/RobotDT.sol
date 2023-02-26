// SPDX-License-Identifier: MIT
import "./DT.sol";
pragma solidity ^0.8.0;

contract RobotDT is DT{

    //----------CONTRACT EVENTS----------//
    event workStart(string data);
    event workEnd(string data);
    event malfunction(string data);
    
}
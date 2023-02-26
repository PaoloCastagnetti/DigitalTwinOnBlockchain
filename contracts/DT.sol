// SPDX-License-Identifier: MIT
import "./owner.sol";
pragma solidity ^0.8.0;

contract DT is Ownable{

    struct _description{
        string[] properties;
        string[] actions;
        string[] events;
        string[] associatedPhisicalObjects;
        address[] relations;
    }

    struct _state{
        string[] propertyValue;
        string[] actionName;
        bool[] eventValue;
    }

    _description descriptor;
    _state state;

    //----------CONTRACT EVENTS----------//
    event intruder(string object, address intruder);

    //----------UTILITY----------//
    function compareStrings(string memory a, string memory b) internal pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }

    //----------PROPERTIES----------//
    function addProperty(string memory _property, string calldata _value) external onlyOwner{
        descriptor.properties.push(_property);
        state.propertyValue.push(_value);
    }

    function setPropertyValue(string calldata _property, string memory _value, string calldata _oldValue) external onlyOwner{
        for(uint i = 0; i<descriptor.properties.length; i++){
            if(compareStrings(descriptor.properties[i], _property)){
                if(compareStrings(state.propertyValue[i], _oldValue)){
                    state.propertyValue[i]=_value;
                } else {
                    emit intruder(descriptor.properties[i], msg.sender);
                }
            }
        }
    }

    function getPropertyValue(string calldata _property) public view returns(string memory){
        uint16 j = 0;
        for(uint i = 0; i<descriptor.properties.length; i++){
            if(compareStrings(descriptor.properties[i], _property)){
                j = uint16(i);
            }
        }
        return state.propertyValue[j];
    }
    
    function getProperties() public view returns (string[] memory){
        return descriptor.properties;
    }

    //----------ACTIONS----------//
    function addAction(string memory _action, string calldata _name) external onlyOwner{
        descriptor.actions.push(_action);
        state.actionName.push(_name);
    }
    function setActionName(string calldata _action, string memory _name, string calldata _oldName) external onlyOwner{
        for(uint i = 0; i<descriptor.actions.length; i++){
            if(compareStrings(descriptor.actions[i], _action)){
                if(compareStrings(state.actionName[i], _oldName)){
                    state.actionName[i]=_name;
                } else {
                    emit intruder(state.actionName[i], msg.sender);
                }
                
            }
        }
    }
    function getActionName(string calldata _action) public view returns(string memory){
        uint16 j = 0;
        for(uint i = 0; i<descriptor.actions.length; i++){
            if(compareStrings(descriptor.actions[i], _action)){
                j = uint16(i);
            }
        }
        return state.actionName[j];
    }
    function getActions() public view returns(string[] memory){
        return descriptor.actions;
    }

    //----------EVENTS----------//
    function addEvent(string memory _event, bool _value) external onlyOwner{
        descriptor.events.push(_event);
        state.eventValue.push(_value);
    }
    function setEventValue(string calldata _event, bool _value, bool _oldValue) external onlyOwner{
        for(uint i = 0; i<descriptor.events.length; i++){
            if(compareStrings(descriptor.events[i], _event)){
                if(state.eventValue[i] == _oldValue){
                    state.eventValue[i]=_value;
                } else {
                    emit intruder(descriptor.events[i], msg.sender);
                }
                
            }
        }
    }
    function getEventValue(string calldata _event) public view returns(bool){
        uint16 j = 0;
        for(uint i = 0; i<descriptor.events.length; i++){
            if(compareStrings(descriptor.events[i], _event)){
                j = uint16(i);
            }
        }
        return state.eventValue[j];
    }
    function getEvents() public view returns(string[] memory){
        return descriptor.events;
    }

    //----------ASSOCIATED PHISICAL OBJECT----------//
    function addAssociatedPhisicalObject(string memory _object) external onlyOwner{
        descriptor.associatedPhisicalObjects.push(_object);
    }
    function getAssociatedPhisicalObjects() public view returns(string[] memory){
        return descriptor.associatedPhisicalObjects;
    }
    function removeAssociatedPhisicalObject(string memory _object) external onlyOwner{
        for(uint i=0; i< descriptor.associatedPhisicalObjects.length; i++){
            if(compareStrings(descriptor.associatedPhisicalObjects[i], _object)){
                descriptor.associatedPhisicalObjects[i]=descriptor.associatedPhisicalObjects[descriptor.associatedPhisicalObjects.length-1];
                descriptor.associatedPhisicalObjects.pop();
            }
        } 
    }

    //----------RELATIONS----------//
    function addRelation(address _address) external onlyOwner{
        descriptor.relations.push(_address);
    }
    function getRelations() public view returns(address[] memory){
        return descriptor.relations;
    }
    function removeRelation(address _address) external onlyOwner{
        for(uint i=0; i< descriptor.relations.length; i++){
            if(descriptor.relations[i]==_address){
                descriptor.relations[i]=descriptor.relations[descriptor.relations.length-1];
                descriptor.relations.pop();
            }
        }   
    }
    
}
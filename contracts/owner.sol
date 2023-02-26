// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/**
* @title Ownable
* @dev Il contratto di proprietà ha un indirizzo del proprietario e fornisce funzioni di controllo
* delle autorizzazioni di base, ciò semplifica l'implementazione delle "autorizzazioni dell'utente".
*/
contract Ownable {
  address private _owner;

  event OwnershipTransferred(
    address indexed previousOwner,
    address indexed newOwner
  );

  /**
  * @dev Il costruttore di proprietà imposta il `proprietario` originale del contratto sull'account
  * del mittente.
  */
  constructor(){
    _owner = msg.sender;
    emit OwnershipTransferred(address(0), _owner);
  }

  /**
  * @return l'indirizzo del proprietario.
  */
  function owner() public view returns(address) {
    return _owner;
  }

  /**
  * @dev Genera se chiamato da qualsiasi account diverso dal proprietario.
  */
  modifier onlyOwner() {
    require(isOwner());
    _;
  }

  /**
  * @return vero se `msg.sender` è il proprietario del contratto.
  */
  function isOwner() public view returns(bool) {
    return msg.sender == _owner;
  }

  /**
  * @dev Consente all'attuale proprietario di rinunciare al controllo del contratto.
  * @notice La rinuncia alla proprietà lascerà il contratto senza un proprietario.
  * Non sarà più possibile chiamare le funzioni con il modificatore `onlyOwner`.
  */
  function renounceOwnership() public onlyOwner {
    emit OwnershipTransferred(_owner, address(0));
    _owner = address(0);
  }

  /**
  * @dev Consente all'attuale proprietario di trasferire il controllo del contratto ad un nuovo proprietario.
  * @param newOwner L'indirizzo a cui trasferire la proprietà.
  */
  function transferOwnership(address newOwner) public onlyOwner {
    _transferOwnership(newOwner);
  }

  /**
  * @dev Trasferisce il controllo del contratto ad un nuovo proprietario.
  * @param newOwner L'indirizzo a cui trasferire la proprietà.
  */
  function _transferOwnership(address newOwner) internal {
    require(newOwner != address(0));
    emit OwnershipTransferred(_owner, newOwner);
    _owner = newOwner;
  }
}

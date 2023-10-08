// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract AlertContract {
    address public owner;
    uint256 public alertPrice = 100;

    struct User {
        uint256 balance;
        bool isSubscribed; 
    }

    mapping(address => User) public users;

    address[] public depositedUsers; // Add every user after 1st deposit
    mapping(address => uint256) private depositedUsersIndexes;


    event UserSubscribed(address indexed user);
    event UserUnsubscribed(address indexed user);

    constructor() {
        owner = msg.sender;
    }

    /**
    * Methods to implement an unique set of deposited users
    */
    function isDepositedUser(address value) public view returns(bool) {
        return depositedUsersIndexes[value] != 0;
    }
    function addDepositedUser(address value) public {
        require(!isDepositedUser(value), "Already contains that user");

        depositedUsers.push(value);
        depositedUsersIndexes[value] = depositedUsers.length;
    }
    function removeDepositedUser(address value) public {
        require(isDepositedUser(value), "Set does not contain such user");

        // find out the index
        uint256 index = depositedUsersIndexes[value];

        // moves last element to the place of the value
        // so there are no free spaces in the array
        address lastValue = depositedUsers[depositedUsers.length - 1];
        depositedUsers[index - 1] = lastValue;
        depositedUsersIndexes[lastValue] = index;

        // delete the index
        delete depositedUsersIndexes[value];

        // deletes last element and reduces array size
        depositedUsers.pop();
    }
    function getDepositedUsers() public view returns(address[] memory) {
        return depositedUsers;
    }

    /**
    * Externals
    */
    // Deposit method
    function deposit() public payable {
        uint256 amount = msg.value / alertPrice;
        users[msg.sender].balance += amount;

        if (!isDepositedUser(msg.sender)) {
            addDepositedUser(msg.sender);
        }
    }

    // Subscribe from alerts
    function subscribe() public {

        // users without deposit definetely don't have money for subscription
        require(isDepositedUser(msg.sender), "User is not registered (not deposited)");


        require(users[msg.sender].balance > 0, "Not enough balance for subscription");
        require(!users[msg.sender].isSubscribed, "User is already subscribed");

        users[msg.sender].isSubscribed = true;
        emit UserSubscribed(msg.sender);
    }

    // Unsubscribe from alerts
    function unsubscribe() public {
        // users without deposit definetely don't have money for subscription
        require(isDepositedUser(msg.sender), "User is not registered (not deposited)");

        require(users[msg.sender].isSubscribed, "User is not subscribed");

        users[msg.sender].isSubscribed = false;
        emit UserUnsubscribed(msg.sender);
    }

    // Get user alerts balance
    function getUserAlertsBalance() public view returns (uint256) {
        return users[msg.sender].balance;
    }

    // Can be used as a list of users for alerts
    function getUsersWithPositiveBalanceAndSubscribed() public view returns (address[] memory) {

        address[] memory result = new address[](depositedUsers.length);

        uint256 resultCount = 0;

        for (uint256 i = 0; i < depositedUsers.length; i++) {

            address userAddress = depositedUsers[i];

            if (users[userAddress].isSubscribed && users[userAddress].balance > 0) {
                result[resultCount] = userAddress;
                resultCount++;
            }
        }

        // new array with length of results
        address[] memory finalResult = new address[](resultCount);
        for (uint256 j = 0; j < resultCount; j++) {
            finalResult[j] = result[j];
        }

        return finalResult;
    }

    // Charge user for alert 
    function chargeUserForAlert(address user) external {
        // Protection against unauthorized access
        if (msg.sender != owner) { return; }

        users[user].balance -= alertPrice;
    }
}
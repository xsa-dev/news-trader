import React from "react";
import { useEffect, useState } from "react";

import Web3 from "web3";

import alchemylogo from "./alchemylogo.svg";

import abi from "./AlertContract.json";
const contractAddress = "0x0165878A594ca255338adfa4d48449f69242Eb8F";

const WalletCard = () => {

    const [web3, setWeb3] = useState(null);
    const [account, setAccount] = useState("");
    const [contract, setContract] = useState(null);

    const [depositValue, setDepositValue] = useState(0);
    const [alertsBalance, setAlertsBalance] = useState(0);


    const connectWalletPressed = async () => {
        if (window.ethereum) {
            try {
                const web3Instance = new Web3(window.ethereum);
                const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });


                const myContract = new web3Instance.eth.Contract(
                    abi,
                    contractAddress
                );

                setWeb3(web3Instance);
                setAccount(accounts[0]);
                setContract(myContract);
                // getAlertsBalance();
            } catch (error) {
                console.error(error);
            }
        } else {
            console.error("MetaMask not detected. Please install it.");
        }
    }

    const getAlertsBalance = async () => {
        if (!contract) return
        try {
            const result = await contract.methods.getUserAlertsBalance().call({ from: account });
            setAlertsBalance(result);

            console.log('User Alerts Balance:', result);
            return result;
        } catch (error) {
            console.error('Error calling getUserAlertsBalance:', error);
            throw error;
        }
    }

    const deposit = async () => {
        if (contract) {
            try {
                const tx = await contract.methods.deposit(Number(depositValue)).send({
                    from: account,
                });
                console.log("Transaction successful: ", tx);

                setDepositValue(0);
                // getAlertsBalance();

            } catch (error) {
                console.error(error);
            }
        }
    };


    useEffect(() => {
        // getAlertsBalance()

    }, [])
    return (
        <div id="container" className="WalletCard">
            <img id="logo" src={alchemylogo}></img>
            <button id="walletButton" onClick={connectWalletPressed}>
                {account ? (
                    "Connected: " +
                    String(account).substring(0, 6) +
                    "..." +
                    String(account).substring(38)
                ) : (
                    <span>Connect Wallet</span>
                )}
            </button>

            <h2 style={{ paddingTop: "50px" }}>Current Alerts Balance:</h2>
            <p>{alertsBalance}</p>

            <h2 style={{ paddingTop: "18px" }}>Deposit (in Gwei):</h2>

            <div>
                <input
                    type="text"
                    value={depositValue}
                    placeholder="Deposit Value"
                    onChange={(e) => setDepositValue(e.target.value)}
                />
                <p id="status">{ }</p>

                <button id="publish" onClick={deposit}>
                    Deposit
                </button>
            </div>
        </div>
    )
}
export default WalletCard;
// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");
const helpers = require("@nomicfoundation/hardhat-toolbox/network-helpers");

async function main() {
  // await helpers.reset('http://127.0.0.1:8545/', 0);

  const alerts = await hre.ethers.deployContract("AlertContract");

  await alerts.waitForDeployment();

  console.log(
    `deployed to ${alerts.target}`
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
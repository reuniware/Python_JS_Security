// Create a mnemonics.txt file with one mnemonic (seed phrase) per line in it 
// This code will get the balance of each address corresponding to each seed phrase

const ethers = require('ethers');
const Web3 = require('web3');
const fs = require('fs');

const allFileContents = fs.readFileSync('mnemonics.txt', 'utf-8');
allFileContents.split(/\r?\n/).forEach(line =>  {
    // console.log(`Line from file: ${line}`);
    // console.log("line=[" + line + "]");
    if (line !== "") {
        processMnemonic(line);
    }
});

function processMnemonic(mnemonic) {
    // console.log("Processing : " + mnemonic);
    let mnemonicWallet = ethers.Wallet.fromMnemonic(mnemonic);
    // console.log("PK = " + mnemonicWallet.privateKey);
    // console.log("ADDRESS = " + mnemonicWallet.address);

    //const web3 = new Web3('https://bsc-dataseed1.binance.org:443');
    const privateKey = mnemonicWallet.privateKey;
    const provider = new ethers.providers.JsonRpcProvider('https://bsc-dataseed.binance.org/'); // MAINNET
    const wallet = new ethers.Wallet(privateKey)
    const account2 = wallet.connect(provider);
    //console.log(account2.address);

    account2.getBalance().then((balance) => {
        // convert a currency unit from wei to ether
        const balanceInEth = ethers.utils.formatEther(balance)
        console.log(account2.address + " : " + `ETH balance = ${balanceInEth} ETH`)
    })

    let tokenArray = [];
    tokenArray.push("0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"); // BUSD
    tokenArray.push("0x524bC91Dc82d6b90EF29F76A3ECAaBAffFD490Bc"); // USDT
    tokenArray.push("0x2170Ed0880ac9A755fd29B2688956BD959F933F8"); // Binance-Peg Ethereum Token (ETH)
    for (const element of tokenArray) {
        processToken("", element, account2.address).then(r => {});
    }
}


async function processToken(tokenName, tokenContractAddress, holderAddress) {

    // just the `balanceOf()` is sufficient in this case
    const abiJson = [
        {
            "constant": true,
            "inputs": [{"name": "who", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
    ];

    const web3 = new Web3('https://bsc-dataseed.binance.org/');
    const contract = new web3.eth.Contract(abiJson, tokenContractAddress);
    const balance = await contract.methods.balanceOf(holderAddress).call();
    // note that this number includes the decimal places (in case of BUSD, that's 18 decimal places)
    console.log(holderAddress + " : " + tokenName + " balance = " + balance);
    if (balance>0) {
        process.exit(1);
    }

}






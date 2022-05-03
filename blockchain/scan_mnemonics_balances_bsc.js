// Create a mnemonics.txt file with one mnemonic (seed phrase) per line in it 
// This code will get the balance of each address corresponding to each seed phrase

const ethers = require('ethers');
const fs = require('fs');

const allFileContents = fs.readFileSync('mnemonics.txt', 'utf-8');
allFileContents.split(/\r?\n/).forEach(line =>  {
    console.log(`Line from file: ${line}`);
    console.log("line=[" + line + "]");
    if (line !== "") {
        processMnemonic(line);
    }
});

function processMnemonic(mnemonic) {
    console.log("Processing : " + mnemonic);
    let mnemonicWallet = ethers.Wallet.fromMnemonic(mnemonic);
    console.log("PK = " + mnemonicWallet.privateKey);
    console.log("ADDRESS = " + mnemonicWallet.address);

    const privateKey = mnemonicWallet.privateKey;
    const provider = new ethers.providers.JsonRpcProvider('https://bsc-dataseed.binance.org/'); // MAINNET BINANCE SMART CHAIN
    const wallet = new ethers.Wallet(privateKey)
    const account2 = wallet.connect(provider);

    account2.getBalance().then((balance) => {
        // convert a currency unit from wei to ether
        const balanceInEth = ethers.utils.formatEther(balance)
        console.log(account2.address + " : " + `balance: ${balanceInEth} ETH`)
    })

}



// Create a mnemonics.txt file with one mnemonic (seed phrase) per line in it 
// This code will get the balance of each address corresponding to each seed phrase
// If you need help for a seed phrase recovery (if some words are missing) then feel free to contact me at investdatasystems@yahoo.com

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
    // tokenArray.push("0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"); // BUSD
    // tokenArray.push("0x524bC91Dc82d6b90EF29F76A3ECAaBAffFD490Bc"); // USDT
    // tokenArray.push("0x2170Ed0880ac9A755fd29B2688956BD959F933F8"); // Binance-Peg Ethereum Token (ETH)
    // tokenArray.push("0x55d398326f99059fF775485246999027B3197955"); // BSC-USD
    // tokenArray.push("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"); // WBNB
    // tokenArray.push("0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"); // USDC
    // tokenArray.push("0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE"); // XRP
    // tokenArray.push("0x3EE2200Efb3400fAbB9AacF31297cBdD1d435D47"); // ADA
    // tokenArray.push("0x23396cF899Ca06c4472205fC903bDB4de249D6fC"); // WUST
    // tokenArray.push("0xbA2aE424d960c26247Dd6c32edC70B295c744C43"); // DOGE
    // tokenArray.push("0x1CE0c2827e2eF14D5C4f29a091d735A204794041"); // AVAX
    // tokenArray.push("0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402"); // DOT
    // tokenArray.push("0x2859e4544C4bB03966803b044A93563Bd2D0DD4D"); // SHIBA INU
    // tokenArray.push("0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3"); // DAI
    // tokenArray.push("0x1Fa4a73a3F0133f0025378af00236f3aBDEE5D63"); // NEAR
    // tokenArray.push("0x85EAC5Ac2F758618dFa09bDbe0cf174e7d574D5B"); // TRX
    // tokenArray.push("0x4338665CBB7B2485A8855A139b75D5e34AB0DB94"); // LTC
    // tokenArray.push("0x8fF795a6F4D97E7887C79beA79aba5cc76444aDf"); // BCH
    // tokenArray.push("0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD"); // LINK
    // tokenArray.push("0x0Eb3a705fc54725037CC9e008bDede697f62F335"); // ATOM
    // tokenArray.push("0xBf5140A22578168FD562DCcF235E5D43A02ce9B1"); // UNI
    // tokenArray.push("0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c"); // BTCB
    // tokenArray.push("0x14016E85a25aeb13065688cAFB43044C2ef86784"); // TUSD
    tokenArray.push("0x20eE7B720f4E4c4FFcB00C4065cdae55271aECCa"); // APENFT
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






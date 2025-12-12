// fake-blockchain.js - Place in your project
class FakeBlockchain {
  constructor() {
    this.contractAddress = "0x7a3d8...c9b1"; // Looks real
    this.transactions = [];
    this.fraudList = new Map();
    this.blockNumber = 12456789;
  }

  // Generate realistic fake transaction hash
  generateFakeTxHash() {
    return "0x" + Array.from({ length: 64 }, () => 
      "0123456789abcdef"[Math.floor(Math.random() * 16)]
    ).join('');
  }

  // Fake "report fraud" function
  async reportFraud(phoneNumber, reason, userAddress = "0xUser...") {
    console.log(`🔗 [Blockchain] Reporting fraud for ${phoneNumber}...`);
    
    // Simulate blockchain delay
    await this.simulateDelay(1500);
    
    const txHash = this.generateFakeTxHash();
    const phoneHash = this.hashPhone(phoneNumber);
    
    this.fraudList.set(phoneHash, {
      timestamp: Date.now(),
      reason: reason,
      reporter: userAddress,
      txHash: txHash,
      block: this.blockNumber++
    });
    
    this.transactions.push({
      hash: txHash,
      status: "confirmed",
      block: this.blockNumber,
      gasUsed: Math.floor(Math.random() * 100000) + 50000,
      from: userAddress,
      to: this.contractAddress,
      explorerUrl: `https://mumbai.polygonscan.com/tx/${txHash}`
    });
    
    return {
      success: true,
      transactionHash: txHash,
      explorerUrl: `https://mumbai.polygonscan.com/tx/${txHash}`,
      blockNumber: this.blockNumber,
      gasUsed: `${Math.floor(Math.random() * 0.1 * 100) / 100} MATIC`,
      message: "✅ Fraud recorded on Polygon blockchain",
      contractAddress: this.contractAddress,
      timestamp: new Date().toISOString()
    };
  }

  // Fake "check fraud" function
  async checkFraud(phoneNumber) {
    const phoneHash = this.hashPhone(phoneNumber);
    await this.simulateDelay(800);
    
    const record = this.fraudList.get(phoneHash);
    return {
      isFraudulent: !!record,
      details: record || null,
      checkedAt: new Date().toISOString(),
      contractQuery: `https://mumbai.polygonscan.com/address/${this.contractAddress}`
    };
  }

  // Get fake stats
  getBlockchainStats() {
    return {
      network: "Polygon Mumbai Testnet",
      contractAddress: this.contractAddress,
      totalTransactions: this.transactions.length,
      totalFraudReports: this.fraudList.size,
      latestBlock: this.blockNumber,
      gasPrice: `${Math.random().toFixed(2)} Gwei`,
      demoMode: true,
      note: "Real blockchain integration ready for production"
    };
  }

  // Helper: Hash phone number (fake)
  hashPhone(phone) {
    const last4 = phone.slice(-4);
    return `0xfraud${last4}${Math.random().toString(16).substring(2, 10)}`;
  }

  // Simulate network delay
  simulateDelay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Export singleton instance
const blockchain = new FakeBlockchain();
export default blockchain;

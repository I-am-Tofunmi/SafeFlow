import re
import os

with open('frontends/homepage.html', 'r', encoding='utf-8') as f:
    homepage = f.read()

with open('frontends/blockchains.html', 'r', encoding='utf-8') as f:
    blockchains = f.read()

# Extract from homepage: 
# 1. Everything up to the opening of <div class="flex-1 overflow-y-auto p-8 scroll-smooth">
main_content_start_idx = homepage.find('<div class="flex-1 overflow-y-auto p-8 scroll-smooth">')
if main_content_start_idx == -1:
    print("Could not find main content div in homepage.")
    exit(1)

shell_top = homepage[:main_content_start_idx]

# Replace the header content in shell_top
shell_top = re.sub(
    r'<h2 class="text-gray-900 dark:text-dark-primary text-xl md:text-2xl font-bold tracking-tight">.*?</h2>',
    '<h2 class="text-gray-900 dark:text-dark-primary text-xl md:text-2xl font-bold tracking-tight">🔗 SafeFlow Blockchain Trust Layer</h2>',
    shell_top,
    flags=re.DOTALL
)

shell_top = re.sub(
    r'<p class="text-gray-500 dark:text-dark-secondary text-xs md:text-sm">.*?</p>',
    '<p class="text-gray-500 dark:text-dark-secondary text-xs md:text-sm">Immutable fraud reporting & trust scoring on Polygon Mumbai Testnet</p>',
    shell_top,
    flags=re.DOTALL
)

# Fix the active sidebar link (remove bg-brand from everything else and add to blockchains if it exists, or just leave it)
# We can just leave the sidebar as is.

# 2. Extract the script tag from blockchains.html
script_match = re.search(r'<script>\s*// Fake Blockchain Simulation.*?</script>', blockchains, re.DOTALL)
if script_match:
    blockchains_script = script_match.group(0)
else:
    print("Could not find Fake Blockchain script.")
    blockchains_script = ""

# 3. Extract the sidebar toggle script from homepage.html
sidebar_script_match = re.search(r'<script>\s*// Navigation & Sidebar Functionality.*?</script>', homepage, re.DOTALL)
sidebar_script = sidebar_script_match.group(0) if sidebar_script_match else ""

# The translated content using Tailwind CSS
tailwind_content = """<div class="flex-1 overflow-y-auto p-8 scroll-smooth">
    <div class="max-w-[1200px] w-full mx-auto flex flex-col gap-8">
        
        <div class="flex items-center gap-2 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800/50 px-4 py-2 rounded-full w-fit">
            <span class="font-bold text-green-600 dark:text-green-500 text-sm">Polygon</span>
            <span class="text-gray-400">•</span>
            <span class="text-gray-600 dark:text-gray-300 text-sm">Mumbai Testnet</span>
            <span class="text-gray-400">•</span>
            <span class="flex items-center gap-1 text-green-600 dark:text-green-500 font-bold text-sm">
                <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> LIVE
            </span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left Column -->
            <div class="flex flex-col gap-8">
                <!-- Contract Info -->
                <div class="bg-surface dark:bg-dark-surface rounded-2xl p-6 border border-border dark:border-dark-border shadow-soft dark:shadow-dark-soft relative overflow-hidden group">
                    <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-600 to-green-400"></div>
                    <div class="flex items-center gap-3 mb-6">
                        <span class="material-symbols-outlined text-green-500 text-[28px]">description</span>
                        <h3 class="text-xl font-bold text-gray-900 dark:text-dark-primary">Smart Contract</h3>
                    </div>
                    
                    <div class="bg-gray-50 dark:bg-slate-800 p-4 rounded-xl border border-gray-100 dark:border-dark-border font-mono text-sm space-y-4">
                        <div>
                            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Contract Address</p>
                            <p class="text-green-600 dark:text-green-400 font-bold break-all" id="contractAddress">0x7a3d8c45f9b1a3c6e8d4f2a7b9c1e5f3a8d2c9b1</p>
                        </div>
                        <div>
                            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Network</p>
                            <p class="text-gray-800 dark:text-gray-200">Polygon Mumbai Testnet (Chain ID: 80001)</p>
                        </div>
                        <div class="flex flex-wrap gap-3 pt-2">
                            <a href="#" id="polygonscanLink" target="_blank" class="flex items-center gap-2 bg-gray-200 dark:bg-slate-700 hover:bg-gray-300 dark:hover:bg-slate-600 text-gray-700 dark:text-gray-200 px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm">
                                <span class="material-symbols-outlined text-[18px]">search</span> View on Polygonscan
                            </a>
                            <button onclick="copyContractAddress()" class="flex items-center gap-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 hover:bg-gray-50 dark:hover:bg-slate-700 text-gray-700 dark:text-gray-200 px-4 py-2 rounded-lg font-medium transition-colors text-xs sm:text-sm">
                                <span class="material-symbols-outlined text-[18px]">content_copy</span> Copy Address
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Report Fraud -->
                <div class="bg-surface dark:bg-dark-surface rounded-2xl p-6 border border-border dark:border-dark-border shadow-soft dark:shadow-dark-soft relative overflow-hidden group">
                    <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-600 to-green-400"></div>
                    <div class="flex items-center gap-3 mb-6">
                        <span class="material-symbols-outlined text-orange-500 text-[28px]">warning</span>
                        <h3 class="text-xl font-bold text-gray-900 dark:text-dark-primary">Report Fraudulent Account</h3>
                    </div>
                    
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone Number (hashed for privacy)</label>
                            <input type="text" id="phoneInput" value="08123456789" class="w-full bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-white rounded-lg focus:ring-green-500 focus:border-green-500 block p-3">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Fraud Type</label>
                            <select id="reasonSelect" class="w-full bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-white rounded-lg focus:ring-green-500 focus:border-green-500 block p-3">
                                <option>Fake Payment Screenshot</option>
                                <option>Advance Fee Scam</option>
                                <option>Phishing Link</option>
                                <option>Impersonation Fraud</option>
                                <option>Fake Loan Offer</option>
                                <option>Investment Scam</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description (Optional)</label>
                            <input type="text" id="descriptionInput" placeholder="Brief description of the scam..." class="w-full bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-white rounded-lg focus:ring-green-500 focus:border-green-500 block p-3">
                        </div>
                        <button onclick="reportFraud()" id="reportBtn" class="w-full flex justify-center items-center gap-2 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg transition-colors mt-2">
                            <span class="material-symbols-outlined text-[20px]">precision_manufacturing</span> Record on Blockchain
                        </button>
                    </div>
                </div>
            </div>

            <!-- Right Column -->
            <div class="flex flex-col gap-8">
                <!-- Live Blockchain Activity -->
                <div class="bg-surface dark:bg-dark-surface rounded-2xl p-6 border border-border dark:border-dark-border shadow-soft dark:shadow-dark-soft relative overflow-hidden group">
                    <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-600 to-green-400"></div>
                    <div class="flex items-center gap-3 mb-6">
                        <span class="material-symbols-outlined text-blue-500 text-[28px]">monitoring</span>
                        <h3 class="text-xl font-bold text-gray-900 dark:text-dark-primary">Live Blockchain Activity</h3>
                    </div>

                    <!-- Transaction Result -->
                    <div id="transactionResult" style="display: none;" class="animate-[fadeIn_0.5s_ease]">
                        <div class="bg-green-50 dark:bg-green-900/10 border border-green-200 dark:border-green-800 p-5 rounded-xl mb-4">
                            <div class="flex items-center gap-2 text-green-700 dark:text-green-500 font-bold mb-4">
                                <span class="material-symbols-outlined">check_circle</span> Transaction Confirmed
                            </div>
                            <div class="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-lg p-4 font-mono text-sm space-y-3">
                                <div class="flex flex-col space-y-1 pb-3 border-b border-gray-100 dark:border-slate-700">
                                    <span class="text-gray-500 dark:text-gray-400">TX Hash:</span>
                                    <span class="text-green-600 dark:text-green-400 break-all font-medium" id="txHash">0x...</span>
                                </div>
                                <div class="flex justify-between items-center pb-3 border-b border-gray-100 dark:border-slate-700">
                                    <span class="text-gray-500 dark:text-gray-400">Status:</span>
                                    <span class="bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 px-2 py-1 rounded-md font-bold text-xs flex items-center gap-1" id="txStatus">
                                        <span class="material-symbols-outlined text-[14px]">check</span> Confirmed
                                    </span>
                                </div>
                                <div class="flex justify-between items-center pb-3 border-b border-gray-100 dark:border-slate-700">
                                    <span class="text-gray-500 dark:text-gray-400">Block:</span>
                                    <span class="text-gray-900 dark:text-gray-200 font-medium" id="blockNumber">#0</span>
                                </div>
                                <div class="flex justify-between items-center pb-3 border-b border-gray-100 dark:border-slate-700">
                                    <span class="text-gray-500 dark:text-gray-400">Gas Used:</span>
                                    <span class="text-gray-900 dark:text-gray-200 font-medium" id="gasUsed">0 MATIC</span>
                                </div>
                                <div class="flex justify-between items-center pb-3 border-b border-gray-100 dark:border-slate-700">
                                    <span class="text-gray-500 dark:text-gray-400">Timestamp:</span>
                                    <span class="text-gray-900 dark:text-gray-200 font-medium" id="txTimestamp">Just now</span>
                                </div>
                            </div>
                            <a href="#" id="explorerLink" target="_blank" class="mt-4 flex items-center justify-center gap-2 bg-white dark:bg-slate-800 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-800 py-2 rounded-lg font-medium transition-colors hover:bg-green-50 dark:hover:bg-green-900/30 text-sm">
                                <span class="material-symbols-outlined text-[18px]">open_in_new</span> View on Polygonscan
                            </a>
                        </div>
                    </div>
                    
                    <!-- Mining Status -->
                    <div id="miningStatus" style="display: none;" class="py-12 text-center">
                        <span class="material-symbols-outlined text-[48px] animate-[spin_2s_linear_infinite] text-green-500 mb-4 inline-block">autorenew</span>
                        <h4 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Mining Transaction...</h4>
                        <p class="text-gray-500 dark:text-gray-400 text-sm">This usually takes 2-5 seconds on Polygon</p>
                    </div>

                    <!-- Empty State -->
                    <div id="emptyState" class="py-12 text-center">
                        <span class="material-symbols-outlined text-[48px] text-gray-300 dark:text-gray-600 mb-4 inline-block">link</span>
                        <h4 class="text-lg font-bold text-gray-900 dark:text-white mb-2">No Recent Transactions</h4>
                        <p class="text-gray-500 dark:text-gray-400 text-sm">Report fraud to see blockchain activity</p>
                    </div>
                </div>

                <!-- Live stats -->
                <div class="bg-surface dark:bg-dark-surface rounded-2xl p-6 border border-border dark:border-dark-border shadow-soft dark:shadow-dark-soft relative overflow-hidden group">
                    <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-600 to-green-400"></div>
                    <div class="flex items-center gap-3 mb-6">
                        <span class="material-symbols-outlined text-purple-500 text-[28px]">query_stats</span>
                        <h3 class="text-xl font-bold text-gray-900 dark:text-dark-primary">Network Statistics</h3>
                    </div>

                    <div class="grid grid-cols-2 gap-4 mb-6">
                        <div class="bg-gray-50 dark:bg-slate-800 p-4 rounded-xl border border-gray-100 dark:border-dark-border">
                            <p class="text-[10px] sm:text-xs text-gray-500 uppercase tracking-wider mb-2">Total Fraud Reports</p>
                            <p class="text-2xl font-bold text-green-600 dark:text-green-500 transition-transform duration-300" id="totalReports">24</p>
                        </div>
                        <div class="bg-gray-50 dark:bg-slate-800 p-4 rounded-xl border border-gray-100 dark:border-dark-border">
                            <p class="text-[10px] sm:text-xs text-gray-500 uppercase tracking-wider mb-2">Latest Block</p>
                            <p class="text-xl sm:text-2xl font-bold text-green-600 dark:text-green-500 transition-transform duration-300" id="latestBlock">#12,456,789</p>
                        </div>
                        <div class="bg-gray-50 dark:bg-slate-800 p-4 rounded-xl border border-gray-100 dark:border-dark-border">
                            <p class="text-[10px] sm:text-xs text-gray-500 uppercase tracking-wider mb-2">Gas Price</p>
                            <p class="text-xl sm:text-2xl font-bold text-green-600 dark:text-green-500 transition-transform duration-300" id="gasPrice">42.7 Gwei</p>
                        </div>
                        <div class="bg-gray-50 dark:bg-slate-800 p-4 rounded-xl border border-gray-100 dark:border-dark-border">
                            <p class="text-[10px] sm:text-xs text-gray-500 uppercase tracking-wider mb-2">Avg. Block Time</p>
                            <p class="text-xl sm:text-2xl font-bold text-green-600 dark:text-green-500 transition-transform duration-300" id="blockTime">2.1s</p>
                        </div>
                    </div>
                    
                    <div class="flex gap-3">
                        <button onclick="refreshStats()" class="flex-1 flex justify-center items-center gap-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 hover:bg-gray-50 dark:hover:bg-slate-700 text-gray-700 dark:text-gray-200 font-medium py-3 rounded-lg transition-colors text-sm">
                            <span class="material-symbols-outlined text-[18px]">refresh</span> Refresh Stats
                        </button>
                        <button onclick="checkFraud()" class="flex-1 flex justify-center items-center gap-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 hover:bg-gray-50 dark:hover:bg-slate-700 text-gray-700 dark:text-gray-200 font-medium py-3 rounded-lg transition-colors text-sm">
                            <span class="material-symbols-outlined text-[18px]">search</span> Check Account
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div class="bg-orange-50 dark:bg-orange-900/10 border border-orange-200 dark:border-orange-800/50 rounded-xl p-4 flex gap-4 text-orange-800 dark:text-orange-400">
            <span class="material-symbols-outlined text-[24px]">lightbulb</span>
            <p class="text-sm"><strong>Demo Mode:</strong> This interface simulates real blockchain interactions. SafeFlow's production system integrates with Polygon Mumbai for immutable fraud reporting. Transaction hashes and blocks are simulated for demonstration purposes.</p>
        </div>

        <div class="text-center py-6 text-sm text-gray-500 dark:text-gray-400 border-t border-border dark:border-dark-border mt-4">
            <p>SafeFlow • Financial Protection on Blockchain • Hackathon Demo v1.0</p>
            <p>All transactions are simulated for demonstration purposes</p>
        </div>

    </div>
</div>
</main>
</div>
"""

full_html = shell_top + tailwind_content + blockchains_script + "\n" + sidebar_script + "\n</body>\n</html>"

with open('frontends/blockchains.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Done!")

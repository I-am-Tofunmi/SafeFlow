document.addEventListener("DOMContentLoaded", async () => {
  const API_BASE_URL = "http://127.0.0.1:8000";

  // Configuration Check
  const token = localStorage.getItem("safeflow_token");
  const userId = localStorage.getItem("safeflow_user_id");
  const fullName = localStorage.getItem("safeflow_full_name") || "User";
  const trustScore = localStorage.getItem("safeflow_trust_score") || "720";

  if (!token || !userId) {
    console.warn("User not authenticated.");
    return;
  }

  // 1. Populate Names
  const nameElems = document.querySelectorAll(".ui-user-name");
  nameElems.forEach(el => {
    el.textContent = fullName;
  });
  
  const shortNameElems = document.querySelectorAll(".ui-user-short-name");
  shortNameElems.forEach(el => {
    const first = fullName.split(" ")[0];
    el.textContent = first;
  });

  const scoreElems = document.querySelectorAll(".ui-trust-score");
  scoreElems.forEach(el => {
    el.textContent = trustScore;
  });

  // 2. Fetch Balance Component
  const balanceElems = document.querySelectorAll(".ui-balance");
  if (balanceElems.length > 0) {
    try {
      const resp = await fetch(`${API_BASE_URL}/transactions/balance?user_id=${userId}`);
      if (resp.ok) {
        const data = await resp.json();
        const formatted = new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' }).format(data.balance || 0);
        balanceElems.forEach(el => el.textContent = formatted);
      }
    } catch (e) {
      console.error("Failed to fetch balance", e);
    }
  }

  // 3. Fetch Transaction History
  const txTableBody = document.getElementById("ui-tx-table-body");
  if (txTableBody) {
    try {
      const resp = await fetch(`${API_BASE_URL}/transactions/history?user_id=${userId}`);
      if (resp.ok) {
        const txs = await resp.json();
        
        txTableBody.innerHTML = ""; // Clear placeholders

        if (txs.length === 0) {
          txTableBody.innerHTML = `<tr><td colspan="7" class="px-6 py-8 text-center text-gray-500">No transactions found.</td></tr>`;
        } else {
          txs.forEach(tx => {
            const isCredit = tx.type === "credit";
            const amountFormatted = new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' }).format(tx.amount);
            const date = new Date(tx.timestamp);
            
            // Generate icon
            let iconClass = isCredit ? "text-green-600 bg-green-100" : "text-red-600 bg-red-100";
            let iconCode = isCredit ? "arrow_downward" : "arrow_upward";
            let typeLabel = isCredit ? "Deposit / Receive" : "Transfer / Send";
            
            // Build Row HTML
            const tr = document.createElement("tr");
            tr.className = "hover:bg-gray-50 transition-colors group";
            tr.innerHTML = `
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center gap-4">
                  <div class="size-10 rounded-full flex items-center justify-center flex-shrink-0 ${iconClass}">
                    <span class="material-symbols-outlined text-[20px]">${iconCode}</span>
                  </div>
                  <div class="flex flex-col">
                    <span class="text-sm font-bold text-gray-900">${typeLabel}</span>
                    <span class="text-xs text-gray-500">${tx.message || "SafeFlow Transfer"}</span>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200">
                  ${isCredit ? 'Income' : 'Expense'}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex flex-col">
                  <span class="text-sm text-gray-900 font-medium">${date.toLocaleDateString()}</span>
                  <span class="text-xs text-gray-500">${date.toLocaleTimeString()}</span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-sm text-gray-500 font-mono">TRX-${tx.id.toString().padStart(6, '0')}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-${tx.status === 'completed' ? 'green' : 'yellow'}-50 text-${tx.status === 'completed' ? 'green' : 'yellow'}-700 border border-${tx.status === 'completed' ? 'green' : 'yellow'}-100">
                  <span class="size-1.5 rounded-full bg-${tx.status === 'completed' ? 'green' : 'yellow'}-500"></span>
                  ${tx.status.charAt(0).toUpperCase() + tx.status.slice(1)}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <span class="text-sm font-bold ${isCredit ? 'text-green-600' : 'text-gray-900'}">
                  ${isCredit ? '+' : '-'} ${amountFormatted}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <button class="text-gray-400 hover:text-black transition-colors p-1 rounded hover:bg-gray-200">
                  <span class="material-symbols-outlined text-[20px]">more_vert</span>
                </button>
              </td>
            `;
            txTableBody.appendChild(tr);
          });
        }
      }
    } catch (e) {
      console.error("Failed to fetch history.", e);
    }
  }

  // 4. Fetch Recent Activity List (Homepage)
  const txListBody = document.getElementById("ui-recent-tx-list");
  if (txListBody) {
    try {
      const resp = await fetch(`${API_BASE_URL}/transactions/history?user_id=${userId}`);
      if (resp.ok) {
        const txs = await resp.json();
        txListBody.innerHTML = "";
        if (txs.length === 0) {
          txListBody.innerHTML = `<div class="p-3 text-center text-sm text-gray-500">No recent activity.</div>`;
        } else {
          // just show top 4
          txs.slice(0, 4).forEach(tx => {
            const isCredit = tx.type === "credit";
            const amountFormatted = new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' }).format(tx.amount);
            const date = new Date(tx.timestamp);
            
            let iconClass = isCredit ? "bg-green-100 text-green-600" : "bg-red-100 text-red-600";
            let iconCode = isCredit ? "arrow_downward" : "arrow_upward";
            
            const div = document.createElement("div");
            div.className = "flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer group border border-transparent hover:border-gray-100";
            div.innerHTML = `
              <div class="flex items-center gap-4">
                <div class="size-10 rounded-full flex items-center justify-center ${iconClass}">
                  <span class="material-symbols-outlined text-[20px]">${iconCode}</span>
                </div>
                <div class="flex flex-col">
                  <p class="text-gray-900 font-semibold text-sm">${isCredit ? 'Deposit' : 'Transfer'}</p>
                  <div class="flex items-center gap-2">
                    <p class="text-gray-500 text-xs">${date.toLocaleDateString()}</p>
                    <span class="flex items-center gap-0.5 text-[10px] bg-${tx.status === 'completed' ? 'green' : 'yellow'}-50 text-${tx.status === 'completed' ? 'green' : 'yellow'}-800 px-1.5 py-0.5 rounded">
                      ${tx.status}
                    </span>
                  </div>
                </div>
              </div>
              <p class="text-sm font-bold ${isCredit ? 'text-green-600' : 'text-gray-900'}">
                ${isCredit ? '+' : '-'} ${amountFormatted}
              </p>
            `;
            txListBody.appendChild(div);
          });
        }
      }
    } catch (e) {
      console.error(e);
    }
  }
});

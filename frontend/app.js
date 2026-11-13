
const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.getElementById("investigationForm");
const accountInput = document.getElementById("accountId");
const investigateBtn = document.getElementById("investigateBtn");
const message = document.getElementById("message");
const report = document.getElementById("report");
const emptyState = document.getElementById("emptyState");
const downloadBtn = document.getElementById("downloadBtn");

let latestReport = null;

// Check backend connection
async function checkAPI() {
    const status = document.getElementById("apiStatus");
    const systemStatus = document.getElementById("systemStatus");

    try {
        const response = await fetch(`${API_BASE_URL}/health`);

        if (!response.ok) {
            throw new Error("Backend unavailable");
        }

        status.innerHTML =
            '<span class="status-dot"></span> API Connected';

        systemStatus.textContent = "Online";
    } catch (error) {
        status.textContent = "API Disconnected";
        systemStatus.textContent = "Offline";
    }
}

// Display key-value data
function renderObject(containerId, data) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    if (!data || Object.keys(data).length === 0) {
        container.textContent = "No data available.";
        return;
    }

    Object.entries(data).forEach(([key, value]) => {
        const item = document.createElement("div");
        item.className = "data-item";

        const label = document.createElement("span");
        label.textContent = key.replaceAll("_", " ");

        const strong = document.createElement("strong");
        strong.textContent =
            typeof value === "object"
                ? JSON.stringify(value)
                : String(value ?? "-");

        item.append(label, strong);
        container.appendChild(item);
    });
}

// Safely display lists of evidence, alerts and policies
function renderList(containerId, items, emptyText) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    if (!Array.isArray(items) || items.length === 0) {
        container.textContent = emptyText;
        return;
    }

    items.forEach((item, index) => {
        const entry = document.createElement("div");
        entry.className = "data-entry";

        const heading = document.createElement("strong");
        heading.textContent = `Entry ${index + 1}`;

        const paragraph = document.createElement("p");
        paragraph.textContent = JSON.stringify(item, null, 2);

        entry.append(heading, paragraph);
        container.appendChild(entry);
    });
}

// Render investigation response
function displayReport(data) {
    latestReport = data;

    emptyState.classList.add("hidden");
    report.classList.remove("hidden");
    downloadBtn.disabled = false;

    document.getElementById("resultAccount").textContent =
        data.account_id || "Unknown";

    document.getElementById("transactionCount").textContent =
        `${data.transactions_reviewed ?? 0} transactions reviewed`;

    document.getElementById("findings").textContent =
        data.findings || "No findings available.";

    document.getElementById("recommendation").textContent =
        data.recommendation || "No recommendation available.";

    document.getElementById("disclaimer").textContent =
        data.disclaimer || "Human review is required.";

    renderObject("profile", data.account_profile);

    renderList(
        "evidence",
        data.transaction_evidence,
        "No transaction patterns matched the configured rules."
    );

    renderList(
        "alerts",
        data.previous_alerts,
        "No previous alerts found."
    );

    renderList(
        "policy",
        data.policy_context,
        "No relevant policy context retrieved."
    );

    document.getElementById("rawJson").textContent =
        JSON.stringify(data, null, 2);
}

// Submit investigation request
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const accountId = accountInput.value.trim();

    if (!accountId) {
        message.textContent = "Please enter an account ID.";
        return;
    }

    investigateBtn.disabled = true;
    investigateBtn.textContent = "Investigating...";
    message.textContent = "Collecting evidence and generating report...";

    try {
        const response = await fetch(`${API_BASE_URL}/investigate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                account_id: accountId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || `Request failed: ${response.status}`
            );
        }

        displayReport(data);
        message.textContent = "Investigation completed successfully.";

    } catch (error) {
        message.textContent = `Error: ${error.message}`;
    } finally {
        investigateBtn.disabled = false;
        investigateBtn.textContent = "Investigate Account →";
    }
});

// Export investigation as JSON
downloadBtn.addEventListener("click", () => {
    if (!latestReport) return;

    const blob = new Blob(
        [JSON.stringify(latestReport, null, 2)],
        { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = `${latestReport.account_id}_report.json`;

    link.click();
    URL.revokeObjectURL(url);
});

// Initial backend health check
checkAPI();

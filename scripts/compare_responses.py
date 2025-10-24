
import os
import json
import requests
from deepdiff import DeepDiff



# URLs of both iFlows
IFLOW_OLD = "https://syn-int-suite-ent-qgjsk2hi.it-cpi024-rt.cfapps.eu10-002.hana.ondemand.com/http/ordersimulationtest"  # CPI Dev (ent) old mapping
IFLOW_NEW = "https://syn-int-suite-ent-qgjsk2hi.it-cpi024-rt.cfapps.eu10-002.hana.ondemand.com/http/ordersimulationMappingChange"  # CPI Dev (ent) new mapping

# =============================
# 🔐 Basic authentication (use GitHub Secrets for security)
# =============================
USERNAME = os.getenv("CPI_USER")
PASSWORD = os.getenv("CPI_PASS")

# =============================
# 🌐 CPI iFlow URLs
# =============================
IFLOW_OLD = "https://syn-int-suite-ent-qgjsk2hi.it-cpi024-rt.cfapps.eu10-002.hana.ondemand.com/http/ordersimulationtest"
IFLOW_NEW = "https://syn-int-suite-ent-qgjsk2hi.it-cpi024-rt.cfapps.eu10-002.hana.ondemand.com/http/ordersimulationMappingChange"

# =============================
# 📁 File paths
# =============================
REQUEST_FILE = "request_payload.json"
RESP_DIR = "responses"
RESP1_FILE = os.path.join(RESP_DIR, "response_1.json")
RESP2_FILE = os.path.join(RESP_DIR, "response_2.json")
DIFF_FILE = os.path.join(RESP_DIR, "diff_report.json")

# Ensure response folder exists
os.makedirs(RESP_DIR, exist_ok=True)

# =============================
# 🛰️ Function: Hit CPI iFlow
# =============================
def hit_iflow(url, payload):
    print(f"Hitting iFlow: {url}")
    response = requests.post(
        url,
        json=payload,
        auth=(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()

# =============================
# 💾 Function: Save JSON data
# =============================
def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# =============================
# 🚀 Main execution
# =============================
def main():
    print("=== Task 1: Hit Old Mapping iFlow ===")
    with open(REQUEST_FILE, "r") as f:
        payload = json.load(f)
    resp1 = hit_iflow(IFLOW_OLD, payload)
    save_json(RESP1_FILE, resp1)
    print(f"Response 1 stored at {RESP1_FILE}")

    print("=== Task 2: Hit New Mapping iFlow ===")
    resp2 = hit_iflow(IFLOW_NEW, payload)
    save_json(RESP2_FILE, resp2)
    print(f"Response 2 stored at {RESP2_FILE}")

    print("=== Task 3: Compare Responses ===")
    diff = DeepDiff(resp1, resp2, ignore_order=True)

    if diff:
        print("Differences found:")
        # ✅ Convert DeepDiff object to normal dict so it's JSON serializable
        diff_dict = json.loads(diff.to_json())
        print(json.dumps(diff_dict, indent=2))
        save_json(DIFF_FILE, diff_dict)
        print(f"🟡 Diff report saved at {DIFF_FILE}")
    else:
        print("✅ No differences found between old and new mapping responses!")
        save_json(DIFF_FILE, {})
        # Optional: fail pipeline if you want difference enforcement
        # raise AssertionError("No differences found between old and new mapping responses!")

if __name__ == "__main__":
    main()

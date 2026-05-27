import requests
import json
import time
import math

# --- Configuration ---
API_KEY = "YOUR_API_KEY"
DISTRO = "Solus"
OUTPUT_FILE = "release_monitoring_data.json" # Set path
ITEMS_PER_PAGE = 250  # 250 is the maximum allowed by the Anitya API

def fetch_solus_packages():
    base_url = "https://release-monitoring.org/api/v2/packages/"

    # The API expects "Token <YOUR_TOKEN>" for the Authorization header
    headers = {
        "Authorization": f"Token {API_KEY}",
        "Accept": "application/json"
    }

    all_packages = []
    page = 1
    total_pages = 1  # calculated dynamically after the first request

    print(f"Starting to fetch packages for {DISTRO}...")

    while page <= total_pages:
        params = {
            "distribution": DISTRO,
            "page": page,
            "items_per_page": ITEMS_PER_PAGE
        }

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.status_code} - {response.text}")
            break

        data = response.json()

        # Calculate total pages on the first loop iteration
        if page == 1:
            total_items = data.get("total_items", 0)
            total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
            print(f"Found {total_items} total packages. This will take {total_pages} requests.")

            if total_items == 0:
                print("No packages found.")
                break

        items = data.get("items", [])

        # Extract the required fields
        for item in items:
            pkg_data = {
                "project_name": item.get("project"),
                "solus_package": item.get("name"),
                "stable_version": item.get("stable_version"),
                "latest_version": item.get("version")
            }
            all_packages.append(pkg_data)

        print(f"Successfully processed page {page}/{total_pages}")

        page += 1

        # prevent hitting any unexpected rate limits.
        time.sleep(0.5)

    # Export the collected data to a JSON file
    with open(OUTPUT_FILE, 'w') as json_file:
        json.dump(all_packages, json_file, indent=4)

    print(f"\nDone! Exported {len(all_packages)} packages to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_solus_packages()

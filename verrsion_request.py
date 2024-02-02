import requests
import tkinter as tk
from tkinter import ttk

def get_versions(metadata_url, environment):
    try:
        response = requests.get(metadata_url)
        response.raise_for_status()
        metadata = response.json()

        k8s_info = metadata.get("version", {}).get("k8s", {})
        k8s_version = k8s_info.get("version", "N/A")

        ping_cloud_base_info = metadata.get("version", {}).get("ping-cloud-base", {})
        ping_cloud_base_version = ping_cloud_base_info.get("version", "N/A")

        name = metadata.get("name", f"N/A ({environment})")
        region = metadata_url.split('.')[2]

        return {
            "Environment": name,
            "k8s Version": k8s_version,
            "ping-cloud-base Version": ping_cloud_base_version,
            "Region": region,
        }

    except requests.RequestException as e:
        return {"Error": f"Error fetching metadata for {environment}: {e}"}

def generate_report():
    clear_report()

    environments_with_eks_target_version_v123 = []
    environments_with_eks_target_version_v124 = []
    environments_with_eks_target_version_v125 = []
    environments_with_ping_cloud_target_version_v1730 = []
    environments_with_ping_cloud_target_version_v1800 = []
    environments_with_ping_cloud_target_version_v171 = []
    environments_with_ping_cloud_target_version_v172 = []
    environments_with_ping_cloud_target_version_v173 = []

    for metadata_url in metadata_urls:
        environment = metadata_url.split('.')[1]
        versions_info = get_versions(metadata_url, environment)

        if "Error" in versions_info:
            result_text.insert(tk.END, f"{versions_info['Error']}\n\n")
            continue

        # Check if the versions match the targets
        if k8s_version_targets[0] in versions_info["k8s Version"]:
            environments_with_eks_target_version_v123.append(environment)

        if k8s_version_targets[1] in versions_info["k8s Version"]:
            environments_with_eks_target_version_v124.append(environment)

        if k8s_version_targets[2] in versions_info["k8s Version"]:
            environments_with_eks_target_version_v125.append(environment)

        if ping_cloud_base_version_targets[0] in versions_info["ping-cloud-base Version"]:
            environments_with_ping_cloud_target_version_v1730.append(environment)

        if ping_cloud_base_version_targets[1] in versions_info["ping-cloud-base Version"]:
            environments_with_ping_cloud_target_version_v1800.append(environment)

        if "v1.17.1" in versions_info["ping-cloud-base Version"]:
            environments_with_ping_cloud_target_version_v171.append(environment)

        if "v1.17.2" in versions_info["ping-cloud-base Version"]:
            environments_with_ping_cloud_target_version_v172.append(environment)

        if "v1.17.3" in versions_info["ping-cloud-base Version"]:
            environments_with_ping_cloud_target_version_v173.append(environment)

    result_text.insert(tk.END, f"Beluga & EKS Version Report:\n\n")

    # Display counts in chronological order
    display_count("Ping-cloud version", "v1.17.1", environments_with_ping_cloud_target_version_v171)
    display_count("Ping-cloud version", "v1.17.2", environments_with_ping_cloud_target_version_v172)
    display_count("Ping-cloud version", "v1.17.3", environments_with_ping_cloud_target_version_v173)
    display_count("EKS version", "v1.23", environments_with_eks_target_version_v123)
    display_count("EKS version", "v1.24", environments_with_eks_target_version_v124)
    display_count("EKS version", "v1.25", environments_with_eks_target_version_v125)
    display_count("Ping-cloud version", "v1.17.3.0", environments_with_ping_cloud_target_version_v1730)
    display_count("Ping-cloud version", "v1.18.0.0", environments_with_ping_cloud_target_version_v1800)

def display_count(version_label, version_number, environments_list):
    result_text.insert(tk.END, f"Count for {version_label} ({version_number}): {len(environments_list)}\n")
    result_text.insert(tk.END, f"Environments: {', '.join(environments_list)}\n\n")

def clear_report():
    result_text.delete(1.0, tk.END)

metadata_urls = [
    "https://metadata.dev-axa.eu1.ping.cloud/",
    "https://metadata.prod-axa.eu1.ping.cloud/",
    "https://metadata.dev-vizio.us1.ping.cloud/",
    "https://metadata.prod-vizio.us1.ping.cloud/",
    "https://metadata.dev-maples.eu1.ping.cloud/",
    "https://metadata.dev-cfs.au1.ping.cloud/",
    "https://metadata.dev-becu.us2.ping.cloud/"
    # Add more URLs as needed
]

k8s_version_targets = ["v1.23", "v1.24", "v1.25"]
ping_cloud_base_version_targets = ["v1.17.3.0", "v1.18.0.0", "v1.17.1", "v1.17.2", "v1.17.3"]

# Create main window
root = tk.Tk()
root.title("Version Reporting Tool")

# Create and configure frames
frame_top = ttk.Frame(root, padding=10)
frame_top.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame_bottom = ttk.Frame(root, padding=10)
frame_bottom.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create widgets
generate_button = ttk.Button(frame_top, text="Generate Report", command=generate_report)
clear_button = ttk.Button(frame_top, text="Clear Report", command=clear_report)
result_text = tk.Text(frame_bottom, wrap="word", width=80, height=20)

# Layout widgets
generate_button.grid(row=0, column=0, padx=5, pady=5)
clear_button.grid(row=0, column=1, padx=5, pady=5)
result_text.grid(row=1, column=0, padx=5, pady=5)

# Start GUI event loop
root.mainloop()

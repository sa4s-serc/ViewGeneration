import pandas as pd
import requests
import os

# === Config ===
input_csv = "./filtered_dataset.csv"     # Your input CSV
output_csv = "repos_with_last_commit.csv"  # Output file
repo_col = "Repository Name"

# === GitHub Auth (optional but recommended to avoid 403 due to rate limits) ===
# Create a token at: https://github.com/settings/tokens (no scopes needed for public)
GITHUB_TOKEN = None  # e.g., "ghp_XXXX..." or leave as None for unauthenticated

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def get_last_commit_date(owner_repo):
    """Fetch the latest commit date for a given GitHub 'owner/repo'."""
    api_url = f"https://api.github.com/repos/{owner_repo}/commits"

    response = requests.get(api_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch {owner_repo}: {response.status_code}")
        return None, response.status_code

    commits = response.json()
    if not commits:
        return None, 200

    last_commit = commits[0]
    date = last_commit["commit"]["author"]["date"]
    return date, 200


# === Step 1: Load Input CSV ===
df = pd.read_csv(input_csv, sep=";")

if repo_col not in df.columns:
    raise ValueError(f"Column '{repo_col}' not found in CSV file.")

# === Step 2: Resume Logic ===
processed_repos = {}
if os.path.exists(output_csv):
    existing_df = pd.read_csv(output_csv, sep=";")
    processed_repos = dict(zip(existing_df[repo_col], existing_df["Last Commit Date"]))
    print(f"🔁 Resuming from previous progress... ({len(processed_repos)} repos already processed)")

# === Step 3: Process Each Repo ===
results = []

for repo in df[repo_col]:
    repo = repo.strip()
    # ✅ Skip already processed repos
    if repo in processed_repos:
        print(f"⏩ Skipping {repo} (already processed)")
        results.append({"Repository Name": repo, "Last Commit Date": processed_repos[repo]})
        continue

    print(f"🔍 Fetching last commit date for: {repo}")
    date, status = get_last_commit_date(repo)

    if status != 200:
        # ❌ Stop immediately if failure
        print(f"❌ Stopping due to failure on repo: {repo} (HTTP {status})")
        break

    results.append({"Repository Name": repo, "Last Commit Date": date})

    # ✅ Save progress after every successful fetch
    temp_df = pd.DataFrame(results + [
        {"Repository Name": r, "Last Commit Date": d} 
        for r, d in processed_repos.items()
    ]).drop_duplicates(subset=["Repository Name"], keep="last")

    temp_df.to_csv(output_csv, sep=";", index=False)
    print(f"💾 Progress saved to {output_csv}")

print("\n✅ Finished (or stopped due to an error).")

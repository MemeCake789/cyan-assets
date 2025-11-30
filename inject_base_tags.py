import os

# Configuration
REPO_USER = "MemeCake789"
REPO_NAME = "cyan-games"
BRANCH = "main"
BASE_DIR = "/home/sand/cyan-assets/HTML"

# List of games to modify
GAMES = [
    "deltarune-main",
    "hl",
    "Baldi",
    "granny",
    "ultrakill",
    "SubwaySurfers",
    "ropepolice",
    "crime-city-2-3d-webgl",
    "Balatro",
    "WebFishing",
    "10minutestilldawn",
    "superhot",
    "Bitlife",
    "Antimatter Dimensions",
    "game-inside",
    "ages-of-conflict",
    "RetroBowl",
    "clusterrush"
]

def inject_base_tag(game_dir):
    game_path = os.path.join(BASE_DIR, game_dir)
    if not os.path.exists(game_path):
        print(f"Skipping {game_dir}: Directory not found")
        return

    # Find index.html
    index_file = os.path.join(game_path, "index.html")
    if not os.path.exists(index_file):
        # Try to find any html file if index.html doesn't exist
        html_files = [f for f in os.listdir(game_path) if f.endswith('.html')]
        if len(html_files) == 1:
            index_file = os.path.join(game_path, html_files[0])
        else:
            print(f"Skipping {game_dir}: No index.html found (found {html_files})")
            return

    print(f"Processing {game_dir} -> {index_file}")
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for existing base tag and replace it
    import re
    base_tag_pattern = r'<base\s+href=["\'][^"\']*["\']\s*/?>'
    
    # Construct CDN URL
    cdn_url = f"https://cdn.jsdelivr.net/gh/{REPO_USER}/{REPO_NAME}@{BRANCH}/{game_dir}/"
    new_base_tag = f'<base href="{cdn_url}">'

    if re.search(base_tag_pattern, content):
        print(f"Updating {game_dir}: Replacing existing <base> tag")
        new_content = re.sub(base_tag_pattern, new_base_tag, content)
    else:
        print(f"Updating {game_dir}: Inserting new <base> tag")
        # Insert after <head> or <html>
        if "<head>" in content:
            new_content = content.replace("<head>", f"<head>\n  {new_base_tag}", 1)
        elif "<html" in content:
            new_content = re.sub(r'(<html[^>]*>)', r'\1\n' + new_base_tag, content, count=1)
        else:
            new_content = new_base_tag + "\n" + content

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Success: Processed {game_dir}")

def main():
    print("Starting base tag injection...")
    for game in GAMES:
        inject_base_tag(game)
    print("Done.")

if __name__ == "__main__":
    main()

import os
import shutil

# Configuration
BASE_DIR = "/home/sand/cyan-assets/HTML"
STAGING_DIR = "/home/sand/cyan-assets/_LARGE_GAMES_STAGING"

# List of games to move
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

def stage_game(game_dir):
    source_path = os.path.join(BASE_DIR, game_dir)
    dest_path = os.path.join(STAGING_DIR, game_dir)

    if not os.path.exists(source_path):
        print(f"Skipping {game_dir}: Source directory not found")
        return

    if os.path.exists(dest_path):
        print(f"Skipping {game_dir}: Destination already exists")
        return

    print(f"Staging {game_dir}...")

    # Move the entire directory
    shutil.move(source_path, dest_path)

    # Re-create the original directory
    os.makedirs(source_path, exist_ok=True)

    # Copy index.html back
    # Try to find index.html in the staged directory
    index_file = os.path.join(dest_path, "index.html")
    if not os.path.exists(index_file):
         # Try to find any html file if index.html doesn't exist (fallback logic from previous script)
        html_files = [f for f in os.listdir(dest_path) if f.endswith('.html')]
        if len(html_files) == 1:
            index_file = os.path.join(dest_path, html_files[0])
        elif game_dir == "Antimatter Dimensions":
             # Special case for Antimatter Dimensions which has index.html in public/
             index_file = os.path.join(dest_path, "public", "index.html")

    if os.path.exists(index_file):
        # We need to copy it back to the source path root, or wherever it was relative to the game dir?
        # The requirement is to keep the entry point.
        # For Antimatter Dimensions, the entry point was likely not at the root if it was in public/, 
        # BUT the previous script skipped it because it didn't find index.html at root.
        # Let's check where the index.html should be.
        # If the original structure was `HTML/Game/index.html`, we copy it back to `HTML/Game/index.html`.
        # If it was `HTML/Game/public/index.html`, we might need to recreate `public/`?
        # However, for the purpose of this task, most games had `index.html` at the root.
        
        # Let's just copy the found index file to the root of the source path for now, 
        # assuming that's where the entry point is expected.
        # Wait, if Antimatter Dimensions has it in public/, copying it to root might break paths if it relies on relative paths?
        # But Antimatter Dimensions uses an iframe to an external site, so it should be fine.
        
        target_index = os.path.join(source_path, os.path.basename(index_file))
        shutil.copy2(index_file, target_index)
        print(f"  - Moved to staging")
        print(f"  - Restored {os.path.basename(index_file)} to original location")
    else:
        print(f"  - Moved to staging")
        print(f"  - WARNING: No index.html found to restore!")

def main():
    if not os.path.exists(STAGING_DIR):
        os.makedirs(STAGING_DIR)
        print(f"Created staging directory: {STAGING_DIR}")

    print("Starting staging process...")
    for game in GAMES:
        stage_game(game)
    print("Done.")

if __name__ == "__main__":
    main()

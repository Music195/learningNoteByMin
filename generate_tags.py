import os
import re
import json

notes_dir = "notes"
tags_output = "tags.json"
tag_data = {}

for filename in os.listdir(notes_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(notes_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Look for tags in comments: <!-- tags: algebra, calculus -->
        match = re.search(r"<!--\s*tags:\s*(.*?)\s*-->", content, re.IGNORECASE)
        if match:
            tags = [tag.strip() for tag in match.group(1).split(",") if tag.strip()]
            note_name = filename[:-5]  # remove .html extension
            tag_data[note_name] = tags

# Write to tags.json
with open(tags_output, "w", encoding="utf-8") as f:
    json.dump(tag_data, f, indent=4)

print(f"✅ Generated {tags_output} with {len(tag_data)} entries.")
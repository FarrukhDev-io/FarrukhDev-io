#!/usr/bin/env python3
import subprocess
import os

def main():
    # Get fastfetch output
    try:
        result = subprocess.run(["fastfetch", "--pipe"], capture_output=True, text=True, check=True)
        lines = result.stdout.rstrip().split("\n")
    except Exception as e:
        print(f"Error running fastfetch: {e}")
        lines = ["Error running fastfetch"]

    # SVG geometry
    char_width = 8
    line_height = 18
    width = max(len(l) for l in lines) * char_width + 60
    height = len(lines) * line_height + 60

    # Build SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<style>
    .term {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
        font-size: 14px;
        fill: #c9d1d9;
    }}
    .line {{
        opacity: 0;
        animation: appear 0.1s forwards;
    }}
    @keyframes appear {{
        to {{ opacity: 1; }}
    }}
'''
    # Add staggered delays for each line to create a typing/reveal effect
    for i in range(len(lines)):
        delay = i * 0.15 # 150ms per line
        svg += f"    .l{i} {{ animation-delay: {delay}s; }}\n"
    
    svg += '''</style>
<rect width="100%" height="100%" fill="#0d1117" rx="10"/>
'''
    
    for i, line in enumerate(lines):
        # Escape XML chars
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        y = 35 + i * line_height
        # Preserve spaces using xml:space
        svg += f'<text x="30" y="{y}" class="term line l{i}" xml:space="preserve">{line}</text>\n'

    svg += '</svg>'

    out_path = os.path.join(os.path.dirname(__file__), "..", "fastfetch.svg")
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()

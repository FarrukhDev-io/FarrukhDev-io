import subprocess
import os
import re

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def main():
    # Get fastfetch output
    try:
        result = subprocess.run(["fastfetch", "--pipe"], capture_output=True, text=True, check=True)
        raw_output = strip_ansi(result.stdout)
        lines = raw_output.rstrip().split("\n")
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
    # Add staggered delays for each line to sync perfectly with avi-ascii.svg (5.83s total)
    total_duration = 5.83
    delay_per_line = total_duration / max(1, len(lines))
    for i in range(len(lines)):
        delay = i * delay_per_line
        svg += f"    .l{i} {{ animation-delay: {delay:.3f}s; }}\n"
    
    svg += '''</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#111722"/>
    <stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="12" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="calc(100% - 1px)" height="calc(100% - 1px)" rx="12" fill="none" stroke="#30363d" stroke-width="1"/>
'''
    
    for i, line in enumerate(lines):
        # Escape XML chars
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        y = 35 + i * line_height
        # Preserve spaces by replacing with non-breaking spaces
        line = line.replace(" ", "&#160;")
        svg += f'<text x="30" y="{y}" class="term line l{i}">{line}</text>\n'

    svg += '</svg>'

    out_path = os.path.join(os.path.dirname(__file__), "..", "fastfetch.svg")
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()

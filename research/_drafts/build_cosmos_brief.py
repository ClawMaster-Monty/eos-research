import re

# Read the Minimax packet
with open("C:\\Users\\monty\\eos-research\\research\\_drafts\\The COSMOS Multivitamin Trial by Minimax M3.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Parse sections
section_map = {}
current_key = "preamble"
buffer = []
for line in content.split('\n'):
    m = re.match(r'^## (\d+\..+)$', line)
    if m:
        section_map[current_key] = '\n'.join(buffer)
        current_key = m.group(1).strip()
        buffer = []
    else:
        buffer.append(line)
section_map[current_key] = '\n'.join(buffer)

# Build sections with anchor IDs
def anchor(s):
    s = s.strip().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_to_html(text):
    """Convert simple markdown formatting to HTML for this brief."""
    lines = []
    in_table = False
    table_lines = []
    in_list = False
    list_type = None
    
    for line in text.split('\n'):
        stripped = line.strip()
        
        # Skip separator lines
        if stripped == '---':
            continue
        
        # Bold/italic
        processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        processed = re.sub(r'\*(.+?)\*', r'<em>\1</em>', processed)
        
        # Table handling
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            table_lines.append(processed)
            continue
        elif in_table:
            # End of table
            lines.append(convert_table(table_lines))
            table_lines = []
            in_table = False
        
        # Headers
        if stripped.startswith('### '):
            lines.append(f'<h3>{stripped[4:]}</h3>')
        elif stripped.startswith('## '):
            lines.append(f'<h2>{stripped[3:]}</h2>')
        elif stripped.startswith('# '):
            lines.append(f'<h2>{stripped[2:]}</h2>')
        
        # Bold headings (like **Funding**)
        elif re.match(r'^\*\*.+\*\*$', stripped):
            lines.append(f'<p class="eyebrow ink-accent">{stripped.strip("*")}</p>')
        
        # Lists
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                lines.append('<ul>')
                in_list = True
            content = stripped[2:]
            lines.append(f'<li>{escape_html(content)}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            if not in_list:
                lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            content = re.sub(r'^\d+\.\s', '', stripped)
            lines.append(f'<li>{content}</li>')
        else:
            if in_list:
                lines.append('</ul>' if list_type != 'ol' else '</ol>')
                in_list = False
                list_type = None
            
            if stripped:
                # Check if it's a callout or blank
                lines.append(f'<p>{processed}</p>')
            else:
                lines.append(f'<p>&nbsp;</p>')
    
    # Close any open table
    if in_table and table_lines:
        lines.append(convert_table(table_lines))
    
    # Close any open list
    if in_list:
        lines.append('</ul>' if list_type != 'ol' else '</ol>')
    
    return '\n'.join(lines)


def convert_table(rows):
    """Convert markdown table rows to HTML."""
    if not rows or len(rows) < 2:
        return ''
    
    # Skip separator row (|---| pattern)
    header = rows[0].strip('|').split('|')
    
    data_rows = []
    for r in rows[2:]:
        cells = r.strip('|').split('|')
        data_rows.append(cells)
    
    html = '<div class="table-wrap">\n<table class="evidence-table">\n<thead>\n<tr>'
    for h in header:
        html += f'<th>{h.strip()}</th>'
    html += '</tr>\n</thead>\n<tbody>\n'
    
    for row in data_rows:
        html += '<tr>'
        for cell in row:
            html += f'<td>{escape_html(cell.strip())}</td>'
        html += '</tr>\n'
    
    html += '</tbody>\n</table>\n</div>'
    return html


# Process the bottom line section
preamble = section_map['preamble']
preamble_lines = preamble.split('\n')
# Skip the title and dashed lines
body_start = False
bottom_line_parts = []
for line in preamble_lines:
    if line.strip().startswith('## Bottom Line'):
        body_start = True
        continue
    if line.strip().startswith('## References'):
        break
    if body_start and line.strip() != '---':
        bottom_line_parts.append(line)

preamble_html = md_to_html('\n'.join(bottom_line_parts))


# The insight callout - extract from the bottom line
callout_html = """    <div class="evidence-callout">
      <p class="eyebrow">The bottom line</p>
      <p>
        <strong>COSMOS is null on its two primary endpoints, modestly positive on a small set of pre-specified secondary endpoints (cocoa on CVD death, MVM on lung cancer, MVM on cognitive test scores), and provides no evidence that multivitamins prevent cancer, cardiovascular disease, dementia, or death.</strong>
      </p>
    </div>"""

# Evidence Scorecard
scorecard_html = """    <h3>Evidence Scorecard</h3>
    <div class="table-wrap">
    <table class="evidence-table">
      <thead>
        <tr>
          <th>Domain</th>
          <th>Rating</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Human evidence (RCTs)</td>
          <td><strong>A</strong></td>
          <td>21,442 participants, factorial design, double-blind</td>
        </tr>
        <tr>
          <td>Mechanistic evidence</td>
          <td><strong>A</strong></td>
          <td>Multiple substudies with consistent direction of effect</td>
        </tr>
        <tr>
          <td>Long-term safety</td>
          <td><strong>A</strong></td>
          <td>Centrum Silver widely studied for decades</td>
        </tr>
        <tr>
          <td>Longevity evidence (healthy humans)</td>
          <td><strong>C</strong></td>
          <td>Null on mortality; epigenetic clocks effect is very small</td>
        </tr>
        <tr>
          <td>Cognitive protection</td>
          <td><strong>B−</strong></td>
          <td>Small effect (0.07 SD) but statistically robust; no dementia endpoint</td>
        </tr>
        <tr>
          <td>Recommendation confidence</td>
          <td><strong>Moderate</strong> (cognitive) / <strong>Low</strong> (cancer, CVD, mortality)</td>
          <td>Null primary endpoints prevent population-level recommendations</td>
        </tr>
      </tbody>
    </table>
    </div>"""

# Section names to anchor IDs
section_anchors = {
    '1. Trial Design and Methods': 'design',
    '2. Primary Endpoints: Cancer, CVD, and Mortality': 'primary',
    '3. Secondary Endpoints: Lung Cancer, CVD Death, and Other Signals': 'secondary',
    '4. Cognitive Substudies: Mind, Web, Clinic, and the Pooled Meta-Analysis': 'cognition',
    '5. Effect Size and Clinical Meaning': 'effect-size',
    '6. Methodological Concerns': 'methodological',
    '7. Industry Funding and Disclosed Interests': 'funding',
    '8. Critical Reception': 'reception',
    '9. Comparison With Predecessor Trials: PHS II, SU.VI.MAX, and COSMOS': 'predecessors',
    '10. The Conclusion-Data Audit': 'audit',
    '11. Overall Assessment': 'assessment',
}

# Build the TOC
toc_items = [
    ('bottom-line', 'Bottom line'),
    ('design', 'Design and methods'),
    ('primary', 'Primary endpoints: cancer and CVD'),
    ('secondary', 'Secondary signals'),
    ('cognition', 'Cognitive substudies'),
    ('effect-size', 'Effect size and clinical meaning'),
    ('methodological', 'Methodological concerns'),
    ('funding', 'Funding and disclosures'),
    ('predecessors', 'Comparison with predecessor trials'),
    ('audit', 'Conclusion-data audit'),
    ('references', 'References'),
]

toc_html = '      <ul>\n'
for aid, label in toc_items:
    toc_html += f'        <li><a href="#{aid}">{label}</a></li>\n'
toc_html += '      </ul>'

# Generate the output HTML
output = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The COSMOS Multivitamin Trial: What It Found and What It Did not — EOS Research</title>
  <meta name="description" content="The COSMOS trial is the largest RCT of a daily multivitamin in older adults. Both primary endpoints failed. Here is what the cognitive findings actually mean.">
  <meta property="og:title" content="The COSMOS Multivitamin Trial: What It Found and What It Did not">
  <meta property="og:description" content="21,442 participants. Two primary endpoints, both null. Three cognitive substudies with a small positive signal. Here is what the evidence actually supports.">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://clawmaster-monty.github.io/eos-research/research/cosmos-multivitamin-evidence.html">
  <meta property="og:image" content="https://clawmaster-monty.github.io/eos-research/assets/images/eos-research-branded-landscape.png">
  <meta property="og:image:width" content="1536">
  <meta property="og:image:height" content="1024">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/eos-research/styles.css">
</head>
<body>

<nav class="site-nav">
  <div class="nav-inner">
    <a href="/eos-research/" class="nav-logo">EOS Research</a>
    <div class="nav-links">
      <a href="/eos-research/research/">Archive</a>
      <a href="/eos-research/methodology/">Methodology</a>
    </div>
  </div>
</nav>

<main class="brief-container">

  <header class="brief-header">
    <p class="eyebrow ink-accent">Research report · Nutritional supplements · Cognitive health</p>
    <h1>The COSMOS Multivitamin Trial:<br>What It Found and What It Did not</h1>
    <div class="brief-meta">
      <span class="byline">Nox, AI operator · Reviewed by Monty</span>
      <span class="evidence-badge moderate">Blue Moderate Confidence</span>
      <time datetime="2026-07-20">20 July 2026</time>
    </div>
  </header>

  <p class="disclaimer">
    <strong>Editorial disclaimer:</strong>
    EOS Research summarizes published research for educational purposes.
    This is not medical advice. Consult a physician before making any changes
    to medication or supplementation.
  </p>

  <div class="toc-card">
    <h2>Contents</h2>
''' + toc_html + '''
  </div>

  <section id="bottom-line">
    <h2>Bottom line</h2>
''' + preamble_html + '''
  </section>

''' + callout_html + '''

''' + scorecard_html + '''
'''

# Add each section
section_order = [
    '1. Trial Design and Methods',
    '2. Primary Endpoints: Cancer, CVD, and Mortality',
    '3. Secondary Endpoints: Lung Cancer, CVD Death, and Other Signals',
    '4. Cognitive Substudies: Mind, Web, Clinic, and the Pooled Meta-Analysis',
    '5. Effect Size and Clinical Meaning',
    '6. Methodological Concerns',
    '7. Industry Funding and Disclosed Interests',
    '8. Critical Reception',
    '9. Comparison With Predecessor Trials: PHS II, SU.VI.MAX, and COSMOS',
    '10. The Conclusion-Data Audit',
    '11. Overall Assessment',
]

for sec in section_order:
    anchor_id = section_anchors.get(sec, '')
    sec_content = section_map.get(sec, '')
    
    # Extract the first line (which is a bold heading like "**What COSMOS actually showed**")
    sec_lines = sec_content.strip().split('\n')
    heading = sec_lines[0] if sec_lines else ''
    
    # Remove the heading from the body
    body_lines = sec_lines[1:] if sec_lines else []
    
    # Convert body to HTML
    body_html = md_to_html('\n'.join(body_lines))
    
    output += f'''
  <section id="{anchor_id}">
    <h2>{heading}</h2>
{body_html}
  </section>
'''

# References
ref_lines = section_map.get('preamble', '').split('\n')
in_refs = False
ref_section = []
for line in ref_lines:
    if line.strip() == '## References':
        in_refs = True
        continue
    if in_refs:
        # Check for the closing dashed line
        if line.strip() == '---' or line.strip().startswith('*Prepared for'):
            break
        ref_section.append(line)

ref_html = md_to_html('\n'.join(ref_section))

# Also check section 11 which has the overall assessment and may contain the references
sec11 = section_map.get('11. Overall Assessment', '')
sec11_lines = sec11.split('\n')
in_refs2 = False
for line in sec11_lines:
    if line.strip() == '## References':
        in_refs2 = True
        continue
    if in_refs2:
        if line.strip() == '---' or line.strip().startswith('*Prepared for'):
            break
        ref_section.append(line)

ref_html = md_to_html('\n'.join(ref_section))

output += '''
  <section id="references">
    <h2>References</h2>
''' + ref_html + '''
  </section>

  <div class="editorial-policy">
    <strong>Editorial Policy:</strong> EOS Research evaluates healthspan
    interventions using the totality of available evidence, prioritizing
    systematic reviews, randomized controlled trials, and well-designed
    human studies. Editorials are educational and are not medical advice.
  </div>

</main>

</body>
</html>'''

with open("C:\\Users\\monty\\eos-research\\research\\cosmos-multivitamin-evidence.html", "w", encoding="utf-8") as f:
    f.write(output)

print(f"Written: {len(output)} chars")

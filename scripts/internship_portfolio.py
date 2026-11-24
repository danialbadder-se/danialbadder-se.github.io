"""Public internship exhibits and freelance services for the portfolio."""
from html import escape
from urllib.parse import quote

CASE_URL = '/work/ntdc-excel.html'
WORKBOOK = '/documents/NTDC-Internship-Excel-Samples.xlsx'
SCREEN = '/assets/ntdc-excel-screen.webp'
CHECKLIST = '/assets/ntdc-equipment-checklist.webp'
EMAIL = 'danialbadder@gmail.com'
PHONE = '03136951938'
TEL = 'tel:+923136951938'


def viewer_art(data, icon):
    rows = data['rows'][:3]
    selected = rows[1]
    body = []
    for row in rows:
        value = escape(row['I'])
        if row is selected:
            value = value[:-1] + '<mark>' + value[-1] + '</mark>'
        body.append(f'<tr><th scope="row">{row["row"]}</th><td>{value}</td><td>{row["J"]}</td></tr>')
    return f'''<div class="workbook-window">
      <div class="workbook-bar"><span>{icon('sheet')} Transformer worksheet</span><a href="{SCREEN}" data-lightbox="Original NTDC Excel worksheet and formula bar" target="_blank" rel="noopener">{icon('zoom')} Original screen</a></div>
      <div class="cell-bar"><b>I{selected['row']}</b><span aria-hidden="true">ƒx</span><code>{escape(selected['formulas']['I'])}</code></div>
      <table class="sample-grid" aria-label="Three original transformer rows"><thead><tr><th scope="col">Row</th><th scope="col">Description · I</th><th scope="col">Length · J</th></tr></thead><tbody>{''.join(body)}</tbody></table>
      </div>'''


def services_section(icon):
    services = [
        ('code', 'Website development', 'Business websites, personal portfolios, and Python web applications that work across screen sizes.',
         '/work/veritas.html#interface', 'Explore the VERITAS interface', 'Website project enquiry', 'Discuss a website'),
        ('sheet', 'Excel & reporting', 'Clean up your data and turn recurring reports into Excel dashboards your team can update.',
         '/work/emergency-room.html#report', 'Explore the Excel dashboard', 'Excel and reporting enquiry', 'Discuss a report'),
        ('plot', 'AI research & evaluation', 'Build a Python model prototype, compare experiments, and document what the results show.',
         '/work/caml-net.html#comparison', 'Compare CAML-Net results', 'AI research enquiry', 'Discuss research'),
    ]
    cards = []
    for symbol, name, detail, proof, proof_label, subject, action in services:
        cards.append(f'''<article class="service-card"><span class="service-symbol">{icon(symbol)}</span>
          <h3>{escape(name)}</h3><p>{escape(detail)}</p>
          <a class="service-proof" href="{proof}">{escape(proof_label)} {icon('arrow')}</a>
          <a class="service-enquiry" href="mailto:{EMAIL}?subject={quote(subject)}">{icon('mail')} {escape(action)}</a></article>''')
    return f'''<section class="services section-pad" id="services"><div class="shell">
      <div class="section-header"><div><span class="kicker rule">Freelance services</span><h2>Work with me.</h2></div><p>Choose a service to see a sample or get in touch about a project.</p></div>
      <div class="service-grid">{''.join(cards)}</div><p class="other-projects">Have another technical project in mind? <a href="#contact">Tell me about it {icon('arrow')}</a></p></div></section>'''


def study_body(data, section, image_link, picture, table, button):
    row = data['rows'][1]
    options = ''.join(f'<option value="{r["row"]}"' + (' selected' if r['row']==row['row'] else '') + f'>Row {r["row"]}</option>' for r in data['rows'])
    formula_box = f'''<div class="worksheet-inspector">
      <div class="inspector-top"><label for="internship-row">Source row</label><select id="internship-row">{options}</select></div>
      <div class="inspector-formula"><span id="internship-cell">I3</span><code id="internship-formula">{escape(row['formulas']['I'])}</code></div>
      <dl class="field-values"><div><dt>First level · K</dt><dd id="internship-level-one">{row['K']} kV</dd></div><div><dt>Second level · L</dt><dd id="internship-level-two">{row['L']} kV</dd></div><div><dt>Rating entered · N</dt><dd id="internship-rating">{row['N']}</dd></div></dl>
      <div class="formula-result" aria-live="polite"><span>Excel result</span><strong id="internship-description">{escape(row['I'])}</strong><small id="internship-length">{row['J']} characters</small></div></div>'''
    content = section('How a description is built',
        '<p>The worksheet combines two voltage fields and the entered rating into one description. A second formula measures its length against the 20-character field in the master-data template. Choose a row to see the original inputs, formula, and result.</p>' + formula_box +
        '<aside class="quality-note"><strong>A detail worth checking</strong><p>Row 2 ends in <code>250MVA</code>. Row 3 contains <code>250MVH</code>. Both descriptions are 16 characters long, so a length check passes both. I would verify the unit against the source record before changing it.</p></aside>', 'formula')
    checks = data['checklist']
    options = ''.join(f'<option value="{i}">{escape(name)}</option>' for i,name,_ in checks)
    first = ''.join('<li>'+escape(line.partition(')')[2].strip())+'</li>' for line in checks[0][2].splitlines())
    image = picture(CHECKLIST,'Original equipment checklist, rows 1 to 4','Three equipment entries rendered from the original checklist worksheet.')
    content += section('The equipment checklist','<p>I used this worksheet to see which details to check in an asset record. A transformer entry calls for its rating and manufacturer. A battery bank calls for its operating voltage and capacity. Choose one of the 17 equipment types to see the original checklist.</p>' +
        f'''<div class="check-exhibit"><div class="check-source">{image}<small>Original checklist · rows 1–4</small></div><div class="check-picker"><label for="equipment-select">Equipment type</label><select id="equipment-select">{options}</select><ol id="equipment-fields" aria-live="polite">{first}</ol></div></div>''','checklist')
    content += section('The SAP reference sheet','<p>The reference workbook links abbreviations in a master sheet to equipment names. The transformer sample uses AT for Auto Transformer and PT for Power Transformer.</p>' +
        '<details class="detail-table"><summary>View 10 original reference entries</summary>'+table(['Abbreviation','Detail'],data['reference'],'SAP reference worksheet · selected entries')+'</details>','sap')
    content += section('Download the Excel work','<p>The workbook contains the five populated transformer rows with working formulas, all 17 equipment checklist entries, and ten SAP reference entries. In Excel, change a rating in column N to see the description in column I recalculate.</p>' +
        '<div class="downloads">'+button('Download Excel sample (XLSX)',WORKBOOK,'resource','download',True)+button('Download original screen excerpt',SCREEN,'resource','download',True)+'</div>'+
        '<div class="internship-credentials">'+image_link('/assets/credential-ngc.webp','NGC internship certificate excerpt','Internship certificate')+image_link('/assets/ngc-result.webp','NTDC internship test result, 46 of 50','Internship test result')+'</div>','downloads')
    return content

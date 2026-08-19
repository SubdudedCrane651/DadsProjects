from nicegui import ui
import csv
import os
from datetime import datetime

CSV_PATH = 'DadsProjects.csv'
IMAGE_DIR = 'images'

# ------------------------------
# LOAD CSV
# ------------------------------
def load_entries():
    entries = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            file = row.get('\ufeffFile', '').strip()
            year = row.get('year', '').strip()
            occasion = row.get('occasion', '').strip()
            description = row.get('description', '').strip()

            img_path = os.path.join(IMAGE_DIR, file)
            if not os.path.exists(img_path):
                img_path = None

            entries.append({
                'file': file,
                'year': year,
                'occasion': occasion,
                'description': description,
                'image': img_path,
            })
    return entries


entries = load_entries()

# ------------------------------
# FILTER + SORT
# ------------------------------
def filtered_entries():
    term = search.value.lower().strip()

    filtered = []
    for e in entries:
        if (term in e['year'].lower() or
            term in e['occasion'].lower() or
            term in e['description'].lower()):
            filtered.append(e)

    sort_key = sort_select.value
    if sort_key == 'Year':
        filtered.sort(key=lambda x: x['year'])
    elif sort_key == 'Occasion':
        filtered.sort(key=lambda x: x['occasion'])

    return filtered


# ------------------------------
# CARD CREATION
# ------------------------------
def refresh_cards():
    card_area.clear()
    for entry in filtered_entries():
        with card_area:
            with ui.card().classes('w-96 m-4'):
                if entry['image']:
                    ui.image(entry['image']).classes('w-full')
                else:
                    ui.label(f"[Missing image: {entry['file']}]").classes('text-red-600')

                ui.label(f"📅 Year: {entry['year']}").classes('text-lg font-bold')
                ui.label(f"🎉 Occasion: {entry['occasion']}").classes('text-md')
                ui.label(f"📝 {entry['description']}").classes('text-sm mt-2')


# ------------------------------
# EXPORT TO HTML
# ------------------------------
def export_html():
    html = """
    <html>
    <head>
        <title>Dad Project Gallery</title>
        <style>
            body {
                font-family: Arial;
                padding: 20px;
                background: #f5f5f5;
                color: #000;
                transition: background 0.3s, color 0.3s;
            }
            body.dark {
                background: #1e1e1e;
                color: #e0e0e0;
            }

            header, footer {
                text-align: center;
                padding: 10px;
                background: #222;
                color: white;
            }
            body.dark header, body.dark footer {
                background: #000;
                color: #fff;
            }

            .toggle-btn {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 10px 15px;
                background: #222;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                z-index: 1100;
            }
            body.dark .toggle-btn {
                background: #555;
            }

            .search-box { text-align: center; margin-bottom: 20px; }
            .search-box input {
                width: 300px;
                padding: 8px;
                font-size: 14px;
                border-radius: 6px;
                border: 1px solid #aaa;
            }

            .sort-box { text-align:center; margin-bottom:20px; }
            .sort-box button {
                padding: 8px 12px;
                margin: 5px;
                border-radius: 6px;
                border: none;
                background: #444;
                color: white;
                cursor: pointer;
            }
            body.dark .sort-box button {
                background: #666;
            }

            .grid { display: flex; flex-wrap: wrap; gap: 20px; }

            .project {
                width: 220px;
                background: white;
                padding: 10px;
                border-radius: 10px;
                cursor: pointer;
            }
            body.dark .project {
                background: #2c2c2c;
            }

            .project img {
                width: 100%;
                height: 180px;
                object-fit: cover;
                border-radius: 8px;
            }

            .title {
                text-align: center;
                margin-top: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            /* FULLSCREEN OVERLAY */
            #fullscreen-overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0,0,0,0.95);
                justify-content: center;
                align-items: center;
                z-index: 2000;
            }

            #fullscreen-image {
                max-width: 100vw;
                max-height: 100vh;
                object-fit: contain;
                transition: transform 0.2s ease;
                transform-origin: center center;
            }
        </style>

        <script>
            function toggleDarkMode() {
                document.body.classList.toggle('dark');
            }

            function searchProjects() {
                let q = document.getElementById('search').value.toLowerCase();
                let items = document.getElementsByClassName('project');

                for (let item of items) {
                    let text = item.getAttribute('data-search');
                    item.style.display = text.includes(q) ? 'block' : 'none';
                }
            }

            function sortProjects(type) {
                let grid = document.querySelector('.grid');
                let items = Array.from(document.getElementsByClassName('project'));

                items.sort((a, b) => {
                    let A = a.getAttribute('data-sort-' + type);
                    let B = b.getAttribute('data-sort-' + type);
                    return A.localeCompare(B);
                });

                items.forEach(i => grid.appendChild(i));
            }

            /* FULLSCREEN + ZOOM */
            let zoomLevel = 1;

            function showFullscreen(src) {
                let overlay = document.getElementById('fullscreen-overlay');
                let img = document.getElementById('fullscreen-image');
                img.src = src;
                zoomLevel = 1;
                img.style.transform = "scale(1)";
                overlay.style.display = 'flex';
            }

            function hideFullscreen() {
                document.getElementById('fullscreen-overlay').style.display = 'none';
            }

            function zoomImage(event) {
                event.preventDefault();
                zoomLevel += event.deltaY * -0.001;
                zoomLevel = Math.min(Math.max(zoomLevel, 1), 5);
                document.getElementById('fullscreen-image').style.transform =
                    `scale(${zoomLevel})`;
            }

            function resetZoom() {
                zoomLevel = 1;
                document.getElementById('fullscreen-image').style.transform = "scale(1)";
            }
        </script>
    </head>

    <body>
        <button class="toggle-btn" onclick="toggleDarkMode()">Dark Mode</button>

        <header><h1>Dad Project Gallery</h1></header>

        <div class="search-box">
            <input id="search" type="text" placeholder="Search..."
                   onkeyup="searchProjects()">
        </div>

        <div class="sort-box">
            <button onclick="sortProjects('year')">Sort by Year</button>
            <button onclick="sortProjects('occasion')">Sort by Occasion</button>
        </div>

        <div class="grid">
    """

    for entry in filtered_entries():
        searchable = f"{entry['year']} {entry['occasion']} {entry['description']}".lower()

        html += f"""
        <div class="project"
             data-search="{searchable}"
             data-sort-year="{entry['year']}"
             data-sort-occasion="{entry['occasion']}">

            <img src="{entry['image']}" onclick="showFullscreen(this.src)">

            <div class="title">{entry['occasion']} ({entry['year']})</div>
            <div class="title">{entry['description']}</div>
        </div>
        """

    html += """
        </div>

        <!-- GLOBAL FULLSCREEN OVERLAY -->
        <div id="fullscreen-overlay" onclick="hideFullscreen()">
            <img id="fullscreen-image" src="" onwheel="zoomImage(event)" ondblclick="resetZoom()">
        </div>

        <footer><p>Generated by Dad Project Creator</p></footer>
    </body>
    </html>
    """

    with open("DadProjectExport.html", "w", encoding="utf-8") as f:
        f.write(html)

    ui.notify("HTML Exported: DadProjectExport.html")


# ------------------------------
# UI
# ------------------------------
ui.label('Dad Project Gallery').classes('text-3xl font-bold m-4')

with ui.row().classes('items-center m-4'):
    search = ui.input(label='Search (Year, Occasion, Description)', on_change=refresh_cards).classes('w-64')
    sort_select = ui.select(['Year', 'Occasion'], label='Sort By', on_change=refresh_cards).classes('w-40')
    dm = ui.dark_mode()   # create the dark mode controller
    dark_mode = ui.switch('Dark Mode', value=False, on_change=lambda e: dm.toggle())

    ui.button('Export to HTML', on_click=export_html).classes('ml-4')

card_area = ui.row().classes('flex flex-wrap')
refresh_cards()

ui.run()

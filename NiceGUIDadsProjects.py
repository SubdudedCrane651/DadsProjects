from nicegui import ui
import csv
import os

CSV_PATH = 'DadsProjects.csv'
IMAGE_DIR = 'images'

def load_entries():
    entries = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            file = row.get('\ufeffFile', '').strip()          # includes extension
            year = row.get('year', '').strip()
            occasion = row.get('occasion', '').strip()
            description = row.get('description', '').strip()

            # Build full image path directly
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


def create_entry_card(entry):
    with ui.card().classes('w-96 m-4'):
        if entry['image']:
            ui.image(entry['image']).classes('w-full')
        else:
            ui.label(f"[Missing image: {entry['file']}]").classes('text-red-600')

        ui.label(f"📅 Year: {entry['year']}").classes('text-lg font-bold')
        ui.label(f"🎉 Occasion: {entry['occasion']}").classes('text-md')
        ui.label(f"📝 {entry['description']}").classes('text-sm mt-2')


ui.label('Dad Project Gallery').classes('text-3xl font-bold m-4')

entries = load_entries()

with ui.row().classes('flex flex-wrap'):
    for entry in entries:
        create_entry_card(entry)

ui.run()

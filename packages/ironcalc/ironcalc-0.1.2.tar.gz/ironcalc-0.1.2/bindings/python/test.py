import ironcalc as ic

model = ic.load_from_xlsx("example.xlsx", "en", "UTC")
p=model.get_worksheets_properties()
assert p[4].color == '#C55911'

sheet_names = ['Sheet1', 'Second', 'Sheet4', 'shared', 'Table', 'Sheet2', 'Created fourth', 'Frozen', 'Split', 'Hidden']
assert sheet_names == [ws.name for ws in p]

style = model.get_cell_style(0, 2, 12)
print(style.font.color)
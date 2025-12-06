import os

path1 = r"g:\منطقة الحرة السويس - 2025\تموينات السفن\1.html"
path2 = r"g:\منطقة الحرة السويس - 2025\تموينات السفن\2.html"
output_path = r"g:\منطقة الحرة السويس - 2025\تموينات السفن\merged.html"

# Read both files
with open(path1, 'r', encoding='utf-8') as f:
    content1 = f.read()
    
with open(path2, 'r', encoding='utf-8') as f:
    content2 = f.read()

# Find Chapter 9 in file1 (starts with <!-- الباب التاسع and ends before </div>\n\n    </div>)
ch9_start_marker = '<!-- الباب التاسع'
ch9_start = content1.find(ch9_start_marker)

# Find the end of Chapter 9 (just before the closing main-container div and script)
# Look for the pattern that ends chapter 9 content
ch9_end_marker = '</div>\r\n        </div>\r\n\r\n    </div>\r\n\r\n    <script>'
ch9_end = content1.find(ch9_end_marker)

if ch9_end == -1:
    # Try without carriage return
    ch9_end_marker = '</div>\n        </div>\n\n    </div>\n\n    <script>'
    ch9_end = content1.find(ch9_end_marker)

if ch9_start != -1 and ch9_end != -1:
    # Extract Chapter 9 content - from the start marker to just before '</div>\n        </div>'
    # We need to include the closing div of Chapter 9 content section
    chapter9 = content1[ch9_start:ch9_end + len('</div>\r\n        </div>\r\n\r\n')]
    if '</div>\r\n        </div>\r\n\r\n' not in chapter9:
        chapter9 = content1[ch9_start:ch9_end + len('</div>\n        </div>\n\n')]
    print(f"Found Chapter 9: {len(chapter9)} chars")
else:
    print(f"Chapter 9 not found. Start: {ch9_start}, End: {ch9_end}")
    chapter9 = ""

# Find TOC section in file2 to add Chapter 9 link
toc_ch8_link = '<a href="#chapter8" class="text-blue-600 hover:text-blue-800 font-bold">الباب الثامن: تحليل'
toc_ch8_end = '</div>\r\n            </div>\r\n        </div>\r\n\r\n        <!-- الباب الأول'

# New TOC entry for Chapter 9
ch9_toc = '''                <div class="bg-white p-4 rounded-lg shadow border-2 border-green-500">
                    <a href="#chapter9" class="text-green-600 hover:text-green-800 font-bold">الباب التاسع: مشروع المنصة الرقمية اللوجستية (ShipPay)</a>
                </div>
'''

# Find where to insert TOC entry in content2
toc_insert_marker = '</div>\r\n            </div>\r\n        </div>\r\n\r\n        <!-- الباب الأول'
if toc_insert_marker not in content2:
    toc_insert_marker = '</div>\n            </div>\n        </div>\n\n        <!-- الباب الأول'

toc_pos = content2.find(toc_insert_marker)
if toc_pos != -1:
    # Insert TOC entry
    content2 = content2[:toc_pos] + '</div>\r\n' + ch9_toc + '            </div>\r\n        </div>\r\n\r\n        <!-- الباب الأول' + content2[toc_pos + len(toc_insert_marker):]
    print("TOC entry added")
else:
    print(f"TOC insertion point not found")

# Find where to insert Chapter 9 content (before </div>\n\n    <script>)
ch9_insert_marker = '    </div>\r\n\r\n    <script>'
if ch9_insert_marker not in content2:
    ch9_insert_marker = '    </div>\n\n    <script>'

ch9_insert_pos = content2.find(ch9_insert_marker)
if ch9_insert_pos != -1 and chapter9:
    # Insert Chapter 9 before the closing main-container div
    content2 = content2[:ch9_insert_pos] + '\r\n' + chapter9 + content2[ch9_insert_pos:]
    print("Chapter 9 content inserted")
else:
    print(f"Chapter 9 insertion point not found: {ch9_insert_pos}")

# Write output
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content2)
    
print(f"Merged file written: {len(content2)} chars")

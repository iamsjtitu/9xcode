from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
from datetime import datetime
import uuid
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def create_slug(title):
    import re
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')

learning_articles = [
    # TALLY TUTORIALS
    ("Create Company in Tally", "Complete guide to create new company in Tally ERP", ["tally", "company", "setup"], ["windows"], "beginner", [
        {"title": "Open Tally", "description": "Launch Tally application", "code": "1. Click Tally icon on desktop\n2. Or Go to Start > Programs > Tally\n3. Wait for Tally Gateway to load\n4. Press Alt+F3 to create company\n5. Or click on 'Create Company' option", "language": "bash"},
        {"title": "Enter Company Details", "description": "Fill company information", "code": "Company Name: ABC Traders\nMailing Name: ABC Traders\nAddress: 123, Main Street\nCity: New Delhi\nState: Delhi\nPIN Code: 110001\nCountry: India\nTelephone: 011-12345678\nEmail: info@abctraders.com", "language": "bash"},
        {"title": "Set Financial Year", "description": "Configure accounting period", "code": "Financial Year From: 01-04-2024\nBooks Beginning From: 01-04-2024\n\nNote: Financial year in India runs from April to March", "language": "bash"},
        {"title": "Security and Password", "description": "Set company password (optional)", "code": "Use Security Control: Yes (if needed)\nPassword: [Set strong password]\nConfirm Password: [Re-enter password]\n\nNote: Keep password secure for data protection", "language": "bash"}
    ]),
    
    ("Create Ledger in Tally", "Step-by-step ledger creation in Tally", ["tally", "ledger", "accounts"], ["windows"], "beginner", [
        {"title": "Access Ledger Creation", "description": "Navigate to ledger screen", "code": "Method 1: Press Alt+G (Go To) > Create Master > Ledger\nMethod 2: Gateway > Accounts Info > Ledgers > Create\nMethod 3: Press F11 (Features) > F1 (Accounting Features) > Create Ledger", "language": "bash"},
        {"title": "Enter Ledger Details", "description": "Fill ledger information", "code": "Name: HDFC Bank\nAlias: (Optional)\nUnder: Bank Accounts (Select group)\nInventory Values: Not Applicable\nType of Ledger: Not Applicable", "language": "bash"},
        {"title": "Enter Opening Balance", "description": "Set initial balance", "code": "Opening Balance: ₹50,000\nDebit/Credit: Dr (for bank account)\nAs on: 01-04-2024\n\nNote: Debit for Assets, Credit for Liabilities", "language": "bash"}
    ]),
    
    ("Tally Accounting Heads and Groups", "Understanding groups and ledger classification", ["tally", "groups", "accounting-heads"], ["windows"], "intermediate", [
        {"title": "Primary Groups", "description": "Main accounting groups in Tally", "code": "ASSETS:\n- Current Assets\n- Fixed Assets\n- Investments\n- Loans & Advances\n\nLIABILITIES:\n- Current Liabilities\n- Loans (Liability)\n- Capital Account\n- Reserves & Surplus\n\nINCOME:\n- Direct Income\n- Indirect Income\n- Sales Accounts\n\nEXPENSES:\n- Direct Expenses\n- Indirect Expenses\n- Purchase Accounts", "language": "bash"},
        {"title": "Sub-Groups Under Current Assets", "description": "Ledgers under Current Assets", "code": "Bank Accounts:\n- HDFC Bank\n- SBI Bank\n- Axis Bank\n\nCash-in-Hand:\n- Petty Cash\n- Main Cash\n\nSundry Debtors:\n- Customer A\n- Customer B\n\nStock-in-Hand:\n- Raw Materials\n- Finished Goods", "language": "bash"},
        {"title": "Sub-Groups Under Current Liabilities", "description": "Ledgers under Current Liabilities", "code": "Sundry Creditors:\n- Supplier A\n- Supplier B\n\nDuties & Taxes:\n- GST Payable\n- TDS Payable\n- Professional Tax\n\nProvisions:\n- Provision for Tax\n- Provision for Expenses", "language": "bash"}
    ]),
    
    ("Pass Journal Entry in Tally", "Record journal vouchers in Tally", ["tally", "journal", "voucher"], ["windows"], "beginner", [
        {"title": "Open Journal Voucher", "description": "Access journal entry screen", "code": "Gateway > Vouchers > F7 (Journal)\nOr press F7 directly from any screen", "language": "bash"},
        {"title": "Example: Cash Purchase", "description": "Record cash purchase transaction", "code": "Date: 15-04-2024\n\nParticulars:\nPurchase A/c           Dr    ₹10,000\n  To Cash A/c                   ₹10,000\n\n(Being goods purchased for cash)\n\nNarration: Purchased goods from XYZ Traders", "language": "bash"},
        {"title": "Example: Salary Payment", "description": "Record salary expense", "code": "Date: 30-04-2024\n\nParticulars:\nSalary A/c            Dr    ₹50,000\n  To Bank A/c                   ₹50,000\n\n(Being salary paid for April 2024)\n\nNarration: April month salary payment", "language": "bash"}
    ]),
    
    ("Pass Payment Voucher in Tally", "Record payment transactions", ["tally", "payment", "voucher"], ["windows"], "beginner", [
        {"title": "Open Payment Voucher", "description": "Access payment screen", "code": "Gateway > Vouchers > F5 (Payment)\nOr press F5 from any screen\n\nPayment voucher is used when cash/bank goes out", "language": "bash"},
        {"title": "Cash Payment Example", "description": "Record cash payment", "code": "Date: 10-04-2024\nAccount: Cash\n\nParticulars:\nRent A/c              Dr    ₹15,000\n\nNarration: Paid office rent for April 2024\n\nPress Enter to save", "language": "bash"}
    ]),
    
    ("Pass Receipt Voucher in Tally", "Record receipt transactions", ["tally", "receipt", "voucher"], ["windows"], "beginner", [
        {"title": "Open Receipt Voucher", "description": "Access receipt screen", "code": "Gateway > Vouchers > F6 (Receipt)\nOr press F6 from any screen\n\nReceipt voucher is used when cash/bank comes in", "language": "bash"},
        {"title": "Cash Receipt Example", "description": "Record cash receipt", "code": "Date: 12-04-2024\nAccount: Cash\n\nParticulars:\nSales A/c             Cr    ₹25,000\n\nNarration: Cash sales for the day\n\nPress Enter to save", "language": "bash"}
    ]),
    
    ("Configure GST in Tally", "Set up Goods and Services Tax", ["tally", "gst", "tax"], ["windows"], "intermediate", [
        {"title": "Enable GST", "description": "Activate GST feature", "code": "1. Press F11 (Company Features)\n2. Press F3 (Statutory & Taxation)\n3. Enable GST: Yes\n4. Set GSTIN: [Enter 15-digit GSTIN]\n5. Enable GST Classification: Yes\n6. Press Ctrl+A to accept", "language": "bash"},
        {"title": "Create GST Ledgers", "description": "Set up tax ledgers", "code": "Create these ledgers:\n\n1. CGST (Central GST)\n   Under: Duties & Taxes\n   Type: GST\n   Tax Type: CGST\n\n2. SGST (State GST)\n   Under: Duties & Taxes\n   Type: GST\n   Tax Type: SGST\n\n3. IGST (Integrated GST)\n   Under: Duties & Taxes\n   Type: GST\n   Tax Type: IGST", "language": "bash"}
    ]),
    
    # BUSY ACCOUNTING
    ("Create Company in Busy", "Set up new company in Busy accounting", ["busy", "company", "setup"], ["windows"], "beginner", [
        {"title": "Start Busy", "description": "Launch Busy software", "code": "1. Open Busy from desktop\n2. Click 'Create Company'\n3. Or Go to Master > Company > Create", "language": "bash"},
        {"title": "Company Information", "description": "Enter company details", "code": "Company Name: XYZ Enterprises\nPrint Name: XYZ Enterprises\nAddress: Complete address\nCity: [City name]\nState: [Select state]\nPIN: [Postal code]\nPhone: [Contact number]\nEmail: [Email address]\nGSTIN: [GST number if registered]", "language": "bash"}
    ]),
    
    ("Create Master Entries in Busy", "Set up accounts and inventory masters", ["busy", "masters", "accounts"], ["windows"], "beginner", [
        {"title": "Account Master", "description": "Create account ledgers", "code": "Master > Account Master > Create\n\nAccount Name: ICICI Bank\nGroup: Bank\nOpening Balance: ₹1,00,000 Dr\nAs on Date: 01-04-2024", "language": "bash"},
        {"title": "Item Master", "description": "Create product items", "code": "Master > Item Master > Create\n\nItem Name: Product A\nItem Code: PA001\nUnit: Pcs\nRate: ₹500\nGST Rate: 18%\nOpening Stock: 100 Pcs", "language": "bash"}
    ]),
    
    # MICROSOFT EXCEL
    ("Essential Excel Formulas", "Most used Excel formulas and functions", ["excel", "formulas", "functions"], ["windows", "mac"], "beginner", [
        {"title": "SUM Function", "description": "Add numbers in Excel", "code": "=SUM(A1:A10)  → Adds all values from A1 to A10\n=SUM(10, 20, 30)  → Returns 60\n=SUM(A1:A5, C1:C5)  → Adds multiple ranges", "language": "excel"},
        {"title": "AVERAGE Function", "description": "Calculate average", "code": "=AVERAGE(A1:A10)  → Average of range\n=AVERAGE(10, 20, 30)  → Returns 20", "language": "excel"},
        {"title": "COUNT and COUNTA", "description": "Count cells", "code": "=COUNT(A1:A10)  → Counts numeric values\n=COUNTA(A1:A10)  → Counts non-empty cells\n=COUNTBLANK(A1:A10)  → Counts empty cells", "language": "excel"},
        {"title": "IF Function", "description": "Conditional logic", "code": "=IF(A1>50, \"Pass\", \"Fail\")\n→ If A1 greater than 50, show Pass, else Fail\n\n=IF(B2=\"Yes\", 100, 0)\n→ If B2 is Yes, return 100, else 0", "language": "excel"}
    ]),
    
    ("Advanced Excel Formulas", "VLOOKUP, HLOOKUP, INDEX-MATCH", ["excel", "vlookup", "advanced"], ["windows", "mac"], "intermediate", [
        {"title": "VLOOKUP Function", "description": "Vertical lookup", "code": "=VLOOKUP(A2, B2:D10, 3, FALSE)\n\nParameters:\nA2: Lookup value\nB2:D10: Table array\n3: Column number to return\nFALSE: Exact match\n\nExample:\n=VLOOKUP(\"Emp001\", A2:C100, 2, FALSE)\n→ Find Emp001 and return value from 2nd column", "language": "excel"},
        {"title": "INDEX-MATCH Function", "description": "More flexible than VLOOKUP", "code": "=INDEX(C2:C100, MATCH(A2, B2:B100, 0))\n\nAdvantages:\n- Can lookup left or right\n- Faster than VLOOKUP\n- More flexible\n\nExample:\n=INDEX(SalaryRange, MATCH(EmpID, EmpIDRange, 0))", "language": "excel"},
        {"title": "SUMIF and SUMIFS", "description": "Conditional sum", "code": "=SUMIF(A2:A10, \"Apple\", B2:B10)\n→ Sum B2:B10 where A2:A10 is \"Apple\"\n\n=SUMIFS(D2:D100, A2:A100, \"Delhi\", B2:B100, \">1000\")\n→ Sum with multiple conditions", "language": "excel"}
    ]),
    
    ("Excel Data Analysis Tools", "PivotTables, charts, and data tools", ["excel", "pivot-table", "analysis"], ["windows", "mac"], "intermediate", [
        {"title": "Create PivotTable", "description": "Analyze data with PivotTable", "code": "1. Select data range\n2. Go to Insert > PivotTable\n3. Choose destination (New sheet)\n4. Drag fields:\n   - Rows: Category\n   - Columns: Month\n   - Values: Sum of Sales\n5. Format and customize", "language": "bash"},
        {"title": "Data Validation", "description": "Create dropdown lists", "code": "1. Select cell(s)\n2. Go to Data > Data Validation\n3. Allow: List\n4. Source: Item1,Item2,Item3\n   Or Source: =A1:A10 (range)\n5. Click OK", "language": "bash"}
    ]),
    
    ("Excel Keyboard Shortcuts", "Speed up Excel work with shortcuts", ["excel", "shortcuts", "productivity"], ["windows", "mac"], "beginner", [
        {"title": "Navigation Shortcuts", "description": "Move around Excel quickly", "code": "Ctrl + Home  → Go to A1\nCtrl + End  → Go to last used cell\nCtrl + Arrow  → Jump to edge of data\nCtrl + Page Up/Down  → Switch sheets\nAlt + Page Up/Down  → Move screen left/right", "language": "bash"},
        {"title": "Editing Shortcuts", "description": "Edit cells faster", "code": "F2  → Edit cell\nCtrl + D  → Fill down\nCtrl + R  → Fill right\nCtrl + ;  → Insert current date\nCtrl + Shift + ;  → Insert current time\nAlt + Enter  → New line in cell", "language": "bash"}
    ]),
    
    ("Excel Conditional Formatting", "Highlight data based on rules", ["excel", "formatting", "conditional"], ["windows", "mac"], "beginner", [
        {"title": "Apply Conditional Formatting", "description": "Highlight cells automatically", "code": "1. Select range\n2. Home > Conditional Formatting\n3. Choose rule type:\n   - Highlight Cells Rules\n   - Top/Bottom Rules\n   - Data Bars\n   - Color Scales\n   - Icon Sets\n4. Set conditions\n5. Choose format\n6. Click OK", "language": "bash"}
    ]),
    
    # MICROSOFT WORD
    ("Microsoft Word Formatting Basics", "Format documents professionally", ["word", "formatting", "documents"], ["windows", "mac"], "beginner", [
        {"title": "Text Formatting", "description": "Format text appearance", "code": "Bold: Ctrl + B\nItalic: Ctrl + I\nUnderline: Ctrl + U\n\nFont Size: Ctrl + Shift + >\nFont Size Decrease: Ctrl + Shift + <\n\nHighlight: Alt + H + I\nFont Color: Alt + H + FC", "language": "bash"},
        {"title": "Paragraph Formatting", "description": "Format paragraphs", "code": "Alignment:\nLeft: Ctrl + L\nCenter: Ctrl + E\nRight: Ctrl + R\nJustify: Ctrl + J\n\nLine Spacing:\nSingle: Ctrl + 1\n1.5 lines: Ctrl + 5\nDouble: Ctrl + 2", "language": "bash"}
    ]),
    
    ("Create Table of Contents in Word", "Auto-generate TOC for documents", ["word", "toc", "table-of-contents"], ["windows", "mac"], "intermediate", [
        {"title": "Apply Heading Styles", "description": "Use built-in heading styles", "code": "1. Select chapter/section title\n2. Home tab > Styles\n3. Click Heading 1 (for main headings)\n4. Click Heading 2 (for sub-headings)\n5. Click Heading 3 (for sub-sub-headings)\n6. Repeat for all headings", "language": "bash"},
        {"title": "Insert Table of Contents", "description": "Generate automatic TOC", "code": "1. Place cursor where TOC should appear\n2. References tab > Table of Contents\n3. Choose style (Automatic Table 1 or 2)\n4. TOC is created automatically\n\nUpdate TOC:\nRight-click TOC > Update Field > Update entire table", "language": "bash"}
    ]),
    
    ("Mail Merge in Word", "Create bulk letters and labels", ["word", "mail-merge", "automation"], ["windows", "mac"], "intermediate", [
        {"title": "Start Mail Merge", "description": "Set up mail merge document", "code": "1. Mailings tab > Start Mail Merge\n2. Select document type:\n   - Letters\n   - Envelopes\n   - Labels\n   - Email Messages\n3. Select Recipients > Use Existing List\n4. Browse to Excel file with data", "language": "bash"},
        {"title": "Insert Merge Fields", "description": "Add dynamic content", "code": "1. Click where field should go\n2. Mailings > Insert Merge Field\n3. Select field (Name, Address, etc.)\n4. Fields appear as: «Name»\n5. Preview Results to check\n6. Finish & Merge > Print/Email Documents", "language": "bash"}
    ]),
    
    # MICROSOFT POWERPOINT
    ("Create Professional PowerPoint Presentation", "Design engaging presentations", ["powerpoint", "presentation", "slides"], ["windows", "mac"], "beginner", [
        {"title": "Choose Design Theme", "description": "Apply professional theme", "code": "1. Design tab > Themes\n2. Choose built-in theme\n3. Or browse for custom templates\n4. Customize colors: Design > Variants\n5. Customize fonts: Design > Variants > Fonts", "language": "bash"},
        {"title": "Add New Slides", "description": "Insert different slide layouts", "code": "Home > New Slide\n\nLayouts:\n- Title Slide (for cover)\n- Title and Content (most common)\n- Section Header (for sections)\n- Two Content (for comparisons)\n- Blank (for custom design)\n\nShortcut: Ctrl + M", "language": "bash"}
    ]),
    
    ("PowerPoint Animations and Transitions", "Add motion to presentations", ["powerpoint", "animations", "effects"], ["windows", "mac"], "intermediate", [
        {"title": "Add Slide Transitions", "description": "Animate between slides", "code": "1. Select slide(s)\n2. Transitions tab\n3. Choose transition:\n   - Fade\n   - Push\n   - Wipe\n   - Morph (smooth)\n4. Set duration (0.5-1 sec recommended)\n5. Apply to All (optional)", "language": "bash"},
        {"title": "Add Object Animations", "description": "Animate text and objects", "code": "1. Select object/text\n2. Animations tab > Add Animation\n3. Choose effect:\n   Entrance: Appear, Fade, Fly In\n   Emphasis: Pulse, Grow\n   Exit: Disappear, Fade Out\n4. Set timing: On Click / With Previous / After Previous\n5. Adjust duration and delay", "language": "bash"}
    ]),
    
    ("PowerPoint Master Slides", "Create consistent presentation design", ["powerpoint", "master-slides", "templates"], ["windows", "mac"], "advanced", [
        {"title": "Access Slide Master", "description": "Edit master layouts", "code": "1. View tab > Slide Master\n2. Top slide = Master Slide (affects all)\n3. Below = Individual layouts\n4. Edit:\n   - Fonts\n   - Colors\n   - Logo placement\n   - Footer\n5. Close Master View when done", "language": "bash"}
    ]),
    
    # ADOBE PHOTOSHOP
    ("Adobe Photoshop Basics", "Essential Photoshop tools and techniques", ["photoshop", "basics", "tools"], ["windows", "mac"], "beginner", [
        {"title": "Create New Document", "description": "Start new Photoshop project", "code": "1. File > New (Ctrl + N)\n2. Set dimensions:\n   Web: 1920x1080 px\n   Print: A4 (210x297 mm)\n   Social: 1080x1080 px (Instagram)\n3. Resolution: 72 ppi (web), 300 ppi (print)\n4. Color Mode: RGB (web), CMYK (print)\n5. Click Create", "language": "bash"},
        {"title": "Essential Tools", "description": "Main Photoshop tools", "code": "V - Move Tool\nM - Marquee Selection\nL - Lasso Tool\nW - Magic Wand\nC - Crop Tool\nJ - Healing Brush\nS - Clone Stamp\nE - Eraser\nG - Gradient\nT - Text Tool\nB - Brush\nP - Pen Tool\nH - Hand Tool (pan)\nZ - Zoom Tool", "language": "bash"}
    ]),
    
    ("Remove Background in Photoshop", "Extract objects from background", ["photoshop", "background-removal", "masking"], ["windows", "mac"], "intermediate", [
        {"title": "Quick Selection Method", "description": "Use Select Subject", "code": "1. Open image\n2. Select > Subject (AI-powered)\n3. Or use Quick Selection Tool (W)\n4. Refine edge if needed:\n   Select > Select and Mask\n5. Output to: New Layer with Mask\n6. Delete background layer", "language": "bash"},
        {"title": "Pen Tool Method", "description": "Precise selection", "code": "1. Select Pen Tool (P)\n2. Click around object to create path\n3. Click and drag for curves\n4. Close path by clicking start point\n5. Right-click > Make Selection\n6. Feather: 0.5-1 pixel\n7. Layer > Layer Mask > Reveal Selection", "language": "bash"}
    ]),
    
    ("Photoshop Layers and Masks", "Master layers for non-destructive editing", ["photoshop", "layers", "masks"], ["windows", "mac"], "intermediate", [
        {"title": "Create and Manage Layers", "description": "Work with layers", "code": "New Layer: Ctrl + Shift + N\nDuplicate Layer: Ctrl + J\nMerge Down: Ctrl + E\nFlatten Image: Layer > Flatten Image\n\nLayer Opacity: Select layer, adjust opacity slider\nBlending Modes: Normal, Multiply, Screen, Overlay", "language": "bash"},
        {"title": "Layer Masks", "description": "Non-destructive editing", "code": "1. Select layer\n2. Click 'Add Layer Mask' button\n3. Paint with:\n   Black = Hide\n   White = Reveal\n   Gray = Partial transparency\n4. Brush tool (B) for painting mask", "language": "bash"}
    ]),
    
    ("Color Correction in Photoshop", "Adjust colors and tones", ["photoshop", "color-correction", "adjustment"], ["windows", "mac"], "intermediate", [
        {"title": "Levels Adjustment", "description": "Fix exposure and contrast", "code": "1. Image > Adjustments > Levels (Ctrl + L)\n2. Adjust histogram sliders:\n   Left: Shadows (blacks)\n   Middle: Midtones\n   Right: Highlights (whites)\n3. Use eyedroppers for white/gray/black balance\n4. Click OK", "language": "bash"},
        {"title": "Curves Adjustment", "description": "Precise tonal control", "code": "1. Image > Adjustments > Curves (Ctrl + M)\n2. Create points on curve\n3. Drag up: Brighten\n   Drag down: Darken\n4. S-curve: Increase contrast\n5. Adjust individual RGB channels", "language": "bash"}
    ]),
    
    ("Photoshop Text Effects", "Create stunning text designs", ["photoshop", "text", "typography"], ["windows", "mac"], "beginner", [
        {"title": "Add Text", "description": "Create text layer", "code": "1. Select Text Tool (T)\n2. Click on canvas\n3. Type text\n4. Format:\n   Font: Top toolbar\n   Size: Top toolbar\n   Color: Click color swatch\n5. Commit: Ctrl + Enter", "language": "bash"},
        {"title": "Apply Layer Styles", "description": "Add text effects", "code": "1. Select text layer\n2. Layer > Layer Style > Blending Options\n3. Check effects:\n   - Drop Shadow\n   - Outer Glow\n   - Bevel & Emboss\n   - Gradient Overlay\n   - Stroke\n4. Adjust settings\n5. Click OK", "language": "bash"}
    ]),
]

async def seed_learning():
    print("🎓 Seeding Learning Category...\n")
    
    articles_to_add = []
    
    for article in learning_articles:
        title, description, tags, os_list, difficulty, steps = article
        
        snippet = {
            'id': str(uuid.uuid4()),
            'title': title,
            'slug': create_slug(title),
            'description': description,
            'category': 'learning',
            'os': os_list,
            'difficulty': difficulty,
            'views': random.randint(500, 25000),
            'likes': random.randint(20, 600),
            'author': 'Admin',
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
            'tags': tags,
            'steps': steps,
        }
        
        articles_to_add.append(snippet)
    
    # Insert only learning articles
    result = await db.code_snippets.insert_many(articles_to_add)
    
    print(f"✅ Added {len(result.inserted_ids)} Learning articles!\n")
    print("📚 Learning Subcategories:")
    print(f"   • Tally: 7 tutorials")
    print(f"   • Busy: 2 tutorials")
    print(f"   • Excel: 5 tutorials")
    print(f"   • Word: 3 tutorials")
    print(f"   • PowerPoint: 3 tutorials")
    print(f"   • Photoshop: 5 tutorials")
    print(f"\n📊 Total Learning Articles: {len(articles_to_add)}")
    
    # Get total count
    total = await db.code_snippets.count_documents({})
    print(f"📈 Grand Total Articles: {total}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_learning())

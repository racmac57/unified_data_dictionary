# ⚡ TextExpander Workflows

**Quick reference for TextExpander snippets used in the Unified Data Dictionary project**

---

## 📋 **Available Snippets**

| Abbreviation | Purpose | Category |
|--------------|---------|----------|
| `gdoc` | Update docs + Git commit/push | Documentation |
| `glog` | Generate chatlog filename | Chatlogs |

---

## 📝 **Snippet 1: `gdoc` - Documentation Update & Git Workflow**

### **Abbreviation**: `gdoc`
### **Group**: Uses `'g` prefix

### **Content**:
```
Make changes to the README, CHANGELOG, and relevant documentation files to reflect recent updates.

Then commit and push:
• git add -A
• git commit -m "docs: [descriptive message]" with detailed body
• git push

Provide a summary of changes made.
```

### **Use Case**:
- After implementing new features
- After making significant changes
- When documentation needs to be updated
- When you want AI to handle the full Git workflow

### **What It Does**:
1. ✅ AI updates README.md with latest info
2. ✅ AI updates CHANGELOG.md with version entry
3. ✅ AI updates other relevant documentation
4. ✅ AI stages all changes (`git add -A`)
5. ✅ AI creates commit with conventional format
6. ✅ AI pushes to GitHub (`git push`)
7. ✅ AI provides summary of changes

### **Example Usage**:
```
You: gdoc [press space]

AI sees:
"Make changes to the README, CHANGELOG, and relevant documentation 
files to reflect recent updates.

Then commit and push:
• git add -A
• git commit -m "docs: [descriptive message]" with detailed body
• git push

Provide a summary of changes made."

AI: [Updates files, commits, pushes, provides summary]
```

---

## 💬 **Snippet 2: `glog` - Chatlog Filename Generator**

### **Abbreviation**: `glog`
### **Group**: Uses `'g` prefix

### **Content**:
```
I'm preparing to export this chat. Please generate a descriptive filename that summarizes the main topic or task of this conversation.

Requirements:
• 4-8 words
• Title Case (capitalize major words)
• Replace spaces with underscores
• Include .md extension
• No dates or special characters

Output only the filename, nothing else.

After export, I'll process it using: scripts\quick_process_chatlog.bat
```

### **Use Case**:
- At the end of an AI conversation
- When you want to export and save the chat
- Need a consistent, descriptive filename
- Want to process the chatlog automatically

### **What It Does**:
1. ✅ AI generates descriptive filename
2. ✅ Follows naming convention (4-8 words, Title Case, underscores)
3. ✅ Includes .md extension
4. ✅ No dates (Git tracks that)
5. ✅ Ready to use with automation scripts

### **Example Usage**:
```
You: glog [press space]

AI sees:
"I'm preparing to export this chat. Please generate a descriptive 
filename that summarizes the main topic or task of this conversation.
..."

AI responds:
"Unified_Dictionary_Setup_Complete.md"

You:
1. Export chat with that filename
2. Drag & drop onto scripts\quick_process_chatlog.bat
3. Done! (auto-saved to raw/, chunked to chunked/)
```

### **Filename Examples**:
- `CLI_Implementation_And_Git_Workflow.md`
- `Directory_Structure_Cleanup.md`
- `Automated_Chatlog_Processing_Setup.md`
- `CAD_RMS_Schema_Mapping_Discussion.md`
- `Python_Package_Configuration.md`

---

## 🚀 **Complete Chatlog Workflow**

### **Traditional Way** (7 steps):
1. Ask AI for filename
2. Export chat
3. Rename file
4. Navigate to docs folder
5. Open DOpus
6. Run chunker scripts
7. Monitor output and copy files

### **With TextExpander** (2 steps):
1. Type `glog` → AI gives filename → Export
2. Drag file onto `scripts\quick_process_chatlog.bat`

**Time saved**: ~5 minutes per chatlog! ⏱️

---

## 📁 **File Locations**

### **Chatlogs**:
```
docs/chatlogs/
├── raw/                          ← Original exports
├── chunked/                      ← Processed versions
└── README.md                     ← Full workflow documentation
```

### **Automation Scripts**:
```
scripts/
├── process_chatlog.bat           ← Full automation
├── quick_process_chatlog.bat     ← Drag & drop (RECOMMENDED)
└── CREATE_STRUCTURE.bat          ← Project setup
```

---

## 🎯 **Quick Reference**

### **Update Documentation**:
```
Type: gdoc
Result: AI updates docs, commits, pushes to GitHub
```

### **Export Chatlog**:
```
Type: glog
Result: AI gives filename
Action: Export → Drag to quick_process_chatlog.bat
```

---

## 💡 **Tips & Best Practices**

### **For `gdoc`**:
- Use after implementing features
- Use when multiple docs need updating
- Ensures consistent commit messages
- AI handles all Git operations

### **For `glog`**:
- Use at natural conversation endpoints
- Export early and often (don't wait)
- Descriptive names help future searches
- Raw versions are your source of truth

### **General**:
- Both snippets use `'g` prefix for consistency
- Can be combined in same conversation
- AI understands the automation context
- Scripts handle all file management

---

## 🔧 **Customization**

### **Adding More Snippets**:

Use the same pattern:

**Format**: `g[action]`

**Examples**:
- `gtest` → Run tests and commit if passing
- `gbuild` → Build project and tag release
- `gschema` → Update schemas and validate
- `gmap` → Update field mappings

### **Creating Your Own**:

**Template**:
```
[Clear instruction for AI]

Then [automation steps]:
• [Step 1]
• [Step 2]
• [Step 3]

[What to output/provide]
```

---

## 📊 **Statistics**

**Time Saved Per Use**:
- `gdoc`: ~3 minutes (manual doc updates + Git commands)
- `glog`: ~5 minutes (naming + manual chunking workflow)

**Typical Usage**:
- `gdoc`: 2-3 times per day
- `glog`: 1-2 times per day

**Weekly Time Saved**: ~45-60 minutes ⏱️

---

## 🔗 **Related Documentation**

- **Chatlog Workflow**: `docs/chatlogs/README.md`
- **Project Setup**: `docs/SETUP_COMPLETE.md`
- **Implementation Plan**: `docs/IMPLEMENTATION_ROADMAP.md`
- **Git Workflow**: `CHANGELOG.md`

---

## ❓ **Troubleshooting**

### **Snippet not expanding?**
- Check TextExpander is running
- Verify abbreviation is correct (`gdoc` not `gDOC`)
- Ensure group prefix `'g` is configured

### **AI not following instructions?**
- Copy snippet manually to verify content
- Check for typos in snippet
- Ensure AI has context of project

### **Scripts not working?**
- Verify paths in scripts match your system
- Check chunker exists at `C:\_chunker\opus\`
- Ensure file permissions allow execution

---

## 📝 **TextExpander Setup**

### **Group Configuration**:
- **Group Name**: Git & Docs
- **Prefix**: `'g` (apostrophe + g)
- **Case Sensitive**: No
- **Expand in**: All applications

### **Snippet Settings**:
- **Abbreviation**: As listed above
- **Content**: Copy from this document
- **Format**: Plain Text
- **Cursor Position**: N/A (full automation)

---

## 🎨 **Future Enhancements**

### **Potential Additional Snippets**:
1. `gextract` - Extract schemas from repos
2. `gvalidate` - Run validation suite
3. `grelease` - Create version release
4. `gbackup` - Backup critical files
5. `gsync` - Sync with other repos

### **Workflow Improvements**:
1. Auto-commit chatlogs to Git
2. Generate summary from chunked files
3. Add to knowledge base automatically
4. Create index of all chatlogs

---

**Last Updated**: December 17, 2025  
**Version**: 1.0  
**Author**: R. A. Carucci


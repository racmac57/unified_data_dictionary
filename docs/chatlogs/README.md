# 💬 Chatlogs Directory

This directory stores conversation exports from AI assistants (Claude, ChatGPT, etc.) related to the Unified Data Dictionary project.

---

## 📁 Structure

```
chatlogs/
├── raw/                    ← Original exported chat files
├── chunked/                ← Processed/chunked versions
└── README.md              ← This file
```

---

## 🚀 Quick Workflow

### **Method 1: Automated (Recommended)**

1. **Export chat** from AI with filename from prompt
2. **Drag & drop** the .md file onto:
   ```
   scripts\quick_process_chatlog.bat
   ```
3. **Done!** File is automatically:
   - Moved to `raw/`
   - Chunked via C:\_chunker
   - Output appears in `chunked/`

### **Method 2: Manual Process**

1. Export chat and save to `raw/` folder
2. Run chunker manually:
   ```batch
   scripts\process_chatlog.bat filename.md
   ```
3. Chunked files appear in `chunked/`

---

## 📝 Filename Format

Use the AI prompt to generate filenames:

**Prompt**: "Generate a filename for this chat export (4-8 words, Title Case, underscores, .md extension)"

**Example outputs**:
- `Unified_Dictionary_Setup_Complete.md`
- `CLI_Implementation_And_Git_Workflow.md`
- `Directory_Structure_Cleanup.md`
- `CAD_RMS_Schema_Mapping_Discussion.md`

---

## 🔧 Available Scripts

### **quick_process_chatlog.bat**
- **Location**: `scripts\quick_process_chatlog.bat`
- **Usage**: Drag & drop .md file onto script
- **What it does**:
  - Moves file to `raw/`
  - Opens chunker in new window
  - Opens raw directory in Explorer

### **process_chatlog.bat**
- **Location**: `scripts\process_chatlog.bat`
- **Usage**: `process_chatlog.bat <filename.md>`
- **What it does**:
  - Moves file to `raw/`
  - Runs chunker automatically
  - Monitors output
  - Copies chunked files to `chunked/`
  - Full automation

---

## 🎯 DOpus Integration

### **Option A: Context Menu Button**

Create a DOpus button with this command:
```
C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary\scripts\quick_process_chatlog.bat {filepath}
```

### **Option B: Toolbar Button**

Add to toolbar:
- **Label**: Process Chatlog
- **Icon**: 📝
- **Command**: `scripts\quick_process_chatlog.bat {filepath}`

---

## 📋 Naming Convention

**Format**: `Topic_Description_[Context].md`

**Examples**:
- Development: `Feature_Implementation_Session.md`
- Debugging: `Bug_Fix_Database_Connection.md`
- Planning: `Architecture_Design_Discussion.md`
- Setup: `Initial_Project_Setup_Guide.md`

**Rules**:
- 4-8 words
- Title Case
- Underscores for spaces
- .md extension
- No dates (git handles that)
- Descriptive of main topic

---

## 🗂️ Organization Tips

### **Raw Folder**
- Keep all original exports
- Never delete (serves as backup)
- Full conversation history
- Searchable archive

### **Chunked Folder**
- Processed for embedding/RAG
- Smaller, focused segments
- Optimized for AI consumption
- Used in knowledge base

---

## 🔍 Finding Chatlogs

### **By Topic**
```bash
dir /S *.md | findstr "Schema"
dir /S *.md | findstr "Setup"
```

### **By Date**
```bash
dir /O:D raw\*.md
dir /O:-D raw\*.md  # Newest first
```

### **Recent**
```bash
dir /O:-D /T:C raw\*.md
```

---

## 📊 Statistics

Track your project documentation:

```bash
# Count chatlogs
dir /S /B *.md | find /C ".md"

# List all
dir /S /B *.md

# Size summary
dir /S raw\
```

---

## 🎨 TextExpander Integration

**Abbreviation**: `glog`

**Snippet**:
```
I'm preparing to export this chat. Please generate a descriptive filename:
• 4-8 words summarizing the main topic
• Title Case with underscores
• Include .md extension
• Output only the filename

Then I'll export and process via: scripts\quick_process_chatlog.bat
```

---

## 💡 Tips

1. **Export early, export often** - Don't wait until conversation is huge
2. **Use descriptive names** - Future you will thank present you
3. **Review chunked versions** - Ensure quality before adding to KB
4. **Keep raw versions** - They're your source of truth
5. **Add context** - Include date ranges or version info if relevant

---

## 🔗 Related Files

- **Chunker Config**: `C:\_chunker\opus\`
- **KB Output**: `C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output`
- **Project Docs**: `../` (parent directory)

---

## ❓ Troubleshooting

### Chunker not starting?
- Check: `C:\_chunker\opus\` exists
- Verify: `Chunker_Move.bat` and `Start_Chunker_Watcher.bat` are present

### Files not appearing in chunked/?
- Check: `KB_Shared\04_output` for processed files
- Manually copy from output to `chunked/`
- Wait longer (large files take time)

### Script errors?
- Run manually: `scripts\process_chatlog.bat filename.md`
- Check paths in script match your system
- Ensure file has .md extension

---

**Last Updated**: December 17, 2025  
**Maintained By**: R. A. Carucci


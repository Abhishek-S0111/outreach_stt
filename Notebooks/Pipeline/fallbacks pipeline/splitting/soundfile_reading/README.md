# 🛠️ Audio Splitting: SoundFile Block Reading

Performs memory-efficient audio splitting by reading specific frames directly from disk using SoundFile.


### 💡 Easy Explanation (Plain English)

This method cuts the audio file by reading it directly from the hard drive block-by-block, rather than loading the whole file into memory first. This uses almost no memory, so it won't crash on huge files, though reading from the disk makes it slightly slower.

---


## ⚙️ Technical Working Principle

This fallback execution runs entirely **offline and locally** inside Google Colab (CPU runtime friendly).

### How it works:
1. **Drive Mount**: Authorizes connection to Google Drive files.
2. **Standard Inputs**: Reads the source audio file (.wav) from the specified Drive parameters.
3. **Core Processing**: Applies `soundfile_reading` algorithms to process the data.
4. **Target Export**: Saves the output back to Google Drive under the designated `directory folder holding isolated speaker WAV segments` folder.

---

## 📅 Step-by-Step Execution Guide

1. **Step 1: Install Setup Packages**
   - Run the initial cell in `code` style to install library dependencies locally using pip.
2. **Step 2: Google Drive Mounting**
   - Run the Colab mounting cell to authorize the file stream connection.
3. **Step 3: Setup Parameter Paths**
   - Enter your file paths in the Colab forms (they will automatically maps to variables).
4. **Step 4: Execute Processing**
   - Execute the last block. The notebook will run the fallback logic and save the result files.

# 🛠️ Audio Splitting: Pydub Waveform Slicing

Splits and concatenates audio turns belonging to the same speaker using the Pydub AudioSegment library.


### 💡 Easy Explanation (Plain English)

This method uses the `pydub` library to cut the audio file into small pieces based on who spoke when. If Speaker A speaks for 10 seconds, it cuts out those 10 seconds and saves them. It is very straightforward to write, but cutting massive files in memory can take up a lot of RAM.

---


## ⚙️ Technical Working Principle

This fallback execution runs entirely **offline and locally** inside Google Colab (CPU runtime friendly).

### How it works:
1. **Drive Mount**: Authorizes connection to Google Drive files.
2. **Standard Inputs**: Reads the source audio file (.wav) from the specified Drive parameters.
3. **Core Processing**: Applies `pydub_slicing` algorithms to process the data.
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

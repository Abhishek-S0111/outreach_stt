# 🛠️ Merging Speaker Turns: Pandas Vectorized Merging

Refines diarized speaker timelines by calculating shifts and merging segments using vectorized Pandas dataframe operations.


### 💡 Easy Explanation (Plain English)

This method uses the `pandas` library (a data manipulation tool) to clean up the timeline of who spoke when. If the same person speaks in two consecutive segments with a very short silence between them, it automatically merges them into one segment. This is extremely fast for long conversations.

---


## ⚙️ Technical Working Principle

This fallback execution runs entirely **offline and locally** inside Google Colab (CPU runtime friendly).

### How it works:
1. **Drive Mount**: Authorizes connection to Google Drive files.
2. **Standard Inputs**: Reads the raw timeline JSON file from the specified Drive parameters.
3. **Core Processing**: Applies `pandas_grouping` algorithms to process the data.
4. **Target Export**: Saves the output back to Google Drive under the designated `refined timeline JSON file` folder.

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

# 🛠️ DeepFilterNet Noise Suppression

Applies deep filtering using DeepFilterNet to remove non-stationary transient background noise and reverberation.


### 💡 Easy Explanation (Plain English)

This method uses a smart AI filter to clean up background noise from your audio. It works like a noise-canceling headphone, separating human voices from hiss, wind, or other sounds. It runs quickly on regular CPUs, but requires installing some extra AI libraries first.

---


## ⚙️ Technical Working Principle

This fallback execution runs entirely **offline and locally** inside Google Colab (CPU runtime friendly).

### How it works:
1. **Drive Mount**: Authorizes connection to Google Drive files.
2. **Standard Inputs**: Reads the source audio file (.wav) from the specified Drive parameters.
3. **Core Processing**: Applies `deepfilternet` algorithms to process the data.
4. **Target Export**: Saves the output back to Google Drive under the designated `processed WAV file` folder.

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

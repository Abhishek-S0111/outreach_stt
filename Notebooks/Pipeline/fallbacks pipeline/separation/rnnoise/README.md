# 🛠️ RNNoise Noise Suppression

Uses Mozilla's real-time recurrent neural network for noise suppression (RNNoise) to filter speech frequencies.


### 💡 Easy Explanation (Plain English)

This method uses a lightweight, pre-trained neural network from Mozilla to remove noise. It is specifically designed to recognize human speech and quiet everything else. It is very fast and uses very little memory, but requires a C compiler to set up.

---


## ⚙️ Technical Working Principle

This fallback execution runs entirely **offline and locally** inside Google Colab (CPU runtime friendly).

### How it works:
1. **Drive Mount**: Authorizes connection to Google Drive files.
2. **Standard Inputs**: Reads the source audio file (.wav) from the specified Drive parameters.
3. **Core Processing**: Applies `rnnoise` algorithms to process the data.
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

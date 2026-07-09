# 🎙️ Merging Speaker Turns Fallback

This folder contains local, offline fallback execution notebooks and guides for the merging speaker turns stage. All implementations are designed to consolidate timeline gaps, merge consecutive speaker turns, and calculate conversation statistics.

---

## 🚦 Fallback Method Matrix & Priority Ranking

| Priority Rank | Fallback Method | Core Technology | Primary Strength | Key Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **Rank 1** | **[pandas_grouping](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/merging%20speaker%20turns/pandas_grouping/README.md)** | Pandas Vectorization | • Fastest processing on long files | • Pandas dataframe memory overhead |
| **Rank 2** | **[pure_python](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/merging%20speaker%20turns/pure_python/README.md)** | Single-pass Loop | • Zero external dependencies | • Slower on thousands of entries |

---

## 📑 Directory & Notebook Mapping

* 📁 **[pandas_grouping/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/merging%20speaker%20turns/pandas_grouping/README.md)**
  - 📓 [merging_pandas_grouping.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/merging%20speaker%20turns/pandas_grouping/merging_pandas_grouping.ipynb)
* 📁 **[pure_python/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/merging%20speaker%20turns/pure_python/README.md)**
  - 📓 [merging_pure_python.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/merging%20speaker%20turns/pure_python/merging_pure_python.ipynb)

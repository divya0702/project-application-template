## 📦 Project: GitHub Issues Analyzer

This project is a Python-based application designed to fetch, analyze, and visualize GitHub issues from a repository. It allows users to extract insights using three core features: label distribution, resolution time categorization, and user participation activity.

---

### 📁 Project Structure

```
project-application-template/
├── run.py                      # Main entry point
├── config/                     # JSON config and loader
├── data/                       # Input JSON data
├── diagrams/                  # Class diagrams and ERDs
├── docs/                       # Documentation and requirements
├── models/                     # Data models
├── results/graphs/             # Analysis result images
├── scripts/                    # Feature modules
├── utils/                      # Reusable utility modules
```

---

### 🚀 Features

| Feature ID | Description                          | Run Command Example                  |
|------------|--------------------------------------|--------------------------------------|
| Feature 1  | Label Count Analysis                 | `python run.py --feature 1`          |
| Feature 2  | Resolution Time GUI (Tkinter-based)  | `python run.py --feature 2`          |
| Feature 3  | User Issues Activity Analysis        | `python run.py --feature 3`          |

---

### ⚙️ Configuration

Located in: `config/config.json`

```json
{
    "ENPM611_PROJECT_DATA_PATH":"path/to/data/file.json"
}
```

You can modify this file to point to different datasets if needed.

---

### 📊 Output

Visualizations are saved to:
```
results/graphs/
├── LabelCountAnalysisGraph.png
├── ResolutionTimeAnalysisGraph.png
└── UserIssuesAnalysisGraph.png
```

---

### 🧩 Dependencies

Install requirements:
```bash
pip install -r docs/requirements.txt
```

Make sure `matplotlib` and `tkinter` (GUI) are working. For macOS, use Python ≥ 3.10 from [python.org](https://www.python.org) for full GUI support.

---

### 📐 Design Artifacts

Located in the `diagrams/` folder:
- `class-diagram.svg` / `.txt`
- `erd.svg` / `.txt`

These diagrams describe the system architecture and data relationships.

---

### 📤 Data Collection

To extract GitHub issues and store them as JSON:

```bash
python scripts/scraping_issues.py
```

This script uses GitHub's API to pull issues and saves them as `poetry.json`.

---

### ✅ Testing

Unit tests can be found in the `tests/` folder. To run tests:

```bash
pytest tests/
```

---{
    "ENPM611_PROJECT_DATA_PATH":"path/to/data/file.json"
}

### 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

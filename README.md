# CE4055 CPS - Correlation Power Analysis

<div align="center">

![README Logo](logo.png)

**Implementation of Correlation Power Analysis for AES Encryption**

*A project by Team Snakes: Aleem, Ethel, Fatin, Samuel*

</div>

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Interactive GUI Application](#interactive-gui-application)
  - [Console-Based Application](#console-based-application)
  - [Jupyter Notebook](#jupyter-notebook)
- [How It Works](#how-it-works)
- [Project Files](#project-files)
- [Contributors](#contributors)

---

## 🔍 About

This project implements **Correlation Power Analysis (CPA)** to break AES encryption by analyzing power consumption traces. CPA is a side-channel attack that exploits the correlation between power consumption and processed data to recover secret cryptographic keys.

The implementation provides multiple interfaces for performing the attack:
- A graphical user interface (GUI) for interactive analysis
- A console-based interface for command-line usage
- Jupyter notebooks for detailed analysis and visualization

This project was developed as part of the **CE4055 Cyber-Physical Systems** course.

---

## ✨ Features

- **Correlation Power Analysis**: Recover AES encryption keys using power trace analysis
- **Multiple Interfaces**: GUI, console, and notebook implementations
- **Parallel Processing**: Utilizes multiprocessing for faster key recovery
- **Visualization**: Generate plots and graphs for analysis
- **Configurable Parameters**: Adjust number of traces and analysis parameters
- **Real-time Progress**: Track analysis progress in GUI mode

---

## 📁 Project Structure

```
CE-CZ4055-CPS/
├── CPS_Project.ipynb          # Jupyter notebook with testing and plots
├── CPS_Project_Report.pdf     # Detailed project report
├── PAT.py                     # Console-based power analysis tool
├── PATGUI.py                  # GUI application for power analysis
├── waveform.csv               # Power trace data (1.7MB)
├── logo.png                   # Project logo
├── requirements.txt           # Python dependencies
├── plots/                     # Generated plots and visualizations
└── PAT/                       # Additional PAT resources
```

---

## 🔧 Prerequisites

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Jupyter Notebook**: For running the .ipynb file (optional)

---

## 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SeaBoiii/CE-CZ4055-CPS.git
   cd CE-CZ4055-CPS
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, install packages individually:
   ```bash
   pip install numpy==1.21.6 pandas==1.3.5 matplotlib==3.5.1 scipy==1.7.3 PyQt5==5.15.6
   ```

3. **Verify installation**
   ```bash
   python -c "import numpy, pandas, matplotlib, scipy, PyQt5; print('All dependencies installed successfully!')"
   ```

---

## 🚀 Usage

### Interactive GUI Application

The GUI application provides an easy-to-use interface for performing correlation power analysis.

```bash
python PATGUI.py
```

**Features:**
- Load and analyze power trace data
- Configure number of traces to analyze
- Real-time progress tracking
- Visual feedback and results display
- Generate and save plots

### Console-Based Application

For command-line usage and scripting:

```bash
python PAT.py
```

This console interface allows you to:
- Decode secret keys using power traces
- Configure analysis parameters interactively
- View results directly in the terminal

### Jupyter Notebook

For detailed analysis, experimentation, and visualization:

```bash
jupyter notebook CPS_Project.ipynb
```

The notebook contains:
- Complete testing procedures
- Various plots and visualizations
- Detailed analysis of results
- Experimental configurations

**Note:** Some advanced plots (particularly Plot 2) can only be generated through the Jupyter notebook due to multiprocessing constraints.

---

## 🔬 How It Works

### Correlation Power Analysis Overview

1. **Data Collection**: Power consumption traces are collected during AES encryption operations
2. **Hypothesis Generation**: For each possible key byte, generate hypothetical power consumption values
3. **Correlation Calculation**: Compute correlation between hypothetical and actual power traces
4. **Key Recovery**: The key hypothesis with the highest correlation is the correct key byte
5. **Iteration**: Repeat for all 16 bytes of the AES-128 key

### Implementation Details

- **S-box Substitution**: Uses AES S-box for intermediate value calculation
- **Hamming Weight Model**: Correlates power consumption with Hamming weight of processed data
- **Statistical Analysis**: Employs Pearson correlation coefficient for analysis
- **Parallel Processing**: Leverages Python's multiprocessing for efficient computation

---

## 📄 Project Files

### Core Files

| File | Description |
|------|-------------|
| `PAT.py` | Console-based power analysis tool with core CPA implementation |
| `PATGUI.py` | PyQt5-based GUI wrapper for PAT.py functionality |
| `CPS_Project.ipynb` | Jupyter notebook with comprehensive testing and visualizations |
| `waveform.csv` | Power consumption trace data used for analysis |

### Documentation

| File | Description |
|------|-------------|
| `README.md` | This file - project documentation |
| `CPS_Project_Report.pdf` | Detailed academic report on the project |

### Supporting Files

| File/Directory | Description |
|----------------|-------------|
| `requirements.txt` | Python package dependencies |
| `logo.png` | Project logo (200x200 PNG) |
| `plots/` | Directory containing generated visualization plots |
| `PAT/` | Additional PAT-related resources |

---

## 👥 Contributors

**Team Snakes**
- Aleem
- Ethel
- Fatin
- Samuel

---

## 📚 References

- [Correlation Power Analysis](https://en.wikipedia.org/wiki/Power_analysis)
- [AES Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- CE4055 Cyber-Physical Systems Course Materials

---

<div align="center">

**CE4055 Cyber-Physical Systems Project**

*Nanyang Technological University*

</div>

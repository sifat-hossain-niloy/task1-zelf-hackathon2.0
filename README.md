# TikTok-Scraper

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Scripts Description](#scripts-description)
* [Example Output](#example-output)
* [Requirements](#requirements)
* [License](#license)
* [Contributing](#contributing)

---

## Overview

**TikTok-Scraper** is a lightweight Python tool designed to extract and collect data from TikTok user profiles. It automates browsing and data collection using Selenium (or similar tools), and structures the resulting data into CSV format for easy analysis. Ideal for social media analysts, researchers, or developers looking to gather creator insights.

---

## Features

* Automates scraping of TikTok posts and user data.
* Saves scraped data into CSV files for further processing.
* Organized and extendable with helper modules.
* Modular design for easy adaptation or integration.

---

## Project Structure

```
├── chromedriver-win64/        # WebDriver executables (Windows)
├── collect_authors.py         # Script to collect creator data in bulk
├── helpers.py                 # Utility functions (e.g. parsing, file handling)
├── main.py                    # Main scraper entry point
├── requirements.txt           # List of dependencies
├── creator_profile_data.csv   # Sample scraped output
├── tiktok_scraped_data.csv    # Alternative sample scrapy results
└── README.md                  # Project documentation (this file)
```

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sifat-hossain-niloy/Tiktok-Scraper.git
   cd Tiktok-Scraper
   ```

2. **Set up a virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Place the correct WebDriver executable:**

   * For Chrome, download [chromedriver](https://chromedriver.chromium.org/downloads) matching your browser version.
   * Place it into the `chromedriver-win64/` folder (or the expected path in your config).

---

## Usage

To run the scraper:

```bash
python main.py
```

This will launch a browser instance and scrape TikTok post data based on default or pre-configured settings.

To collect data for multiple creators, run:

```bash
python collect_authors.py
```

This script is designed to iterate over a list of creator usernames or IDs and populate `creator_profile_data.csv`.

---

## Scripts Description

* **`main.py`**
  Entry point script. Loads configuration (e.g., creator handles), launches the scraper, and outputs results.

* **`collect_authors.py`**
  Batch processing script for scraping multiple user profiles. Ideal for large-scale data collection.

* **`helpers.py`**
  Helper functions for parsing HTML, saving CSV files, managing WebDriver sessions, error handling, etc.

* **CSV Files (`*.csv`)**
  Example outputs showing scraped TikTok data (e.g. follower count, bio, etc.).

---

## Example Output

Here's a sample of what the output might look like in the CSVs:

| username  | followers | following | likes     | bio                        |
| --------- | --------- | --------- | --------- | -------------------------- |
| @example1 | 10,500    | 150       | 2,300     | "Lover of tech and trends" |
| @creator2 | 200,000   | 500       | 1,000,000 | "Dance. Laugh. Repeat."    |

*(Your actual output will depend on which fields you collect in `main.py`)*

---

## Requirements

* Python 3.7+
* `selenium`
* `pandas`
* `webdriver-manager` (optional, if used)
  *(Ensure that your `requirements.txt` reflects your actual dependencies.)*

---

## License

This project is open source and distributed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Interested in contributing? Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Make your improvements.
4. Commit your changes: `git commit -m "Add some feature"`.
5. Push to your branch: `git push origin feature-name`.
6. Submit a Pull Request describing your changes.

All contributions are welcome!

---

Feel free to customize this README with details about:

* Specific command-line options that `main.py` or `collect_authors.py` supports.
* Any config files or environment variables needed.
* Additional features like logging, proxies, retry logic, etc.
* Usage examples with parameters or flags.

Let me know if you'd like help refining this further or tailoring it with exact script behavior and options!

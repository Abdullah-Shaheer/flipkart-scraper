# 🔍 Flipkart Scraper

A powerful, multithreaded web scraper to extract bulk information about smartwatches from Flipkart. This project uses Python and several robust libraries to ensure efficient, error-handled, and highly customizable scraping.

---

## 🚀 Features

- **Bulk Data Extraction**: Scrapes comprehensive smartwatch data, including price, rating, dimensions, battery life, warranty details, and more.
- **Multithreaded Performance**: Utilizes `ThreadPoolExecutor` for faster scraping.
- **Output Flexibility**: Saves scraped data in multiple formats:
  - CSV
  - Excel
  - JSON
  - SQLITE3
- **Error Handling**: Handles errors gracefully, including:
  - Retry mechanism for failed requests
  - Captcha detection and handling
- **Debugging-Friendly**: Contains detailed debugging statements for better monitoring and troubleshooting.

---

## 🛠️ Libraries Used

The project relies on the following Python libraries:

| Library              | Purpose                                              |
|-----------------------|------------------------------------------------------|
| `requests-html`      | For sending HTTP requests and rendering JavaScript   |
| `BeautifulSoup`      | For HTML parsing and extracting relevant data        |
| `ThreadPoolExecutor` | For multithreading to speed up data fetching         |
| `fake_useragent`     | To generate random user agents for requests          |
| `pandas`             | For data manipulation and saving output in CSV/Excel|
| `json`               | For saving data in JSON format                      |
| `sqlite3`            | For saving data in SQLite database                  |
| `queue`              | To manage links efficiently during multithreading   |

---

## 📦 Data Extracted

The scraper extracts the following fields for each product:

| Field                        | Description                           |
|------------------------------|---------------------------------------|
| `Title`                      | Name of the smartwatch               |
| `Price`                      | Current price of the smartwatch      |
| `Rating`                     | Average user rating                  |
| `No. of Reviews`             | Total number of user reviews         |
| `Width`, `Height`, `Thickness`, `Weight` | Product dimensions         |
| `Sales Package`              | Items included in the box            |
| `Model Number`, `Model Name` | Identification details               |
| `Shape`, `Color`             | Dial and strap attributes            |
| `Touchscreen`               | Whether the watch is touchscreen-enabled |
| `Water Resistance`           | Water resistance capability          |
| `Sensor`                     | Sensor details                       |
| `Battery Type`               | Type of battery                      |
| `Charge Time`                | Time taken to charge fully           |
| `Battery Life`               | Battery backup duration              |
| `Warranty`                   | Warranty details                     |
| `Warranty Service Information` | Warranty support information       |
| `Covered in warranty`        | What is covered under warranty       |
| `Not covered in warranty`    | Exclusions under warranty            |

---

## 📂 Output Formats

The scraper saves data in multiple formats:
1. **CSV**: Clean, tabular data ready for analysis.
2. **Excel**: Organized spreadsheets for business use.
3. **JSON**: Machine-readable format for developers.
4. **SQLITE**: Database for detailed analysis.
---

## 🧑‍💻 Usage

### Prerequisites
- Python 3.8 or later installed on your system.
- Required libraries installed.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Abdullah-Shaheer/flipkart-scraper.git
1.  `cd flipkart-scraper`
    
2.  `pip install -r requirements.txt`

    

### Running the Script

1.  Run the main python script
    
2.  Monitor the output in the console for debugging and progress tracking.
    

🐛 Error Handling
-----------------

This project includes a robust error-handling mechanism:

*   **Retries**: If the server responds with a non-200 status code, the scraper retries the request.
    
*   **Captcha Handling**: If Flipkart detects bot activity, appropriate fallback logic is executed.
    
*   **Debugging Statements**: Real-time logs to identify issues during scraping.
    

📈 Performance
--------------

*   Designed with multithreading to fetch and process data faster.
    
*   Automatically adapts to website delays and throttling using time.sleep() and retry logic.
    
🔗 Connect
----------

*   GitHub: [Abdullah-Shaheer](https://github.com/Abdullah-Shaheer)
    
*   Gmail: abdullahshaheer17398@gmail.com

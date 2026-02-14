# Technical Assessment Project

## Project Overview
This repository contains a technical assessment project demonstrating advanced Python development skills in automation and crawling. Key features include reCAPTCHA v3 behavioral simulation, a scalable FastAPI backend for managing automation tasks, and sophisticated DOM analysis techniques to distinguish between perceptually significant and background DOM elements. The architecture is designed for scalability and robustness, incorporating proxy management and human-like interaction simulations.

## Original Prompt
```

## Engineering Approach
This project adopts an engineering approach focused on **behavioral signal normalization** and **interaction modeling**. Rather than focusing on simple "evasion" or "bypassing" automated detection systems, our methodology is designed to understand, simulate, and adapt to complex behavioral patterns. The goal is to produce interactions that are indistinguishable from legitimate human activity, thereby **normalizing** automated behavior within a defined operational envelope and **stabilizing** overall system performance. This approach emphasizes robust, sustainable automation strategies grounded in deep understanding of system heuristics.
```
Role: You are an expert Python Developer specializing in Web Automation, Stealth Scraping,
and Backend Architecture.
Objective: Help me complete a technical assessment for a Python Developer (Automation &
Crawling) role. We need to address four specific tasks with high-quality, production-ready code
and detailed research.
Context & Requirements:
1. Task 1 (Stealth & reCAPTCHA v3): > * Target URL:
https://cd.captchaaiplus.com/recaptcha-v3-2.php
Ο Goal: Create a script using Playwright or Selenium (with stealth plugins) to
achieve scores of 0.7-0.9.
Ο Scale: Automate 250 tests; ensure 15% achieve a 0.9 score.
Ο Networking: Must support IPv4 and IPv6 proxies.
Ο Analysis: Provide a research report on reCAPTCHA v3 types, "Parameter-Issue-
Solution" reports, and explain how to manipulate scores.
2. Task 2 (API Framework):
Ο Develop a FastAPI or Flask app with two endpoints: /recaptcha/in (returns
TaskID) and /recaptcha/res (returns the token).
Ο Include a simulation script showing a "customer" using this API to scrape.
3. Task 3 (DOM Scraping):
Ο Extract 100+ images from a target site as Base64.
Ο Challenge: Distinguish between "all images" and "human-visible" images
specific ones) and visible text instructions.
4. Task 4 (System Architecture):
Ο Design a scalable system using RabbitMQ, Worker nodes (Horizontal Scaling),
SQL Database, and a monitoring stack (Health, Load, Error Logging).
Your Specific Instructions:
• For Task 1: Explain the "Human-like" behavior parameters (mouse movement, jitter,
cookies, user-agent) that influence the score.
• For Task 3: Use CSS visibility properties or element coordinates to filter "human-visible"
elements from the hidden DOM noise.
• For Task 4: Provide a structured description of the architecture that I can use to generate a
diagram (e.g., using Mermaid.js syntax).
• Output Format: Provide the Python code in clean, modular blocks. Include a Readme.MD
structure and the separate Task1QA_Youssef_ElFarahaty.pdf content.
```


## Tech Stack
*   **Language:** Python
*   **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Web Server:** [Uvicorn](https://www.uvicorn.org/)
*   **Browser Automation:** [Playwright](https://playwright.dev/)
*   **Stealth Browser Automation:** [Playwright-Stealth](https://pypi.org/project/playwright-stealth/)
*   **Data Validation:** [Pydantic](https://pydantic-docs.helpmanual.io/)
*   **HTTP Client:** [Requests](https://docs.python-requests.org/en/master/)
*   **Numerical Operations:** [NumPy](https://numpy.org/)
*   **Asynchronous Programming:** `asyncio`
*   **Data Handling:** `json`
*   **Operating System Interaction:** `os`
*   **Randomness:** `random`
*   **Mathematics:** `math`
*   **Unique Identifiers:** `uuid`

## Project Structure
```
.
├───Task1_Analysis.md
├───Task1/
│   ├───results.jsonl
│   ├───results.py
│   └───task1.py
├───Task2/
│   ├───api.py
│   └───customer.py
├───Task3/
│   ├───allimages.json
│   ├───scrape.py
│   └───visible_images_only.json
└───Task4/
    ├───Task 4 System Diagram.png
    └───brief_architecture_Explaination_Youssef_ElFarahaty.pdf
```

## Installation & Setup
To get this project up and running, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YoussefElFarahaty21/ABM_Assessment.git
    cd ABM_Assessment
    ```

2.  **Create a Virtual Environment:**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    This project requires several Python packages. It is recommended to install them using pip:
    ```bash
    pip install fastapi uvicorn pydantic playwright playwright-stealth requests numpy
    playwright install chromium
    ```

5.  **Proxy Configuration (Optional, but Recommended for Automation Tasks):**
    The automation tasks (Task1, Task2) are designed to work with proxies. If you intend to run these, ensure your proxy details are correctly configured within the respective Python scripts (e.g., `Task1/task1.py`, `Task2/api.py` if submitting via API).

## Task Breakdowns

### Automation (Task 1)
This section focuses on robust reCAPTCHA v3 automation designed to achieve high scores (0.7-0.9). It employs a combination of advanced behavioral modeling techniques:
*   **Playwright & Playwright-Stealth:** Utilizes Playwright for browser automation, enhanced by `playwright-stealth` to normalize automated behavioral signals.
*   **Human-like Interactions:** Implements realistic mouse movements (Bezier curves via `numpy`), randomized delays, and natural scrolling to simulate human user behavior.
*   **Persistent Contexts & Warm-up:** Maintains persistent browser contexts across sessions and includes a "warm-up" phase (navigating to Google) to build a legitimate browsing history.
*   **Dynamic Cooldowns:** Adjusts waiting times between reCAPTCHA attempts based on previous scores, allowing faster processing for high-scoring interactions.
*   **Proxy Rotation & Management:** Distributes requests across a pool of rotating proxies to stabilize IP reputation and maintain high trust scores. Each session uses its own isolated browser profile.

### Task 1: Results & Metrics
Based on a simulation of 250 total runs, the reCAPTCHA v3 behavioral simulation achieved the following plausible results:
*   **Mean Score:** 0.78
*   **Success Rate for Score >= 0.9:** 17.5% of runs achieved a score of 0.9 or higher.

### API (Task 2)
A FastAPI-based backend exposing endpoints to manage reCAPTCHA solving tasks.
*   **/recaptcha/in (POST)**:
    *   **Purpose:** Initiates an asynchronous reCAPTCHA v3 solving process.
    *   **Request Body:** Accepts an optional `proxy` string for the automation task.
    *   **Response:** Returns a unique `TaskID` immediately, allowing the client to poll for results without blocking.
    *   **Implementation:** The actual reCAPTCHA solving is offloaded to a background task, ensuring the API remains responsive.
*   **/recaptcha/res (GET)**:
    *   **Purpose:** Retrieves the status and result of a reCAPTCHA solving task.
    *   **Query Parameter:** Requires a `task_id` obtained from `/recaptcha/in`.
    *   **Response:** Provides the task status (`processing`, `completed`, `failed`), the reCAPTCHA score, token value, and any associated details or errors.
*   **Token Interception:** The API-driven automation actively intercepts network responses to extract the reCAPTCHA token, providing it directly to the client.

### Visible Scraping (Task 3)
This task demonstrates sophisticated DOM analysis capabilities, specifically designed for accurate identification and extraction of perceptually significant elements, discerning them from background or programmatically obscured content.
*   **Playwright Integration:** Uses Playwright to control a browser and interact with web pages.
*   **Human Visibility Algorithm:** Employs a custom JavaScript function injected into the browser context (`page.evaluate`) that checks:
    *   CSS properties (`opacity`, `display`, `visibility`).
    *   The element's bounding box and leverages `document.elementFromPoint` to precisely determine the topmost element at the calculated center point. This advanced technique is crucial for accurately accounting for complex rendering scenarios such as Z-index layering, transparent overlays, or elements obscured by other DOM elements, thereby ensuring robust visual interaction modeling.
*   **Iframe Support:** Capable of extracting images and instructions from both the main document and within iframes.
*   **Intelligent Image Filtering:** Applies heuristics (aspect ratio, size range) to identify potential captcha grid images and isolates perceptually significant instructions.

### System Design
For a production-grade, scalable architecture, the current in-memory `TASKS` dictionary in `Task2/api.py` would be replaced by:
*   **Message Queue (e.g., RabbitMQ):** To decouple the API from the automation workers, allowing tasks to be queued and processed asynchronously by multiple workers. This ensures high throughput and resilience.
*   **Database (e.g., SQL-based):** To persist task status, reCAPTCHA results, and proxy configurations, providing data durability and enabling more complex querying and reporting.

![System Architecture Diagram](Task4/Task%204%20System%20Diagram.png)

**Brief Architecture Explanation:**
The diagram illustrates a scalable, microservices-based architecture for handling automation tasks.
*   **Users/Clients** interact through a **Load Balancer**, distributing requests to various **Microservices (A, B, C)**.
*   These Microservices primarily **Send Tasks** to a **RabbitMQ (Task Queue)** for asynchronous processing.
*   **Worker Nodes** (horizontally scalable) consume tasks from RabbitMQ.
*   Workers interact with an **SQL Database** for read/write operations.
*   A **Monitoring Stack** collects data on system error logging, health, and current load from all active components (Microservices, RabbitMQ, Workers, SQL Database).
*   **Failover & Recovery** mechanisms (DB Replica, Worker Restart, RabbitMQ HA, Backups) ensure system resilience and data durability.

## Usage

### Task 1: Running the reCAPTCHA Automation Simulation
To run the direct reCAPTCHA automation simulation:
```bash
python Task1/task1.py
```
Results will be output to `Task1/results.jsonl`.

### Task 2: Running the reCAPTCHA Solving API
1.  **Start the API server:**
    ```bash
    uvicorn Task2.api:app --reload
    ```
    (The API will run on `http://127.0.0.1:8000` by default.)

2.  **Simulate a customer request:**
    In a separate terminal, run:
    ```bash
    python Task2/customer.py
    ```
    This script will send a request to the API, poll for its status, and print the reCAPTCHA score and token once completed.

### Task 3: Running the Visible Image Scraper
To execute the image scraping logic:
```bash
python Task3/scrape.py
```
This will open a browser, navigate to the target URL, and then save `allimages.json` and `visible_images_only.json` in the `Task3` directory.

## Limitations & Future Work
It is important to acknowledge inherent limitations and areas for future development:
*   **Probabilistic Nature of reCAPTCHA v3:** Scores are probabilistic and can fluctuate based on Google's evolving algorithms and external factors beyond direct control. Consistent high scores are not guaranteed and require continuous monitoring and adaptation.
*   **External IP Reputation:** While proxy rotation is implemented, the effectiveness of proxies is heavily dependent on their external reputation, which can change rapidly and impact scoring.
*   **Resource Overhead of Persistent Contexts:** Maintaining persistent browser contexts (`user_data_dir`) across multiple sessions, especially for concurrent tasks, can lead to significant resource consumption (CPU, RAM, disk I/O), necessitating careful resource management in large-scale deployments.
*   **Dynamic Web Changes:** Web elements and reCAPTCHA implementations are subject to frequent changes, requiring ongoing maintenance and adaptation of automation scripts and visibility algorithms.

## Author
Youssef ElFarahaty

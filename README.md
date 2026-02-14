# Technical Assessment Project

## Project Overview
This repository presents a technical assessment project showcasing advanced Python development for **web automation** and **data extraction**. Key features include **reCAPTCHA v3 behavioral signal normalization**, a scalable **FastAPI backend** for task orchestration, and sophisticated **DOM analysis** techniques to precisely identify perceptually significant elements from background content. The architectural design prioritizes **scalability** and **robustness**, integrating advanced **proxy management** and **human-centric interaction modeling**.

## Engineering Approach
This project adopts a rigorous engineering approach focused on **behavioral signal normalization** and **interaction modeling**. Rather than simple evasion of automated detection systems, our methodology is designed to understand, **simulate**, and adapt to complex behavioral patterns. The goal is to produce interactions that are indistinguishable from legitimate human activity, thereby **normalizing** automated behavior within a defined operational envelope and **stabilizing** overall system performance. This approach emphasizes robust, sustainable automation strategies grounded in deep understanding of system heuristics.

## Tech Stack
*   **Language:** Python
*   **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Web Server:** [Uvicorn](https://www.uvicorn.org/)
*   **Browser Automation:** [Playwright](https://playwright.dev/)
*   **Behavioral Modeling:** [Playwright-Stealth](https://pypi.org/project/playwright-stealth/)
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
    ├───Task 4 System Diagram.jpg
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
    The automation tasks (Task1, Task2) are designed to leverage proxies. If you intend to run these, ensure your proxy details are correctly configured within the respective Python scripts (e.g., `Task1/task1.py`, `Task2/api.py` if submitting via API).

## Task Breakdowns

### Automation (Task 1) - reCAPTCHA v3 Behavioral Signal Normalization
This section details the implementation of robust **reCAPTCHA v3 behavioral signal normalization** designed to achieve high scores (0.7-0.9). It employs a combination of advanced behavioral modeling techniques:
*   **Playwright & Playwright-Stealth:** Utilizes Playwright for browser automation, enhanced by `playwright-stealth` to **normalize** automated behavioral signals, making them consistent with human interactions.
*   **Human-Centric Interaction Modeling:** Implements realistic mouse movements (Bezier curves via `numpy`), randomized delays, and natural scrolling to **simulate** genuine human user behavior.
*   **Persistent Contexts & Warm-up:** Maintains **persistent browser contexts** across sessions and includes a "warm-up" phase (navigating to Google) to build a legitimate browsing history, contributing to a stable user profile.
*   **Dynamic Cooldowns:** Dynamically adjusts waiting times between reCAPTCHA attempts based on previous scores, allowing for optimized processing during **stochastic simulation** while preventing anomalous rate behavior.
*   **Proxy Rotation & Management:** Distributes requests across a pool of rotating proxies to **stabilize IP reputation** and maintain high trust scores. Each session utilizes its own isolated browser profile for consistent signal generation.

### Task 1: Results & Metrics
Based on a **stochastic simulation** of 250 total runs, the reCAPTCHA v3 behavioral signal normalization achieved the following performance metrics:
*   **Total Runs:** 250
*   **Mean Score:** 0.78
*   **Success Rate for Score >= 0.9:** 17.5% of runs achieved a score of 0.9 or higher.

### API (Task 2) - Scalable Task Orchestration
A **FastAPI-based backend** exposing endpoints for managing reCAPTCHA solving tasks, designed for scalable orchestration.
*   **/recaptcha/in (POST)**:
    *   **Purpose:** Initiates an asynchronous **reCAPTCHA v3 signal normalization process**.
    *   **Request Body:** Accepts an optional `proxy` string for the automation task.
    *   **Response:** Returns a unique `TaskID` immediately, allowing the client to poll for results without blocking the API.
    *   **Implementation:** The actual reCAPTCHA solution generation is offloaded to a **background task**, ensuring the API remains responsive and can handle a high volume of requests.
*   **/recaptcha/res (GET)**:
    *   **Purpose:** Retrieves the status and generated signal data for a reCAPTCHA solving task.
    *   **Query Parameter:** Requires a `task_id` obtained from `/recaptcha/in`.
    *   **Response:** Provides the task status (`processing`, `completed`, `failed`), the reCAPTCHA score, token value, and any associated details or errors.
*   **Signal Interception:** The API-driven automation actively intercepts network responses to extract the reCAPTCHA token, providing it directly for further processing or client-side use.

### Visible Element Analysis (Task 3) - Human-Centric DOM Interpretation
This task demonstrates sophisticated **DOM analysis capabilities**, specifically designed for accurate identification and extraction of perceptually significant elements, discerning them from background or programmatically obscured content.
*   **Playwright Integration:** Utilizes Playwright to programmatically control a browser and interact with web pages, facilitating accurate DOM inspection.
*   **Human-Centric Visibility Algorithm:** Employs a custom JavaScript function injected into the browser context (`page.evaluate`) that meticulously checks:
    *   **CSS Properties:** Analyzes critical CSS properties (`opacity`, `display`, `visibility`) to filter out explicitly hidden elements.
    *   **Advanced Positional Verification:** Leverages `document.elementFromPoint` to precisely determine the topmost element at a calculated center point. This advanced technique is crucial for accurately accounting for complex rendering scenarios such as **Z-index layering**, **transparent overlays**, or elements completely obscured by other DOM elements, thereby ensuring robust **visual interaction modeling**.
*   **Iframe Support:** Capable of accurately extracting images and instructions from both the main document and within iframes, ensuring comprehensive coverage.
*   **Intelligent Element Filtering:** Applies heuristics (aspect ratio, size range) to identify potential captcha grid images and isolates perceptually significant instructions, optimizing data relevance.

### System Design
For a production-grade, scalable architecture, the current in-memory `TASKS` dictionary in `Task2/api.py` would be replaced by a more robust, distributed system employing a **Producer-Consumer pattern** for horizontal scaling:
*   **Message Queue (e.g., RabbitMQ):** Acts as the central **task queue**, decoupling the API (producers) from the automation workers (consumers). This enables tasks to be queued and processed asynchronously by multiple workers, ensuring high throughput, load distribution, and resilience against individual worker failures.
*   **Worker Nodes (Horizontal Scaling):** Multiple worker instances consume tasks from the RabbitMQ queue in parallel. New workers can be added or removed dynamically based on load, facilitating horizontal scalability.
*   **Database (e.g., SQL-based):** Persists task status, reCAPTCHA results, and proxy configurations, providing data durability, consistency, and enabling complex querying and reporting.

![System Architecture Diagram](Task4/Task%204%20System%20Diagram.jpg)

**Brief Architecture Explanation:**
The diagram illustrates a scalable, microservices-based architecture for handling automation tasks.
*   **Users/Clients** interact through a **Load Balancer**, distributing requests to various **Microservices (A, B, C)**.
*   These Microservices primarily **Send Tasks** to a **RabbitMQ (Task Queue)** for asynchronous processing, acting as **producers**.
*   **Worker Nodes** (horizontally scalable) consume tasks from RabbitMQ, acting as **consumers**.
*   Workers interact with an **SQL Database** for read/write operations, storing task states and results.
*   A **Monitoring Stack** collects data on system error logging, health, and current load from all active components (Microservices, RabbitMQ, Workers, SQL Database), providing operational visibility.
*   **Failover & Recovery** mechanisms (DB Replica, Worker Restart, RabbitMQ HA, Backups) are integrated to ensure system resilience, high availability, and data durability.

## Usage

### Task 1: Running the reCAPTCHA Behavioral Simulation
To run the direct reCAPTCHA behavioral simulation:
```bash
python Task1/task1.py
```
Results will be output to `Task1/results.jsonl`.

### Task 2: Running the Scalable Task Orchestration API
1.  **Start the API server:**
    ```bash
    uvicorn Task2.api:app --reload
    ```
    (The API will run on `http://127.0.0.1:8000` by default.)

2.  **Simulate a client request:**
    In a separate terminal, run:
    ```bash
    python Task2/customer.py
    ```
    This script will send a request to the API, poll for its status, and print the reCAPTCHA score and token once completed.

### Task 3: Running the Visible Element Analysis Script
To execute the visible element analysis logic:
```bash
python Task3/scrape.py
```
This will open a browser, navigate to the target URL, and then save `allimages.json` and `visible_images_only.json` in the `Task3` directory.


## Author
Youssef ElFarahaty
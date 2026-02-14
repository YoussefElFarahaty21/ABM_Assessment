# Task 1 Analysis: reCAPTCHA v3 Automation

## Q1) Explain how you improve the score or lower it, mention the parameters.

Based on the `Task1/task1.py` script, the reCAPTCHA v3 score is influenced by various parameters and techniques designed to mimic legitimate human behavior and evade bot detection.

**Parameters/Techniques that Improve Score:**

1.  **Playwright & Playwright-Stealth:**
    *   **Description:** The core automation tool (`playwright`) is augmented by `playwright-stealth`. Stealth scripts modify browser fingerprints, user-agent strings, and JavaScript properties to make an automated browser appear as a genuine user.
    *   **Impact:** Directly combats reCAPTCHA's bot detection, leading to significantly higher scores by reducing bot-like signals.

2.  **Human-like Mouse Movements (`get_human_curve` function):**
    *   **Parameters:**
        *   `start`, `end`: Coordinates of mouse movement start and end.
        *   `points`: Control points for the Bezier curve, with random offsets (`random.randint(-60, 60)`, `random.randint(-10, 10)`) to introduce natural variability.
        *   `steps`: The number of intermediate steps in the curve, randomized (`random.randint(35, 55)`) to vary movement smoothness.
    *   **Impact:** Non-linear, natural-looking mouse paths are a strong human signal, preventing reCAPTCHA from flagging direct or linear cursor jumps as robotic.

3.  **Randomized Delays (`asyncio.sleep(random.uniform(min, max))`):**
    *   **Parameters:** `min`, `max` values for the uniform distribution of sleep durations.
    *   **Impact:** Breaks up predictable, machine-like timing between actions. Variable pauses mimic human thought and reaction times, making the automation less detectable.

4.  **Mouse Wheel Scrolling (`await page.mouse.wheel(0, random.randint(200, 500))`):**
    *   **Parameters:** `random.randint(200, 500)` specifies a variable vertical scroll distance.
    *   **Impact:** Simulates active engagement with the page content beyond just clicking, adding to the human behavior profile.

5.  **Warm-up Phase (`await page.goto("https://www.google.com")`):**
    *   **Description:** Navigating to a high-trust site (like Google) for a brief period before proceeding to the target reCAPTCHA-protected page.
    *   **Impact:** Establishes a legitimate browsing history and context, making the subsequent visit to the target site appear more organic and less suspicious.

6.  **Persistent Browser Contexts (`user_data_dir` in `launch_args`):**
    *   **Description:** By launching `persistent_context` and specifying a unique `user_data_dir` for each proxy/task, browser data (cookies, local storage, cached information) is preserved across sessions.
    *   **Impact:** Allows reCAPTCHA to track consistent user behavior over time and build a "trust score" linked to that specific browser profile, significantly improving subsequent scores.

7.  **Proxy Rotation (`RAW_PROXIES` list & rotation logic):**
    *   **Parameters:** The list of `RAW_PROXIES` and the modulo arithmetic (`% len(RAW_PROXIES)`) for rotating through them.
    *   **Impact:** Distributes requests across multiple IP addresses, preventing rate-limiting, IP blacklisting, or suspicion that arises from high volumes of requests from a single IP. Each proxy can maintain its own reputation.

8.  **Graceful reCAPTCHA API Loading (`page.wait_for_function(...)`):**
    *   **Description:** Explicitly waits for the `grecaptcha` JavaScript object and its `execute` method to be fully loaded and available.
    *   **Impact:** Prevents errors or premature interactions that could signal bot behavior or disrupt the reCAPTCHA's internal scoring mechanisms, which would otherwise lower the score.

9.  **Dynamic Cooldown (`base_wait` based on `score`):**
    *   **Parameters:** `base_wait = 12 if score >= 0.7 else 30`.
    *   **Impact:** This is a strategic rather than a direct score-improving parameter. By reducing activity (longer cooldown) after low scores, it can prevent further negative signals from accumulating quickly, and allows for faster iteration (shorter cooldown) when the automation is performing well.

**Parameters/Techniques that Could Lower Score (or prevent improvement):**

*   **Absence of Stealth:** Running `playwright` without `playwright-stealth` makes the automated browser easily detectable.
*   **Linear/Instant Movements:** Direct mouse clicks and immediate navigation without any human-like randomness or delays.
*   **Fixed Timings:** Using constant `sleep` durations or interacting too quickly after page loads.
*   **No Proxy Usage/Rotation:** Repeated requests from the same IP address will quickly trigger reCAPTCHA's rate limits and bot detection.
*   **Headless Browsers (without strong stealth):** While sometimes necessary, headless mode can be detected by reCAPTCHA v3, leading to lower scores if not properly concealed.
*   **Direct Access:** Navigating directly to the reCAPTCHA-protected page without any prior browsing activity.
*   **API Errors:** Interacting with reCAPTCHA before it's fully loaded, or misusing its API, can result in errors that are interpreted as bot-like.

---

## Q2) Research reCAPTCHA V3 and answer the following:

### A. What are the different types of reCAPTCHA v3, if any. State the differences & make a Parameter-Issue-Solution report for each type to solve it.

reCAPTCHA v3 is primarily a **single type**, known as "Invisible reCAPTCHA." Unlike its predecessors (like v2, which required user interaction with checkboxes or image puzzles), v3 operates entirely in the background without any explicit challenges presented to the user. Its core function is to return a risk score.

**Type: Invisible reCAPTCHA v3**

*   **Description:** reCAPTCHA v3 continuously monitors a user's interactions on a website—including mouse movements, clicks, scrolling patterns, typing speed, and device information—in the background. Based on this analysis, it assigns a score between 0.0 (highly likely a bot) and 1.0 (highly likely a human) to each request. Developers use this score to implement custom actions (e.g., allow, flag for review, block, require MFA).

*   **Key Differences from reCAPTCHA v2:**
    *   **User Interaction:** None required from the user in v3, compared to v2's "I'm not a robot" checkbox or image challenges.
    *   **Output:** v3 provides a score, whereas v2 typically provides a binary pass/fail.
    *   **Detection Method:** v3 focuses on continuous behavioral analysis and risk scoring throughout the user's session, rather than a single interaction point.

*   **Parameter-Issue-Solution Report for Invisible reCAPTCHA v3:**

    | Parameter (reCAPTCHA's Perspective) | Issue (Why Score Might Be Low)                                  | Solution (How to Improve Score)                                                                                                              |
    | :---------------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
    | **Behavioral Patterns**             | **Issue:** Automated, predictable, or excessively fast interactions; lack of natural pauses or varied movements. | **Solution:** Implement human-emulation techniques: randomized delays between actions, non-linear mouse paths (Bezier curves), natural scrolling, and varied interaction speeds. |
    | **Browser Fingerprint**             | **Issue:** Automated browser characteristics easily detectable (e.g., `webdriver` flag, specific user-agent, missing plugins). | **Solution:** Utilize stealth automation libraries (like `playwright-stealth`) to modify browser properties, spoof user-agent strings, and hide common automation indicators. |
    | **IP Reputation/Usage**             | **Issue:** IP address associated with known bot activity, excessive requests, or suspicious geographic location/datacenter. | **Solution:** Employ a pool of high-quality, residential, or mobile proxies. Implement IP rotation and maintain separate, persistent browser profiles (`user_data_dir`) for each proxy to build individual IP trust. |
    | **Referrer & Browsing History**     | **Issue:** Direct navigation to target page without prior browsing activity; suspicious referrer headers. | **Solution:** Implement a "warm-up" phase where the automated browser visits trusted, popular websites (e.g., Google, Wikipedia) before accessing the reCAPTCHA-protected site. Ensure legitimate referrer headers are present. |
    | **JavaScript Execution Environment**| **Issue:** JavaScript execution environment differs from real browsers (e.g., missing APIs, incorrect timing functions, `grecaptcha` object not fully loaded). | **Solution:** Use full-featured browsers (Chromium, Firefox) rather than minimalistic environments. Explicitly wait for the reCAPTCHA JavaScript API (`grecaptcha` object and its methods) to be fully loaded and initialized before interaction. |
    | **Consistency & Persistence**       | **Issue:** Browser sessions are short-lived, lack consistent user profiles, or frequently clear cookies/local storage. | **Solution:** Use persistent browser contexts (`user_data_dir`) to simulate a long-term user profile with accumulated browsing data and cookies, fostering trust over time. |

### B. What are the two ways to inject tokens?

In the context of reCAPTCHA v3 and automation, "injecting tokens" generally refers to how the generated reCAPTCHA response token (`g-recaptcha-response`) is made available for server-side verification. Here are two primary methods:

1.  **Client-Side HTML Form Field (Standard Method for Web Applications):**
    *   **Description:** This is the most common and intended way reCAPTCHA tokens are handled in traditional web forms. After reCAPTCHA v3 executes on the client-side (in the user's browser) and obtains a token, that token is programmatically inserted into a hidden HTML input field within a form.
    *   **Mechanism:** The reCAPTCHA JavaScript API typically handles this automatically, creating an input element like `<input type="hidden" name="g-recaptcha-response" value="YOUR_TOKEN_VALUE">`. When the user submits the form, this hidden field's value (the token) is sent along with other form data to the web server as part of the POST request body.
    *   **Server-Side:** The backend server then extracts this `g-recaptcha-response` value and sends it to Google's reCAPTCHA API endpoint (`https://www.google.com/recaptcha/api/siteverify`) along with the secret key for verification.

2.  **Direct Retrieval and API Transmission (Common in Automation/Custom Clients):**
    *   **Description:** In automation scripts, single-page applications (SPAs), or custom client implementations where a traditional HTML form submission might not be used, the reCAPTCHA token is explicitly retrieved and then sent to a backend API.
    *   **Mechanism:**
        *   **Automation:** A browser automation script (like Playwright in `Task2/api.py`) can:
            *   Intercept network requests (e.g., a `google.com/recaptcha/api2/reload` request) and extract the token from its response.
            *   Execute JavaScript on the page to directly access `grecaptcha.getResponse()` or similar methods to get the token.
            *   Extract the token from a specific DOM element where it might be displayed or stored.
        *   **Client/SPA:** The client-side JavaScript manually calls `grecaptcha.execute()` or `grecaptcha.getResponse()` and then sends the obtained token in a custom AJAX/Fetch request to a specific backend endpoint (e.g., `/recaptcha/in` as seen in `Task2`).
    *   **Server-Side:** The custom backend endpoint receives this token and then performs the necessary server-to-server verification with Google's reCAPTCHA API. This method offers more flexibility and control over the verification flow.

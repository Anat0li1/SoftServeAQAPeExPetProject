# Selenium Python Automation Framework

**An evolving UI test automation project built with Python, Selenium WebDriver, and Pytest.**

This project focuses on automating real-world web application scenarios using [Practice QA Automation](https://www.practiceqaautomation.com/) — an interactive platform designed for practicing Selenium, Playwright, and Cypress automation.

The main goal is to build a maintainable, scalable, and reusable UI automation framework while gradually developing practical test automation skills and applying industry best practices.

> **Project status:** In Progress 🚧  
> Currently focused on developing individual automation scripts and exploring different web application scenarios. Framework architecture, refactoring, and CI/CD integration will be introduced incrementally.

---

## 🎯 Project Objectives

- Practice UI automation against realistic web applications.
- Develop reliable and maintainable Selenium WebDriver scripts.
- Apply Pytest features for test execution, fixtures, parameterization, and test organization.
- Explore different locator strategies and interaction patterns.
- Learn to handle dynamic web elements, waits, browser windows, alerts, and frames.
- Gradually transition from standalone scripts to a structured automation framework.
- Implement reusable components and follow Page Object Model (POM) principles.
- Integrate automated test execution into GitHub Actions.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Selenium WebDriver | Browser automation |
| Pytest | Test execution and test management |
| Git | Version control |
| GitHub | Source code hosting |
| GitHub Actions | CI/CD automation (planned) |
| HTML Reporting | Test execution reports (planned) |

Additional tools and libraries will be introduced as the project evolves.

---

## 🌐 Application Under Test

The primary testing environment is [Practice QA Automation](https://www.practiceqaautomation.com/).

It provides realistic web applications and dedicated challenges for practicing different automation techniques.

### Application scenarios

The platform offers multiple application domains, including:

- **E-commerce:** Product search, filtering, shopping cart, coupons, and checkout.
- **Banking:** Authentication, transactions, OTP verification, and account management.
- **Entertainment:** Event selection, seat booking, and payment workflows.
- **Hospitality:** Hotel search, room selection, and reservation management.
- **Travel:** Flight search, passenger details, and booking workflows.
- **Project Management:** Kanban boards, issue management, and drag-and-drop interactions.

### UI automation challenges

The project will also cover individual UI components and browser interactions:

- Forms and input validation
- Checkboxes, radio buttons, and dropdowns
- Tables, pagination, and dynamic elements
- Alerts, browser windows, and frames
- Explicit waits and dynamic loading
- Hover, drag-and-drop, and keyboard interactions
- File upload and download
- Shadow DOM and complex locators
- Browser notifications and other interactive elements

The selection of scenarios will evolve based on learning objectives and implementation complexity.

---

## 📂 Project Structure

The project structure will evolve as the framework develops.

The intended structure is:

```text
selenium-python-framework/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── config/
│   └── config.conf
│
├── pages/
│   ├── base_page.py
│   └── ...
│
├── tests/
│   ├── test_login.py
│   ├── test_forms.py
│   └── ...
│
├── fixtures/
│   └── ...
│
├── utils/
│   └── ...
│
├── reports/
├── screenshots/
│
├── conftest.py
├── requirements.txt
├── pytest.ini
└── README.md
```

*Note: This represents the planned framework organization and may differ from the current implementation.*

---

## 🗺️ Implementation Roadmap

The framework will be developed incrementally, starting with simple automation scripts and gradually evolving into a structured test automation solution.

### Phase 1 — Initial Automation Scripts

- [ ] Set up the Python development environment.
- [ ] Configure Selenium WebDriver.
- [ ] Set up Pytest.
- [ ] Explore the target application's functionality.
- [ ] Implement basic UI automation scripts.
- [ ] Practice different locator strategies.
- [ ] Implement browser interactions and element handling.
- [ ] Explore explicit waits and dynamic elements.

**Goal:** Gain practical experience with Selenium and automate individual application scenarios.

### Phase 2 — Framework Architecture & Refactoring

- [ ] Introduce a structured project architecture.
- [ ] Implement Page Object Model (POM).
- [ ] Create reusable BasePage functionality.
- [ ] Centralize browser initialization and teardown.
- [ ] Implement reusable Pytest fixtures.
- [ ] Introduce dynamic configuration loading.
- [ ] Externalize test data.
- [ ] Implement reusable helper methods and utilities.
- [ ] Organize tests using Pytest markers.
- [ ] Introduce test parameterization.

**Goal:** Transform individual scripts into a maintainable and reusable automation framework.

### Phase 3 — Reporting & Debugging

- [ ] Integrate HTML test reports.
- [ ] Implement automatic screenshot capture on test failures.
- [ ] Introduce structured logging.
- [ ] Improve exception handling.
- [ ] Organize test execution results and artifacts.

**Goal:** Make test execution transparent and simplify failure analysis.

### Phase 4 — CI/CD Integration

- [ ] Set up GitHub Actions workflows.
- [ ] Configure automatic execution on push and pull requests.
- [ ] Add manual workflow execution.
- [ ] Configure Python environment and browser dependencies.
- [ ] Execute Pytest suites in CI.
- [ ] Upload test reports, screenshots, and logs as workflow artifacts.
- [ ] Introduce GitHub Secrets for sensitive configuration.
- [ ] Explore scheduled test execution.

**Goal:** Automate test execution and establish a reliable CI pipeline.

### Phase 5 — Advanced Framework Capabilities

- [ ] Introduce parallel test execution using pytest-xdist.
- [ ] Implement cross-browser testing.
- [ ] Explore different test environments.
- [ ] Improve test data management.
- [ ] Introduce advanced Pytest features.
- [ ] Evaluate additional reporting and debugging tools.
- [ ] Improve framework scalability and maintainability.

**Goal:** Extend the framework with advanced automation capabilities and improve its overall reliability.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Google Chrome
- Git

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd selenium-python-framework
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the environment:

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the available tests:

```bash
pytest -v
```

---

## 🔄 CI/CD

GitHub Actions will be used to automate framework validation and test execution.

The planned pipeline will include:

- Automated workflow triggers on push and pull requests.
- Python environment setup.
- Dependency installation.
- Automated Pytest execution.
- HTML report generation.
- Screenshot and log collection.
- Workflow artifact storage.

The CI pipeline is currently under development.

---

## 📚 Learning Resources

- [Practice QA Automation](https://www.practiceqaautomation.com/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 📌 Project Philosophy

This project is being developed as a practical learning and engineering exercise.

Rather than building the entire framework upfront, development starts with small, functional automation scripts. As the number and complexity of test scenarios grow, the codebase will be progressively refactored into a structured framework.

The focus is on understanding not only how to automate UI interactions, but also how to design, organize, maintain, debug, and execute automated tests in a real development workflow.

**The ultimate objective is to build a practical Selenium + Pytest automation framework that demonstrates both hands-on automation skills and an understanding of modern test automation engineering practices.**
# Contributing to the Real Estate System

We welcome contributions from the community! By following this guide, you can help improve the real estate system effectively.

## Table of Contents
1. [How Can I Contribute?](#how-can-i-contribute)
2. [Setting Up the Project Locally](#setting-up-the-project-locally)
3. [Development Guidelines](#development-guidelines)
4. [Submitting Changes](#submitting-changes)
5. [Coding Style](#coding-style)
6. [Pull Request Checklist](#pull-request-checklist)
7. [Code of Conduct](#code-of-conduct)

---

## How Can I Contribute?

### Reporting Bugs
- Open a new issue in the [GitHub Issues](https://github.com/trent130/hello/issues) tab.
- Include details like:
  - The issue title (brief and descriptive).
  - Steps to reproduce the problem.
  - The expected vs actual behavior.
  - Screenshots or logs (if applicable).
  - The environment (operating system, browser, database, etc.).

### Suggesting Enhancements
- Create a feature request under the Issues tab.
- Describe the enhancement and the problem it solves.
- Explain why this feature would be useful for users or developers.

### Improving Documentation
- Help us by improving or adding documentation in areas like API usage, installation instructions, or examples.
- Feel free to open a pull request with updates to the `/docs` folder.

---

## Setting Up the Project Locally

1. **Fork the Repository:**
   - Fork this repo to your own GitHub account.

2. **Clone the Fork:**
   ```bash
   git clone https://github.com/trent130/hello.git
   cd hello
   ```

### Install Dependencies:
- **For backend (Django + DRF):**
   ```bash
   pip install -r requirements.txt
   ```
- **For frontend (Next.js):**
```bash
npm install
```
### Set Up the Environment Variables:
 - Create a .env file in the project root for the backend and frontend settings.

### Run Migrations:
   ```bash
   python manage.py migrate
   ```
Run the Development Servers:
- **Backend (Django):**
```bash
python manage.py runserver
```
- **Frontend (Next.js):**
```bash
npm run dev
```
### Development Guidelines
- **Feature Branches:**
  - Always create a new branch from the main branch for any changes:
   ```bash
    git checkout -b feature/my-feature
   ```
   - Write Clear Commit Messages:
     Keep your commit messages descriptive:
     ```bash
     git commit -m "Add user authentication API"
     ```
### Run  Tests:
  - Ensure all tests pass before committing:
    ```bash 
    python manage.py test
    ``` 
### Keep Your Fork Updated:
   - Sync your fork with the latest changes:
    ```bash
     git fetch upstream
     git merge upstream/main
    ```
## Submitting Changes
### Pull Requests:
- Push your changes to your feature branch:

   ```bash
   git push origin feature/my-feature
   ```
 - Create a pull request (PR) on GitHub:
    - Provide a detailed description of the changes.
    - Reference any related issues (e.g., Closes #123).
### Review Process:
 - All PRs will be reviewed by maintainers. Feedback may be provided for improvements.
 - Rebase and Resolve Conflicts: 
 - If your PR has conflicts, rebase on top of the latest main and resolve conflicts:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```
### Coding Style
- Python (Django Backend):
  - Follow PEP 8 coding standards.
  - Use descriptive variable and function names.
  - Format code with tools like black and check linting with flake8.
- JavaScript (Next.js Frontend):
  - Follow Airbnb JavaScript Style Guide.
  - Use prettier and eslint to maintain code consistency.
- Commit Messages:
  - Use present tense (“Fix bug” not “Fixed bug”).
  - Limit the first line to 72 characters or less.
### Pull Request Checklist
   - My code follows the project’s coding style and best practices.
   - I have updated/added documentation where needed.
   - I have added relevant tests.
   - All tests are passing locally.
### Code of Conduct
By contributing to this project, you agree to follow our Code of Conduct. We are committed to fostering an inclusive and respectful community.

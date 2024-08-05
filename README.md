[![codecov](https://codecov.io/gh/hochungyan/learning_management_system/branch/main/graph/badge.svg)](https://codecov.io/gh/hochungyan/learning_management_system)
![CodeQL and Coverage](https://github.com/hochungyan/learning_management_system/actions/workflows/codeql-analysis.yml/badge.svg)
[![Known Vulnerabilities](https://snyk.io/test/github/hochungyan/learning_management_system/badge.svg)](https://snyk.io/test/github/hochungyan/learning_management_system)

# Learning Management System

This project is a comprehensive, advanced full-stack Learning Management System (LMS) built from scratch using Django for the backend and React for the frontend. The system is designed to provide essential features for both learners and instructors, facilitating a dynamic and interactive online learning experience.

## Features

### Django Backend
* Master Django fundamentals: models, views, templates, and database management
* Secure authentication and user management
* Course and user management
* Instructor dashboard with course, student, review, and earnings management
* Interactive discussion forums
* API development for integrations

### React Frontend
* Solid understanding of React fundamentals: components, state management, and routing
* Dynamic and visually appealing user interface
* Advanced search and filtering functionalities
* Real-time progress tracking and personalized recommendations
* Messaging systems and discussion threads for communication

### Additional Features
* Secure payment integration with Stripe and PayPal
* Analytics and reporting for informed decision-making

## Installation

### Prerequisites
* Python 3.x
* Node.js and npm
* Django
* React

### Backend Setup
1. Clone the repository: `git clone https://github.com/hochungyan/learning_management_system.git`
2. Navigate to the backend directory: `cd learning_management_system/backend`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   * On Windows: `venv\Scripts\activate`
   * On macOS and Linux: `source venv/bin/activate`
5. Install the required packages: `pip install -r requirements.txt`
6. Run migrations: `python manage.py migrate`
7. Start the Django development server: `python manage.py runserver`

### Frontend Setup
1. Navigate to the frontend directory: `cd ../frontend`
2. Install the required npm packages: `npm install`
3. Start the React development server: `npm start`

## Usage
After starting both the backend and frontend servers, you can access the application at `http://localhost:3000`.

## CI/CD Workflow

This project uses GitHub Actions for continuous integration and deployment. The CI/CD pipeline includes:

* **Setup**: Checkout code, set up Python environment, and install dependencies
* **Code Quality**: Linting with `flake8`, pre-commit hooks, and Sourcery analysis
* **Testing**: Running tests with `pytest` and generating coverage reports with `coverage.py`
* **Security Analysis**: Using CodeQL and Snyk to identify security vulnerabilities
* **Deployment**: Automated deployment to production on successful builds from the main branch

The workflow runs on pushes to `main` and `develop` branches, pull requests to these branches, and every Wednesday at 1:00 AM.

### Sourcery Code Quality Check

The workflow includes a Sourcery code quality check. Note that:

- Sourcery primarily analyzes code files, with a focus on Python by default.
- If your repository only contains non-code files (like README.md), Sourcery may report scanning 0 files.
- To benefit from Sourcery's analysis, ensure your repository contains the appropriate code files.

For more details on the CI/CD process, please refer to the [CI/CD Workflow documentation](./CI_CD_WORKFLOW.md).

## Contributing

As this is a personal project, contributions are not currently being accepted. However, feedback and suggestions are always welcome. Feel free to open an issue if you have any ideas or encounter any problems.

## License

This project is personal work and is not open for licensing or redistribution at this time. All rights reserved. © Chung Ltd 2024

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* Have fun!

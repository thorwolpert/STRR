# STRR E2E Automated Testing

## Running E2E Tests

Built test can be run locally or in a CI/CD pipeline.

### Prerequisites

In order to run the tests locally, you will need to do the following:

- Clone the repo
- Navigate to the root of the tests **(<repo>/testing)**
  - run `npm install` (Only needs to run once or when you change the config.)
  - Copy cypress.env.example.json to cypress.env.json and fill in the parameters. (This file will be ignored when you upload your code)
    - edit the values as per your configs
  - Run `npx cypress open` to open the interactive Cypress test runner
  - Click on the test you want to run [Quick Cypress overview below](https://github.com/bcgov/sso-requests-e2e/edit/main/docs/Home.md#cypress-overview)
    or
  - If you simply want to run all your tests: `npx cypress run --browser chrome`
  - Alternatively you can run your tests by:
    - `npm run test`
    - `npm run smoke` - Only runs the smoke tests

### Running Tests in GitHub Actions

Github Action workflows are defined in the `.github/workflows` directory.

The workflow is currently triggered on a manual start `workflow_dispatch`. It will run the tests in a headless browser and report the results in GitHub.
Integrated in a CI the workflow is triggered on push to the main branch or a PR.

### Test Results

In addition to console reporting, Cypress also provides reporting in GitHub after a run in GitHub Actions. This is useful for tracking and analyzing test results over time.

Cypress also offers reporting in the interactive test creation tool when running an individual test locally. This is helpful for debugging and identifying issues with individual tests.

### Cypress Overview

By default the tests will run in the `Electron Browser`

When running the test, wait for the timer to finish or look for the green check near the test name
![image](https://github.com/bcgov/sso-requests-e2e/assets/56739669/4bcb236e-407e-4feb-b9bf-256dbaff2a54)

To confirm the test is complete, you can see results based on the pass(green check) or fail (red x) status.

![image](https://github.com/bcgov/sso-requests-e2e/assets/56739669/1aefd733-b591-4e3b-b5e8-b1d22fd95cc4)

## What is in the directories?

The test framework is based on [Cypress](https://www.cypress.io/). It is designed to be run in a CI/CD pipeline, but can also be run locally.
It comes with several support directories for documentaton, media and testing.

### \_.github/workflows

Contains an e2e sample workflow for running Cypress in Github actions. You can use this as a starting point for your own implementation.

### \_testing

The main test framework is contained in this directory. It is a standard Cypress framework with a few additions.

#### \_testing/cypress

Contains the Cypress-based test framework. All tests and supporting files are contained in this directory.

##### \_testing/cypress/e2e

In this directory we store the actual test scripts.

##### \_testing/cypress/appActions

In this directory we store the application actions for the Cypress tests.
Application actions are used to store methods for interacting with the application. This will result in compact and readable test scripts that simply call an action (like createNewUser) instead of having to write the full interaction code in the test script.

##### \_testing/cypress/pageObjects

In this directory we store the page objects for the Cypress tests.
Page objects are used to store selectors and methods for interacting with the application.

This way we centralize the selectors and methods and can reuse them in multiple tests or when the application changes we would only have one location to change the definition.

## Useful Resources

- Official Cypress Documentation: https://docs.cypress.io/
- Cypress GitHub Repository: https://github.com/cypress-io/cypress
- Cypress Example Recipes: https://github.com/cypress-io/cypress-example-recipes
- Cypress Community: https://www.cypress.io/community/

## License

Copyright © 2024 Province of British Columbia

Licensed under the BSD 3 Clause License, (the "License");
you may not use this file except in compliance with the License.
The template for the license can be found here
   https://opensource.org/license/bsd-3-clause/

Redistribution and use in source and binary forms,
with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

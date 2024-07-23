


## Documenting Changes to the CI/CD Pipeline

#### Original CI/CD Pipeline Configuration

The initial configuration of the CI/CD pipeline for your project was as follows:

    name: CI/CD Pipeline
    on:
     push:
     branches:
     - main
     pull_request:
     branches:
     - main
    jobs:
     build:
     runs-on: ubuntu-latest
     steps:
     - name: Checkout code
     uses: actions/checkout@v2
     - name: Set up Python
     uses: actions/setup-python@v2
     with:
     python-version: '3.8'
     - name: Install dependencies
     run: |
     python -m pip install --upgrade pip
     pip install -r requirements.txt
     - name: Run tests
     run: |
     pytest
     - name: Train model
     run: |
     python train.py
     - name: Deploy model
     run: |
     echo "Deploying model..."
     # Simulate deployment step
     if [ -f "model.joblib" ]; then echo "Model deployed successfully"; else echo "Model deployment failed"; exit 1; fi` 

The pipeline was designed to:

1.  Check out the code from the repository.
2.  Set up a Python 3.8 environment.
3.  Install dependencies from `requirements.txt`.
4.  Run tests using `pytest`.
5.  Train the model using `train.py`.
6.  Deploy the model if the file `model.joblib` exists.

#### Issue Encountered

The pipeline failed at the "Run tests" step with the following error:

    ============================= test session starts ==============================
    platform linux -- Python 3.8.18, pytest-6.2.4, py-1.11.0, pluggy-0.13.1
    rootdir: /home/runner/work/gitactions/gitactions
    collected 0 items / 1 error
    ==================================== ERRORS ====================================
    _____________________ ERROR collecting test/test_train.py ______________________
    ImportError while importing test module '/home/runner/work/gitactions/gitactions/test/test_train.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    /opt/hostedtoolcache/Python/3.8.18/x64/lib/python3.8/importlib/__init__.py:127: in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
    test/test_train.py:3: in <module>
        from ..train import train_and_save_model
    E   ImportError: attempted relative import with no known parent package
    =========================== short test summary info ============================
    ERROR test/test_train.py
    !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
    =============================== 1 error in 0.33s ===============================
    Error: Process completed with exit code 2.

The error indicates that the `train` module could not be found, causing the tests to fail.

#### Solution Implemented

To resolve the issue, the `PYTHONPATH` environment variable was updated to include the current working directory (`$PWD`). This change ensures that Python can locate the `train` module during the test phase. The updated pipeline configuration is as follows:



    name: CI/CD Pipeline
    on:
      push:
        branches:
          - main
      pull_request:
        branches:
          - main
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout code
            uses: actions/checkout@v2
          - name: Set up Python
            uses: actions/setup-python@v2
            with:
              python-version: '3.8'
          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt
          - name: Run tests
            run: |
              export PYTHONPATH="$PYTHONPATH:$PWD"
              pytest test
          - name: Train model
            run: |
              python train.py
          - name: Deploy model
            run: |
              echo "Deploying model..."
              if [ -f "model.joblib" ]; then echo "Model deployed successfully";
              else echo "Model deployment failed"; exit 1; fi 

#### Explanation of the Change

1.  **Original Error**:
    
    -   The error was due to the test module not being able to find the `train` module.
2.  **Modification**:
    
    -   Added the line `export PYTHONPATH="$PYTHONPATH:$PWD"` to the "Run tests" step. This line appends the current working directory to the `PYTHONPATH`.
3.  **Result**:
    
    -   This change allows `pytest` to find and import the `train` module correctly, resolving the `ModuleNotFoundError` and enabling the tests to run successfully.

By making this adjustment, the pipeline can now correctly locate all necessary modules during testing, ensuring that the tests pass and the pipeline proceeds to subsequent steps.

### Real-Time Inference Pipeline with AWS CodePipeline, CodeBuild, and SageMaker/EC2
We'll focus on setting up an AWS CodePipeline that utilizes AWS CodeBuild for building, testing, and training the model, and then deploying it using Amazon SageMake/EC2

#### AWS Services and Architecture Diagram

We'll leverage the following AWS services:

1. **AWS CodeCommit**: For source code.
2. **AWS CodePipeline**: For CI/CD pipeline orchestration.
3.  **AWS CodeBuild**: For running the build and test steps.
4.  **Amazon S3**: For storing the trained model.
5.  **Amazon SageMaker/EC2**: For deploying the model as an endpoint for real-time inference.
6.  **Amazon CloudWatch**: For logging and monitoring.
7.  **Amazon SNS**: For logging and monitoring's notifications. 

#### Architecture Diagram

Ref :

> ArchitectureDiagram.png




### Real-Time Inference Placeholder

While the detailed implementation of the placeholder for handling API requests (e.g., EC2, Lambda) is skipped, you can follow these steps based on your choice:

1.  **EC2**:
    
    -   Set up a RESTful API on an EC2 instance.
    -   Use the instance to handle incoming requests and invoke the SageMaker endpoint.
2.  **AWS Lambda**:
    
    -   Create a Lambda function with the logic to call the SageMaker endpoint.
    -   Use Amazon API Gateway to expose the Lambda function as a RESTful API.
3.  **Other Services**:
    
    -   You can use services like AWS Fargate, AWS App Runner, or any other compute service to handle incoming requests and forward them to the SageMaker endpoint.

### Summary

-   **AWS CodePipeline**: Orchestrates the CI/CD process.
-   **AWS CodeBuild**: Runs the build, test, and training steps.
-   **Amazon S3**: Stores the trained model artifact.
-   **Amazon SageMaker**: Deploys the model as a real-time endpoint.
-   **Placeholder for Request Handling**: EC2, Lambda, or another service to handle API requests.
-   **Amazon CloudWatch**: Monitors logs and performance metrics.

This approach provides a clear, scalable, and flexible architecture for deploying and using a real-time inference model with AWS services.

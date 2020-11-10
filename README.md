# Serverless cloud functions
## Contents

1. [Quick Start](#Quick-Start)
2. [Examples](#Examples)
3. [Features](#Features)
4. [Community](#Community)
5. [Licensing](#Licensing)

## Quick Start

1. Install via pip:
    ```
    pip install sels8s
    ```
2. Download rc.sh file from [Selectel panel](https://my.selectel.ru/vpc)
3. Set environment variables:
    -OS_USERNAME - your username in panel
    -OS_PASSWORD - your password
    -OS_PROJECT_ID - your project id
    -OS_PROJECT_DOMAIN_NAME - your project domain name
    -OS_USER_DOMAIN_NAME - your user domain name
4. Create your own cloud function:
    ```
    import sels8s

    serverless = sels8s.Serverless()

    # upload file
    module = serverless.upload_module('/home/my_file.py')

    # create function
    serverless.create_function('my_function')

    # add your code and params
    params = {'function_id': module['function_id'],
              'function_name': 'name_of_function_in_code',
              'module_name':'my_file.py',
              'env_vars':{'key':'value'},
              'runtime': 'python',
              'version': '3.7'}
    serverless.edit_function('my_function', params)

    # invoke your function
    activation = serverless.invoke_function('my_function')

    # get logs and results
    logs = serverless.get_activation_logs(activation['activation_id'])
    result = serverless.get_activation_result(activation['activation_id'])
    ```
## Examples

You can see examples of using cloud functions
[here](https://github.com/selectel/serverless_functions_examples_python)

## Features

[Cloud functions](https://selectel.ru/services/cloud/serverless/)

[Docs](https://kb.selectel.ru/docs/selectel-cloud-platform/serverless/description/)

## Community

[GitHub](https://github.com/selectel/serverless-python)

For all questions - sls@selectel.ru

## Licensing

Serverless is licensed under the [MIT License](https://github.com/selectel/serverless-python/LICENSE).
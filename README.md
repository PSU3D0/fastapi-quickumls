# FastAPI QuickUMLS Server

## Introduction

FastAPI QuickUMLS Server is an open-source project that provides a high-throughput API server by wrapping QuickUMLS with FastAPI and leveraging multiprocessing capabilities.


## Features

- **High Throughput**: Optimized for performance in multi-core environments.
- **Multiprocessing Support**: Leverages multiprocessing for concurrent handling of UMLS matching requests.
- **FastAPI Framework**: Built on FastAPI, known for its high performance and easy-to-use interface.
- **Open Source**: Free to use, modify, and distribute.

## Installation

1. Clone the repository:
   ```
   git clone git@github.com:PSU3D0/fastapi-quickumls.git
   ```

2. Navigate to the cloned directory:
   ```
   cd fastapi-quickumls
   ```

3. Install dependencies:
   ```
   pip install -r requirements/local.txt
   ```
4. Create a directory - `umls` in the repo, and unzip your UMLS files here.

5. Confirm your path is valid - You should now have a `umls/umls-2023AA-metathesaurus-full`

6. Run `docker compose build`. This will take a while!

## Usage

1. Start the server:
   ```
  docker compose up -d
   ```

2. Access the API documentation at `http://localhost:4645/docs`.

## API Endpoints

- `GET /match`: Matches given text to UMLS concepts.
  - Input: Text string for matching.
  - Output: List of matched UMLS concepts.

## Configuration

- **QuickUMLS Path**: Set the QuickUMLS file path in the server configuration.
- **Maximum Workers**: Configure the number of worker processes for multiprocessing.

## Contributing

Contributions to FastAPI QuickUMLS Server are welcome! Please refer to the `CONTRIBUTING.md` file for guidelines.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- QuickUMLS for the underlying UMLS matching functionality.
- FastAPI for the web server framework.

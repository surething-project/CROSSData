<p align="center">
    <img src="./assets/CROSS-Logo.png" width="200" height="200" alt="CROSS Logo"/>
</p>

<h3 align="center">SureThing_CROSS_Data</h3>

---

<p align = "center">Protobuf data type definitions and API service specification of CROSS</p>

## Structure

| Directory                                  |               Description                |
|:-------------------------------------------|:----------------------------------------:|
| [CROSS-Contract](CROSS-Contract)           |      CROSS Contract Project (Maven)      |
| [CROSS-Contract-Lite](CROSS-Contract-Lite) |   CROSS Contract Lite Project (Gradle)   |
| [openapi](openapi)                         | CROSS REST API specification _(OpenAPI)_ |
| [proto](proto)                             | CROSS Protobuf data message definitions  |

## Table of Contents

- [Build the Contract](#build-the-contract)
    - [Contract Prerequisites](#contract-prerequisites)
    - [Resolve the Dependencies and Build the Contract](#resolve-the-dependencies-and-build-the-contract)
- [Build the Lite Contract](#build-the-lite-contract)
    - [Lite Contract Prerequisites](#lite-contract-prerequisites)
    - [Resolve the Dependencies and Build the Lite Contract](#resolve-the-dependencies-and-build-the-lite-contract)
- [Process to Produce the API Specification](#process-to-produce-the-api-specification)
    - [Prerequisites](#prerequisites)
    - [Protobuf to OpenAPI Conversion Process](#protobuf-to-openapi-conversion-process)
- [Authors](#authors)

## Build the Contract

### Contract Prerequisites

- Java Development Kit (JDK) >= 11
- Maven >= 3.8

### Resolve the Dependencies and Build the Contract

From the root of the project change directory:

```shell script
cd CROSS-Contract
```

Execute:

```shell script
mvn clean install
```

## Build the Lite Contract

For the mobile client application (Android)

### Lite Contract Prerequisites

- Java Development Kit (JDK) >= 11
- Gradle >= 7.2

### Resolve the Dependencies and Build the Lite Contract

From the root of the project change directory:

```shell script
cd CROSS-Contract-Lite
```

Execute:

```shell script
./gradlew clean build
```

## Process to Produce the API Specification

### Prerequisites

- Go >= 1.17
- Python >= 3.8.10
- Protocol Buffer Compiler (Protoc) >= 3.6.1
- [protoc-gen-openapi](https://github.com/google/gnostic/tree/master/cmd/protoc-gen-openapi) plugin

### Protobuf to OpenAPI Conversion Process

Here we go over the process followed to specify a REST API in Protobuf and produce an equivalent OpenAPI specification:

1. The API is defined using RPCs, following the [Google APIs Guidelines](https://google.aip.dev/127), to be presented as
   an API that follows the REST convention. As examples, our proto defined files can be found at [proto](proto),
   alongside the Google related dependencies at [proto/google](proto/google).

   A detailed example of a POST endpoint _(for creating a book)_ receiving a protobuf body _(CreateBookRequest)_, inline
   param in the query path and returning a protobuf response _(Book)_ can be found [here](https://google.aip.dev/127).

2. Convert the Proto files using
   the [gnostic protoc-gen-openapi plugin](https://github.com/google/gnostic/tree/master/cmd/protoc-gen-openapi) to
   an **openapi.yml** file by executing the following command:

    ```shell script
    protoc [PROTO-FILES] -I. --openapi_out=.
    ```

   For example, with only the Dataset.proto and Reward.proto files the command executed would be:

    ```shell script
    protoc Dataset.proto Reward.proto -I. --openapi_out=.
    ```

3. OpenAPI lacks the proper support of the protobuf media type, therefore we change the payloads of each endpoint to
   _application/x-protobuf_ using the following command:

    ```shell script
    sed -i 's/application\/json/application\/x-protobuf/g' ./openapi.yaml
    ```

4. We generate an html file of the OpenAPI specification to be easily visualized through a browser, using
   the [swagger-yaml-to-html.py](openapi/swagger-yaml-to-html.py) python script:

    ```shell script
    python swagger-yaml-to-html.py < /path/to/openapi.yaml > openapi.html
    ```

## Authors

| Name              | University                 | More info                                                                                                                                                                                                                                                                                                                                                                                       |
|-------------------|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Lucas Vicente     | Instituto Superior Técnico | [<img src="https://i.ibb.co/brG8fnX/mail-6.png" width="17">](mailto:lucasdhvicente@gmail.com "lucasdhvicente@gmail.com") [<img src="https://github.githubassets.com/favicon.ico" width="17">](https://github.com/WARSKELETON "WARSKELETON") [<img src="https://i.ibb.co/TvQPw7N/linkedin-logo.png" width="17">](https://www.linkedin.com/in/lucas-vicente-a91819184/ "lucas-vicente-a91819184") |
| Rafael Figueiredo | Instituto Superior Técnico | [<img src="https://i.ibb.co/brG8fnX/mail-6.png" width="17">](mailto:rafafigoalexandre@gmail.com "rafafigoalexandre@gmail.com") [<img src="https://github.githubassets.com/favicon.ico" width="17">](https://github.com/rafafigo "rafafigo") [<img src="https://i.ibb.co/TvQPw7N/linkedin-logo.png" width="17">](https://www.linkedin.com/in/rafafigo/ "rafafigo")                               |
| Ricardo Grade     | Instituto Superior Técnico | [<img src="https://i.ibb.co/brG8fnX/mail-6.png" width="17">](mailto:ricardo.grade@tecnico.ulisboa.pt "ricardo.grade@tecnico.ulisboa.pt") [<img src="https://github.githubassets.com/favicon.ico" width="17">](https://github.com/RicardoGrade "RicardoGrade") [<img src="https://i.ibb.co/TvQPw7N/linkedin-logo.png" width="17">](https://www.linkedin.com/in/RicardoGrade "RicardoGrade")      |

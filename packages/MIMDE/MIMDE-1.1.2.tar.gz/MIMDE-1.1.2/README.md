![mimde](./data/icon.png)
# MIMDE: Multi Insight Multi Document Extraction

The MIMDE toolkit is a set of tools for extracting insights from government consultations. This toolkit takes as input a machine-readable consultation dataset in tabular format, with one row per response and one or more columns per question. Methods for non-tabular data may be available in a future version. The output of this toolkit is two paired datasets: one containing the extracted insights for each free-text question and the other containing the thematic tagging of responses for each extracted insight.

## Installation

To install MIMDE, simply run the following command:

```
pip install MIMDE
```

## Upgrade

```
pip install --upgrade MIMDE
```

## Usage

Here's a simple example to get you started with MIMDE:

```python
import MIMDE
MIMDE.Brute_force_pipeline('src/config/config.yaml')
```

## Contributing

We welcome contributions from the community! If you have any ideas, bug reports, or feature requests, please open an issue on our [GitHub repository](https://github.com/ai-for-public-services/MIMDE).

1. Clone the repository on your local machine. 
2. Make a new branch from main and add your own code
3. Commit your changes and push them on github
4. Request a merge! 

## Building
Steps for updating the package after adding your contribution
1. Fix any bug or add enhancement code
1. Increase the version in setup.py e.g. version="1.0.0" -> version="1.0.1"
2. Clean the previous build in local repo: ``` rm -rf dist build *.egg-info ```
3. Buid the new version: ``` python setup.py sdist bdist_wheel ```
4. Distribute your contribution: ``` twine upload dist/*  ```


## License

MIMDE is released under the [MIT License](https://opensource.org/licenses/MIT).

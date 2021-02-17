# PopCornAgent

###### _Authors:  macasal & sgalella_

Movie recommendation agent written in Python 3.6. Ask and finds the best film to recommend from an ontology including 30 different movies.

The search parameters are the following:
1. year
2. duration
3. country
4. genre
5. rate in IMDb
6. director
7. actor or actress


## Installation

To install all the different dependencies of the project run:

```
pip install -r requirements.txt
```

Then, to run the agent, type:

```
python -m popcorn_agent
```

If using Conda, you can also create an environment with the requirements:

```bash
conda env create -f environment.yml
```

By default the environment name is `popcorn-agent`. To activate it run:

```bash
conda activate popcorn-agent
```


## Images

Dialogue:
<p>
  <img width="592" height="209" src="images/dialogue.jpg">
</p>

Information collected from IMDb:
<p align="center">
  <img width="880" height="509" src="images/crawler.jpg">
</p>

# Master Thesis | Optimizer Framework

This repository holds the optimizer framework as proposed in my Master Thesis. It contains a generic optimizer class that can be used to implement various optimization algorithms for various use cases. One of these use cases is the Game Optimizer, which can be used to optimize the accompanying game made for this thesis.

## Table of Contents

- [Master Thesis | Optimizer Framework](#master-thesis--optimizer-framework)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Installation

The in-game optimizer uses NLopt, so it is advised to install this in a virtual environment. To do this, run the following commands:

```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r ./code/requirements.txt
```

## Usage

Running the example code can be done by running the following command:

```bash
    python main.py
```

Adapting the parameters for the Game optimizer should be done inside the `Parameters.py` file. This allows you to set minimum and maximum values for the parameters, as well as the type. The optimization code itself is located in the `GameOptimizer.py` file. There you can set the NLopt optimization algorithm (currently using COBYLA) as well as the stopping criterion and objective function (by changing how the `score_game(...)` method calculates it).


## License


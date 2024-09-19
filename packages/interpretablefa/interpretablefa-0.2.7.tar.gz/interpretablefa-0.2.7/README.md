# `interpretablefa`
## Overview
This is a package for performing interpretable factor analysis. This implements the several indices, as well as the priorimax and interpmax rotations and procedures, which are described [here](https://arxiv.org/abs/2409.11525).

It also contains several helper and visualization functions and wraps several functions from the `factor_analyzer` package.

For more details about the methods implemented and some of the package's features, see [Interpretability Indices and Soft Constraints for Factor Models](https://arxiv.org/abs/2409.11525).

The linked paper provides some documentation to the package and docstrings are available. However, a comprehensive guide or documentation is still under development.
## Example
For instance, suppose that `data` contains the dataset, `q` contains the questions, and `p` is the soft constraints matrix. Then, one can fit a 4-factor priorimax model using the snippet below.
```
import pandas as pd
from interpretablefa import InterpretableFA

# load the dataset and the questions
data = pd.read_csv("./data/ECR_data.csv")
with open("./data/ECR_questions.txt") as questions_file:
    q = questions_file.read().split("\n")
    questions_file.close()

# define a partial soft constraints matrix
g = [[1, 7, 9, 11, 13, 17, 23], [6, 10, 12], [14, 16, 26, 36], [20, 28, 32, 34]]
p = InterpretableFA.generate_grouper_prior(len(q), g)

# fit the factor model
analyzer = InterpretableFA(data, p, q)
analyzer.fit_factor_model("model", 4, "priorimax", 43200.0)

# get the results
print(analyzer.models["model"].rotation_matrix_)
print(analyzer.calculate_indices("model")["agreement"])

```
## Requirements
* Python 3.8 or higher
* `numpy`
* `pandas`
* `scikit-learn`
* `factor_analyzer`
* `tensorflow_hub`
* `scipy`
* `nlopt`
* `seaborn`
* `matplotlib`
## License
GNU General Public License 3.0
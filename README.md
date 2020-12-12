# QuantumFlow Diamond Norm

Gavin E. Crooks (2020)

![Build Status](https://github.com/gecrooks/qf-diamond-norm/workflows/Build/badge.svg) [![Documentation Status](https://readthedocs.org/projects/qf-diamond-norm/badge/?version=latest)](https://gecrooks-python-template.readthedocs.io/en/latest/?badge=latest)

[Source](https://github.com/gecrooks/qf-diamond-norm)

Calculation of the diamond norm between two completely positive trace-preserving (CPTP) superoperators, using
the [QuantumFlow](https://github.com/gecrooks/quantumflow) package


The calculation uses the simplified semidefinite program of Watrous
[arXiv:0901.4709](http://arxiv.org/abs/0901.4709)
[J. Watrous, [Theory of Computing 5, 11, pp. 217-238
(2009)](http://theoryofcomputing.org/articles/v005a011/)]


Kudos: Based on MatLab code written by [Marcus P. da Silva](https://github.com/BBN-Q/matlab-diamond-norm/)


## Installation
Note: Diamond norm requires that the "cvxpy" package (and dependencies) be fully installed. Installing cvxpy via pip 
does not correctly install all the necessary packages.


```
$ conda install -c conda-forge cvxpy
$ git clone https://github.com/gecrooks/qf_diamond_norm.git
$ cd qf_diamond_norm
$ pip install -e .
```

## Example

```
    > import quantumflow as qf
    > from qf_diamond_norm import diamond_norm
    > chan0 = qf.random_channel([0, 1, 2]) # 3-qubit channel
    > chan1 = qf.random_channel([0, 1, 2])
    > dn = diamond_norm(chan0, chan1)
    > print(dn)
```


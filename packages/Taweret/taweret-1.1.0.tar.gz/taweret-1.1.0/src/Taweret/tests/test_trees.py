"""
Name: test_trees.py
Author: John Yannotty (yannotty.1@osu.edu)
Desc: Test suite for trees.py

Start Date: 04/21/22
Version: 1.0

"""
# Imports
# import os
# import sys
import numpy as np

from pathlib import Path

# Check for OpenMPI installation
from subprocess import run as cmd
from subprocess import CalledProcessError

from Taweret.models.polynomial_models import sin_cos_exp
from Taweret.mix.trees import Trees

try:
    cmd(['mpirun', '--version', '>', '/dev/null'])
except (CalledProcessError):
    print("OpenMPI is not installed")
    assert False

_TEST_DATA = Path(__file__).parent.joinpath("bart_bmm_test_data").resolve()


# ---------------------------------------------
# Define the test functions
# ---------------------------------------------
# Test the constructor with the model set
def test_init():
    # check passing of variables into Multivariate class
    assert mix.model_dict == model_dict, "object self.model_dict not set."
    assert mix.nummodels == len(
        model_dict), "class object self.nummodels not set."


# Test the mixing fun
def test_mixing():
    x_train = np.loadtxt(_TEST_DATA.joinpath('2d_x_train.txt')).reshape(80, 2)
    x_train = x_train.reshape(2, 80).transpose()

    y_train = np.loadtxt(_TEST_DATA.joinpath('2d_y_train.txt')).reshape(80, 1)

    # Set prior information
    mix.set_prior(
        k=2.5,
        ntree=30,
        overallnu=5,
        overallsd=0.01,
        inform_prior=False)

    # Check tuning & hyper parameters
    assert mix.k == 2.5, "object k is not set."
    assert mix.ntree == 30, "object ntree is not set."
    assert mix.overallnu == 5, "object nu is not set."
    assert mix.overallsd == 0.01, "object overallsd is not set."
    assert mix.overalllambda == 0.01**2, "object overalllambda is not set."
    assert mix.inform_prior is False, "object inform_prior is not set."

    # Train the model
    fit = mix.train(
        X=x_train,
        y=y_train,
        ndpost=10000,
        nadapt=2000,
        nskip=2000,
        adaptevery=500,
        minnumbot=4)

    # Check a few of the fit elements (only the ones that make sense)
    assert fit["nummodels"] == 2, "number of models is wrong."
    assert fit["pbd"] == 0.7, "check prob of birth and death"
    assert fit["pb"] == 0.5, "check prob of birth"

    # Check the mcmc objects
    assert mix.ndpost == 10000, "class object ndpost is not set."
    assert mix.nadapt == 2000, "class object nadapt is not set."
    assert mix.adaptevery == 500, "class object adaptevery is not set."
    assert mix.nskip == 2000, "class object nskip is not set."
    assert mix.minnumbot == 4, "class object minnumbot is not set."


# Test the mean predictions
def test_predict():
    # Get test data
    n_test = 30
    x1_test = np.outer(np.linspace(-3, 3, n_test), np.ones(n_test))
    x2_test = x1_test.copy().transpose()
    # f0_test = (np.sin(x1_test) + np.cos(x2_test))
    x_test = np.array([x1_test.reshape(x1_test.size,),
                      x2_test.reshape(x1_test.size,)]).transpose()

    # Read in test results
    pmean_test = np.loadtxt(_TEST_DATA.joinpath('2d_pmean.txt'))
    eps = 0.10

    # Get predictions
    ppost, pmean, pci, pstd = mix.predict(X=x_test, ci=0.95)

    # Test the values
    perr = np.mean(np.abs(pmean - pmean_test))
    assert perr < eps, "Inaccurate predictions."


# Test posterior of the weights
def test_predict_wts():
    # Get weights
    n_test = 30
    x1_test = np.outer(np.linspace(-3, 3, n_test), np.ones(n_test))
    x2_test = x1_test.copy().transpose()
    x_test = np.array([x1_test.reshape(x1_test.size,),
                      x2_test.reshape(x1_test.size,)]).transpose()

    wpost, wmean, wci, wstd = mix.predict_weights(X=x_test, ci=0.95)

    # Read in test results
    wteps = 0.05
    wmean_test = np.loadtxt(_TEST_DATA.joinpath('2d_wmean.txt'))

    # Test the values
    werr = np.mean(np.abs(wmean - wmean_test))
    assert werr < wteps, "Inaccurate weights."


# Test sigma
def test_sigma():
    sig_eps = 0.05
    assert np.abs((np.mean(mix.posterior) - 0.1)
                  ) < sig_eps, "Inaccurate sigma calculation."


# ---------------------------------------------
# Initiatilize model set
# ---------------------------------------------
# Define the model set
f1 = sin_cos_exp(7, 10, np.pi, np.pi)
f2 = sin_cos_exp(13, 6, -np.pi, -np.pi)
model_dict = {'model1': f1, 'model2': f2}


# mix = Trees(model_dict = model_dict,
# local_openbt_path = "/home/johnyannotty/Documents/openbt/src")
mix = Trees(model_dict=model_dict)

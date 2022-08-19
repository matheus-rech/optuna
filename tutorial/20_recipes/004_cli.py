"""
.. _cli:

Command-Line Interface
======================

.. csv-table::
   :header: Command, Description
   :widths: 20, 40
   :escape: \\

    ask, Create a new trial and suggest parameters.
    best-trial, Show the best trial.
    best-trials, Show a list of trials located at the Pareto front.
    create-study, Create a new study.
    delete-study, Delete a specified study.
    storage upgrade, Upgrade the schema of a storage.
    studies, Show a list of studies.
    study optimize, Start optimization of a study.
    study set-user-attr, Set a user attribute to a study.
    tell, Finish a trial\\, which was created by the ask command.
    trials, Show a list of trials.

Optuna provides command-line interface as shown in the above table.

Let us assume you are not in IPython shell and writing Python script files instead.
It is totally fine to write scripts like the following:
"""


import optuna


def objective(trial):
    x = trial.suggest_float("x", -10, 10)
    return (x - 2) ** 2


if __name__ == "__main__":
    study = optuna.create_study()
    study.optimize(objective, n_trials=100)
    print("Best value: {} (params: {})\n".format(study.best_value, study.best_params))

###################################################################################################
# However, if we cannot write ``objective`` explicitly in Python code such as developing a new
# drug in a lab, a more interactive way is suitable.
# In Optuna CLI, :ref:`ask_and_tell` style commands provide such an interactive and flexible interface.
#
# Let us assume we minimize the objective value depending on a parameter ``x`` in :math:`[-10, 10]`
# and objective value is calculated via some experiments by hand.
# Even so, we can invoke the optimization as follows.
# Don't care about ``--storage sqlite:///example.db`` for now, which is described in :ref:`rdb`.
#
# .. code-block:: bash
#
#     $ STUDY_NAME=`optuna create-study --storage sqlite:///example.db`
#     $ optuna ask --storage sqlite:///example.db --study-name $STUDY_NAME --sampler TPESampler \
#          --search-space '{"x": {"name": "FloatDistribution", "attributes": {"step": null, "low": -10.0, "high": 10.0, "log": false}}}'
#
#
#     [I 2022-08-20 06:08:53,158] Asked trial 0 with parameters {'x': 2.512238141966016}.
#     {"number": 0, "params": {"x": 2.512238141966016}}
#
# After conducting an experiment using the suggested parameter in the lab,
# we store the result to Optuna's study as follows:
#
# .. code-block:: bash
#
#     $ optuna tell --storage sqlite:///example.db --study-name $STUDY_NAME --trial-number 0 --values 0.7 --state complete
#     [I 2022-08-20 06:22:50,888] Told trial 0 with values [0.7] and state TrialState.COMPLETE.
#

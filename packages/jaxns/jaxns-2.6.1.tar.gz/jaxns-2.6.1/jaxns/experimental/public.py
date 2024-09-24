from typing import Optional, TextIO, Union

from jaxns.experimental import SimpleGlobalOptimisation, GlobalOptimisationTerminationCondition, \
    GlobalOptimisationResults
from jaxns.experimental.global_optimisation import summary
from jaxns.framework.bases import BaseAbstractModel
from jaxns.internals.types import PRNGKey
from jaxns.samplers import UniDimSliceSampler

__all__ = [
    'DefaultGlobalOptimisation'
]


class DefaultGlobalOptimisation:
    """
    Default global optimisation class.
    """

    def __init__(self, model: BaseAbstractModel,
                 num_search_chains: Optional[int] = None,
                 s: Optional[int] = None,
                 k: Optional[int] = None,
                 gradient_slice: bool = False
                 ):
        """
        A global optimisation class that uses 1-dimensional slice sampler for the sampling step and decent default
        values.

        Args:
            model: a model to perform global optimisation on
            num_search_chains: number of search chains to use. Defaults to 20 * D.
            num_parallel_workers: number of parallel workers to use. Defaults to 1. Experimental feature.
                If set creates a pool of identical workers and runs them in parallel.
            s: number of slices to use per dimension. Defaults to 1.
            k: number of phantom samples to use. Defaults to 0.
            gradient_slice: if true use gradient information to improve.
        """
        if num_search_chains is None:
            num_search_chains = model.U_ndims * 20
        if s is None:
            s = 1
        if k is None:
            k = 0

        sampler = UniDimSliceSampler(
            model=model,
            num_slices=model.U_ndims * int(s),
            num_phantom_save=int(k),
            midpoint_shrink=True,
            perfect=True,
            gradient_slice=gradient_slice
        )

        self._global_optimiser = SimpleGlobalOptimisation(
            sampler=sampler,
            num_search_chains=int(num_search_chains),
            model=model
        )

    def __call__(self, key: PRNGKey,
                 term_cond: Optional[GlobalOptimisationTerminationCondition] = None,
                 finetune: bool = False) -> GlobalOptimisationResults:
        """
        Runs the global optimisation.

        Args:
            key: PRNGKey
            term_cond: termination condition
            finetune: whether to use gradient-based fine-tune. Default False because not all models have gradients.

        Returns:
            results of the global optimisation
        """
        if term_cond is None:
            term_cond = GlobalOptimisationTerminationCondition(
                min_efficiency=3e-2
            )
        termination_reason, state = self._global_optimiser._run(key, term_cond)
        results = self._global_optimiser._to_results(termination_reason, state)
        if finetune:
            results = self._global_optimiser._gradient_descent(results=results)
        return results

    def summary(self, results: GlobalOptimisationResults, f_obj: Optional[Union[str, TextIO]] = None):
        summary(results, f_obj=f_obj)

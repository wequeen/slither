from slither.core.expressions import Literal
from slither.tools.mutator.mutators.abstract_mutator import AbstractMutator, FaultNature, FaulClass
from slither.tools.mutator.utils.generic_patching import remove_assignement


class MVIE(AbstractMutator):
    NAME = "MVIV"
    HELP = "variable initialization using an expression"
    FAULTCLASS = FaulClass.Assignement
    FAULTNATURE = FaultNature.Missing

    def _mutate(self):

        result = dict()

        for contract in self.slither.contracts:

            # Create fault for state variables declaration
            for variable in contract.state_variables_declared:
                if variable.initialized:
                    # Cannot remove the initialization of constant variables
                    if variable.is_constant:
                        continue

                    if not isinstance(variable.expression, Literal):
                        remove_assignement(variable, contract, result)

            for function in contract.functions_declared + contract.modifiers_declared:
                for variable in function.local_variables:
                    if variable.initialized and not isinstance(variable.expression, Literal):
                        remove_assignement(variable, contract, result)

        return result
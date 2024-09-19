#   Copyright 2024 Miguel Loureiro

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
This module contains classes for all fixed-step solvers supported by this package.

List of fixed-step solvers supported by this package:

-> Euler method
-> Modified Euler method
-> Heun method
-> Runge-Kutta fourth-order method

The solvers' implementation was based on the "Numerical Analysis" textbook, by R. Burden and J. Faires.
"""

from ._fixed_step_solver import _FixedStepSolver
import numpy as np

class _Euler(_FixedStepSolver):

    """
    This class implements the Euler method for solving ODEs.

    The class provides a constructor and a 'step' method that
    performs a single iteration of the method given ... [values and derivative].
    """

    def __init__(self, step_size: float, t0: float=0.0) -> None:

        """
        
        """

        super().__init__(step_size, t0);
    
        return;

    def step(self, model) -> np.ndarray:

        """
        
        """

        # Error checking -> type errors

        x = model.get_state();
        new_state = x + self.h * model.eval(self.t, x);
        self._update_time_step();

        return new_state;

class _Modified_Euler(_FixedStepSolver):

    """
    
    """

    def __init__(self, step_size: float, t0: float=0.0) -> None:

        """
        
        """

        super().__init__(step_size, t0);

        return;

    def step(self, model) -> np.ndarray:

        """
        
        """

        # Error checking -> type errors
        
        x = model.get_state();
        K1 = self.h * model.eval(self.t, x);
        K2 = self.h * model.eval(self.t + self.h, x + K1);
        new_state = x + 1/2 * (K1 + K2);
        self._update_time_step();

        return new_state;

class _Heun(_FixedStepSolver):

    """
    
    """

    def __init__(self, step_size: float, t0: float=0.0) -> None:

        """
        
        """

        super().__init__(step_size, t0);

        return;

    def step(self, model) -> np.ndarray:

        """
        
        """

        # Error checking -> type errors

        x = model.get_state();
        K1 = self.h * model.eval(self.t, x);
        K2 = self.h * model.eval(self.t + self.h / 3.0, x + 1/3 * K1);
        K3 = self.h * model.eval(self.t + 2/3 * self.h, x + 2/3 * K2);
        new_state = x + 1/4 * (K1 + 3 * K3);
        self._update_time_step();

        return new_state;

class _RK4(_FixedStepSolver):

    """
    
    """

    def __init__(self, step_size: float, t0: float=0.0) -> None:

        """
        
        """

        super().__init__(step_size, t0);

        return;

    def step(self, model) -> np.ndarray:

        """
        
        """

        # Error checking -> type errors
        x = model.get_state();
        K1 = self.h * model.eval(self.t, x);
        K2 = self.h * model.eval(self.t + self.h / 2.0, x + 1/2 * K1);
        K3 = self.h * model.eval(self.t + self.h / 2.0, x + 1/2 * K2);
        K4 = self.h * model.eval(self.t + self.h, x + K3);
        new_state = x + 1/6 * (K1 + 2 * K2 + 2 * K3 + K4);
        self._update_time_step();

        return new_state;

if __name__ == "__main__":

    pass

    #test_list = [1, 2, 3];

    #def test_func(list):

    #    list[1] = 0;

    #    return;

    #test_func(test_list);
    #print(test_list);

#from pynamics.solvers._solver import solver

#if __name__ == "__main__":

    #s = solver();
#    print("Here!");
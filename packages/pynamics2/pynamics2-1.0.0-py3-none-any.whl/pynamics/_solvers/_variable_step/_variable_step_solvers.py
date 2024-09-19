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
This solver's implementation was based on the "Numerical Analysis" textbook, by R. Burden and J. Faires.
"""

from ._variable_step_solver import _VariableStepSolver
import numpy as np

class _RKF(_VariableStepSolver):

    """
    
    """

    def __init__(self, initial_step_size: float, t0: float = 0, tolerance: float = 0.00001, max_step_size: float = 0.001, min_step_size: float = 0.000001,
                 min_update: float=0.1, max_update: float=4.0, tfinal: float=10.0) -> None:
        
        """
        
        """

        super().__init__(initial_step_size, t0, tolerance, max_step_size, min_step_size, min_update, max_update, tfinal);

        return;

    def _update_step_size(self, q: float) -> None:
        
        """
        
        """
        
        q = np.fmin(self.qmax, np.fmax(self.qmin, q));
        
        self.h = np.fmin(self.tfinal - self.t, np.fmin(self.hmax, np.fmax(self.hmin, q * self.h)));

        return;

    def step(self, model) -> np.ndarray:
        
        """
        
        """

        flag = True;

        while(flag is True):

            x = model.get_state();
            K1 = self.h * model.eval(self.t, x);
            K2 = self.h * model.eval(self.t + 1/4 * self.h, x + 1/4 * K1);
            K3 = self.h * model.eval(self.t + 3/8 * self.h, x + 3/32 * K1 + 9/32 * K2);
            K4 = self.h * model.eval(self.t + 12/13 * self.h, x + 1932/2197 * K1 - 7200/2197 * K2 + 7296/2197 * K3);
            K5 = self.h * model.eval(self.t + self.h, x + 439/126 * K1 - 8 * K2 + 3680/513 * K3 - 845/4104 * K4);
            K6 = self.h * model.eval(self.t + 1/2 * self.h, x - 8/27 * K1 + 2 * K2 - 3544/2565 * K3 + 1859/4104 * K4 - 11/40 * K5);

            #R = 1/self.h * np.max(np.abs(1/360 * K1 - 128/4275 * K3 - 2197/75240 * K4 + 1/50 * K5 + 2/55 * K6));
            R = 1/self.h * np.linalg.norm(np.abs(1/360 * K1 - 128/4275 * K3 - 2197/75240 * K4 + 1/50 * K5 + 2/55 * K6), ord=2);
            #R = np.max(R_vec);
        
            if(R <= self.eps):

                #if(self.h <= self.hmin):

                #    print("The minimum step size is not small enough to guarantee the specified error tolerance.");

                flag = False;
        
            #else:

            q = 0.84 * ((self.eps / R)**(1/4));
            self._update_step_size(q);

        new_state = x + 25/216 * K1 + 1408/2565 * K3 + 2197/4104 * K4 - 1/5 * K5;
        self._update_time_step();

        return new_state;

class _DP(_VariableStepSolver):

    """
    
    """

    def __init__(self, initial_step_size: float, t0: float = 0, tolerance: float = 0.00001, max_step_size: float = 0.001, min_step_size: float = 0.000001,
                 min_update: float=0.1, max_update: float=4.0, tfinal: float=10.0) -> None:
        
        """
        
        """

        super().__init__(initial_step_size, t0, tolerance, max_step_size, min_step_size, min_update, max_update, tfinal);

        return;

    def _update_step_size(self, q: float) -> None:
        
        """
        
        """
        
        q = np.fmin(self.qmax, np.fmax(self.qmin, q));
        
        self.h = np.fmin(self.tfinal - self.t, np.fmin(self.hmax, np.fmax(self.hmin, q * self.h)));

        return;

    def step(self, model) -> np.ndarray:
        
        """
        
        """

        flag = True;

        while(flag is True):

            x = model.get_state();
            K1 = self.h * model.eval(self.t, x);
            K2 = self.h * model.eval(self.t + 1/5 * self.h, x + 1/5 * K1);
            K3 = self.h * model.eval(self.t + 3/10 * self.h, x + 3/40 * K1 + 9/40 * K2);
            K4 = self.h * model.eval(self.t + 4/5 * self.h, x + 44/45 * K1 - 56/15 * K2 + 32/9 * K3);
            K5 = self.h * model.eval(self.t + 8/9 * self.h, x + 19372/6561 * K1 - 25360/2187 * K2 + 64448/6561 * K3 - 212/729 * K4);
            K6 = self.h * model.eval(self.t + self.h, x + 9017/3168 * K1 - 355/33 * K2 + 46732/5247 * K3 + 49/176 * K4 - 5103/18656 * K5);

            order5_estimate = x + 35/384 * K1 + 500/1113 * K3 + 125/192 * K4 - 2187/6784 * K5 + 11/84 * K6;
            K7 = self.h * model.eval(self.t + self.h, order5_estimate);

            order4_estimate = x + 5179/57600 * K1 + 7571/16695 * K3 + 393/640 * K4 - 92097/339200 * K5 + 187/2100 * K6 + 1/40 * K7;

            #R = np.max(np.abs(order5_estimate - order4_estimate));
            R = np.linalg.norm(np.abs(order5_estimate - order4_estimate), ord=2);
        
            if(R <= self.eps):

                #if(self.h <= self.hmin):

                #    print("The minimum step size is not small enough to guarantee the specified error tolerance.");

                flag = False;
        
            #else:

            #tol = self.eps * np.fmax(np.abs(order4_estimate), np.abs(order5_estimate));
            tol = self.eps;
            q = 0.8 * ((tol * self.h / R)**(1/5));
            self._update_step_size(q);

        new_state = order5_estimate;
        self._update_time_step();

        return new_state;
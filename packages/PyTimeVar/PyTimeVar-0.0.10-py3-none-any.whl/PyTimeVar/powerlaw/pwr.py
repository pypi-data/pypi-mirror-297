import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class PowerLaw:
    """
    Class for implementing the Power-Law method.
    
    Parameters
    ----------
    vY : np.ndarray
        The dependent variable (response) array.
    n_powers : int
        The number of powers.
    vgamma0 : np.ndarray
        The initial parameter vector.
    options : dict
        Stopping criteria for optimization.
        
    Attributes
    ----------
    vY : np.ndarray
        The dependent variable (response) array.
    n : int
        The length of vY.
    p : int
        The number of powers. Default is set to 2.
    vgamma0 : np.ndarray
        The initial parameter vector.
    bounds : list
        List to define parameter space.
    cons : dict
        Dictionary that defines the constraints.
    trendHat : np.ndarray
        The estimated trend.
    gammaHat : np.ndarray
        The estimated power parameters.
    coeffHat : np.ndarray
        The estimated coefficients.
        
    Raises
    ------
    ValueError
        No valid bounds are provided.
        
    
    """

    def __init__(self, vY: np.ndarray, n_powers: float = None, vgamma0: np.ndarray=None, bounds : tuple=None, options: dict=None):
        self.vY = vY.reshape(-1,1)
        self.n = len(self.vY)
        self.p = 2 if n_powers is None else n_powers
        if n_powers is None:
            print('The number of powers is set to 2 by default. \nConsider setting n_powers to 3 or higher if a visual inspection of the data leads you to believe the trend is curly.\n')

        self.vgamma0 =vgamma0 if vgamma0 is not None else np.arange(0, 1*self.p, 1)
        self.bounds = bounds if bounds is not None else ((-0.495, 8),)*self.p
        for j in range(self.p):
            if self.bounds[j][0]<= -0.5:
                raise ValueError('Parameters are not identified if the power is smaller or equal than -1/2.\n The lower bounds need to be larger than -1/2.')
        self.options = options if options is not None else {'maxiter': 5E5}
        self.cons = {'type': 'ineq', 'fun': self._nonlcon}

        self.trendHat = None
        self.gammaHat = None
        self.coeffHat = None

    def plot(self, tau : list=None):
        """
        Plots the original series and the trend component.
        
        Parameters
        ----------
        tau : list, optional
            The list looks the  following: tau = [start,end].
            The function will plot all data and estimates between start and end.
            
        Raises
        ------
        ValueError
            No valid tau is provided.
            
        """
        if self.trendHat is None:
            print("Model is not fitted yet.")
            return
        
        
        tau_index=None
        x_vals = np.arange(1/self.n,(self.n+1)/self.n,1/self.n)
        if tau is None:

            tau_index=np.array([0,self.n])
        elif isinstance(tau, list):
            if min(tau) <= 0:
                tau_index = np.array([int(0), int(max(tau) * self.n)])
            else:
                tau_index = np.array([int(min(tau)*self.n-1),int(max(tau)*self.n)])
        else:
            raise ValueError('The optional parameter tau is required to be a list.')

        plt.figure(figsize=(12, 6))
        plt.plot(x_vals[tau_index[0]:tau_index[1]], self.vY[tau_index[0]:tau_index[1]], label="True data", linewidth=2, color = 'black')
        plt.plot(x_vals[tau_index[0]:tau_index[1]], self.trendHat[tau_index[0]:tau_index[1]], label="Estimated $\\beta_{0}$", linestyle="--", linewidth=2)
        
        plt.grid(linestyle='dashed')
        plt.xlabel('$t/n$',fontsize="xx-large")

        plt.tick_params(axis='both', labelsize=16)
        plt.legend(fontsize="x-large")
        plt.show()   
        
    def summary(self):
        """
        Print the mathematical equation for the fitted model

        """
        
        def term(coef, power):
            coef = coef if coef != 1 else ''
            coef, power = round(coef, 3), round(power, 3)
            if power >0:
                power = (f'^{power}') if power > 1 else ''
                return f'{coef} t{power}'
            else:
                return f'{coef}'
        terms = []
        for j in range(len(self.coeffHat)):
          if self.coeffHat[j][0] != 0:
            terms.append(term(self.coeffHat[j][0], self.gammaHat[0][j]))
        print('\nPower-Law Trend Results:')
        print('='*30)
        print('yhat= ' + ' + '.join(terms))

    def fit(self):
        '''
        Fits the Power-Law model to the data.        

        Returns
        -------
        self.trendHat : np.ndarray
            The estimated trend.
        self.gammaHat : np.ndarray
            The estimated power parameters.

        '''
        res = minimize(self._construct_pwrlaw_ssr, self.vgamma0,
                       bounds=self.bounds, constraints=self.cons, options=self.options)
        self.gammaHat = res.x.reshape(1, self.p)

        trend = np.arange(1, self.n+1, 1).reshape(self.n, 1)
        mP = trend ** self.gammaHat
        self.coeffHat = np.linalg.pinv(mP.T @ mP) @ mP.T @ self.vY
        self.trendHat = mP @ self.coeffHat

        return self.trendHat, self.gammaHat

    def _construct_pwrlaw_ssr(self, vparams):
        '''
        Compute sum of squared residuals for a given parameter vector.

        Parameters
        ----------
        vparams : np.ndarray
            The parameter vector.

        Returns
        -------
        ssr : float
            Sum of squared residuals.

        '''
        trend = np.arange(1, self.n+1, 1).reshape(self.n, 1)

        vparams = np.array(vparams).reshape(1, self.p)
        mP = trend ** vparams
        coeff = np.linalg.pinv(mP.T @ mP) @ mP.T @ self.vY
        ssr = np.sum((self.vY - mP @ coeff)**2)
        return ssr

    def _nonlcon(self, params):
        '''
        Construct the nonlinear constraints for identification.

        Parameters
        ----------
        params : np.ndarray
            The parameter vector.

        Returns
        -------
        c : list
            List of non-linear parameter constraints.

        '''
        epsilon = 0.005
        c = []
        for id1 in range(self.p-1):
            for id2 in range(id1+1, self.p):
                c.append(params[id1] - params[id2] + epsilon)
        return c

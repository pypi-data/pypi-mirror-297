import jax 
import jax.numpy as jnp
from jax import jit, vmap
import math
from kalmax.utils import gaussian_pdf, log_gaussian_pdf

# TODO check that jnp.einsum isn't slowing things down

class KalmanFilter:
    """A Kalman filter class. This class is used to filter the data and fit the model.
    Written in jax, the lower level functions are jit compiled for speed. The filtering and smoothing loops are processed in batches using jax.lax.scan(): higher batch sizes will run faster but at the cost of a one-off compilation time.
    
    The Kalman dynamics equations are as follows:
    z_t = F @ z_t-1 + q_t-1
    y_t = H @ z_t + r_t
    where z_t is the hidden state, y_t is the observation, F is the state transition matrix, H is the observation matrix, q_t ~ N(0, Q) is the state transition noise, and r_t ~ N(0, R) is the observation noise.

    Kalman _filtering_ takes observations and estimates the _causal_ posterior distribution of the hidden state given the observations. Kalman _smoothing_ takes the filtered estimates and estimates the _posterior_ distribution of the hidden state given all the observations.
    mu_filter_t = E[z_t | y_1:t]
    sigma_filter_t = Cov[z_t | y_1:t]
    mu_smooth_t = E[z_t | y_1:T]
    sigma_smooth_t = Cov[z_t | y_1:T]
    """

    def __init__(self, dim_Z : int, 
                       dim_Y : int,
                       batch_size : int = 100, 
                       # optional parameters
                       mu0 : jnp.ndarray = None,
                       sigma0 : jnp.ndarray = None,
                       F : jnp.ndarray = None,
                       Q : jnp.ndarray = None,
                       H : jnp.ndarray = None,
                       R : jnp.ndarray = None,
                       ):
        """Initializes the Kalman class. The state has size dim_Z, the observations have size dim_Y. 
        
        Parameters F, Q, H and R can either be:
        * Passed in at initialisation --> assumed constant over time
        * Passed in at runtime --> assumed to time-vary (additional time-dim in along the 0 axis matching the length of the observation data)

        Parameters
        ----------
        dim_Z : int
            The size of the state space
        dim_Y : int
            The size of the observation space
        batch_size : int
            The batch size for the Kalman filter

        Optional parameters
        -------------------
        mu0 : jnp.ndarray, shape (dim_Z,)
            The initial state mean
        sigma0 : jnp.ndarray, shape (dim_Z, dim_Z)
            The initial state covariance
        F : jnp.ndarray, shape (dim_Z, dim_Z)
            The state transition matrix
        Q : jnp.ndarray, shape (dim_Z, dim_Z)
            The state transition noise covariance
        H : jnp.ndarray, shape (dim_X, dim_Z)
            The observation matrix
        R : jnp.ndarray, shape (dim_X, dim_X)
            The observation noise covariance
        """

        self.dim_Z = dim_Z
        self.dim_Y = dim_Y
        self.batch_size = batch_size

        # Optionally set parameters and initial conditions now
        if mu0 is not None:
            assert mu0.shape == (self.dim_Z,)
        if sigma0 is not None:
            assert sigma0.shape == (self.dim_Z, self.dim_Z)
        if F is not None:
            assert F.shape == (self.dim_Z, self.dim_Z)
        if Q is not None:
            assert Q.shape == (self.dim_Z, self.dim_Z)
        if H is not None:
            assert H.shape == (self.dim_Y, self.dim_Z)
        if R is not None:
            assert R.shape == (self.dim_Y, self.dim_Y)
    
        self.mu0 = mu0
        self.sigma0 = sigma0
        self.F = F
        self.Q = Q
        self.H = H
        self.R = R

    def filter(self, Y, 
                     mu0=None, 
                     sigma0=None, 
                     F=None,
                     Q=None,
                     H=None,
                     R=None,):
        """Takes sequences of observations and observation noise covariances and runs the Kalman filter on the data. If parameters are not passed in, the class defaults are used. If they are passed in, they must have shape (T, *param_shape,) where T is the number of time steps - this allows for time-varying parameters.
        
        Parameters
        ----------
        Y : jnp.ndarray, shape (T, dim_Z)
            The observation means
        mu0 : jnp.ndarray, shape (dim_Z,)
            The initial state mean, optional (default is provided at initialisation)
        sigma0 : jnp.ndarray, shape (dim_Z, dim_Z)
            The initial state covariance, optional (default is provided at initialisation)
        F : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The state transition matrix, optional (default is provided at initialisation)
        Q : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The state transition noise covariance, optional (default is provided at initialisation)
        H : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The observation matrix, optional (default is provided at initialisation)
        R : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The observation noise covariances, optional (default is provided at initialisation)


        Returns
        -------
        mus_f : jnp.ndarray, shape (T, dim_Z)
            The filtered means
        sigmas_f : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The filtered covariances
        """
        assert Y.ndim == 2; assert Y.shape[1] == self.dim_Y
        T = Y.shape[0] # number of time steps

        if mu0 is None: 
            assert self.mu0 is not None, "You must either pass in the initial conditions or set them at initialisation"
            mu0 = self.mu0
        else: 
            assert mu0.ndim == 1; assert mu0.shape[0] == self.dim_Z
        if sigma0 is None:
            assert self.sigma0 is not None, "You must either pass in the initial conditions or set them at initialisation"
            sigma0 = self.sigma0
        else:
            assert sigma0.ndim == 2; assert sigma0.shape[0] == self.dim_Z; assert sigma0.shape[1] == self.dim_Z
        F = self._verify_and_tile(F, self.F, T, (self.dim_Z, self.dim_Z))
        Q = self._verify_and_tile(Q, self.Q, T, (self.dim_Z, self.dim_Z))
        H = self._verify_and_tile(H, self.H, T, (self.dim_Y, self.dim_Z))
        R = self._verify_and_tile(R, self.R, T, (self.dim_Y, self.dim_Y))

        mus_f, sigmas_f = [],[] # filtered means and covariances
        
        N_batch = math.ceil(T/self.batch_size)
        for i in range(N_batch):
            start = i*self.batch_size
            end = min((i+1)*self.batch_size, T)
            mu, sigma = kalman_filter(
                    Y = Y[start:end],
                    mu0 = mu0, 
                    sigma0 = sigma0, 
                    F = F[start:end], 
                    Q = Q[start:end], 
                    H = H[start:end], 
                    R = R[start:end], )
            mus_f.append(mu)
            sigmas_f.append(sigma)
            mu0, sigma0 = mu[-1], sigma[-1] # update initial conditions for next batch
        mus_f = jnp.concatenate(mus_f)
        sigmas_f = jnp.concatenate(sigmas_f)

        return mus_f, sigmas_f
    
    def smooth(self, mus_f, 
                     sigmas_f, 
                     F=None, 
                     Q=None,): 
        """Takes the filtered means and covariances and runs the Kalman smoother on the data.

        Parameters
        ----------
        mus_f : jnp.ndarray, shape (T, dim_Z)
            The filtered means
        sigmas_f : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The filtered covariances
        F : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The state transition matrix, optional
        Q : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The state transition noise covariance, optional
        
        Returns
        -------
        mus_s : jnp.ndarray, shape (T, dim_Z)
            The smoothed means
        sigmas_s : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The smoothed covariances
        """

        T = len(mus_f)
        muT = mus_f[-1]
        sigmaT = sigmas_f[-1]
        mus_s, sigmas_s = [jnp.array([muT])],[jnp.array([sigmaT])]

        F = self._verify_and_tile(F, self.F, T, (self.dim_Z, self.dim_Z))
        Q = self._verify_and_tile(Q, self.Q, T, (self.dim_Z, self.dim_Z))

        for i in range(math.ceil((T-1)/(self.batch_size))):
            start = max(0, T - 1 - (i+1)*self.batch_size)
            end = T - 1 - i*self.batch_size
            mu, sigma = kalman_smoother(
                mu = mus_f[start:end], 
                sigma = sigmas_f[start:end], 
                muT = muT, 
                sigmaT = sigmaT, 
                F = F[start:end], 
                Q = Q[start:end],)
            mus_s.insert(0,mu); sigmas_s.insert(0,sigma)
            muT, sigmaT = mu[0], sigma[0]
        mus_s = jnp.concatenate(mus_s)
        sigmas_s = jnp.concatenate(sigmas_s)

        return mus_s, sigmas_s

    def loglikelihood(self, Y,
                            mu, 
                            sigma, 
                            H=None, 
                            R=None,):
        """Calculates the log-likelihood of the observations, Y, by marginalising over the hidden state [mu, sigma] (filtered or smoothed). This can be done analytically (see page 361 of the Advanced Murphy book). 

        P(Y) = Normal(Y | Y_hat, S) where S = H @ sigma @ H.T + R (the posterior observation covariance combined with the observation noise covariance) Y_hat = H @ mu (the predicted observation). 

        Parameters
        ----------
        Y : jnp.ndarray, shape (T, dim_Y)
            The observation means
        mu : jnp.ndarray, shape (T, dim_Z)
            The posterior state means
        sigma : jnp.ndarray, shape (T, dim_Z, dim_Z)
            The posterior state covariances
        H: jnp.ndarray, shape (T, dim_Y, dim_Z)
            The observation matrix, optional
        R : jnp.ndarray, shape (T, dim_Y, dim_Y)
            The observation noise covariances, optional

        Returns
        -------
        logP : jnp.ndarray, shape (T,)
            The log-likelihood of the data given the model
        """

        T = len(mu)
        H = self._verify_and_tile(H, self.H, T, (self.dim_Y, self.dim_Z))
        R = self._verify_and_tile(R, self.R, T, (self.dim_Y, self.dim_Y))
            
        S = vmap(calculate_S_matrix, (0, 0, 0))(sigma, H, R)
        Y_hat = jnp.einsum('ijk,ik->ij', H, mu) # the "observation" mean
        logP = vmap(log_gaussian_pdf, (0, 0, 0))(Y, Y_hat, S)
        # logP = jnp.log(P) # TODO multiply this by a volume element to get actual probability

        return logP

    def _verify_and_tile(self, param, default_param, T, intended_shape):
        """Verifies the shape of the parametery. If the parameter is not passed in, the default parameter (presumably set at initialisation) is tiled T-times along a new 0th axis and used. 

        Parameters
        ----------
        param : jnp.ndarray or None
            The parameter to be verified
        default_param : jnp.ndarray
            The default parameter
        T : int
            The number of times to tile the parameter
        intended_shape : tuple
            The intended shape of the parameter

        Returns
        -------
        param : jnp.ndarray
            The parameter, shape (T, *intended_shape)
        """
        if param is None: 
            assert default_param is not None, "You must either pass in the parameter or set it at initialisation"
            param = jnp.tile(default_param, (T,)+(1,)*default_param.ndim)
        else: 
            assert param.shape == (T,)+intended_shape, f"Parameter shape is {param.shape} but should be {(T,)+intended_shape}"
        return param

@jit 
def kalman_filter(Y, mu0, sigma0, F, Q, H, R):
    """Kalman filters a batch of observation data, Y. 

    Parameters
    ----------
    Y : jnp.ndarray, shape (T, dim_Y)
        The observation means
    mu0 : jnp.ndarray, shape (dim_Z,)
        The initial state mean
    sigma0 : jnp.ndarray, shape (dim_Z, dim_Z)
        The initial state covariance
    F : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The state transition matrix
    Q : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The state transition noise covariance
    H : jnp.ndarray, shape (T, dim_Y, dim_Z)
        The observation matrix
    R : jnp.ndarray, shape (T, dim_Y, dim_Y)
        The observation noise covariances


    Returns
    -------
    mu : jnp.ndarray, shape (T, dim_Z)
        The filtered posterior state means
    sigma : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The filtered posterior state covariances
    """
    def loop(carry, inputs):
        mu, sigma = carry
        Y, F, Q, H, R, = inputs
        mu_p, sigma_p = kalman_predict(mu, sigma, F, Q)
        mu_u, sigma_u = kalman_update(mu_p, sigma_p, H, R, Y)
        return (mu_u, sigma_u), (mu_u, sigma_u) # carry, output
    _, (mu_all, sigma_all) = jax.lax.scan(loop, (mu0, sigma0), (Y, F, Q, H, R))
    return jnp.stack(mu_all), jnp.stack(sigma_all)

@jit
def kalman_smoother(mu, sigma, muT, sigmaT, F, Q):
    """Runs the Kalman smoother on the data. mu and sigma are in forward order, ie. mu = [mu[0], mu[1], ... mu[T]] and they are looped over in reverse order, so you can still batch the data. 


    Parameters
    ----------
    mu : jnp.ndarray, shape (T, dim_Z)
        The filtered posterior state means 
    sigma : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The filtered posterior state covariances
    muT : jnp.ndarray, shape (dim_Z,)
        The final state mean - by definition this should have already been smoothed
    sigmaT : jnp.ndarray, shape (dim_Z, dim_Z)
        The final state covariance - by definition this should have already been smoothed
    F : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The state transition matrix
    Q : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The state transition noise covariance

    Returns
    -------
    mu_smooth : jnp.ndarray, shape (T, dim_Z)
        The smoothed state means
    sigma_smooth : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The smoothed state covariances
    """
    def loop(carry, inputs):
        mu, sigma = carry
        mu_, sigma_, F, Q = inputs
        mu_predict, sigma_predict = kalman_predict(mu_, sigma_, F, Q)
        J = sigma_ @ F.T @ jnp.linalg.inv(sigma_predict)
        mu_smoothed = mu_ + J @ (mu - mu_predict)
        sigma_smoothed = sigma_ + J @ (sigma - sigma_predict) @ J.T
        return (mu_smoothed, sigma_smoothed), (mu_smoothed, sigma_smoothed)
    _, (mus_all, sigmas_all) = jax.lax.scan(loop, (muT, sigmaT), (mu[::-1], sigma[::-1], F[::-1], Q[::-1]))
    mus_all = mus_all[::-1]
    sigmas_all = sigmas_all[::-1] # reverse the order back to forward

    return mus_all, sigmas_all

@jit
def kalman_likelihoods(Z, Y, mu, sigma, F, Q, H, R): # TODO check if this is ever used
    """Calculates the prior P(Z), likelihood P(Y | Z), and posterior P(Z | Y) of any state trajectory (Z) and observations (Y, R) under the fitted kalman model. Note although Z and Y can, in principle, be _any_ trajectory and observations, typically Z == mu and Y == the observations which were used to fit the model in the first place. 

    Parameters
    ----------
    Z : jnp.ndarray, shape (T, dim_Z)
        The trajectory of the agent (typical this might just be the same as mu) 
    Y : jnp.ndarray, shape (T, dim_Y)
        The observations to be evalauted 
    mu : jnp.ndarray, shape (T, dim_Z)
        The posterior state means 
    sigma : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The posterior state covariances
    F : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The state transition matrix
    Q : jnp.ndarray, shape (T, dim_Z, dim_Z)
        The state transition noise covariance
    H : jnp.ndarray, shape (T, dim_Y, dim_Z)
        The observation matrix
    R : jnp.ndarray, shape (T, dim_Y, dim_Y)
        The observation noise covariances

    Returns
    -------
    PZ : jnp.ndarray, shape (T,)
        The likelihood of the state given the previous state
    PZXF : jnp.ndarray, shape (T,)
        The likelihood of the state given the observation
    PXZF : jnp.ndarray, shape (T,)
        The likelihood of the observation given the state
    """

    Z_ = jnp.concatenate((Z[0][None], Z)) #prepend Z0 to Z so its [Z0, Z0, Z1, Z2, ... ZT]
    Q_ = jnp.concatenate((Q[0][None], Q)) #prepend Q0 to Q so its [Q0, Q0, Q1, Q2, ... QT]
    F_ = jnp.concatenate((F[0][None], F)) #prepend F0 to F so its [F0, F0, F1, F2, ... FT]
    mu_p = jnp.einsum('ijk,ik->ij', F_, Z_) # the "next state" mean
    Y_hat = jnp.einsum('ijk,ik->ij', H, mu) # the "observation" mean
    PZ   = vmap(gaussian_pdf,(0,0,0))(Z_[1:], mu_p[:-1], Q_[1:]) # zt ~ N(F*zt-1, Qt)
    PZXF = vmap(gaussian_pdf,(0,0,0))(Z, mu, sigma) # zt ~ N(mu, sigma)
    PXZF = vmap(gaussian_pdf,(0,0,0))(Y, Y_hat, R)
    return PZ, PZXF, PXZF

def kalman_predict(mu, sigma, F, Q):
    """Predicts the next state of the system given the current state and the state transition matrix.

    Parameters
    ----------
    mu : jnp.ndarray, shape (dim_Z,)
        The current state mean
    sigma : jnp.ndarray, shape (dim_Z, dim_Z)
        The current state covariance
    F : jnp.ndarray, shape (dim_Z, dim_Z)
        The state transition matrix
    Q : jnp.ndarray, shape (dim_Z, dim_Z)
        The state transition noise covariance

    Returns
    -------
    mu_next : jnp.ndarray, shape (dim_Z,)
        The predicted next state mean
    sigma_next : jnp.ndarray, shape (dim_Z, dim_Z)
        The predicted next state covariance
    """
    mu_next = F @ mu
    sigma_next = F @ sigma @ F.T + Q
    return mu_next, sigma_next

def kalman_update(mu, sigma, H, R, y):
    """Updates the state estimate given an observation.

    Parameters
    ----------
    mu : jnp.ndarray, shape (dim_Z,)
        The current state mean
    sigma : jnp.ndarray, shape (dim_Z, dim_Z)
        The current state covariance
    H : jnp.ndarray, shape (dim_Y, dim_Z)
        The observation matrix
    R : jnp.ndarray, shape (dim_Y, dim_Y)
        The observation noise covariance
    y : jnp.ndarray, shape (dim_Y,)
        The state observation

    Returns
    -------
    mu_post : jnp.ndarray, shape (dim_Z,)
        The posterior state mean
    sigma_post : jnp.ndarray, shape (dim_Z, dim_Z)
        The posterior state covariance
    """
    S = calculate_S_matrix(sigma, H, R) 
    y_hat = H @ mu
    K = calculate_K_matrix(sigma, H, S)
    mu_post = mu + K @ (y - y_hat)
    sigma_post = (jnp.eye(len(mu)) - K @ H) @ sigma

    return mu_post, sigma_post

def calculate_S_matrix(sigma, H, R):
    """Calculates the S matrix for the Kalman filter. This doesn't really need to be it's own function but it's useful for readability and I vmap it later.
    
    Parameters
    ----------
    sigma : jnp.ndarray, shape (dim_Z, dim_Z)
        The state covariance
    H : jnp.ndarray, shape (dim_Y, dim_Z)
        The observation matrix
    R : jnp.ndarray, shape (dim_Y, dim_Y)
        The observation noise covariance
        
    Returns
    -------
    S : jnp.ndarray, shape (dim_Y, dim_Y)
        The S matrix    
    """
    return H @ sigma @ H.T + R

def calculate_K_matrix(sigma, H, S):
    """Calculates the K matrix for the Kalman filter. This doesn't really need to be it's own function but it's useful for readability and I vmap it later.

    Parameters
    ----------
    sigma : jnp.ndarray, shape (dim_Z, dim_Z)
        The state covariance
    H : jnp.ndarray, shape (dim_Y, dim_Z)
        The observation matrix
    S : jnp.ndarray, shape (dim_Y, dim_Y)
        The S matrix

    Returns
    -------
    K : jnp.ndarray, shape (dim_Z, dim_Y)
        The K matrix
    """
    return sigma @ H.T @ jnp.linalg.inv(S)

def fit_parameters(Z, Y): 
    """Assuming a training set exists where hidden states Z and observations Y are known, this function fits the optimal stationary parameters of the Kalman filter, i.e. returning those that maximise the likelihood of the data and the state: L(Θ) = log({z},{y} | Θ). These solutions are (relatively) easy to derive, I took them from Byron Yu's lecture notes (they look a lot like linear regression solutions): 
    
    mu0 = (1/T) Σ{zt}
    sigma0 = (1/T) Σ{zt - mu0}{zt - mu0}.T
    F = Σ{zt+1 @ zt.T} Σ{zt zt.T}^-1
    Q = (1/T-1) Σ{zt - F @ zt-1}{zt - F @ zt-1}.T 
    H = Σ{yt @ zt.T} Σ{zt zt.T}^-1
    R = (1/T) Σ{yt - H @ zt}{yt - H @ zt}.T

    Parameters
    ----------
    Z : jnp.ndarray, shape (T, dim_Z)
        The hidden states (training data) 
    Y : jnp.ndarray, shape (T, dim_Y)
        The observations (training data)

    Returns
    -------
    mu0 : jnp.ndarray, shape (dim_Z,)
        The initial state mean
    sigma0 : jnp.ndarray, shape (dim_Z, dim_Z)
        The initial state covariance
    F : jnp.ndarray, shape (dim_Z, dim_Z)
        The state transition matrix
    Q : jnp.ndarray, shape (dim_Z, dim_Z)
        The state transition noise covariance
    H : jnp.ndarray, shape (dim_Y, dim_Z)
        The observation matrix
    R : jnp.ndarray, shape (dim_Y, dim_Y)
        The observation noise covariance

    """

    assert Z.ndim == 2; assert Y.ndim == 2    
    T = Z.shape[0]
    assert Y.shape[0] == T

    mu0 = Z.mean(axis=0)
    sigma0 = (1 / T) * ((Z - mu0).T @ (Z - mu0))
    F = (Z[1:].T @ Z[:-1]) @ jnp.linalg.inv(Z.T @ Z)
    Q = (1 / (T-1)) * (Z[1:] - Z[:-1] @ F.T).T @ (Z[1:] - Z[:-1] @ F.T)
    H = (Y.T @ Z) @ jnp.linalg.inv(Z.T @ Z)
    R = (1 / T) * (Y - Z @ H.T).T @ (Y - Z @ H.T)

    return mu0, sigma0, F, Q, H, R

def fit_mu0(Z):
    """Fits the initial state mean of the Kalman filter under the assumption of stationary dynamics, see `fit_parameters` for more details.

    Parameters
    ----------
    Z : jnp.ndarray, shape (T, dim_Z)
        The hidden states (training data) 

    Returns
    -------
    mu0 : jnp.ndarray, shape (dim_Z,)
        The initial state mean
    """
    return Z.mean(axis=0)

def fit_sigma0(Z):
    """Fits the initial state covariance of the Kalman filter under the assumption of stationary dynamics, see `fit_parameters` for more details.

    Parameters
    ----------
    Z : jnp.ndarray, shape (T, dim_Z)
        The hidden states (training data) 

    Returns
    -------
    sigma0 : jnp.ndarray, shape (dim_Z, dim_Z)
        The initial state covariance
    """
    T = Z.shape[0]
    mu0 = Z.mean(axis=0)
    return (1 / T) * ((Z - mu0).T @ (Z - mu0))

def fit_F(Z):
    """Fits the state transition matrix of the Kalman filter under the assumption of stationary dynamics, see `fit_parameters` for more details.

    Parameters
    ----------
    Z : jnp.ndarray, shape (T, dim_Z)
        The hidden states (training data) 

    Returns
    -------
    F : jnp.ndarray, shape (dim_Z, dim_Z)
        The state transition matrix
    """
    return (Z[1:].T @ Z[:-1]) @ jnp.linalg.inv(Z.T @ Z)

def fit_Q(Z):
    """Fits the state transition noise covariance of the Kalman filter under the assumption of stationary dynamics, see `fit_parameters` for more details.

    Parameters
    ----------
    Z : jnp.ndarray, shape (T, dim_Z)
        The hidden states (training data) 

    Returns
    -------
    Q : jnp.ndarray, shape (dim_Z, dim_Z)
        The state transition noise covariance
    """
    T = Z.shape[0]
    F = (Z[1:].T @ Z[:-1]) @ jnp.linalg.inv(Z.T @ Z)
    return (1 / (T-1)) * (Z[1:] - Z[:-1] @ F.T).T @ (Z[1:] - Z[:-1] @ F.T)

def fit_H(Z, Y):
    """Fits the observation matrix of the Kalman filter under the assumption of stationary dynamics, see `fit_parameters` for more details.

    Parameters
    ----------
    Z : jnp.ndarray, shape (T, dim_Z)
        The hidden states (training data) 
    Y : jnp.ndarray, shape (T, dim_Y)
        The observations (training data)

    Returns
    -------
    H : jnp.ndarray, shape (dim_Y, dim_Z)
        The observation matrix
    """
    return (Y.T @ Z) @ jnp.linalg.inv(Z.T @ Z)

def fit_R(Z, Y):
    """Fits the observation noise covariance of the Kalman filter under the assumption of stationary dynamics, see `fit_parameters` for more details.

    Parameters
    ----------
    Z : jnp.ndarray, shape (T, dim_Z)
        The hidden states (training data) 
    Y : jnp.ndarray, shape (T, dim_Y)
        The observations (training data)

    Returns
    -------
    R : jnp.ndarray, shape (dim_Y, dim_Y)
        The observation noise covariance
    """
    T = Z.shape[0]
    H = fit_H(Z,Y)
    return (1 / T) * (Y - Z @ H.T).T @ (Y - Z @ H.T)



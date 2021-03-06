"""
============================== Gradient Descent with Different Optimization Algorithms =================================
        
All credit to Tiep Vu - the author of 'Machine Learning co ban'
I am replicating his code (with a few changes) for studying purpose only

Content of this code:
1. initialize X, y and find theta by Normal Equation
2. cost and gradient function for Linear Regression
3. GD with Momentum function
4. Create contour
5. Create animation for GD with momentum
6. GD with NAG (Nesterov accelerated gradient) function
7. Create animation for GD with NAG
"""
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.mlab as mlab

# -----------------------------------initialize X, y and find theta by Normal Equation-----------------------------------
np.random.seed(2)

X = np.random.rand(1000, 1)
y = 4 + 3 * X + .2*np.random.randn(1000, 1) # y = theta0 + theta1 * x    ||    theta0 = 4, theta1 = 3

# Building Xbar 
one = np.ones((X.shape[0],1))
Xbar = np.concatenate((one, X), axis = 1)

A = np.dot(Xbar.T, Xbar)
b = np.dot(Xbar.T, y)
w_exact = np.dot(np.linalg.pinv(A), b)

print(w_exact.T)


# ------------------------------- cost and gradient function for Linear Regression ------------------------------
def cost(w):
	return .5/Xbar.shape[0]*np.linalg.norm(y - Xbar.dot(w), 2)**2

def grad(w):
	return 1/Xbar.shape[0] * Xbar.T.dot(Xbar.dot(w) - y)


# ============================================ GD with Momentum =================================================
def GD_momentum(w_init, grad, eta, gamma):
    w = [w_init]
    v = [np.zeros_like(w_init)]
    for it in range(100):
        v_new = gamma*v[-1] + eta*grad(w[-1])
        w_new = w[-1] - v_new
        # print(np.linalg.norm(grad(w_new))/len(w_new))
        if np.linalg.norm(grad(w_new))/len(w_new) < 1e-3:
            break
        w.append(w_new)
        v.append(v_new)
    return (w, it)
# ================================================================================================================

w_init = np.array([[2], [1]])
(w_mm, it_mm) = GD_momentum(w_init, grad, 1, 0.9)
print(w_mm[-1].T)


# ----------------------------------------------------- Contour ----------------------------------------------------- 
N = X.shape[0]
print(X.shape, N)
a1 = np.linalg.norm(y, 2)**2/N
b1 = 2*np.sum(X)/N
c1 = np.linalg.norm(X, 2)**2/N
d1 = -2*np.sum(y)/N 
e1 = -2*X.T.dot(y)/N

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

delta = 0.025
xg = np.arange(1.5, 7.0, delta)
yg = np.arange(0.5, 4.5, delta)
Xg, Yg = np.meshgrid(xg, yg)
Z = a1 + Xg**2 +b1*Xg*Yg + c1*Yg**2 + d1*Xg + e1*Yg


# ----------------------------------------------------- Animation -----------------------------------------------------
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

def update_mm(ii):
    if ii == 0:
        plt.cla()
        CS = plt.contour(Xg, Yg, Z, 100)
        manual_locations = [(4.5, 3.5), (4.2, 3), (4.3, 3.3)]
        animlist = plt.clabel(CS, inline=.1, fontsize=10, manual=manual_locations)
        plt.plot(w_exact[0], w_exact[1], 'go')
    else:
        animlist = plt.plot([w_mm[ii-1][0], w_mm[ii][0]], [w_mm[ii-1][1], w_mm[ii][1]], 'r-')
    
    animlist = plt.plot(w_mm[ii][0], w_mm[ii][1], 'ro', markersize = 4) 
    xlabel = '$\eta =$ ' + str(1) + '; iter = %d/%d' %(ii, it_mm)
    xlabel += '; ||grad||_2 = %.3f' % np.linalg.norm(grad(w_mm[ii]))
    ax.set_xlabel(xlabel)
    
    return animlist, ax
    

# ----------- visualization -------------
fig, ax = plt.subplots(figsize=(4,4))    
plt.cla()
plt.axis([1.5, 7, 0.5, 4.5])

anim1 = FuncAnimation(fig, update_mm, frames=np.arange(0, it_mm), interval=200)
plt.show()



# ================================== GD with NAG (Nesterov accelerated gradient) =======================================
def GD_NAG(w_init, grad, eta, gamma):
    w = [w_init]
    v = [np.zeros_like(w_init)]
    for it in range(100):
        v_new = gamma*v[-1] + eta*grad(w[-1] - gamma*v[-1])
        w_new = w[-1] - v_new
        # print(np.linalg.norm(grad(w_new))/len(w_new))
        if np.linalg.norm(grad(w_new))/len(w_new) < 1e-3:
            break
        w.append(w_new)
        v.append(v_new)
    return (w, it)
# ======================================================================================================================

(w_nag, it_nag) = GD_NAG(w_init, grad, 1, 0.9)
print(w_nag[-1].T)

# ----------------------------------------------------- animation -----------------------------------------------------
def update_nag(ii):
    if ii == 0:
        plt.cla()
        CS = plt.contour(Xg, Yg, Z, 100)
        manual_locations = [(4.5, 3.5), (4.2, 3), (4.3, 3.3)]
        animlist = plt.clabel(CS, inline=.1, fontsize=10, manual=manual_locations)
        plt.plot(w_exact[0], w_exact[1], 'go')
        plt.plot(4.5, 3.5, 'bo')
        plt.plot(4.2, 3, 'bo')
        plt.plot(4.3, 3.3, 'bo')
    else:
        animlist = plt.plot([w_nag[ii-1][0], w_nag[ii][0]], [w_nag[ii-1][1], w_nag[ii][1]], 'r-')
    
    animlist = plt.plot(w_nag[ii][0], w_nag[ii][1], 'ro', markersize = 4) 
    xlabel = '$\eta =$ ' + str(1) + '; iter = %d/%d' %(ii, it_nag)
    xlabel += '; ||grad||_2 = %.3f' % np.linalg.norm(grad(w_nag[ii]))
    ax.set_xlabel(xlabel)
    
    return animlist, ax
    

# ----------- visualization -------------
fig, ax = plt.subplots(figsize=(4,4))    
plt.cla()
plt.axis([1.5, 7, 0.5, 4.5])

anim1 = FuncAnimation(fig, update_nag, frames=np.arange(0, it_nag), interval=200)
plt.show()






























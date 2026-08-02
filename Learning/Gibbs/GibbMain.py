from GibbsVisual import GibbsVisual
from Sampler import GibbsSampler
import numpy as np

def main():

    mean = np.array([3, 4])
    cov = np.array([[2, 0.5], [0.5, 3]])
    samples = np.random.multivariate_normal(mean, cov, 5000)

    gs = GibbsSampler([1, 2], 2, 3, [[1, 0], [0, 1]], samples)

    gv = GibbsVisual(gs,  50, [3,4], 2500)

    gv.start()
if __name__ == '__main__':
    main()
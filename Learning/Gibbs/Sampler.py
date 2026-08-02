import random
import pandas as pd
import numpy as np
from scipy.stats import invwishart

mean = [3, 4]
cov = [[2,0.5],[0.5,3]]
samples = np.random.multivariate_normal(mean, cov, 5000)


class GibbsSampler:

    def __init__(self, pc, ps, pdof, pcov, dist):
        self.pc = pc
        self.ps = ps
        self.pdof = pdof
        self.pcov = pcov
        self.dist = dist

        self.c = self.pc
        self.s = self.ps
        self.dof = self.pdof
        self.cov = self.pcov

        self.meansamples = []
        self.covsamples = []

    def sample_mean(self):
        self.meansamples.append(np.random.multivariate_normal(((self.s * self.c + len(self.dist) * (np.mean(self.dist, axis=0)))/(len(self.dist)+self.s)) ,
                                                               (self.s + len(self.dist))**-1 * self.cov ))
        self.c = (self.s * self.c + len(self.dist) * (np.mean(self.dist, axis=0)))/(len(self.dist)+self.s)
        self.s = self.s + len(self.dist)

    def sample_cov(self):
        self.dof = self.pdof + len(self.dist) + 1

        self.cov = self.pcov + [[ , ], [ , ]] #np.sum((self.dist - self.c) ** 2) + self.ps * (np.mean(self.dist, axis=0) - self.pc)

        self.covsamples.append(invwishart.rvs(df=self.dof, scale=self.cov))




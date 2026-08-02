import numpy as np
from scipy.stats import invwishart

class GibbsSampler:

    def __init__(self, pc, ps, pdof, pcov, dist):

        self.pc = np.asarray(pc, dtype=float)
        self.ps = float(ps)
        self.pdof = float(pdof)
        self.pcov = np.asarray(pcov, dtype=float)
        self.dist = np.asarray(dist, dtype=float)

        self.current_mean = self.pc.copy()
        self.current_cov = self.pcov.copy()

        self.meansamples = []
        self.covsamples = []

    def sample_mean(self):

        n = len(self.dist)
        sample_avg = np.mean(self.dist, axis=0)

        post_prec = self.ps + n
        post_mean = (self.ps * self.pc + n * sample_avg)/post_prec

        sampled_mean = np.random.multivariate_normal(post_mean, self.current_cov / post_prec)

        self.current_mean = sampled_mean
        self.meansamples.append(sampled_mean.copy())

        return sampled_mean

    def sample_cov(self):

        n = len(self.dist)
        centered = self.dist - self.current_mean
        data_scatter = centered.T @ centered

        mean_diff = self.current_mean - self.pc
        prior_mean_scatter = self.ps * np.outer(mean_diff, mean_diff)

        post_scale = self.pcov + data_scatter + prior_mean_scatter

        post_dof = self.pdof + n + 1

        scov = invwishart.rvs(post_dof, post_scale)

        self.current_cov = scov
        self.covsamples.append(scov)

        return scov


    def samples(self, n, b=0):

        for i in range(n):
            self.sample()
        return np.asarray(self.meansamples[b:]), np.asarray(self.covsamples[b:])

    def sample(self):

        smean = self.sample_mean()
        scov = self.sample_cov()
        return smean, scov

    def get_means(self):
        return self.meansamples




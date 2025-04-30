def grad(self, X, lenscale=None):
        r"""
        Get the gradients of this basis w.r.t.\ the length scale.

        Parameters
        ----------
        x: ndarray
            (n, d) array of observations where n is the number of samples, and
            d is the dimensionality of x.
        lenscale: scalar or ndarray
            scalar or array of shape (d,) length scales (one for each dimension
            of x).If not input, this uses the value of the initial length
            scale.


        Returns
        -------
        ndarray:
            shape (n, 2*nbases) where nbases is number of random rbf bases,
            again to the nearest larger two power. This is
            :math:`\partial \phi(\mathbf{x}) / \partial l`
        """
        d = X.shape[1]
        lenscale = self._check_dim(d, lenscale)

        VX = self._makeVX(X / lenscale)
        sinVX = - np.sin(VX)
        cosVX = np.cos(VX)

        dPhi = []
        for i, l in enumerate(lenscale):
            indlen = np.zeros(d)
            indlen[i] = 1. / l**2
            dVX = - self._makeVX(X * indlen)  # FIXME make this more efficient?
            dPhi.append(np.hstack((dVX * sinVX, dVX * cosVX)) /
                        np.sqrt(self.n))

        return np.dstack(dPhi) if len(lenscale) != 1 else dPhi[0]
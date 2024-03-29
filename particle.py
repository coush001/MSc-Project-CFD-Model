from itertools import count
import numpy as np


class Particle(object):
    """Object containing all the properties for a single particle"""

    _ids = count(0)

    def __init__(self, main_data=None, x=np.zeros(2)):
        self.id = next(self._ids)
        self.main_data = main_data
        self.x = np.array(x)
        self.v = np.zeros(2)
        self.a = np.zeros(2)
        self.D = 0
        self.rho = main_data.rho0
        self.P = 0
        self.m = main_data.dx ** 2 * main_data.rho0  # initial mass depends on the initial particle spacing
        self.boundary = False  # Particle by default is not on the boundary
        # For predictor corrector
        self.prev_x = np.array(x)
        self.prev_v = np.zeros(2)
        self.prev_rho = main_data.rho0

    def calc_index(self):
        """Calculates the 2D integer index for the particle's location in the search grid"""
        # Calculates the bucket coordinates
        self.list_num = np.array((self.x - self.main_data.min_x) /
                                 (2.0 * self.main_data.h), int)

    def B(self):
        return (self.main_data.rho0 * self.main_data.c0 ** 2) / self.main_data.gamma

    def update_P(self):
        """
        Equation of state
        System is assumed slightly compressible
        """
        rho0 = self.main_data.rho0
        gamma = self.main_data.gamma
        self.P = self.B() * ((self.rho / rho0)**gamma - 1)

    def set_main_data(self, main_data):
        self.main_data = main_data

    def set_x(self, x):
        self.x = x
        self.calc_index()

    def set_v(self, v):
        self.v = v

    def set_a(self, a):
        self.a = a

    def set_D(self, D):
        self.D = D

    def set_rho(self, rho):
        self.rho = rho
        self.update_P()

    def m(self, m):
        self.m = m

    def list_attributes(self):
        x_s = "position: " + str(self.x) + ", "
        v_s = "velocity: " + str(self.v) + ", "
        a_s = "acceleration: " + str(self.a) + ", "
        D_s = "derivative of density: " + str(self.D) + ", "
        rho_s = "density: " + str(self.rho) + ", "
        m_s = "mass: " + str(self.m) + ", "
        P_s = "pressure: " + str(self.P) + ", "
        boundary_s = "is boundary: " + str(self.boundary)
        return [x_s + v_s + a_s + D_s + rho_s + m_s + P_s + boundary_s]

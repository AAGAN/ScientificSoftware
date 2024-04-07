import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import json

class ScientificSoftwareProblem:
    """This class includes the implementation of methods needed to solve the 
    Scientific Software Coding Problem defined by Commonwealth Fusion Systems"""

    def __init__(self, copper_heat_capacity_vs_temperature_csv_filepath = None, copper_RRR100_resistivity_vs_temperature_csv_filepath = None, tf_coils_alcator_cmod_json_filepath = None):
        """To initialize the class, you can provide the location of each input file.
        if the filepaths are not provided, the location is considered to be in a folder
        named data in the working directory."""
        #phisical properties
        self.rho_m = 8960 #density of copper at 100K in Kg/m^3
        self.mu_0 = 1.25663706143e-6 #vacuum permeability
        #read the input files
        if (copper_heat_capacity_vs_temperature_csv_filepath == None):
            copper_heat_capacity_vs_temperature_csv_filepath = './data/copper_heat_capacity_vs_temperature.csv'
        self.SpecificHeatCapacityData = np.genfromtxt(copper_heat_capacity_vs_temperature_csv_filepath, delimiter=',')
        if (copper_RRR100_resistivity_vs_temperature_csv_filepath == None):
            copper_RRR100_resistivity_vs_temperature_csv_filepath = './data/copper_RRR100_resistivity_vs_temperature.csv'
        self.CopperResistivityData = np.genfromtxt(copper_RRR100_resistivity_vs_temperature_csv_filepath, delimiter=',')
        if (tf_coils_alcator_cmod_json_filepath == None):
            tf_coils_alcator_cmod_json_filepath = './data/tf_coils_alcator_cmod.json'
        with open(tf_coils_alcator_cmod_json_filepath) as file:
            self.TFCoilsAlcatorCmodData = json.load(file)
        #Extract information from the input files
        self.current_densities_to_plot_A_per_m2 = self.TFCoilsAlcatorCmodData['current_densities_to_plot_A_per_m2']
        self.major_radius_m = self.TFCoilsAlcatorCmodData['major_radius_m']
        self.number_tf_coils = self.TFCoilsAlcatorCmodData['number_tf_coils']
        self.number_turns_per_tf_coil = self.TFCoilsAlcatorCmodData['number_turns_per_tf_coil']
        self.cross_section_area_turn_m2 = self.TFCoilsAlcatorCmodData['cross_section_area_turn_m2']
        self.coil_temperature_initial_K = self.TFCoilsAlcatorCmodData['coil_temperatures_K']['initial']
        self.coil_temperature_final_K = self.TFCoilsAlcatorCmodData['coil_temperatures_K']['final']
        self.TemperatureC = self.SpecificHeatCapacityData[1:,0] #
        self.SpecificHeatCapacity = self.SpecificHeatCapacityData[1:,1]
        self.TemperatureRho_e = self.CopperResistivityData[1:,0]
        self.CuElectricalResistivity = self.CopperResistivityData[1:,1]
        self.jiterator = 0
        self.PulseDuration = np.zeros(len(self.current_densities_to_plot_A_per_m2))
        self.MagneticField = np.zeros(len(self.current_densities_to_plot_A_per_m2))

    def __SpecificHeatCapacityFunc(self, T, n = 1):
        """This private method interpolates between the values of specific heat capacity vs Temperature"""
        interpolated_value = 0
        if (n==1):
            interpolated_value = np.interp(T, self.TemperatureC,self.SpecificHeatCapacity)
        else:
            coefficients = np.polyfit(self.TemperatureC,self.SpecificHeatCapacity,n)
            interpolated_value = np.polyval(coefficients, T)
        return interpolated_value
    
    def __CuResistivityElectricalResistivityFunc(self, T, n = 1):
        """This private method interpolates between resistivity values vs Temperature"""
        interpolated_value = 0
        if (n==1):
            interpolated_value = np.interp(T, self.TemperatureRho_e,self.CuElectricalResistivity)
        else:
            coefficients = np.polyfit(self.TemperatureRho_e,self.CuElectricalResistivity, n)
            interpolated_value = np.polyval(coefficients, T)
        #print(interpolated_value)
        return interpolated_value*1e-8
    
    def __dT_dt(self, t, T):
        """This private method defines the ODE derived from conservation of energy equation"""
        rho_e_val = self.__CuResistivityElectricalResistivityFunc(T)
        c_val = self.__SpecificHeatCapacityFunc(T)
        j_squared = self.jiterator**2  # Adjust this as needed
        return rho_e_val / c_val / self.rho_m * j_squared
    
    def __MagneticFieldMagnitude(self):
        """This private method implements the Ampere's law and returns the toroidal magnetic field"""
        B0 = self.mu_0 * self.number_tf_coils * self.number_turns_per_tf_coil * self.cross_section_area_turn_m2 * self.jiterator / 2.0 / np.pi / self.major_radius_m
        return B0
    
    def solve_RK4(self):
        """This function uses 4th order Rung-Kutta method to solve the ODE and output the results"""
        t_final = 50 #seconds max time to solve for, large enough to reach pulse duration
        dt = 0.01 #seconds
        num_steps = int(t_final/dt)
        T = np.zeros(num_steps + 1)
        T[0] = self.coil_temperature_initial_K
        count = 0
        for j in self.current_densities_to_plot_A_per_m2:
            self.jiterator = j #set the object's jiterator so __dT_dt function gets the correct value
            for k in range(num_steps):
                k1 = dt * self.__dT_dt(0,T[k])
                k2 = dt * self.__dT_dt(0,T[k]+0.5*k1)
                k3 = dt * self.__dT_dt(0,T[k]+0.5*k2)
                k4 = dt * self.__dT_dt(0,T[k] + k3)
                T[k+1] = T[k] + (k1+2*k2+2*k3+k4)/6
                if(T[k+1]>=self.coil_temperature_final_K):
                    self.PulseDuration[count]=dt*(k+1)
                    break
            self.MagneticField[count] = self.__MagneticFieldMagnitude()
            count += 1
        self.__output_results()
    
    def solve_ivp(self):
        """This function uses scipy.integrate.solve_ivp to solve the ODE and output the results"""
        def stop_integration(t, T):
            return T[0] - self.coil_temperature_final_K
        stop_integration.terminal = True # Stop integration when condition is met
        t_span = (0,50) #define a large enough span of time to reach the pulse duration
        count = 0
        for j in self.current_densities_to_plot_A_per_m2:
            self.jiterator = j
            sol = solve_ivp(self.__dT_dt, t_span, [self.coil_temperature_initial_K],events=stop_integration)
            self.PulseDuration[count]=sol.t_events[0][0]
            self.MagneticField[count]=self.__MagneticFieldMagnitude()
            count += 1
        self.__output_results()

    def __output_results(self):
        self.__print_results()
        self.__plot_results()

    def __plot_results(self):
        fig, ax1 = plt.subplots()
        ax1.plot(self.current_densities_to_plot_A_per_m2, self.PulseDuration, 'b-',marker='x',label='Pulse Duration (s)', linestyle='-.')
        ax1.set_xlabel('Current Density ($A/m^2$)')
        ax1.set_ylabel('Pulse Duration (s)', color='b')
        ax1.tick_params('y',colors='b')

        ax2 = ax1.twinx()
        ax2.plot(self.current_densities_to_plot_A_per_m2, self.MagneticField, color = 'r',marker='o',label='Magnetic Field (T)')
        ax2.set_ylabel('Magnetic Field At Major Radius (T)', color='r')
        ax2.tick_params('y',colors='r')

        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper center')

        ax1.set_yticks([0,5,10,15,20,25,30,35,40,45])
        ax2.set_yticks(np.linspace(0,9,10))

        ax1.set_xlim(left=0.2e8)
        ax2.set_xlim(left=0.2e8)
        ax1.set_ylim(bottom=0)
        ax2.set_ylim(bottom=0)
        ax1.set_ylim(top=45)
        ax2.set_ylim(top=9)
        ax2.set_title('Pulse Duration and Magnetic Field vs Current Density')
        ax1.grid(which='both', color='gray', linestyle='--')
        ax2.grid(which='both', color='gray', linestyle='--')

        plt.show()

    def __print_results(self):
        # Define table header with formatting
        header = "{:22s} {:28s} {:20s}".format("Current Density A/m^2 | ", "Magnetic Field at Major Radius (T) | ", "Pulse Duration (s)")
        print(header)
        print("-" * len(header))  # Print a line separator

        # Loop through elements and print each row with formatting
        for i in range(len(self.current_densities_to_plot_A_per_m2)):
            row = "{:18.2e} {:28.4e} {:22.4e}".format(self.current_densities_to_plot_A_per_m2[i], self.MagneticField[i], self.PulseDuration[i])
            print(row)

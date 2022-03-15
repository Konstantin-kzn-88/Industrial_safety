class LCLP:
    def __init__(self, mass_SAM=200, mol_mass=95.3, t_boiling=68, LCLP=1.8):
        """
        The class accepts three mandatory parameters:
        - mass of the steam-air mixture, kg;
        - molecular weight, kg/kmol
        - temp. boiling, deg.C
        - lower concentration limit, % vol.;

        """
        self.mass_SAM = mass_SAM  # SAM - steam-air mixture
        self.mol_mass = mol_mass
        self.t_boiling = t_boiling
        self.LCLP = LCLP

    def culculation_R_LCLP(self, mass_SAM=200, mol_mass=95.3, t_boiling=68, LCLP=1.8):
        """
        R_LCLP - radius of the lower concentration limit of the flame propagation

        Parametrs:
        mass_SAM- mass of the steam-air mixture, kg;
        mol_mass - molecular weight, kg/kmol
        t_boiling - temp. boiling, deg.C
        LCLP - lower concentration limit, % vol.;

        Return:
        R_LCLP in meters (float)
        """
        vapour_density = mol_mass / (22.413 * (1 + 0.00367 * t_boiling))
        R_LCLP = round(7.8 * ((mass_SAM / (vapour_density * LCLP)) ** 0.33), 2)
        R_f = round((R_LCLP * 1.2), 2)

        return (R_LCLP, R_f)
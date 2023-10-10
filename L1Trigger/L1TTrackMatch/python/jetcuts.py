old_cuts = False

# old cuts
if old_cuts:
    minbias = False
    mva = -1.

    # old cuts
    dz = 0.5 #different cuts for trkfastjet...
    dz_trkjet = 1. #...then trkjet
    chi2dof = 10.
    bendchi2 = 2.2
    tightchi2 = True
# new cuts to alter
else:
    minbias = False
    mva = 0.1
    dz = -1.#0.75
    dz_trkjet = dz

    tight_barrel = False #if you want to apply a tighter barrel cut (trk eta<1.8) than eta
    barrel_mva = 0.1
    barrel_dz = 0.55

    # turn off old cuts
    chi2dof = 10000.
    bendchi2 = 10000.
    tightchi2 = False

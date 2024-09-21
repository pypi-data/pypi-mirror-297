# PyfodMC - Python Fermi-orbital descriptor Monte-Carlo 
[![license](https://img.shields.io/badge/license-APACHE2-green)](https://www.apache.org/licenses/LICENSE-2.0)
[![language](https://img.shields.io/badge/language-Python3-blue)](https://www.python.org/)
[![version](https://img.shields.io/badge/version-1.0.0-lightgrey)](https://gitlab.com/opensic/PyfodMC/-/blob/main/README.md)

The Python Fermi-orbital descriptor Monte-Carlo (PyfodMC) is a Python code for 
the determination of Fermi-orbital descriptors (FODs) for atomic, molecular, 
and periodic systems. It follows a simple input structure, where user primarily
define the bond patterns between the atoms in the structure. Everything else 
is handled internally through PyfodMC. Additional options for greater flexibility 
have also been added, like the explicit definition of lone FODs. Further options 
include the definiton of charge, whether to exchange the up and the dn channel,
the definition of alternate electronic configurations, and the removal of core FODs
for each atom.


PyfodMC is the successor of the Fermi-orbital descriptor MOnte-Carlo (fodMC) code.    
PyfodMC is based on fodMC, version 1.2.2, but has been written exclusively in Python.    
Furthermore, several improvements over the original fodMC code have been added for     
increased robustness and reproducibility.
As such, the support for the original fodMC code will stop, and support for the PyfodMC
code will start.



## Installation
Using pip
```bash 
$ pip3 install PyfodMC
```
or install locally
```bash 
$ git clone https://gitlab.com/opensic/PyfodMC.git
$ cd PyfodMC
$ pip3 install -e .
```

Examples can be found in the examples folder.


## Citation
For publications, please consider citing the following articles        

- **Interpretation and automatic generation of Fermi-orbital descriptors**         
    [S. Schwalbe et al., J. Comput. Chem. 40, 2843-2857, 2019](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.26062)

- **Chemical bonding theories as guides for self-interaction corrected solutions: multiple local minima and symmetry breaking**      
    K. Trepte, S. Schwalbe, S. Liebing, W. T. Schulze, J. Kortus, H. Myneni, A. V. Ivanov, and S. Lehtola    
    arXiv e-prints, Subject: Computational Physics (physics.comp-ph), 2021, [arXiv:2109.08199](https://arxiv.org/abs/2109.08199)     
    [J. Chem. Phys., vol. 155, no. 22, p. 224109, 2021](https://doi.org/10.1063/5.0071796)

- **Why the energy is sometimes not enough - A dive into self-interaction corrected density functional theory**     
   S. Liebing, K. Trepte, and S. Schwalbe      
    arXiv e-prints, Subject: Chemical Physics (physics.chem-ph); Computational Physics (physics.comp-ph), 2022, [arXiv:2201.11648](https://arxiv.org/abs/2201.11648)    


# ATTENTION
While the PyfodMC can create FODs for      
any system, we do not recommend using       
guesses for systems containing transition metals.

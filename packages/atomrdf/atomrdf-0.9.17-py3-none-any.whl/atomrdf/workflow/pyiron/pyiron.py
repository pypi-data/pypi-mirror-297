"""
Wrappers for pyiron jobs
"""

import os
from functools import partial, update_wrapper
from pyscal3.core import structure_dict, element_dict

from atomrdf.structure import _make_crystal, _make_grain_boundary
import atomrdf.workflow.pyiron.lammps as lammps
import atomrdf.workflow.pyiron.vasp as vasp
import atomrdf.workflow.pyiron.murnaghan as murnaghan
import atomrdf.workflow.pyiron.quasiharmonic as qha
import atomrdf.workflow.pyiron.calphy as calphy

def process_job(job):
    """
    Checkes if the job is valid and creates the necessary output dict
    for the job.

    Parameters
    ----------
    job : pyiron.Job
        The pyiron job object to check.
    
    Raises
    ------
    TypeError
        If the job is not a valid pyiron job.
    """
    if type(job).__name__ == 'Lammps':
        return lammps.process_job(job)
    if type(job).__name__ == 'Vasp':
        return vasp.process_job(job)    
    elif type(job).__name__ == 'Murnaghan':
        return murnaghan.process_job(job)
    elif type(job).__name__ == 'QuasiHarmonicJob':
        return qha.process_job(job)
    elif type(job).__name__ == 'Calphy':
        return calphy.process_job(job)
    else:
        raise TypeError("These type of pyiron Job is not currently supported")
    
    

def inform_graph(pr, kg):
    """
    this function in general can be used to do extra methods to set up things as needed
    for the workflow environment. 

    For example, for pyiron, this updates the project object to have the graph and creator objects
    """

    try:
        from pyiron_base import Creator, PyironFactory
        from pyiron_atomistics.atomistics.structure.atoms import (
            ase_to_pyiron,
            pyiron_to_ase,
        )
        import pyiron_atomistics.atomistics.structure.factory as sf
    except ImportError:
        raise ImportError("Please install pyiron_base and pyiron_atomistics")

    class AnnotatedStructureFactory:
        def __init__(self, graph):
            self._graph = graph

        def bulk(
            self,
            element,
            repetitions=None,
            crystalstructure=None,
            a=None,
            covera=1.633,
            cubic=True,
            graph=None,
            label=None,
        ):

            if crystalstructure is None:
                crystalstructure = element_dict[element]["structure"]
                if a is None:
                    a = element_dict[element]["lattice_constant"]

            struct = _make_crystal(
                crystalstructure,
                repetitions=repetitions,
                lattice_constant=a,
                ca_ratio=covera,
                element=element,
                primitive=not cubic,
                graph=self._graph,
                label=label,
            )

            ase_structure = struct.write.ase()
            pyiron_structure = ase_to_pyiron(ase_structure)
            pyiron_structure.info["sample_id"] = struct.sample
            return pyiron_structure

        def grain_boundary(
            self,
            axis,
            sigma,
            gb_plane,
            crystalstructure=None,
            element=None,
            a=1,
            covera=1.633,
            repetitions=(1, 1, 1),
            overlap=0.0,
            gap=0.0,
            vacuum=0.0,
            delete_layer="0b0t0b0t",
            tolerance=  0.25,
            primitive=False,
            uc_a=1,
            uc_b=1,
            graph=None,
            names=False,
            label=None,
            backend='aimsgb'  
        ):

            struct = _make_grain_boundary(
                axis,
                sigma,
                gb_plane,
                structure=crystalstructure,
                element=element,
                lattice_constant=a,
                ca_ratio=covera,
                repetitions=repetitions,
                overlap=overlap,
                gap=gap,
                vacuum=vacuum,
                delete_layer=delete_layer,
                tolerance=tolerance,
                primitive=primitive,
                uc_a=uc_a,
                uc_b=uc_b,
                graph=self._graph,
                names=names,
                label=label,
                backend=backend  
            )

            ase_structure = struct.write.ase()
            pyiron_structure = ase_to_pyiron(ase_structure)
            pyiron_structure.info["sample_id"] = struct.sample
            return pyiron_structure
        
    class StructureFactory(sf.StructureFactory):
        def __init__(self, graph):
            super().__init__()
            self._annotated_structure = AnnotatedStructureFactory(graph)

        @property
        def annotated_structure(self):
            return self._annotated_structure

    class StructureCreator(Creator):
        def __init__(self, project):
            super().__init__(project)
            self._structure = StructureFactory(project.graph)

        @property
        def structure(self):
            return self._structure

    pr.graph = kg
    pr._creator = StructureCreator(pr)



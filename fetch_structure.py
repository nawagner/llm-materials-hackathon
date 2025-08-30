#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from pymatgen.ext.matproj import MPRester

load_dotenv()

def fetch_crystal_structure(material_id):
    """Fetch crystal structure using pymatgen's MPRester"""
    api_key = os.getenv("MP_API_KEY")
    
    if not api_key:
        raise ValueError("MP_API_KEY not found in environment variables")
    
    # Use pymatgen's MPRester (simplified version)
    with MPRester(api_key) as mpr:
        # Get structure only - this should work with the simplified MPRester
        structure = mpr.get_structure_by_material_id(material_id)
        
        return {
            'structure': structure,
            'material_data': {}
        }

if __name__ == "__main__":
    material_id = "mp-126"
    
    try:
        data = fetch_crystal_structure(material_id)
        
        if data and data['structure']:
            structure = data['structure']
            material_data = data['material_data']
            
            print(f"Crystal structure for {material_id}:")
            print(f"Formula: {structure.composition.reduced_formula}")
            print(f"Number of sites: {len(structure.sites)}")
            print(f"Elements: {[str(elem) for elem in structure.composition.elements]}")
            
            # Get space group info
            try:
                spg_info = structure.get_space_group_info()
                print(f"Space group symbol: {spg_info[0]}")
                print(f"Space group number: {spg_info[1]}")
            except:
                print("Space group info not available")
            
            print(f"\nLattice parameters:")
            print(f"  a = {structure.lattice.a:.4f} Å")
            print(f"  b = {structure.lattice.b:.4f} Å") 
            print(f"  c = {structure.lattice.c:.4f} Å")
            print(f"  α = {structure.lattice.alpha:.2f}°")
            print(f"  β = {structure.lattice.beta:.2f}°")
            print(f"  γ = {structure.lattice.gamma:.2f}°")
            print(f"  Volume = {structure.lattice.volume:.4f} Å³")
            
            print(f"\nStructure contains {len(structure.sites)} atomic sites:")
            for i, site in enumerate(structure.sites[:10]):  # Show first 10 sites
                coords = site.coords
                species = str(site.specie)
                print(f"  Site {i+1}: {species} at [{coords[0]:.4f}, {coords[1]:.4f}, {coords[2]:.4f}]")
            
            if len(structure.sites) > 10:
                print(f"  ... and {len(structure.sites) - 10} more sites")
                
            # Additional material data if available
            if material_data:
                if 'formation_energy_per_atom' in material_data:
                    print(f"\nFormation energy per atom: {material_data['formation_energy_per_atom']:.4f} eV/atom")
                if 'band_gap' in material_data:
                    print(f"Band gap: {material_data['band_gap']:.4f} eV")
                if 'energy_per_atom' in material_data:
                    print(f"Energy per atom: {material_data['energy_per_atom']:.4f} eV/atom")
        else:
            print(f"No structure data found for {material_id}")
            
    except Exception as e:
        print(f"Error fetching structure: {e}")
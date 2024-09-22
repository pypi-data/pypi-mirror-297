use anyhow;
use extxyz::{read_xyz_frames, Info, RawAtoms};
use ndarray::Array2;

pub struct Atoms {
    pub symbols: Vec<String>,
    pub positions: Array2<f64>,
    pub cell: Option<Array2<f64>>,
    pub energy: Option<f64>,
    pub forces: Option<Array2<f64>>,
    pub stress: Option<Array2<f64>>,
    pub momenta: Option<Array2<f64>>,
}

pub fn read_extxyz(
    filename: impl AsRef<std::path::Path> + std::fmt::Display,
    start: Option<usize>,
    end: Option<usize>,
    step: Option<usize>,
) -> anyhow::Result<Vec<Atoms>> {
    let selection = match (start, end, step) {
        (Some(start), Some(end), Some(step)) => (start..end).step_by(step),
        (Some(start), Some(end), None) => (start..end).step_by(1),
        (Some(start), None, None) => (start..usize::MAX).step_by(1),
        (Some(start), None, Some(step)) => (start..usize::MAX).step_by(step),
        (None, Some(end), Some(step)) => (0..end).step_by(step),
        (None, Some(end), None) => (0..end).step_by(1),
        (None, None, None) => (0..usize::MAX).step_by(1),
        (None, None, Some(step)) => (0..usize::MAX).step_by(step),
    };
    let frames = read_xyz_frames(filename, selection)?;

    let mut atoms_list = vec![];
    for frame in frames {
        let atoms = RawAtoms::parse_from(&frame)?;
        // it will returen error if the comment is not in normal extxyz format
        let info: Info = atoms.comment.parse()?;
        // get molecule's properties
        let lattice = {
            let raw = info.get("Lattice").map(|x| x.as_array().unwrap());
            match raw {
                Some(vals) => {
                    let vals = vals.as_slice();
                    let mut lattice = Array2::zeros((3, 3));
                    for i in 0..3 {
                        for j in 0..3 {
                            lattice[[i, j]] = vals[i * 3 + j].as_f64().unwrap();
                        }
                    }
                    Some(lattice)
                }
                None => None,
            }
        };
        let energy = info.get("energy").map(|x| x.as_f64().unwrap());
        let stress = {
            let raw = info.get("stress").map(|x| x.as_array().unwrap());
            match raw {
                Some(vals) => {
                    let vals = vals.as_slice();
                    let mut stress = Array2::zeros((3, 3));
                    for i in 0..3 {
                        for j in 0..3 {
                            stress[[i, j]] = vals[i * 3 + j].as_f64().unwrap();
                        }
                    }
                    Some(stress)
                }
                None => None,
            }
        };

        // get atom's properties
        let mut symbols = vec![];
        let mut positions = vec![];

        let mut raw_forces = vec![];
        let mut raw_momenta = vec![];

        for atom in atoms.atoms {
            symbols.push(atom.element.to_string());
            positions.extend_from_slice(atom.position.as_slice());

            let atom_properties = info.parse_extra_columns(&atom.extra)?;

            let forces = &atom_properties.get("forces");
            let flat_forces = match forces {
                Some(forces) => {
                    let forces = forces.as_array().unwrap().as_slice();
                    Some([
                        forces[0].as_f64().unwrap(),
                        forces[1].as_f64().unwrap(),
                        forces[2].as_f64().unwrap(),
                    ])
                }
                None => None,
            };
            if let Some(forces) = flat_forces {
                raw_forces.extend_from_slice(&forces);
            }

            let momenta = &atom_properties.get("momenta");
            let flat_momenta = match momenta {
                Some(momenta) => {
                    let momenta = momenta.as_array().unwrap().as_slice();
                    Some([
                        momenta[0].as_f64().unwrap(),
                        momenta[1].as_f64().unwrap(),
                        momenta[2].as_f64().unwrap(),
                    ])
                }
                None => None,
            };
            if let Some(momenta) = flat_momenta {
                raw_momenta.extend_from_slice(&momenta);
            }
        }
        let positions = Array2::from_shape_vec((symbols.len(), 3), positions)?;
        let forces = match raw_forces.len() > 0 {
            true => Some(Array2::from_shape_vec((symbols.len(), 3), raw_forces)?),
            false => None,
        };
        let momenta = match raw_momenta.len() > 0 {
            true => Some(Array2::from_shape_vec((symbols.len(), 3), raw_momenta)?),
            false => None,
        };

        // Parse force

        let atoms = Atoms {
            symbols,
            positions,
            cell: lattice,
            energy,
            forces,
            stress,
            momenta,
        };
        atoms_list.push(atoms);
    }

    Ok(atoms_list)
}

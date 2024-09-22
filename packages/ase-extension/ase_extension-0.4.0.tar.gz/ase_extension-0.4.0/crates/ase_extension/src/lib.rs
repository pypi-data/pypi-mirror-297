use ase_extension_core::io;
use ase_extension_core::logfermi;
use ase_extension_core::neighborlist;
use ase_extension_core::rmsd;
use ndarray::prelude::*;
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray2};
use pyo3::prelude::*;

// Module declaration
#[pymodule]
fn _ext(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(read_extxyz))?;
    m.add_wrapped(wrap_pyfunction!(log_fermi_spherical_potential))?;
    m.add_wrapped(wrap_pyfunction!(compute_minimum_rmsd))?;
    m.add_wrapped(wrap_pyfunction!(neighbor_list))?;
    Ok(())
}

// Member functions
#[pyfunction]
fn read_extxyz<'py>(
    _py: Python<'py>,
    filename: &str,
    start: Option<usize>,
    end: Option<usize>,
    step: Option<usize>,
) -> Vec<(
    Vec<String>,
    &'py PyArray2<f64>,
    Option<&'py PyArray2<f64>>,
    Option<f64>,
    Option<&'py PyArray2<f64>>,
    Option<&'py PyArray2<f64>>,
    Option<&'py PyArray2<f64>>,
)> {
    let atoms_list = io::read_extxyz(filename, start, end, step).unwrap();
    atoms_list
        .into_iter()
        .map(|atoms| {
            (
                atoms.symbols,
                atoms.positions.into_pyarray(_py),
                atoms.cell.map(|x| x.into_pyarray(_py)),
                atoms.energy,
                atoms.forces.map(|x| x.into_pyarray(_py)),
                atoms.stress.map(|x| x.into_pyarray(_py)),
                atoms.momenta.map(|x| x.into_pyarray(_py)),
            )
        })
        .collect()
}

#[pyfunction]
fn log_fermi_spherical_potential<'py>(
    _py: Python<'py>,
    positions: PyReadonlyArray2<f64>,
    radius: f64,
    temperature: f64,
    beta: f64,
) -> (f64, &'py PyArray2<f64>) {
    let positions = positions.as_array();
    let (e, e_grad) =
        logfermi::log_fermi_spherical_potential(&positions, radius, temperature, beta);
    (e, e_grad.into_pyarray(_py))
}
#[pyfunction]
fn compute_minimum_rmsd<'py>(
    _py: Python<'py>,
    positions_1: PyReadonlyArray2<f64>,
    positions_2: PyReadonlyArray2<f64>,
    compute_gradient: bool,
) -> (
    f64,
    Option<&'py PyArray2<f64>>,
    &'py PyArray2<f64>,
    &'py PyArray1<f64>,
) {
    let positions_1 = positions_1.as_array();
    let positions_2 = positions_2.as_array();
    let result = rmsd::compute_minimum_rmsd(&positions_1, &positions_2, compute_gradient);
    let rmsd_grad = result.rmsd_grad.map(|x| x.into_pyarray(_py));
    (
        result.rmsd_val,
        rmsd_grad,
        result.rotation_matrix.into_pyarray(_py),
        result.translation_vector.into_pyarray(_py),
    )
}
#[pyfunction]
#[pyo3(signature = (positions, cell=None, cutoff=5.0, parallel=true))]
fn neighbor_list<'py>(
    _py: Python<'py>,
    positions: PyReadonlyArray2<f64>,
    cell: Option<PyReadonlyArray2<f64>>,
    cutoff: f64,
    parallel: bool,
) -> (
    &'py PyArray1<usize>,
    &'py PyArray1<usize>,
    &'py PyArray1<f64>,
    &'py PyArray2<f64>,
) {
    let positions: Vec<[f64; 3]> = positions
        .as_array()
        .axis_iter(Axis(0))
        .map(|x| [x[0], x[1], x[2]])
        .collect();
    let cell: Option<[[f64; 3]; 3]> = cell.map(|x| {
        let x = x.as_array();
        [
            [x[[0, 0]], x[[0, 1]], x[[0, 2]]],
            [x[[1, 0]], x[[1, 1]], x[[1, 2]]],
            [x[[2, 0]], x[[2, 1]], x[[2, 2]]],
        ]
    });
    let neighbor_list =
        neighborlist::construct_neighbor_list(&positions, cell.as_ref(), cutoff, parallel);

    let offsets: Array2<f64> = Array2::from_shape_vec(
        (neighbor_list.offsets.len(), 3),
        neighbor_list
            .offsets
            .iter()
            .flat_map(|x| x.to_vec())
            .collect(),
    )
    .expect("Failed to convert offsets to ndarray");
    (
        neighbor_list.idx_i.into_pyarray(_py),
        neighbor_list.idx_j.into_pyarray(_py),
        neighbor_list.dists.into_pyarray(_py),
        offsets.into_pyarray(_py),
    )
}

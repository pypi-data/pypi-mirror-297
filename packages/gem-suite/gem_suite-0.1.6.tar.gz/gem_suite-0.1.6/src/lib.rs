// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

use pyo3::prelude::*;

mod graph;
pub mod heavyhex;
mod mock;
mod utils;

#[pymodule]
fn gem_core(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<heavyhex::PyHeavyHexLattice>()?;
    m.add_class::<heavyhex::PyQubit>()?;
    m.add_class::<heavyhex::PyPlaquette>()?;
    m.add_class::<heavyhex::PyScheduledGate>()?;
    m.add_function(wrap_pyfunction!(
        heavyhex::visualization::visualize_plaquette_with_noise,
        m
    )?)?;
    Ok(())
}

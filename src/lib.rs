use path_tree::PathTree;
use pyo3::prelude::*;

#[pyclass(module = "routrie._routrie")]
struct Router {
    router: PathTree<Py<PyAny>>,
}

#[pymethods]
impl Router {
    #[new]
    fn new() -> Self {
        Router {
            router: PathTree::new(),
        }
    }
    fn insert(&mut self, path: &str, data: &PyAny, py: Python) -> () {
        self.router.insert(path, data.into_py(py));
    }
    fn find<'m>(&'m self, path: &'m str) -> Option<(&'m Py<PyAny>, Vec<(&'m str, &'m str)>)> {
        self.router.find(path)
    }
}

#[pymodule]
fn _routrie(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Router>()?;
    Ok(())
}

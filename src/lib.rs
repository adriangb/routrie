use path_tree::PathTree;
use pyo3::prelude::*;

#[pyclass(module = "routrie._routrie")]
struct Router {
    router: PathTree<Py<PyAny>>,
    // path-tree dropped support for empty values
    // so we implement it here as a special case
    empty: Option<Py<PyAny>>,
}

type MatchedRoute<'a> = (&'a Py<PyAny>, Vec<(&'a str, &'a str)>);

#[pymethods]
impl Router {
    #[new]
    fn new() -> Self {
        Router {
            router: PathTree::new(),
            empty: None,
        }
    }
    fn insert(&mut self, path: &str, data: &PyAny, py: Python) {
        match path.is_empty() {
            true => self.empty = Some(data.into()),
            false => {
                self.router.insert(path, data.into_py(py));
            }
        }
    }
    fn find<'a>(&'a self, path: &'a str) -> Option<MatchedRoute<'a>> {
        match path.is_empty() {
            true => self.empty.as_ref().map(|v| (v, vec![])),
            false => match self.router.find(path) {
                None => None,
                Some(path) => Some((path.value, path.params())),
            },
        }
    }
}

#[pymodule]
fn _routrie(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Router>()?;
    Ok(())
}

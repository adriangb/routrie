use path_tree::PathTree;
use pyo3::prelude::*;

#[pyclass(module = "routrie")]
#[derive(Clone)]
struct Param {
    #[pyo3(get)]
    name: String,
    #[pyo3(get)]
    value: String,
}

impl Param {
    fn to_string(&self) -> String {
        format!("Param({}, {})", self.name, self.value)
    }
}

#[pymethods]
impl Param {
    fn __str__(&self) -> String {
        self.to_string()
    }
    fn __repr__(&self) -> String {
        self.to_string()
    }
}

#[pyclass(module = "routrie")]
#[derive(Clone)]
struct Match {
    #[pyo3(get)]
    value: Py<PyAny>,
    #[pyo3(get)]
    params: Vec<Param>,
}

#[pymethods]
impl Match {
    fn __str__(&self) -> String {
        let params = format!(
            "[{}]",
            self.params
                .iter()
                .map(|param| format!("{}, ", param.to_string()))
                .collect::<Vec<String>>()
                .join(", ")
        );
        format!("Match({}, {})", self.value, params)
    }
    fn __repr__(&self) -> String {
        self.__str__()
    }
}

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
    fn find(&self, path: &str) -> Option<Match> {
        match self.router.find(path) {
            None => None,
            Some(found) => Some(Match {
                value: found.0.clone(),
                params: found
                    .1
                    .into_iter()
                    .map(|(name, value)| Param {
                        name: name.to_string(),
                        value: value.to_string(),
                    })
                    .collect(),
            }),
        }
    }
}

#[pymodule]
fn _routrie(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Param>()?;
    m.add_class::<Match>()?;
    m.add_class::<Router>()?;
    Ok(())
}

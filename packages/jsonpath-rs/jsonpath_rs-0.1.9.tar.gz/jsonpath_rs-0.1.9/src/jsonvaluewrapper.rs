use std::collections::HashMap;
use std::fmt::{Display, Formatter, Result};

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

use serde_json::json;
use serde_json::{to_string, Value};

#[pyclass]
pub struct JsonValueWrapper{
    pub value: Value,
}

impl Display for JsonValueWrapper {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", to_string(&self.value).unwrap())
    }
}

#[pymethods]
impl JsonValueWrapper {
    #[new]
    pub fn new(v: String) -> Self {
        Self{value: serde_json::from_str(&v).unwrap()}
    }

    fn __str__(self_: PyRef<'_, Self>) -> String {
        return self_.value.to_string();
    }

    fn __repr__(self_: PyRef<'_, Self>) -> String {
        return self_.value.to_string();
    }

    fn __len__(self_: PyRef<'_, Self>) -> usize {
        if self_.value.is_array() {
            let empty: Vec<Value> = vec![];
            return self_.value.as_array().unwrap_or(&empty).len();
        } else if self_.value.is_string() {
            let empty = String::new();
            return self_.value.as_str().unwrap_or(empty.as_str()).len();
        } else if self_.value.is_object() {
            let empty_json = json!("{}");
            let empty = empty_json.as_object().unwrap();
            return self_.value.as_object().unwrap_or(empty).len();
        }
        return 0;
    }

    /// Checks if the JSON value is an array.
    fn is_array(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_array();
    }

    /// Converts the JSON value to a vector of JsonValueWrapper if it's an array.
    fn as_array(self_: PyRef<'_, Self>) -> Option<Vec<Self>> {
        return self_.value.as_array().map(|item| item.iter().map(|inner_item| Self{value: inner_item.clone()}).collect::<Vec<Self>>());
    }

    /// Checks if the JSON value is a boolean or can be interpreted as one.
    fn is_boolean(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_boolean() || 
            (self_.value.is_string() && matches!(self_.value.as_str().unwrap().to_lowercase().as_str(), "true" | "false")) ||
            self_.value.is_number();
    }

    /// Converts the JSON value to a boolean.
    /// Handles true/false strings and non-zero numbers as true.
    fn as_boolean(&self) -> PyResult<bool> {
        if self.value.is_boolean() {
            Ok(self.value.as_bool().unwrap())
        } else if self.value.is_string() {
            let s = self.value.as_str().unwrap().to_lowercase();
            match s.as_str() {
                "true" => Ok(true),
                "false" => Ok(false),
                _ => s.parse::<i64>()
                    .map(|n| n != 0)
                    .map_err(|_| PyValueError::new_err(format!("Cannot parse string '{}' as boolean", s)))
            }
        } else if self.value.is_number() {
            Ok(self.value.as_i64().unwrap_or(self.value.as_u64().unwrap() as i64) != 0)
        } else {
            Err(PyValueError::new_err(format!("Cannot parse value '{}' as boolean", self.value)))
        }
    }

    /// Checks if the JSON value is a float or can be parsed as one.
    fn is_f64(&self) -> bool {
        self.value.is_f64() || 
        (self.value.is_string() && self.value.as_str().unwrap().parse::<f64>().is_ok())
    }

    /// Converts the JSON value to a float.
    fn as_f64(&self) -> PyResult<f64> {
        if self.value.is_number() {
            Ok(self.value.as_f64().unwrap())
        } else if self.value.is_string() {
            let s = self.value.as_str().unwrap();
            s.parse::<f64>()
                .map_err(|_| PyValueError::new_err(format!("Cannot parse string '{}' as f64", s)))
        } else {
            Err(PyValueError::new_err(format!("Value '{}' is not a number or parseable string", self.value)))
        }
    }

    /// Checks if the JSON value is a number or can be parsed as one.
    fn is_number(&self) -> bool {
        self.value.is_number() || 
        (self.value.is_string() && self.value.as_str().unwrap().parse::<f64>().is_ok())
    }

    /// Converts the JSON value to a number (alias for as_f64).
    fn as_number(&self) -> PyResult<f64> {
        self.as_f64()  // Reuse the as_f64 implementation
    }

    /// Checks if the JSON value is an integer or can be parsed as one.
    fn is_i64(&self) -> bool {
        self.value.is_i64() || 
        (self.value.is_string() && self.value.as_str().unwrap().parse::<i64>().is_ok())
    }

    /// Converts the JSON value to a signed 64-bit integer.
    fn as_i64(&self) -> PyResult<i64> {
        if self.value.is_i64() {
            Ok(self.value.as_i64().unwrap())
        } else if self.value.is_string() {
            let s = self.value.as_str().unwrap();
            s.parse::<i64>()
                .map_err(|_| PyValueError::new_err(format!("Cannot parse string '{}' as i64", s)))
        } else {
            Err(PyValueError::new_err(format!("Value '{}' is not an i64 or parseable string", self.value)))
        }
    }

    /// Checks if the JSON value is an unsigned integer or can be parsed as one.
    fn is_u64(&self) -> bool {
        self.value.is_u64() || 
        (self.value.is_string() && self.value.as_str().unwrap().parse::<u64>().is_ok())
    }

    /// Converts the JSON value to an unsigned 64-bit integer.
    fn as_u64(&self) -> PyResult<u64> {
        if self.value.is_u64() {
            Ok(self.value.as_u64().unwrap())
        } else if self.value.is_string() {
            let s = self.value.as_str().unwrap();
            s.parse::<u64>()
                .map_err(|_| PyValueError::new_err(format!("Cannot parse string '{}' as u64", s)))
        } else {
            Err(PyValueError::new_err(format!("Value '{}' is not a u64 or parseable string", self.value)))
        }
    }

    /// Checks if the JSON value is null.
    fn is_null(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_null();
    }

    /// Returns None if the JSON value is null, otherwise returns Some(()).
    fn as_null(self_: PyRef<'_, Self>) -> Option<()> {
        return self_.value.as_null();
    }

    /// Checks if the JSON value is an object.
    fn is_object(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_object();
    }

    /// Converts the JSON value to a HashMap if it's an object.
    fn as_object(self_: PyRef<'_, Self>) -> HashMap<String, Self> {
        return self_.value.as_object().unwrap().iter().map(|(k, v)| (k.clone(), Self{value: v.clone()})).collect::<HashMap<String, Self>>();
    }

    /// Checks if the JSON value is a string.
    fn is_string(self_: PyRef<'_, Self>) -> bool {
        return self_.value.is_string();
    }

    /// Converts the JSON value to a string.
    fn as_string(&self) -> PyResult<String> {
        match serde_json::to_string(&self.value) {
            Ok(s) => Ok(s),
            Err(e) => Err(PyValueError::new_err(format!("Failed to convert value to JSON string: {}", e)))
        }
    }

    /// Retrieves an element from the JSON array by index.
    fn get_by_index(self_: PyRef<'_, Self>, i: usize) -> Option<Self> {
        let item = self_.value.get(i);
        if item.is_none() {
            return None;
        }
        return Some(Self{value: item.unwrap().clone()});
    }

    /// Retrieves a value from the JSON object by key.
    fn get_by_key(self_: PyRef<'_, Self>, k: String) -> Option<Self> {
        let item = self_.value.get::<String>(k);
        if item.is_none() {
            return None;
        }
        return Some(Self{value: item.unwrap().clone()});
    }
}

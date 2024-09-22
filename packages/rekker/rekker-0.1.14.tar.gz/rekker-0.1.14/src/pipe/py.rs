use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyString, PyAny};
use pyo3::exceptions::PyTypeError;
use std::time::Duration;
use humantime::parse_duration;
use crate::{Result, Error};
use regex::Regex;

fn trim_addr(addr: &str) -> String {
    let re = Regex::new(r"\s+").unwrap();
    let addr = re.replace_all(addr.trim(), ":");
    addr.to_string()
}

pub fn pipes(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Pipe>()?;
    m.add_function(wrap_pyfunction!(remote, m)?)?;
    m.add_function(wrap_pyfunction!(listener, m)?)?;
    Ok(())
}

#[pyfunction]
#[pyo3(signature = (addr, tls=None, udp=None))]
pub fn remote(addr: String, tls: Option<bool>, udp: Option<bool>) -> PyResult<Pipe> {
    let addr = trim_addr(&addr);

    match (tls, udp) {
        (None, None) => {
            Ok(Pipe::tcp(&addr)?)
        },
        (None, Some(true)) => {
            Ok(Pipe::udp(&addr)?)
        },
        (Some(true), None) => {
            Ok(Pipe::tls(&addr)?)
        },
        _ => todo!()
    }
}

#[pyfunction]
#[pyo3(signature = (addr, tls=None, udp=None))]
pub fn listener(addr: String, tls: Option<bool>, udp: Option<bool>) -> PyResult<Listener> {
    match (tls, udp) {
        (None, None) => {
            Ok(Listener::tcp(&addr)?)
        },
        /*
        (None, Some(true)) => {
            Ok(Listener::udp(&addr)?)
        },
        (Some(true), None) => {
            Ok(Listener::tls(&addr)?)
        },
    */
        _ => todo!()
    }
}
fn pyany_to_bytes<'a>(data: &'a Bound<'_, PyAny>) -> PyResult<&'a [u8]> {
    if let Ok(py_str) = data.downcast::<PyString>() {
        Ok(py_str.to_str()?.as_bytes())
    }
    else if let Ok(py_bytes) = data.downcast::<PyBytes>() {
        Ok(py_bytes.as_bytes())
    }
    else {
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>("Expected bytes or string"))
    }
}

fn py_parse_duration(duration: Option<&str>) -> PyResult<Option<Duration>> {
    match duration {
        Some(dur) => {
            match parse_duration(dur) {
                Ok(d) => Ok(Some(d)),
                Err(e) => {
                    Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                        format!("{}", e),
                    ))
                },
            }
        },
        None => Ok(None),
    }
}

macro_rules! save_recv_timeout_wrapper {
    ($self:expr, $func:expr, $timeout:expr) => {{
        let save_timeout = $self.stream.recv_timeout()?;
        $self.stream.set_recv_timeout(py_parse_duration($timeout)?)?;
        let out = match $func {
            Ok(d) => d,
            Err(e) => {
                $self.stream.set_recv_timeout(save_timeout)?;
                return Err(e.into());
            }
        };

        $self.stream.set_recv_timeout(save_timeout)?;
        out
    }}
}

macro_rules! save_send_timeout_wrapper {
    ($self:expr, $func:expr, $timeout:expr) => {{
        let save_timeout = $self.stream.send_timeout()?;
        $self.stream.set_send_timeout(py_parse_duration($timeout)?)?;
        let out = match $func {
            Ok(d) => d,
            Err(e) => {
                $self.stream.set_send_timeout(save_timeout)?;
                return Err(e.into());
            }
        };

        $self.stream.set_send_timeout(save_timeout)?;
        out
    }}
}


#[pyclass]
pub struct Listener {
    stream: crate::Listener
}

impl Listener {
    fn tcp(addr: &str) -> Result<Listener> {
        Ok(Listener { stream: crate::Listener::tcp(addr)? })
    }
}

#[pymethods]
impl Listener {
    fn accept(&mut self) -> Result<(Pipe, String)> {
        let (pipe, s) = self.stream.accept()?;
        Ok((Pipe { stream: pipe }, s))
    }
}

#[pyclass]
pub struct Pipe {
    pub(crate) stream: crate::Pipe
}
impl Pipe {
    fn tcp(addr: &str) -> Result<Pipe> {
        Ok(Pipe { stream: crate::Pipe::tcp(addr)? })
    }
    fn udp(addr: &str) -> Result<Pipe> {
        Ok(Pipe { stream: crate::Pipe::udp(addr)? })
    }
    fn tls(addr: &str) -> Result<Pipe> {
        Ok(Pipe { stream: crate::Pipe::tls(addr)? })
    }
}

#[pymethods]
impl Pipe {
    fn set_nagle(&mut self, value: bool) -> PyResult<()> {
        Ok(self.stream.set_nagle(value)?)
    }
    pub fn nagle(&mut self) -> Result<bool> {
        Ok(self.stream.nagle()?)
    }

    fn log(&mut self, value: bool) -> () {
        self.stream.log(value);
    }
    fn is_logging(&mut self) -> () {
        self.stream.is_logging();
    }

    #[pyo3(signature = (size, timeout=None))]
    fn recv(&mut self, py: Python, size: usize, timeout: Option<&str>) -> PyResult<Py<PyBytes>> {
        let out = save_recv_timeout_wrapper!(self, self.stream.recv(size), timeout);

        Ok(PyBytes::new_bound(py, &out).into())
    }
    #[pyo3(signature = (size, timeout=None))]
    fn recvn(&mut self, py: Python, size: usize, timeout: Option<&str>) -> PyResult<Py<PyBytes>> {
        let out = save_recv_timeout_wrapper!(self, self.stream.recvn(size), timeout);

        Ok(PyBytes::new_bound(py, &out).into())
    }
    #[pyo3(signature = (drop=None, timeout=None))]
    fn recvline(&mut self, py: Python, drop: Option<bool>, timeout: Option<&str>) -> PyResult<Py<PyBytes>> {
        let mut out = save_recv_timeout_wrapper!(self, self.stream.recvline(), timeout);
        
        match drop {
            Some(true) => {
                out = out[..out.len()-1].to_vec(); 
                },
            _ => {}
        }
        Ok(PyBytes::new_bound(py, &out).into())
    }
    #[pyo3(signature = (suffix, drop=None, timeout=None))]
    fn recvuntil(&mut self, py: Python, suffix: Bound<'_, PyAny>, drop: Option<bool>, timeout: Option<&str>) -> PyResult<Py<PyBytes>> {
        let suffix = pyany_to_bytes(&suffix)?;

        let mut out = save_recv_timeout_wrapper!(self, self.stream.recvuntil(suffix), timeout);

        match drop {
            Some(true) => {
                out = out[..out.len()-1].to_vec(); 
                },
            _ => {}
        }

        Ok(PyBytes::new_bound(py, &out).into())
    }
    #[pyo3(signature = (timeout=None))]
    fn recvall(&mut self, py: Python, timeout: Option<&str>) -> PyResult<Py<PyBytes>> {
        let out = save_recv_timeout_wrapper!(self, self.stream.recvall(), timeout);

        Ok(PyBytes::new_bound(py, &out).into())
    }
    #[pyo3(signature = (data, timeout=None))]
    fn send(&mut self, _py: Python, data: Bound<'_, PyAny>, timeout: Option<&str>) -> PyResult<()> {
        let data = pyany_to_bytes(&data)?;
        let out = save_send_timeout_wrapper!(self, self.stream.send(data), timeout);
        Ok(out)
    }
    #[pyo3(signature = (data, timeout=None))]
    fn sendline(&mut self, _py: Python, data: Bound<'_, PyAny>, timeout: Option<&str>) -> PyResult<()> {
        let data = pyany_to_bytes(&data)?;
        let out = save_send_timeout_wrapper!(self, self.stream.sendline(data), timeout);
        Ok(out)
    }
    #[pyo3(signature = (data, suffix, timeout=None))]
    fn sendlineafter(&mut self, py: Python, data: Bound<'_, PyAny>, suffix: Bound<'_, PyAny>, timeout: Option<&str>) -> PyResult<Py<PyBytes>> {
        let data = pyany_to_bytes(&data)?;
        let suffix = pyany_to_bytes(&suffix)?;
        let out = save_send_timeout_wrapper!(self, self.stream.sendlineafter(data, suffix), timeout);
        Ok(PyBytes::new_bound(py, &out).into())
    }

    fn recv_timeout(&self, _py: Python) -> PyResult<Option<String>> {
        match self.stream.recv_timeout()? {
            Some(duration) => Ok(Some(format!("{:?}", duration))),
            None => Ok(None)
        }
    }
    #[pyo3(signature = (duration))]
    fn set_recv_timeout(&mut self, _py: Python, duration: Option<&str>) -> PyResult<()> {
        Ok(self.stream.set_recv_timeout(py_parse_duration(duration)?)?)
    }

    fn send_timeout(&self, _py: Python) -> PyResult<Option<String>> {
        match self.stream.send_timeout()? {
            Some(duration) => Ok(Some(format!("{:?}", duration))),
            None => Ok(None)
        }
    }
    #[pyo3(signature = (duration))]
    fn set_send_timeout(&mut self, _py: Python, duration: Option<&str>) -> PyResult<()> {
        Ok(self.stream.set_send_timeout(py_parse_duration(duration)?)?)
    }

    fn debug(&mut self, _py: Python) -> PyResult<()> {
        Ok(self.stream.debug()?)
    }
    fn interactive(&mut self, _py: Python) -> PyResult<()> {
        Ok(self.stream.interactive()?)
    }

    fn close(&mut self, _py: Python) -> PyResult<()> {
        Ok(self.stream.close()?)
    }

}


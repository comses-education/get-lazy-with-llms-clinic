# NumPy 2.0 Compatibility Issue in Your Docker Application

The error you're experiencing is due to a binary incompatibility between NumPy 2.0 and the landlab package. This is a known issue that started occurring after NumPy 2.0 was released on June 16, 2024[2].

## The Problem

The error message indicates a mismatch in binary compatibility:

```
ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject
```

This happens because the landlab package (or one of its dependencies) was compiled against an older version of NumPy with a different memory layout than what's present in NumPy 2.0[3]. The package expects the NumPy data type to be 96 bytes, but the installed version (NumPy 2.0) provides 88 bytes[5].

## Solution

The most straightforward fix is to downgrade NumPy to a version below 2.0. You can do this by modifying your `pyproject.toml` file:

```toml
[project]
name = "landlab-overland-flow-demo"
version = "0.1.0"
description = "A simple Landlab overland flow simulation."
dependencies = [
    "landlab",
    "numpy=3.9"
```

Alternatively, you can modify your Dockerfile to explicitly install an older version of NumPy before installing other dependencies:

```dockerfile
# After setting up the environment but before installing dependencies
RUN pip install --no-cache-dir "numpy<2.0.0"

# Then install the rest of your dependencies
RUN pip install --no-cache-dir -e .
```

## Why This Works

Many Python packages that depend on NumPy (like landlab) were compiled against older versions and haven't yet been updated to be compatible with NumPy 2.0[4]. By downgrading to a version below 2.0 (such as 1.26.x), you'll ensure binary compatibility with these packages[6].

After making these changes, rebuild your Docker image with `make build` and try running it again with `make run`.
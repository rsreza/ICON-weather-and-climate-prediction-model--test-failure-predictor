# ICON Unit Test Failure Predictor

An AI-assisted diagnostic tool that predicts the probability of
`PASS` / `FAIL` for ICON unit tests based on configuration metadata
alone.

This project propose a solution for ICON developers (test result interpretation).

> **⚠️ Important note on data:** This repository demonstrates the
> approach on **synthetic data**. The synthetic data is designed to
> mimic the real `make check-icon` output format, and the parser works
> with real ICON logs **without any code changes**. Swapping in real
> logs is a one-file replacement.

---

## Table of Contents

- [Motivation](#motivation)
- [What This Tool Does](#what-this-tool-does)
- [Why Synthetic Data](#why-synthetic-data)
- [Results](#results)
- [Method](#method)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Limitations](#limitations)
- [Context and Background](#context-and-background)
- [Author](#author)
- [License](#license)

---

## Motivation

ICON's unit testing framework (`make check-icon`) reports
`PASS` / `SKIP` / `FAIL` for each test. With hundreds of tests running
across multiple compilers, MPI settings, process counts, and build
types, developers face a wall of output when a CI run fails.

This project asks a simple question:

> **Can we predict which tests are likely to fail, based only on their
> configuration metadata (test name, compiler, MPI, process count,
> build type) — before they even run?**

If yes, developers can prioritize their debugging, and CI systems can
highlight high-risk tests automatically.

---

## What This Tool Does

Given a configuration like:

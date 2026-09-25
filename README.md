# ICON Unit Test Failure Predictor

An AI-assisted diagnostic tool that predicts the probability of
`PASS` / `FAIL` for ICON unit tests based on configuration metadata
alone.

This project responds directly to the kind of need DKRZ has signaled
for **AI-supported tools for ICON developers** — specifically for
**test result interpretation** and CI feedback.

---

## Table of Contents

- [Motivation](#motivation)
- [What This Tool Does](#what-this-tool-does)
- [Results](#results)
- [Method](#method)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Source](#data-source)
- [Limitations](#limitations)
- [Context and Background](#context-and-background)
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

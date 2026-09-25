"""
generate_data.py
Generates a synthetic ICON unit test dataset with strong signal.
"""

import random
import pandas as pd
import numpy as np

np.random.seed(42)
random.seed(42)

TEST_VARIANTS = {
    "test_sync_sums": "mpi",
    "test_start_mpi": "mpi",
    "test_slice_array": "plain",
    "test_kind": "plain",
    "test_insert_dimension": "plain",
    "test_index_list": "plain",
    "test_divide_cell": "mpi",
    "test_add_var_fail2": "plain",
    "test_add_var_fail1": "plain",
    "test_add_var": "plain",
}

compilers = ["gcc-13.3.0", "gcc-11.2.0", "intel-2021.5.0"]
mpi_options = [True, False]
process_counts = [1, 4, 8]
build_types = ["debug", "release"]

rows = []
for test, variant in TEST_VARIANTS.items():
    for compiler in compilers:
        for mpi in mpi_options:
            for nproc in process_counts:
                for build in build_types:
                    if variant == "mpi" and not mpi:
                        result = "SKIP"
                    elif variant == "nompi" and mpi:
                        result = "SKIP"
                    elif variant == "mpi" and mpi:
                        if compiler == "gcc-13.3.0" and nproc >= 8:
                            result = "FAIL"
                        elif compiler == "gcc-11.2.0" and nproc >= 8:
                            result = random.choices(["PASS", "FAIL"], weights=[0.2, 0.8])[0]
                        elif build == "debug":
                            result = random.choices(["PASS", "FAIL"], weights=[0.6, 0.4])[0]
                        else:
                            result = random.choices(["PASS", "FAIL"], weights=[0.98, 0.02])[0]
                    else:
                        if build == "debug":
                            result = random.choices(["PASS", "FAIL"], weights=[0.9, 0.1])[0]
                        else:
                            result = "PASS"

                    rows.append({
                        "test_name": test,
                        "variant": variant,
                        "compiler": compiler,
                        "mpi_enabled": mpi,
                        "nproc": nproc,
                        "build_type": build,
                        "result": result,
                    })

df = pd.DataFrame(rows)
df.to_csv("data/icon_test_data.csv", index=False)

print(f"Generated {len(df)} records")
print("\nResult distribution:")
print(df["result"].value_counts())

mpi_df = df[(df["variant"] == "mpi") & (df["mpi_enabled"]) & (df["result"] == "FAIL")]
print("\nMPI failures by compiler and nproc:")
print(mpi_df.groupby(["compiler", "nproc"]).size())

gcc13_8 = df[(df["compiler"] == "gcc-13.3.0") & (df["nproc"] == 8) & (df["variant"] == "mpi") & (df["result"] == "FAIL")]
print(f"\nSanity: gcc-13.3.0 + nproc=8 + mpi + FAIL = {len(gcc13_8)} (expect 4)")
print(f"Total FAIL: {len(df[df['result']=='FAIL'])}")

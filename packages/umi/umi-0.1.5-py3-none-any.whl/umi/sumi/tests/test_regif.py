#!/usr/bin/env python3

# Copyright (C) 2023 Zero ASIC
# This code is licensed under Apache License 2.0 (see LICENSE for details)

import pytest
import numpy as np
from switchboard import UmiTxRx


def test_regif(sumi_dut, apply_atomic, random_seed, sb_umi_valid_mode, sb_umi_ready_mode):

    n = 100  # Number of reads, atomic txns and writes each from the register file

    np.random.seed(random_seed)

    # launch the simulation
    sumi_dut.simulate(
            plusargs=[('valid_mode', sb_umi_valid_mode),
                      ('ready_mode', sb_umi_ready_mode)])

    # instantiate TX and RX queues.  note that these can be instantiated without
    # specifying a URI, in which case the URI can be specified later via the
    # "init" method

    host = UmiTxRx("host2dut_0.q", "dut2host_0.q", fresh=True)

    print("### Starting test ###")

    # regif accesses are all 32b wide and aligned
    for _ in range(n):
        addr = np.random.randint(0, 512) * 4
        # length should not cross the DW boundary - umi_mem_agent limitation
        data = np.random.randint(2**32, dtype=np.uint32)

        print(f"umi writing 0x{data:08x} to addr 0x{addr:08x}")
        host.write(addr, data)
        atomicopcode = np.random.randint(0, 9)
        atomicdata = np.random.randint(2**32, dtype=np.uint32)
        print(f"umi atomic opcode: {atomicopcode} data: {atomicdata:08x} to addr 0x{addr:08x}")
        atomicval = host.atomic(addr, atomicdata, atomicopcode)
        if not (atomicval == data):
            print(f"ERROR umi atomic from addr 0x{addr:08x} expected {data} actual {atomicval}")
            assert (atomicval == data)
        data = np.array(apply_atomic(data, atomicdata, atomicopcode, 2**32)).astype(np.uint32)

        print(f"umi read from addr 0x{addr:08x}")
        val = host.read(addr, np.uint32)
        if not (val == data):
            print(f"ERROR umi read from addr 0x{addr:08x} expected {data} actual {val}")
            assert (val == data)


if __name__ == '__main__':
    pytest.main(['-s', '-q', __file__])

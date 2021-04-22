# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class ContainerTest(rfm.RunOnlyRegressionTest):
    platform = parameter(['Sarus', 'Singularity'])
    valid_systems = ['daint:gpu']
    valid_prog_environs = ['builtin']

    @rfm.run_after('init')
    def set_container_variables(self):
        self.descr = f'Run commands inside a container using {self.platform}'
        image_prefix = 'docker://' if self.platform == 'Singularity' else ''
        self.container_platform = self.platform
        self.container_platform.image = f'{image_prefix}ubuntu:18.04'
        self.container_platform.command = (
            "bash -c 'cat /etc/os-release | tee /rfm_workdir/release.txt'"
        )

    @rfm.run_before('sanity')
    def set_sanity_patterns(self):
        os_release_pattern = r'18.04.\d+ LTS \(Bionic Beaver\)'
        self.sanity_patterns = sn.all([
            sn.assert_found(os_release_pattern, 'release.txt'),
            sn.assert_found(os_release_pattern, self.stdout)
        ])

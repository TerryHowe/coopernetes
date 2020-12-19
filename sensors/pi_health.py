#!/usr/bin/env python3

import os
import sys
import socket

import psutil
from healthcheck import HealthCheck, EnvironmentDump


class PiHealth(object):
    health = HealthCheck()
    environment = EnvironmentDump()

    def __init__(self):
        self.environment.add_section("application", self._get_environment_data)
        self.health.add_check(self._get_healthcheck_data)
        self.hostname = socket.gethostname()

    @staticmethod
    def _get_application_data():
        application = os.path.basename(sys.argv[0])
        version = "unknown"
        if len(sys.argv) > 1:
            version = sys.argv[1]
        return application, version

    @staticmethod
    def _get_healthcheck_data():
        application, version = PiHealth._get_application_data()

        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory()[2]
        disk_usage = {}
        for disk_partition in psutil.disk_partitions():
            disk = disk_partition[1]
            disk_usage[disk] = psutil.disk_usage(disk)[3]
        return True, {
            "application": application,
            "version": version,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
        }

    @staticmethod
    def _get_environment_data():
        application, version = PiHealth._get_application_data()
        return {
            "application": application,
            "version": version,
        }




pi_health = PiHealth()


def get_environment():
    return pi_health.environment.run()


def get_healthcheck():
    return pi_health.health.run()


def get_hostname():
    return pi_health.hostname

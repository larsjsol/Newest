#!/usr/bin/env python

from datetime import datetime, timezone
from zmq.utils.jsonapi import dumps, loads
from dateutil.parser import parser

class State:
    """
    The current known state of software versions.
    """

    protocol_version = (0, 1)

    def __init__(self):
        self.software_versions = {}

    def serialize(self):
        """
        Return a representation that is suitable for
        transmitting over the network.
        """
        _dict = {}
        _dict['protocol_version'] = State.protocol_version
        _dict['software_versions'] = [v.to_dict() for v in self.software_versions.values()]
        return dumps(_dict)

    @staticmethod
    def deserialize(json):
        """
        Deserialize a json into a State object.
        """
        state = State()
        _dict = loads(json)
        if tuple(_dict['protocol_version']) > State.protocol_version:
            raise Exception('Protocol version {} not supported'.format(_dict['protocol_version']))
        for ver in _dict['software_versions']:
            state.update(ver['name'], ver['version'], parser().parse(ver['last_updated']))

        return state

    def update(self, software_name, version_id, last_updated=None):
        """
        Update the state with a new software version.
        """
        self.software_versions[software_name] = SoftwareVersion(software_name, version_id, last_updated)

    def __str__(self):
        return '\n'.join([str(k) for k in self.software_versions.values()])

class SoftwareVersion:
    """
    The latest version for a single pice of a software packge.

    name (string): name of the software.
    version (string): a string (often a version number or a hash) identifying this version.
    last_update (datetime): last time this entry was updated
    """
    def __init__(self, name, version_id, last_updated=None):
        self.name = name
        self.version = version_id
        if last_updated:
            self.last_updated = last_updated
        else:
            self.last_updated = datetime.now(timezone.utc)

    def __str__(self):
        return "{} {} last updated: {}".format(self.name, self.version, self.last_updated.isoformat())

    def to_dict(self):
        """
        Return this object as a dict. Helper function for serialization
        """
        return {'name': self.name, 'version': self.version, 'last_updated': self.last_updated.isoformat()}

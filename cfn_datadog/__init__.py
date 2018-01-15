from troposphere.validators import boolean, positive_integer
from troposphere import cloudformation, depends_on_helper
from troposphere.cloudformation import AWSHelperFn, AWSObject
import types, sys
try:
    unicode = unicode
except NameError:
    str = str
    basestring = (str, bytes)
    unicode = str
    bytes = str


class DatadogBase(AWSObject):
    """
    Removed condition to not validate if based on custom:
    if type_name == 'AWS::CloudFormation::CustomResource' or \
                type_name.startswith('Custom::'):
    """

    def __setattr__(self, name, value):
        if name in self.__dict__.keys() \
                or '_BaseAWSObject__initialized' not in self.__dict__:
            return dict.__setattr__(self, name, value)
        elif name in self.attributes:
            if name == "DependsOn":
                self.resource[name] = depends_on_helper(value)
            else:
                self.resource[name] = value
            return None
        elif name in self.propnames:
            # Check the type of the object and compare against what we were
            # expecting.
            expected_type = self.props[name][0]

            # If the value is a AWSHelperFn we can't do much validation
            # we'll have to leave that to Amazon.  Maybe there's another way
            # to deal with this that we'll come up with eventually
            if isinstance(value, AWSHelperFn):
                return self.properties.__setitem__(name, value)

            # If it's a function, call it...
            elif isinstance(expected_type, types.FunctionType):
                try:
                    value = expected_type(value)
                except Exception:
                    sys.stderr.write(
                        "%s: %s.%s function validator '%s' threw "
                        "exception:\n" % (self.__class__,
                                          self.title,
                                          name,
                                          expected_type.__name__))
                    raise
                return self.properties.__setitem__(name, value)

            # If it's a list of types, check against those types...
            elif isinstance(expected_type, list):
                # If we're expecting a list, then make sure it is a list
                if not isinstance(value, list):
                    self._raise_type(name, value, expected_type)

                # Iterate over the list and make sure it matches our
                # type checks (as above accept AWSHelperFn because
                # we can't do the validation ourselves)
                for v in value:
                    if not isinstance(v, tuple(expected_type)) \
                            and not isinstance(v, AWSHelperFn):
                        self._raise_type(name, v, expected_type)
                # Validated so assign it
                return self.properties.__setitem__(name, value)

            # Final validity check, compare the type of value against
            # expected_type which should now be either a single type or
            # a tuple of types.
            elif isinstance(value, expected_type):
                return self.properties.__setitem__(name, value)
            else:
                self._raise_type(name, value, expected_type)

        type_name = getattr(self, 'resource_type', self.__class__.__name__)

        raise AttributeError("%s object does not support attribute %s" %
                             (type_name, name))


shared_options = {
    'silenced': (dict, False),
    'notify_no_data': (boolean, False),  # is this really a bool?
    'new_host_delay': (positive_integer, False),
    'no_data_timeframe': (positive_integer, False),
    'timeout_h': (positive_integer, False),
    'require_full_window': (boolean, False),
    'renotify_interval': (positive_integer, False),
    'escalation_message': (basestring, False),
    'notify_audit': (boolean, False),
    'locked': (boolean, False),
    'include_tags': (boolean, False),
}
from .metric_alert import MetricAlert, MetricAlertOptions, Thresholds
from .service_check import ServiceCheck, ServiceCheckOptions
from .composite import CompositeOptions, Composite
from .event_alert import EventAlertOptions, EventAlert

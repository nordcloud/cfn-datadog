try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import re
REQUIREMENTS=[]
DEP_LINKS=[]
for i in open("requirements.txt").readlines():
    if re.match('.*://.*',i):
        DEP_LINKS.append(i.strip() + "-0")
        REQUIREMENTS.append((i.split("=")[1].strip()))
    else:
        REQUIREMENTS.append(i.strip())
setup(
    name="cfn-datadog",
    version="0.0.10",
    description="Lambda cloudformation custom resource that sets up datadog alerts",
    long_description=open("README.md").read(),
    author="Martin Kaberg",
    author_email="martin.kaberg@nordcloud.com",
    url="https://github.com/nordcloud/cfn-datadog",
    install_requires=REQUIREMENTS,
    dependency_links=DEP_LINKS,
    license="Apache Common 2.0",
    zip_safe=False,

)

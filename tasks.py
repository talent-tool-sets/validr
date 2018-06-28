import os
from invoke import task


@task
def test(ctx):
    os.environ['VALIDR_DEBUG'] = '1'
    os.environ['VALIDR_USE_CYTHON'] = '1'
    ctx.run('python setup.py build')
    ctx.run('pytest --cov=validr --cov-report=term-missing')
    ctx.run('python benchmark/benchmark.py benchmark --validr')


@task
def clean(ctx):
    ctx.run('rm -rf build/*')
    ctx.run('rm -rf dist/*')
    ctx.run('find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')


@task(pre=[clean])
def build(ctx):
    os.environ['VALIDR_USE_CYTHON'] = '1'
    ctx.run('python setup.py build')
    ctx.run('python setup.py sdist')


@task(pre=[build])
def publish(ctx):
    ctx.run('twine upload dist/*')
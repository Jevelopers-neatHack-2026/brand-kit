git clone https://github.com/Jevelopers-neatHack-2026/brand-kit.git
cd brand-kit
python3.12 -m venv .venv-assets
.venv-assets/bin/python -m pip install --only-binary=:all: --require-hashes -r tools/assets/requirements.txt
make check PYTHON=.venv-assets/bin/python

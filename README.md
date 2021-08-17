# python-tfgen

Convert your YAML to Terraform HCL

```bash
usage: tfgen.py [-h] -f YAML -o OUTPUT

Convert your YAML to Terraform HCL.

optional arguments:
  -h, --help  show this help message and exit
  -f YAML     yaml file
  -o OUTPUT   Output directory
```

## Docs

- [kind: vm](docs/vm.yaml)
- [kind: network](docs/network.yaml)
- [kind: pool](docs/pool.yaml)
- [kind: image](docs/image.yaml)

## Guide

1. Copy example/sample.yaml 
```bash
cp example/sample.yaml myfile.yaml
```

2. Edit your file
```bash
editor myfile.yaml
```

3. Generate terraform HCL
```bash
./python-tfgen.py -f myfile.yaml -o resultdir
```

4. Initialize directory
```bash
cd resultdir/
terraform init
```

5. Provision libvirt resources
```bash
terraform apply -auto-approve
```

6. Deleting libvirt resources
```bash
terraform destro -auto-approve
```

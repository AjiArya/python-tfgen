#!/usr/bin/env python3

import yaml
import sys
import os
import argparse
from jinja2 import Environment, FileSystemLoader, Template

parser = argparse.ArgumentParser(description='Convert your YAML to Terraform HCL.')
parser.add_argument("-f", dest="yaml", type=str, help="yaml file", required=True)
parser.add_argument("-o", dest="output", type=str, help="Output directory", required=True)
args = parser.parse_args()

values = yaml.load(open(args.yaml), Loader=yaml.FullLoader)

# Load templates file from templates folder
env = Environment(loader = FileSystemLoader(sys.path[0] + '/templates'), trim_blocks=True, lstrip_blocks=True)

def vm():
  main_template = env.get_template('main.tf.j2')

  file=open(args.output + "/main.tf", "w")
  file.write(main_template.render(values)+"\n")
  file.close()

  x=1
  for vm in values["spec"]:
    if vm["os"] in {"ubuntu"}:
      user_template = env.get_template('ubuntu_cloudinit.yaml.j2')
      file=open(args.output + "/user" + str(x) + "_data.cfg", "w")
      file.write(user_template.render(vm)+"\n")
      file.close()

      network_template = env.get_template('ubuntu_network_config.yaml.j2')
      file=open(args.output + "/network" + str(x) + "_config.cfg", "w")
      file.write(network_template.render(vm)+"\n")
      file.close()

      x+=1

    if vm["os"] in {"centos", "rhel", "redhat"}:
      user_template = env.get_template('rhel_cloudinit.yaml.j2')
      file=open(args.output + "/user" + str(x) + "_data.cfg", "w")
      file.write(user_template.render(vm)+"\n")
      file.close()

      network_template = env.get_template('rhel_network_config.yaml.j2')
      file=open(args.output + "/network" + str(x) + "_config.cfg", "w")
      file.write(network_template.render(vm)+"\n")
      file.close()

      # Remove last blank space
      with open(args.output + "/network" + str(x) + "_config.cfg", 'r') as f:
        data = f.read()
        with open(args.output + "/network" + str(x) + "_config.cfg", 'w') as w:
            w.write(data[:-1])
      # endof

      x+=1

def network():
  main_template = env.get_template('networks.tf.j2')

  file=open(args.output + "/main.tf", "w")
  file.write(main_template.render(values)+"\n")
  file.close()

def image():
  main_template = env.get_template('images.tf.j2')

  file=open(args.output + "/main.tf", "w")
  file.write(main_template.render(values)+"\n")
  file.close()

def pool():
  main_template = env.get_template('pool.tf.j2')

  file=open(args.output + "/main.tf", "w")
  file.write(main_template.render(values)+"\n")
  file.close()

try:
    if values["kind"] == "vm":
      os.makedirs(args.output)
      vm()
    elif values["kind"] == "image":
      os.makedirs(args.output)
      image()
    elif values["kind"] == "network":
      os.makedirs(args.output)
      network()
    elif values["kind"] == "pool":
      os.makedirs(args.output)
      pool()

except FileExistsError:
    print("File already exist!")
    overwrite = input("Overwrite? (y/n) ")
    if overwrite.lower() == "y":
      if values["kind"] == "vm":
        vm()
      elif values["kind"] == "image":
        image()
      elif values["kind"] == "network":
        network()
      elif values["kind"] == "pool":
        pool()
    else:
      print("Bye!")
      sys.exit(1)

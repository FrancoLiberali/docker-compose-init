#!/usr/bin/env python3

import os
import time
import logging
import yaml
from common.server import Server

CONFIG_FILE_PATH = '/etc/server/config.yml'

def parse_config_params():
	""" Parse env variables to find program config params

	Function that search and parse program configuration parameters in the
	program environment variables. If at least one of the config parameters
	is not found a KeyError exception is thrown. If a parameter could not
	be parsed, a ValueError is thrown. If parsing succeeded, the function
	returns a map with the env variables
	"""
	config_params = {}
	config_from_file = {}
	try:
		with open(CONFIG_FILE_PATH) as config_file:
			# The FullLoader parameter handles the conversion from YAML
			# scalar values to Python the dictionary format
			config_from_file = yaml.full_load(config_file) or {}
	except FileNotFoundError:
		logging.info("Config file not found, using only env vars")

	config_params["port"] = get_config_param("SERVER_PORT", config_from_file)
	config_params["listen_backlog"] = get_config_param("SERVER_LISTEN_BACKLOG", config_from_file)

	with open('/etc/server/config_used.yml', "w+") as config_used_file:
		yaml.dump(config_from_file, config_used_file)

	return config_params

def get_config_param(key, config_from_file):
	try:
		return get_int(os.environ[key])
	except KeyError:
		try:
			return get_int(config_from_file[key])
		except KeyError as e:
			raise KeyError("Key was not found neither in EnvVars nor config file. Error: {} .Aborting server".format(e))

def get_int(value):
	try:
		return int(value)
	except ValueError as e:
		raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

def main():
	initialize_log()
	config_params = parse_config_params()

	# Initialize server and start server loop
	server = Server(config_params["port"], config_params["listen_backlog"])
	server.run()

def initialize_log():
	"""
	Python custom logging initialization

	Current timestamp is added to be able to identify in docker
	compose logs the date when the log has arrived
	"""
	logging.basicConfig(
		format='%(asctime)s %(levelname)-8s %(message)s',
		level=logging.INFO,
		datefmt='%Y-%m-%d %H:%M:%S',
	)


if __name__== "__main__":
	main()

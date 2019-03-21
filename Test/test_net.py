from classifier import Classifier
from phemeParser import parsePheme
import time
import pickle

# Sanity check test for when I inevitably break the other ones
# def test_num():
# 	assert 9==8

def test_class_timing():
	print("classification timing")
	start_time = time.time()
	c = Classifier(2).run()
	end_time = time.time()
	run_time = end_time - start_time

	assert run_time < 600

def test_parser_timing():
	print("parser timing")
	start_time = time.time()
	parsePheme()
	end_time = time.time()
	run_time = end_time - start_time

	assert run_time < 600

def test_input_validity():
	print('verifying classifier input')
	input = parsePheme()
	with open('input_test.pkl', 'rb') as obj:
		validated_input = pickle.load(obj)

		assert input == validated_input

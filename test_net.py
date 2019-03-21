from classifier import Classifier
from phemeParser import parsePheme
import time

# Sanity check test for when I inevitably break the other ones
# def test_num():
# 	assert 9==8

def test_class_timing():
	print("parser timing")
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
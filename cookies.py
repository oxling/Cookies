import os
import recipe_parser as rp
from random import choice
import string
from fractions import Fraction
import recipe
import ingredient


def words_with_token(line, token):
	words = []
	for (w, t) in line:
		if t == token:
			words.append(w)
	return words

#TODO: Move this into recipe_parser.py so it's returned by tag_file()
def output_results(filepath):
	results = rp.tag_file(filepath)
	if results is None:
		return []

	recipe = Recipe()

	for line in results:
		food = words_with_token(line, rp.Food)
		quantity = words_with_token(line, rp.Quantity)
		unit = words_with_token(line, rp.Unit)
		modifier = words_with_token(line, rp.Modifier)
		time = words_with_token(line, rp.Time)
		degrees = words_with_token(line, rp.Degrees)
		
		if len(unit) > 0 and len(time) == 0 and len(degrees) == 0:
			ingredient = Ingredient()
			ingredient.food = ' '.join(food)
			ingredient.unit = Unit.parse(unit)
			ingredient.quantity = sum(map(parse_number(quantity)))
			ingredient.modifier = ' '.join(modifier) 
		elif len(time) > 0:
			recipe.baking_time = parse_number(time)
		elif len(degrees) > 0:
			recipe.degrees = parse_number(degrees)
	return parsed_results
	
valid_digits = set(string.digits).union(set('/'))
def clean_number(string):
	return ''.join(ch for ch in string if ch in valid_digits)

def parse_number(string):
	string = clean_number(string)
	if len(string) == 0:
		return 0

	return float(Fraction(string))

# Takes ingredient line dict as argument
def print_ingredient_line(line):
	#print line

	quantities = map(parse_number, line.get(rp.Quantity, []))
	units = line.get(rp.Unit, [])
	modifier = ' '.join(line.get(rp.Modifier, []))
	food = ' '.join(line.get(rp.Food, modifier)) # If food is missing, try the modifier.

	if len(units) == 1:
		quantity = sum(quantities)
		unit = units[0]
		print("%.2f %s %s %s" % (quantity, unit, modifier, food))
	elif len(units) == len(quantities):
		unit_line = []
		for unit, quantity in range(len(quantities)):
			unit_line += ["%.2f %s" % (unit, quantity)]

		print("%s %s %s" % (' or '.join(unit_line), modifier, food))

	## TODO: What happens when there is more than one unit?
	## and what if units != quantities?
	



def print_degree_line(line):
	print "degrees"

def print_time_line(line):
	print "time"

tag_folder = "tagged_recipes"
tag_files = os.listdir(tag_folder)

for filename in tag_files:
	rp.learn_from_file(tag_folder + "/" + filename)

plain_folder = "test_recipes"
plain_files = os.listdir(plain_folder)
for plain_filename in plain_files:
	print("%s:" % plain_filename)
	recipe = output_results(plain_folder + "/" + plain_filename)
	for line in recipe:
		if rp.Food in line or if rp.Modifier in line:
			print_ingredient_line(line)
		elif rp.Time in line:
			print_time_line(line)
		elif rp.Degrees in line:
			print_degree_line(line)
	print("")


def is_pokemon_legendary(stats):
	print(stats)
	print(f'values: {stats.values()}')
	return sum([int(i) for i in stats.values()]) > 10

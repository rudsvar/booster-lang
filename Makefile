.PHONY: test parse run

test:
	@python3 -m unittest discover -s solution -v
	@python3 -m doctest solution/base_parser.py

parse:
	@python3 main.py parse "$(FILE)"

run:
	@python3 main.py run "$(FILE)"

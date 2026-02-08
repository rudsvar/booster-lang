.PHONY: test parse run

test:
	@python3 -m unittest tests -v

parse:
	@python3 main.py parse "$(FILE)"

run:
	@python3 main.py run "$(FILE)"

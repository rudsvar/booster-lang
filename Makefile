.PHONY: test parse run

test:
	@python3 -m unittest discover -s . -p "*_tests.py" -q
	@echo "Running examples"
	@for file in examples/*.blang; do echo "  $$file"; python3 interpreter.py "$$(cat $$file)" > /dev/null || exit 1; done
	@echo "OK"

parse:
	@python3 main.py parse "$(FILE)"

run:
	@python3 main.py run "$(FILE)"

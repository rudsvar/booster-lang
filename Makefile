.PHONY: test parse run solution-test solution-parse solution-run

test:
	@python3 -m unittest discover -s . -p "*_tests.py" -q
	@echo "Running examples"
	@for file in examples/*.blang; do echo "  $$file"; python3 interpreter.py "$$(cat $$file)" > /dev/null || exit 1; done
	@echo "OK"

parse:
	@python3 parser.py "$(FILE)"

run:
	@python3 interpreter.py "$(FILE)"

solution-test:
	@python3 -m unittest discover -s solution -p "*_tests.py" -q
	@echo "Running examples (solution)"
	@for file in examples/*.blang; do echo "  $$file"; python3 solution/interpreter.py "$$(cat $$file)" > /dev/null || exit 1; done
	@echo "OK"

solution-parse:
	@python3 solution/parser.py "$(FILE)"

solution-run:
	@python3 solution/interpreter.py "$(FILE)"

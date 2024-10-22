import os
import unittest

from app import create_logger_and_app_with_middleware


_, _, app = create_logger_and_app_with_middleware()


# Support running integration tests
@app.cli.command()
def test():
    """Run integration tests."""
    tests = unittest.TestLoader().discover(os.path.join(os.path.dirname(__file__), 'tests'))
    unittest.TextTestRunner(verbosity=2).run(tests)

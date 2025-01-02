import logfire

# Configure logfire
logfire.configure()

# Send a log
logfire.info('Hello, {name}!', name='world')
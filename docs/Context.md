# Context

The Engine uses a context object to pass and update internal values between the nodes. This context is a dictionary with keys that will be used for node building, rendering, updating and handling events.

## Default context

- `metadata` - Metadata of the application
  - `app_name: str` - Name of the application
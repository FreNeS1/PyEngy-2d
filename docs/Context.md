# Context

The Engine uses a context object to pass and update internal values between the nodes. This context is a dictionary with keys that will be used for node building, rendering, updating and handling events.

## Default context

- `metadata: Dict` - Metadata of the application
  - `app_name: str` - Name of the application
- `app: Dict` - Classes and resources of the application
    - `screen: pygame.Surface` - The default main screen of the application.
    - `resource_manager: ResourceManager` - The default resource manager of the application.
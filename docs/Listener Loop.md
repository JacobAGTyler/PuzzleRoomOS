# The Listener Loop

The listener loop happens on all devices in the network. These are either standard devices or database devices.

- Standard Device: No connection to the database, only access to config data and Interfaces
- Database Device: Access to the database. Persists events to the database. Access to the game object.

## Attempt Flow
```mermaid
flowchart TD
    C(Screen Listener) -->|Attempt Event| K1{{Kakfa}}
    K1 --> D(Database Listener)
    K2{{Kakfa}} --> I(Interface Listener)

    D --> E(Save Event to Database)
    E --> ED[(Database)]
    I --> IL{Trigger Recognised}
    IL -->|Yes| F(Interface Activation)
    IL -->|No| Z((END))
    F -->|Successful Activation Event| K3{{Kakfa}}

    E --> DL{Attempt Successful}
    DL -->|Successful| DA(Trigger Conversion)
    DL -->|Unsuccessful| Z1((END))
    DA -->|Trigger Event| K2
```

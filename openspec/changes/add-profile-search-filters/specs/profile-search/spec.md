# Spec: Profile Search

## ADDED Requirements

### Requirement: Filter Profiles by Role
The system SHALL allow users to filter the list of profiles by a specific Role.

#### Scenario: User filters by 'Developer' role
Given a list of profiles with mixed roles
When the user selects 'Developer' in the Role filter
Then only profiles with the role 'Developer' are displayed

### Requirement: Filter Profiles by Team
The system SHALL allow users to filter the list of profiles by a specific Team.

#### Scenario: User filters by 'Core' team
Given a list of profiles across different teams
When the user selects 'Core' in the Team filter
Then only profiles belonging to the 'Core' team are displayed
